[app]
# Application title
title = Face Password System

# Package name (reverse domain notation)
package.name = facepassword
package.domain = com.facepassword

# Source code location
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Permissions required for Android
android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Features needed
android.features = android.hardware.camera

# Python version
p4a.python_version = 3.9

# Minimum and target API levels
android.api = 28
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Requirements - Python packages to include
requirements = python3,kivy,opencv-python,numpy,face-recognition,pillow

# Architecture targets
android.archs = arm64-v8a,armeabi-v7a

# Version
version = 1.0

# Requirements for build
android.gradle_dependencies = androidx.appcompat:appcompat:1.2.0

# Orientation
orientation = portrait

# Fullscreen
fullscreen = 0

# Icon and presplash (optional)
# icon.filename = %(source.dir)s/data/icon.png
# presplash.filename = %(source.dir)s/data/presplash.png
# presplash.imgctx = presplash

[buildozer]
# Log level
log_level = 2

# Display warning when buildozer is run as root
warn_on_root = 1

# Path to build artifact storage
build_dir = .buildozer

# Path to build output
bin_dir = ./bin
