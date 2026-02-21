# Android Build Instructions for Face Password System

## Prerequisites

### Install Required Tools (Windows)
1. **Java Development Kit (JDK)**
   - Download: https://www.oracle.com/java/technologies/downloads/
   - Install JDK 11 or later
   - Set JAVA_HOME environment variable

2. **Android SDK**
   - Download Android Studio: https://developer.android.com/studio
   - Or download SDK command-line tools
   - Set ANDROID_SDK_ROOT environment variable

3. **Android NDK**
   - Download from Android Studio: Tools → SDK Manager → SDK Tools → NDK
   - Set ANDROID_NDK_ROOT environment variable

4. **Python Build Tools**
   ```bash
   pip install buildozer cython
   ```

## Option 1: Build APK on Windows (Recommended First Time)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Install Buildozer
```bash
pip install buildozer
```

### Step 3: Build the APK
```bash
buildozer android debug
```

This will:
- Take 15-45 minutes on first build (downloads dependencies)
- Generate: `bin/facepassword-1.0-debug.apk`
- Store intermediate files in `.buildozer/`

### Step 4: Install on Android Device
```bash
adb connect <device_ip>  # For wireless
# OR
adb install bin/facepassword-1.0-debug.apk  # For USB
```

## Option 2: Build on Linux/WSL (Faster Alternative)

If you have WSL2 or Linux, use this faster method:

### Step 1: Update system packages
```bash
sudo apt-get update
sudo apt-get install -y openjdk-11-jdk android-sdk android-ndk python3-pip
```

### Step 2: Set environment variables
```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export ANDROID_SDK_ROOT=/path/to/android-sdk
export ANDROID_NDK_ROOT=/path/to/android-ndk
export PATH=$PATH:$JAVA_HOME/bin:$ANDROID_SDK_ROOT/tools:$ANDROID_SDK_ROOT/platform-tools
```

### Step 3: Build
```bash
buildozer android debug
```

## Troubleshooting

### Issue: "Java not found"
**Solution:** Set JAVA_HOME environment variable
```bash
set JAVA_HOME=C:\Program Files\Java\jdk-11
```

### Issue: "Android SDK not found"
**Solution:** Install Android Studio and set:
```bash
set ANDROID_SDK_ROOT=C:\Users\YourUsername\AppData\Local\Android\Sdk
```

### Issue: "face-recognition not available on Android"
**Solution:** Use TensorFlow Lite instead (see Alternative below)

### Issue: Build fails with OpenCV
**Solution:** The python-opencv package may need special handling. Use:
```
requirements = python3,kivy,numpy,pillow
```
And handle camera via Kivy's Camera widget instead.

## Alternative: Use TensorFlow Lite for Face Recognition

For better Android compatibility, replace face_recognition with TensorFlow Lite:

```python
# Use mediapipe for face detection instead
pip install mediapipe
```

Then update main_android.py to use:
```python
import mediapipe as mp

face_detection = mp.solutions.face_detection.FaceDetection()
```

## Testing the APK

1. **Enable USB Debugging on Android Device:**
   - Settings → About Phone → Tap Build Number 7 times
   - Settings → Developer Options → Enable USB Debugging

2. **Connect Device:**
   ```bash
   adb devices  # Should show your device
   ```

3. **Install:**
   ```bash
   adb install -r bin/facepassword-1.0-debug.apk
   ```

4. **Run:**
   ```bash
   adb shell am start -n com.facepassword.facepassword/com.facepassword.facepassword.FacePasswordApp
   ```

## File Paths on Android

The app stores the reference face at:
```
/data/data/com.facepassword.facepassword/files/person.jpg
```

To push your reference image:
```bash
adb push person.jpg /data/data/com.facepassword.facepassword/files/
```

## Release Build

For production release:
```bash
buildozer android release
```

You'll need to sign the APK. Follow Android Studio's signing process.

## Documentation Links

- Kivy: https://kivy.org/doc/stable/
- Buildozer: https://buildozer.readthedocs.io/
- Android Studio: https://developer.android.com/docs
- adb commands: https://developer.android.com/studio/command-line/adb
