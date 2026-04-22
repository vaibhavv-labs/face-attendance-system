<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Space+Mono&size=28&pause=1000&color=00FF88&center=true&vCenter=true&width=600&lines=FaceID+Attendance+System;Real-Time+Face+Recognition;Auto+CSV+Export+%E2%9C%85" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-00FF88?style=for-the-badge)

<br/>

> 🎯 **Automated attendance tracking using real-time face recognition — no RFID, no manual entry, just your face.**

<br/>

![Demo Banner](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12&height=120&section=header&text=Face%20Attendance%20System&fontSize=28&fontColor=ffffff&animation=fadeIn)

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎥 **Live Camera Feed** | Real-time webcam stream with face detection overlay |
| 🧠 **LBPH Recognition** | Local Binary Pattern Histogram — fast, accurate, no internet needed |
| 🟢 **Auto Mark Present** | Detects & marks attendance the moment a face is recognized |
| 📋 **Live Attendance Table** | Updates instantly on screen — see who's present in real time |
| 💾 **Auto CSV Save** | Saves `attendance.csv` automatically on every detection |
| ⬇️ **One-Click Export** | Download the full attendance sheet with a single button |
| 🖥️ **Beautiful Dark UI** | Neon-themed Streamlit dashboard — looks as good as it works |

---

## 📸 Preview

```
┌─────────────────────────────────────────────────────────┐
│  ⬡ FaceID Attendance System                             │
│  ─────────────────────────────────────────────────────  │
│  👥 Total: 5  │  🟢 Present: 3  │  🔴 Absent: 2  │ 60% │
│                                                         │
│  ┌─── 📷 Live Feed ──────┐  ┌─── 📋 Register ───────┐  │
│  │                       │  │  ● Rahul   Present 09:01│  │
│  │   ┌──────────────┐    │  │  ● Priya   Present 09:03│  │
│  │   │  RAHUL  98%  │    │  │  ● Arjun   Present 09:07│  │
│  │   └──────────────┘    │  │  ● Sneha   Absent  --   │  │
│  │       LIVE 09:07      │  │  ● Karan   Absent  --   │  │
│  └───────────────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/face-attendance-system.git
cd face-attendance-system
```

### 2. Install dependencies

```bash
pip install opencv-contrib-python numpy streamlit pandas
```

> ⚠️ Make sure you install **`opencv-contrib-python`** (not just `opencv-python`) — it includes the LBPH face recognizer.

### 3. Add your training photos

```
known_faces/
├── Rahul/
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── photo3.jpg
├── Priya/
│   ├── img1.jpg
│   └── img2.jpg
└── YourName/
    └── ...
```

> 💡 **Pro tip:** Add 10–20 varied photos per person (different angles, lighting) for best accuracy.

### 4. Run the app

```bash
# Streamlit UI (recommended)
streamlit run app.py

# Terminal / command-line version
python main.py
```

---

## 📁 Project Structure

```
face-attendance-system/
│
├── app.py              # 🖥️  Streamlit web UI
├── main.py             # 💻  Terminal version
├── requirements.txt    # 📦  Dependencies
│
├── known_faces/        # 📂  Training images (you create this)
│   ├── Person1/
│   └── Person2/
│
└── attendance.csv      # 📊  Auto-generated attendance log
```

---

## ⚙️ How It Works

```
  📷 Webcam Frame
       │
       ▼
  🔍 Haar Cascade Detector
  (finds face locations)
       │
       ▼
  🧠 LBPH Recognizer
  (matches face to known person)
       │
       ├── Confidence < 100 ──▶ ✅ Mark Present + Log Time
       │
       └── Confidence ≥ 100 ──▶ ❓ Unknown (ignored)
                                        │
                                        ▼
                               💾 Auto-save attendance.csv
```

---

## 🔧 Configuration

You can tweak these values in `app.py` or `main.py`:

| Parameter | Default | Effect |
|---|---|---|
| `scaleFactor` | `1.1` | Lower = more detections (slower) |
| `minNeighbors` | `3` (train) / `4` (live) | Higher = fewer false positives |
| `confidence < 100` | `100` | Raise to be more lenient, lower to be stricter |
| Face resize | `100x100` | Larger = more detail but slower training |

---

## 📦 Requirements

```txt
opencv-contrib-python
numpy
streamlit
pandas
```

Install all at once:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Troubleshooting

**Face not being recognized?**
- Make sure your `known_faces/` folder exists with subfolders per person
- Add more training images (10–20 per person recommended)
- Ensure good lighting in training photos

**Camera not opening?**
- Check that no other app is using the webcam
- Try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`

**`cv2.face` module not found?**
```bash
pip uninstall opencv-python
pip install opencv-contrib-python
```

---

## 📊 Output — `attendance.csv`

```csv
Name,Status,Time
Rahul,Present,09:01:34
Priya,Present,09:03:12
Arjun,Present,09:07:55
Sneha,Absent,--
Karan,Absent,--
```

---

## 🗺️ Roadmap

- [ ] 🔔 Notification / alert when unknown face detected
- [ ] 📅 Date-wise attendance history
- [ ] 👤 In-app face enrollment (no manual folder setup)
- [ ] 📈 Analytics dashboard (weekly/monthly charts)
- [ ] 🔐 Admin login for secure access
- [ ] 📱 Mobile-responsive UI

---

## 🤝 Contributing

Contributions are welcome!

```bash
# Fork → Clone → Create branch → Make changes → PR
git checkout -b feature/your-feature
git commit -m "Add: your feature"
git push origin feature/your-feature
```

---

## 📄 License

This project is licensed under the **MIT License** — use it, modify it, ship it.

---

<div align="center">

Made with ❤️ using Python + OpenCV + Streamlit

⭐ **Star this repo if it helped you!** ⭐

![Footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12&height=80&section=footer)

</div>
