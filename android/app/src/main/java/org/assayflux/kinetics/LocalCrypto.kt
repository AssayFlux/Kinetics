package org.assayflux.kinetics

import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.io.File
import java.io.FileOutputStream
import java.io.RandomAccessFile
import java.security.KeyStore
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

/** Android Keystore AES-256-GCM. Chunk files use [4-byte length][IV+ciphertext] records. */
object LocalCrypto {
    private const val ALIAS = "kinetics-local-data-v1"
    private const val TRANSFORMATION = "AES/GCM/NoPadding"
    private const val IV_BYTES = 12
    private const val TAG_BYTES = 16
    private const val TAG_BITS = TAG_BYTES * 8
    const val CHUNK_BYTES = 4 * 1024 * 1024

    private fun key(): SecretKey {
        val store = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        val existing = store.getKey(ALIAS, null) as? SecretKey
        if (existing != null) return existing
        val generator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
        generator.init(
            KeyGenParameterSpec.Builder(
                ALIAS, KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT,
            ).setKeySize(256)
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                .setRandomizedEncryptionRequired(true)
                .build(),
        )
        return generator.generateKey()
    }

    fun encrypt(plainText: ByteArray): ByteArray {
        require(plainText.size <= CHUNK_BYTES) { "AES-GCM chunk exceeds the 4 MiB limit" }
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.ENCRYPT_MODE, key())
        return cipher.iv + cipher.doFinal(plainText)
    }

    fun decrypt(payload: ByteArray): ByteArray {
        require(payload.size in (IV_BYTES + TAG_BYTES)..(CHUNK_BYTES + IV_BYTES + TAG_BYTES)) {
            "Encrypted chunk is truncated or exceeds the 4 MiB limit"
        }
        val iv = payload.copyOfRange(0, IV_BYTES)
        val encrypted = payload.copyOfRange(IV_BYTES, payload.size)
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.DECRYPT_MODE, key(), GCMParameterSpec(TAG_BITS, iv))
        return cipher.doFinal(encrypted)
    }

    /** Append one independently authenticated encrypted chunk and fsync its record. */
    fun appendEncryptedChunk(file: File, plainText: ByteArray) {
        require(plainText.isNotEmpty()) { "Encrypted chunks cannot be empty" }
        val payload = encrypt(plainText)
        RandomAccessFile(file, "rw").use { output ->
            output.seek(output.length())
            output.writeInt(payload.size)
            output.write(payload)
            output.fd.sync()
        }
    }

    /**
     * Decrypts a complete chunked file to a temporary sibling, publishing it only
     * after every GCM tag has authenticated successfully.
     */
    fun decryptChunkedFile(source: File, destination: File) {
        require(source.isFile) { "Encrypted source file does not exist" }
        val temporary = File(destination.parentFile, destination.name + ".tmp")
        temporary.delete()
        try {
            RandomAccessFile(source, "r").use { input ->
                FileOutputStream(temporary, false).use { output ->
                    while (input.filePointer < input.length()) {
                        val remaining = input.length() - input.filePointer
                        require(remaining >= 4) { "Encrypted chunk header is truncated" }
                        val length = input.readInt()
                        require(length in (IV_BYTES + TAG_BYTES)..(CHUNK_BYTES + IV_BYTES + TAG_BYTES)) {
                            "Encrypted chunk length is invalid"
                        }
                        require(input.length() - input.filePointer >= length) {
                            "Encrypted chunk payload is truncated"
                        }
                        val payload = ByteArray(length)
                        input.readFully(payload)
                        output.write(decrypt(payload))
                    }
                    output.fd.sync()
                }
            }
            check(temporary.renameTo(destination)) { "Decrypted file could not be finalized" }
        } catch (error: Exception) {
            temporary.delete()
            throw error
        }
    }
}
