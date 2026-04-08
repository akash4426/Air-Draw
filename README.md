# Air Drawer - Hand Gesture Drawing App 🎨

Draw on your screen using only hand gestures! No mouse or touchscreen needed. Professional-grade gesture recognition for an intuitive drawing experience.

## ✨ Features

- 🎨 **Smooth Drawing** - Draw with your finger using advanced position smoothing
- 🖐️ **Accurate Gesture Recognition** - Real-time hand tracking with MediaPipe
- 🔄 **Erase Mode** - Peace sign gesture to erase drawings
- 🗑️ **Clear Canvas** - Open hand gesture to clear the drawing instantly
- 🎯 **Visual Feedback** - Real-time cursor effects and UI indicators
- 🌈 **8 Color Palette** - Multiple colors with keyboard cycling (Red, Green, Blue, Cyan, Magenta, Yellow, Purple, Orange)
- 📊 **Live FPS Counter** - Monitor real-time performance
- 💾 **Save Drawings** - Press 'S' to save your artwork as PNG
- 🖼️ **Blended View** - See your drawing overlaid on camera feed (adjustable transparency)

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Webcam
- Good lighting environment

### Setup

1. **Clone or navigate to the project:**
```bash
cd Air-Draw
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

## 🎮 Usage

Run the application:
```bash
python code.py
```

A window titled "Air Drawer - Hand Gesture Drawing" will open showing your webcam feed with an overlay canvas.

## 🖐️ Hand Gestures

| Gesture | Action | Visual Feedback |
|---------|--------|---|
| **☝️ One Finger Pointing Up** | **Draw Mode** | Cyan circles with visual effect on finger |
| **✌️ Peace Sign (2 fingers)** | **Eraser Mode** | Orange concentric circles show eraser area |
| **✋ Open Hand (all fingers extended)** | **Clear Canvas** | Hold for ~1 second to clear all drawings |

## ⌨️ Keyboard Shortcuts

| Key | Action | Feedback |
|-----|--------|----------|
| `C` | Clear the canvas | Console confirmation |
| `R` | Cycle through drawing colors | Console shows color name |
| `S` | Save current drawing | Saves as `drawing_XXXX.png` |
| `ESC` | Exit the application | Clean shutdown |

## 🎨 Drawing Colors (Cycle with 'R')

Available color palette:
1. **Red** - Vibrant red
2. **Green** - Bright green  
3. **Blue** - Deep blue
4. **Cyan** - Light cyan
5. **Magenta** - Bright magenta
6. **Yellow** - Bright yellow
7. **Purple** - Deep purple
8. **Orange** - Bright orange

## 💡 Usage Tips

### For Best Results:
- ✅ **Good Lighting** - Ensure adequate, uniform lighting for better hand detection
- ✅ **Clear Background** - Works better with simple, non-cluttered backgrounds
- ✅ **Steady Hand** - Keep hand movements smooth and deliberate for cleaner strokes
- ✅ **Distance** - Maintain 30-60cm distance from the camera
- ✅ **Hand Orientation** - Keep your palm facing the camera
- ✅ **Slow Movements** - Move fingers slowly for better tracking accuracy

### For Better Accuracy:
1. Position yourself in good natural light
2. Avoid sudden, jerky hand movements
3. Keep fingers well-separated when using gestures
4. Ensure your entire hand is visible to the camera
5. Take a moment to let the system detect your hand before starting

## 🔧 Technical Features

### Advanced Hand Detection
- **MediaPipe Hand Tracking** - State-of-the-art hand landmark detection
- **Position Smoothing** - Gaussian smoothing (factor: 0.6) reduces jitter
- **Gesture Recognition** - Accurate detection based on finger heights and positions
- **Confidence Thresholds** - Detection confidence: 80%, Tracking confidence: 70%

### Drawing Improvements
- **Smooth Interpolation** - Multi-point drawing queue for fluid strokes
- **Anti-aliased Lines** - CV2.LINE_AA for smooth edges
- **Blended Canvas** - Transparency-adjusted overlay (65%) for clear visibility
- **Real-time Feedback** - Visual effects at cursor position

### Performance
- **FPS Counter** - Real-time performance monitoring
- **Optimized Processing** - Efficient hand detection pipeline
- **Multiple Point Queue** - Smooth curves with 5-point interpolation buffer

## 📋 System Requirements

| Component | Requirement |
|-----------|---|
| Python | 3.8 or higher |
| RAM | 4GB minimum |
| CPU | Modern dual-core |
| Webcam | USB/Built-in camera |
| OS | Windows, macOS, Linux |

## 📦 Dependencies

- `opencv-python` - Computer vision library
- `mediapipe` - Hand detection and tracking
- `numpy` - Numerical computing

(See [requirements.txt](requirements.txt) for specific versions)

## 🐛 Troubleshooting

### Hand not detected?
- **Solution**: Ensure good lighting, move closer to camera (30-60cm)
- **Check**: Verify webcam is working with other applications
- **Adjust**: Try different angles and backgrounds

### Jerky/Laggy drawing?
- **Solution**: Close other CPU-intensive applications
- **Try**: Reduce brush thickness in code (line with `brush_thickness`)
- **Improve**: Use better lighting for more stable detection

### Incorrect gesture recognition?
- **Solution**: Make sure fingers are clearly separated
- **Try**: Hold gestures steady for a moment
- **Ensure**: Your hand is fully visible to the camera

### Eraser or drawing not working?
- **Check**: Make sure your hand is detected (indicator shows "✓")
- **Verify**: Gestures are held clearly with fingers extended/curled properly
- **Reset**: Press 'C' to clear and try again

### Colors look different?
- **Note**: This uses BGR format (OpenCV standard), not RGB
- **Modify**: Edit color tuples in `color_palette` dictionary if needed

### Feedback or issues?
- Check hand lighting and positioning
- Review gesture tutorials in the app
- Consult console output for error messages

## 🎓 How It Works

1. **Capture** - Reads video frames from your webcam
2. **Detect** - MediaPipe detects hand landmarks in real-time
3. **Track** - Smooth position tracking to reduce jitter
4. **Recognize** - Gesture recognition based on finger positions
5. **Render** - Draw on canvas based on detected gestures
6. **Display** - Blend canvas with camera feed for visibility

### Gesture Detection Algorithm
- **Pointing**: Index finger extended, other fingers curled
- **Peace**: Index + Middle extended, ring + pinky curled  
- **Stop**: All fingers extended away from wrist
- Gestures verified by finger heights measured from landmarks

## 📸 Window Layout

```
┌─────────────────────────────────────┬──────────────────┐
│                                     │   CONTROLS       │
│                                     │   ───────────    │
│         Camera Feed +               │ 1 FINGER -> Draw │
│         Drawing Canvas              │ PEACE -> Erase   │
│         (Blended View)              │ OPEN -> Clear    │
│                                     │                  │
│         Status: DRAW                │ C - Clear        │
│         Color: RED                  │ R - Color        │
│         Hand: ✓ DETECTED            │ S - Save         │
│                                     │ ESC - Exit       │
│                                     │                  │
└─────────────────────────────────────┴──────────────────┘
```

## 📝 Tips for Drawing

1. **Smooth Strokes** - Move your hand slowly and deliberately
2. **Precision** - Keep your finger steady when drawing details
3. **Erasing** - Use peace gesture to erase sections
4. **Colors** - Press 'R' to cycle through colors before drawing
5. **Saving** - Press 'S' to save completed drawings

## 🔄 Updates & Future Features

Potential enhancements:
- [ ] Undo/Redo functionality
- [ ] Adjustable brush size with hand width
- [ ] More color options and custom colors
- [ ] Drawing shape templates
- [ ] Export to different formats
- [ ] Drawing filters and effects

## 📄 License

This project is open-source and available for personal and educational use.

## 👨‍💻 Author

Created with ❤️ for gesture-based creative expression.

---

**Enjoy creating! 🎨✨**

For issues or suggestions, please provide feedback. Happy drawing! 👋

