plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "id.mcm.logopreview"
    compileSdk = 35
    defaultConfig {
        applicationId = "id.mcm.logopreview"
        minSdk = 26
        targetSdk = 35
        versionCode = providers.environmentVariable("ANDROID_VERSION_CODE").orElse("1").get().toInt()
        versionName = providers.environmentVariable("ANDROID_VERSION_NAME").orElse("1.0.0").get()
    }
    signingConfigs {
        create("release") {
            val signingFile = providers.environmentVariable("ANDROID_KEYSTORE_PATH").orNull
            if (signingFile != null) {
                storeFile = file(signingFile)
                storeType = "PKCS12"
                storePassword = providers.environmentVariable("ANDROID_KEYSTORE_PASSWORD").orNull
                keyAlias = providers.environmentVariable("ANDROID_KEY_ALIAS").orNull
                keyPassword = providers.environmentVariable("ANDROID_KEY_PASSWORD").orNull
            }
        }
    }
    buildTypes {
        getByName("release") {
            signingConfig = signingConfigs.getByName("release")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
    // Use the actual asset folder directly: avoid generated-asset task ordering/cache issues.
    sourceSets["main"].assets.srcDir(rootProject.file("../html/assets"))
    testOptions { unitTests.isIncludeAndroidResources = true }
}

dependencies {
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.robolectric:robolectric:4.14.1")
}
