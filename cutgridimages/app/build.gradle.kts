plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.emrobinso.cutgridimages"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.emrobinso.cutgridimages"
        minSdk = 26
        targetSdk = 35
        versionCode = providers.environmentVariable("ANDROID_VERSION_CODE").orElse("1").get().toInt()
        versionName = providers.environmentVariable("ANDROID_VERSION_NAME").orElse("1.0.0").get()
    }

    buildTypes {
        getByName("release") {
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions { jvmTarget = "17" }
}

dependencies {
    // Hanya API platform Android + unit test JVM. Tidak ada dependensi runtime eksternal.
    testImplementation("junit:junit:4.13.2")
}
