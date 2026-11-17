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
    sourceSets["main"].assets.srcDir(layout.buildDirectory.dir("generated/logoAssets"))
}

// Package original solid rasters for native Bitmap rendering; no HTML/WebView.
val syncLogoAssets by tasks.registering(Copy::class) {
    from(rootProject.file("../html/assets"))
    include("*.png")
    into(layout.buildDirectory.dir("generated/logoAssets"))
}
tasks.named("preBuild") { dependsOn(syncLogoAssets) }

 dependencies { testImplementation("junit:junit:4.13.2") }
