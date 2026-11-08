package org.assayflux.kinetics

import android.content.Context
import org.json.JSONObject
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.security.MessageDigest

data class DataPackManifest(
    val id: String,
    val version: String,
    val source: String,
    val license: String,
    val sha256: String,
    val sizeBytes: Long,
)

/** Installs data-only packs after manifest, size and checksum checks; never loads executable content. */
class DataPackManager(context: Context) {
    private val root = File(context.filesDir, "datapacks").apply { mkdirs() }
    private val maximumPackBytes = 256L * 1024L * 1024L

    fun parseManifest(json: String): DataPackManifest {
        val value = JSONObject(json)
        val manifest = DataPackManifest(
            id = value.getString("id"),
            version = value.getString("version"),
            source = value.getString("source"),
            license = value.getString("license"),
            sha256 = value.getString("sha256").lowercase(),
            sizeBytes = value.getLong("size_bytes"),
        )
        require(manifest.id.matches(Regex("[A-Za-z0-9._-]{1,80}"))) { "Invalid pack id" }
        require(manifest.version.isNotBlank() && manifest.source.startsWith("https://"))
        require(manifest.license.isNotBlank()) { "License metadata is mandatory" }
        require(manifest.sha256.matches(Regex("[a-f0-9]{64}"))) { "Invalid SHA-256" }
        require(manifest.sizeBytes in 1..maximumPackBytes) { "Pack size outside permitted range" }
        return manifest
    }

    fun install(source: File, manifest: DataPackManifest): File {
        require(source.isFile && source.length() == manifest.sizeBytes) { "Pack size mismatch" }
        val digest = MessageDigest.getInstance("SHA-256")
        FileInputStream(source).use { input ->
            val buffer = ByteArray(DEFAULT_BUFFER_SIZE)
            while (true) {
                val count = input.read(buffer)
                if (count < 0) break
                digest.update(buffer, 0, count)
            }
        }
        val actual = digest.digest().joinToString("") { "%02x".format(it) }
        require(actual == manifest.sha256) { "Pack checksum mismatch" }
        val destinationDir = File(root, manifest.id).apply { mkdirs() }
        val temporary = File(destinationDir, manifest.version + ".tmp")
        val destination = File(destinationDir, manifest.version + ".data")
        FileInputStream(source).use { input ->
            FileOutputStream(temporary).use { output ->
                input.copyTo(output)
                output.fd.sync()
            }
        }
        check(temporary.renameTo(destination)) { "Atomic data-pack installation failed" }
        return destination
    }
}
