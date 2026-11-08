package org.assayflux.kinetics

import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.io.File
import java.io.FileOutputStream
import java.io.RandomAccessFile
import java.security.KeyStore
import java.security.MessageDigest
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

/** Android Keystore AES-256-GCM with per-chunk identity and ordering authenticated as AAD. */
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

    fun associatedData(context: String, chunkIndex: Long): ByteArray {
        require(context.isNotBlank() && chunkIndex >= 0) { "Invalid encrypted chunk identity" }
        return "$context:$chunkIndex".toByteArray(Charsets.UTF_8)
    }

    fun encrypt(plainText: ByteArray, associatedData: ByteArray = byteArrayOf()): ByteArray {
        require(plainText.size <= CHUNK_BYTES) { "AES-GCM chunk exceeds the 4 MiB limit" }
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.ENCRYPT_MODE, key())
        if (associatedData.isNotEmpty()) cipher.updateAAD(associatedData)
        return cipher.iv + cipher.doFinal(plainText)
    }

    fun decrypt(payload: ByteArray, associatedData: ByteArray = byteArrayOf()): ByteArray {
        require(payload.size in (IV_BYTES + TAG_BYTES)..(CHUNK_BYTES + IV_BYTES + TAG_BYTES)) {
            "Encrypted chunk is truncated or exceeds the 4 MiB limit"
        }
        val iv = payload.copyOfRange(0, IV_BYTES)
        val encrypted = payload.copyOfRange(IV_BYTES, payload.size)
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.DECRYPT_MODE, key(), GCMParameterSpec(TAG_BITS, iv))
        if (associatedData.isNotEmpty()) cipher.updateAAD(associatedData)
        return cipher.doFinal(encrypted)
    }

    fun appendEncryptedChunk(file: File, plainText: ByteArray, associatedData: ByteArray) {
        require(plainText.isNotEmpty()) { "Encrypted chunks cannot be empty" }
        val payload = encrypt(plainText, associatedData)
        RandomAccessFile(file, "rw").use { output ->
            output.seek(output.length())
            output.writeInt(payload.size)
            output.write(payload)
            output.fd.sync()
        }
    }

    fun decryptChunkedFile(
        source: File, destination: File, context: String, expectedSha256: String,
    ) {
        require(source.isFile) { "Encrypted source file does not exist" }
        require(expectedSha256.matches(Regex("[a-fA-F0-9]{64}"))) { "Expected SHA-256 is invalid" }
        val temporary = File(destination.parentFile, destination.name + ".tmp")
        temporary.delete()
        val digest = MessageDigest.getInstance("SHA-256")
        try {
            RandomAccessFile(source, "r").use { input ->
                FileOutputStream(temporary, false).use { output ->
                    var chunkIndex = 0L
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
                        val plaintext = decrypt(payload, associatedData(context, chunkIndex))
                        output.write(plaintext)
                        digest.update(plaintext)
                        chunkIndex++
                    }
                    output.fd.sync()
                }
            }
            val actual = digest.digest().joinToString("") { "%02x".format(it) }
            require(actual.equals(expectedSha256, ignoreCase = true)) {
                "Decrypted input SHA-256 does not match recorded provenance"
            }
            if (destination.exists()) {
                check(destination.delete()) { "Previous decrypted output could not be replaced" }
            }
            check(temporary.renameTo(destination)) { "Decrypted file could not be finalized" }
        } catch (error: Exception) {
            temporary.delete()
            throw error
        }
    }
}
