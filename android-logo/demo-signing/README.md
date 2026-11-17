# Public AOSP demo signing identity — NOT SECRET, NOT PRODUCTION

Files copied from https://github.com/aosp-mirror/platform_build/tree/master/target/product/security . These are deliberately public Android test keys, not a private project signing credential. AOSP warns not to use these keys for production. See upstream Android Open Source Project licensing (Apache 2.0): https://github.com/aosp-mirror/platform_build/blob/master/NOTICE .

The user authorized demo signing. A fixed certificate permits demo-to-demo updates without uninstall when application ID stays identical and versionCode increases. Anyone with the public key material can sign a competing APK: install only trusted builds. Do not grant this app sensitive permissions. Do not use for Play Store or production. Moving to a different certificate may require uninstall/reinstall.

Never replace these files for an existing demo release lineage. No generated keystore is committed or uploaded as a release asset. Workflow converts this public test identity to temporary PKCS12 during build and deletes the result afterward.
