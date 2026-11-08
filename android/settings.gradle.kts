pluginManagement {
    repositories {
        google()
        // Filtered Central mirror fallback for Kotlin compiler artifacts; Maven Central remains next.
        maven {
            url = uri("https://maven.wso2.org/nexus/content/repositories/central/")
            content { includeGroup("org.jetbrains.kotlin") }
        }
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        // Filtered Central mirror fallback for Kotlin compiler artifacts; Maven Central remains next.
        maven {
            url = uri("https://maven.wso2.org/nexus/content/repositories/central/")
            content { includeGroup("org.jetbrains.kotlin") }
        }
        mavenCentral()
    }
}
rootProject.name = "KineticsFeasibility"
include(":app", ":designsystem")
