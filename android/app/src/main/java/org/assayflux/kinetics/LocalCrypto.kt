package org.assayflux.kinetics

import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.security.KeyStore
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

/** Android Keystore AES-256-GCM helpers. File format: 12-byte IV followed by authenticated ciphertext. */
object LocalCrypto {
    private const val ALIAS = "kinetics-local-data-v1"
    private const val TRANSFORMATION = "AES/GCM/NoPadding"
    private const val IV_BYTES = 12
    private const val TAG_BYTES = 16
    private const val TAG_BITS = TAG_BYTES * 8

    private fun key(): SecretKey {
        val store = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        val existing = store.getKey(ALIAS, null) as? SecretKey
        if (existing != null) return existing
        val generator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
        generator.init(
            KeyGenParameterSpec.Builder(
                ALIAS,
                KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT,
            ).setKeySize(256)
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                .setRandomizedEncryptionRequired(true)
                .build(),
        )
        return generator.generateKey()
    }

    fun encrypt(plainText: ByteArray): ByteArray {
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.ENCRYPT_MODE, key())
        return cipher.iv + cipher.doFinal(plainText)
    }

    fun decrypt(payload: ByteArray): ByteArray {
        require(payload.size > IV_BYTES + TAG_BYTES) { "Encrypted payload is truncated" }
        val iv = payload.copyOfRange(0, IV_BYTES)
        val encrypted = payload.copyOfRange(IV_BYTES, payload.size)
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.DECRYPT_MODE, key(), GCMParameterSpec(TAG_BITS, iv))
        return cipher.doFinal(encrypted)
    }

    /** Encrypts with bounded memory and truncates/creates the destination file. */
    fun encryptFile(source: File, destination: File) {
        require(source.isFile) { "Source file does not exist" }
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.ENCRYPT_MODE, key())
        FileInputStream(source).use { input ->
            FileOutputStream(destination, false).use { output ->
                output.write(cipher.iv)
                val buffer = ByteArray(DEFAULT_BUFFER_SIZE)
                while (true) {
                    val count = input.read(buffer)
                    if (count < 0) break
                    cipher.update(buffer, 0, count)?.let(output::write)
                }
                output.write(cipher.doFinal())
                output.fd.sync()
            }
        }
    }

    /** Decrypts to a caller-controlled destination; GCM authentication is checked at EOF. */
    fun decryptFile(source: File, destination: File) {
        require(source.isFile && source.length() > IV_BYTES + TAG_BYTES) {
            "Encrypted source is missing or truncated"
        }
        FileInputStream(source).use { input ->
            val iv = ByteArray(IV_BYTES)
            var offset = 0
            while (offset < iv.size) {
                val count = input.read(iv, offset, iv.size - offset)
                require(count > 0) { "Encrypted source is truncated" }
                offset += count
            }
            val cipher = Cipher.getInstance(TRANSFORMATION)
            cipher.init(Cipher.DECRYPT_MODE, key(), GCMParameterSpec(TAG_BITS, iv))
            FileOutputStream(destination, false).use { output ->
                val buffer = ByteArray(DEFAULT_BUFFER_SIZE)
                while (true) {
                    val count = input.read(buffer)
                    if (count < 0) break
                    cipher.update(buffer, 0, count)?.let(output::write)
                }
                output.write(cipher.doFinal())
                output.fd.sync()
            }
        }
    }
}
