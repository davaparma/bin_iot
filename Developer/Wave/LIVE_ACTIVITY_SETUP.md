# Live Activity Setup Guide for Wave App

## Prerequisites
- Xcode 14.1 or later
- iOS 16.1 or later (for Live Activities)
- Physical device for testing (Live Activities don't work in simulator)

## Step-by-Step Setup

### 1. Add ActivityKit Framework
1. Open `Wave.xcodeproj` in Xcode
2. Select the **Wave** target (main app)
3. Go to **Build Phases** → **Link Binary With Libraries**
4. Click **+** button
5. Search for `ActivityKit.framework`
6. Add it to your project

### 2. Create Widget Extension Target
1. In Xcode, go to **File** → **New** → **Target**
2. Choose **Widget Extension**
3. Product Name: `WaveWidgets`
4. Bundle Identifier: `com.yourcompany.Wave.WaveWidgets` (adjust as needed)
5. **IMPORTANT**: Check "Include Live Activity"
6. Click **Finish**
7. When prompted, click **Activate** to create the scheme

### 3. Move Widget Files to Extension
1. In Xcode Project Navigator, find these files:
   - `TimerActivity.swift`
   - `WaveWidgets.swift`
2. Select each file
3. In the File Inspector (right panel), under **Target Membership**
4. **Uncheck** the main app target
5. **Check** the Widget Extension target

### 4. Add Live Activity Capability
1. Select the **Wave** target (main app)
2. Go to **Signing & Capabilities**
3. Click **+ Capability**
4. Search for "Live Activities"
5. Add it to your project

### 5. Update Widget Extension Info.plist
1. Select the Widget Extension target
2. Find `Info.plist` in the extension
3. Add this key:
```xml
<key>NSSupportsLiveActivities</key>
<true/>
```

### 6. Test the Implementation
1. Build and run on a physical device
2. Navigate to a recipe step with a timer
3. Tap the timer button to start
4. Check the Dynamic Island for the timer
5. Lock the device to see the lock screen widget

## Troubleshooting

### Common Issues:
1. **"Live Activity not appearing"**
   - Ensure you're testing on a physical device
   - Check that iOS version is 16.1+
   - Verify Live Activity capability is added

2. **"Build errors"**
   - Make sure ActivityKit framework is linked
   - Verify widget files are in the correct target
   - Check that all imports are correct

3. **"Timer not updating"**
   - Ensure LiveActivityManager is properly integrated
   - Check that update calls are being made

## Files Created:
- ✅ `TimerActivity.swift` - Live Activity data model and UI
- ✅ `LiveActivityManager.swift` - Live Activity management
- ✅ `WaveWidgets.swift` - Widget bundle
- ✅ Updated `Info.plist` with Live Activity support

## Next Steps:
1. Follow the Xcode setup steps above
2. Test on a physical device
3. Verify Dynamic Island and lock screen integration

The Live Activity will show:
- **Dynamic Island**: Timer icon + countdown
- **Lock Screen**: Step title, countdown, progress bar
- **Real-time updates**: Every second during countdown
- **State management**: Running/Paused/Finished states
