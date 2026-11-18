package org.assayflux.kinetics

import org.junit.Assert.assertTrue
import org.junit.Test

class PublicDatabaseClientValidationTest {
    private val client = PublicDatabaseClient()

    @Test
    fun rejectsTooShortGeneSearchBeforeNetwork() {
        val error = runCatching { client.searchNcbiGene("x") }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test
    fun rejectsUnsupportedNcbiDatabaseBeforeNetwork() {
        val error = runCatching { client.searchNcbiSequence("gene", "TP53") }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test
    fun rejectsUnsupportedFetchDatabaseBeforeNetwork() {
        val error = runCatching { client.fetchNcbiFasta("sra", "SRR123") }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test
    fun rejectsMalformedNcbiAccessionBeforeNetwork() {
        val error = runCatching { client.fetchNcbiFasta("protein", "bad accession") }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test
    fun rejectsMalformedUniProtAccessionBeforeNetwork() {
        val error = runCatching { client.fetchUniProtFasta("bad accession") }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }

    @Test
    fun rejectsMalformedPdbIdentifierBeforeNetwork() {
        val error = runCatching { client.fetchRcsbMmcif("abc") }.exceptionOrNull()
        assertTrue(error is IllegalArgumentException)
    }
}
