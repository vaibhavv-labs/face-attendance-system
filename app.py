import streamlit as st
import cv2
import os
import numpy as np
import pandas as pd
from datetime import datetime

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FaceID Attendance",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* ── Root ── */
:root {
    --bg:        #0a0a0f;
    --panel:     #111118;
    --border:    #1e1e2e;
    --accent:    #00ff88;
    --accent2:   #00cfff;
    --danger:    #ff4466;
    --text:      #e8e8f0;
    --muted:     #5a5a7a;
    --glow:      0 0 20px rgba(0,255,136,0.3);
    --glow2:     0 0 20px rgba(0,207,255,0.3);
}

/* ── Global ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 10%, rgba(0,255,136,0.04) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(0,207,255,0.04) 0%, transparent 50%),
                var(--bg) !important;
}

/* ── Hide streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(0,255,136,0.15), rgba(0,207,255,0.1));
    border: 1px solid rgba(0,255,136,0.3);
    color: var(--accent);
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 2rem;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 3.2rem !important;
    letter-spacing: -0.03em !important;
    line-height: 1.1 !important;
    background: linear-gradient(135deg, #ffffff 0%, var(--accent) 50%, var(--accent2) 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin: 0 !important;
    padding: 0 !important;
}
.hero-sub {
    color: var(--muted);
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    margin-top: 0.6rem;
}
.hero-line {
    width: 80px;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    margin: 1.2rem auto 0;
    border-radius: 1px;
}

/* ── Stat Cards ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
}
.stat-card {
    flex: 1;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.stat-card.green::before  { background: linear-gradient(90deg, var(--accent), transparent); }
.stat-card.blue::before   { background: linear-gradient(90deg, var(--accent2), transparent); }
.stat-card.red::before    { background: linear-gradient(90deg, var(--danger), transparent); }
.stat-card.total::before  { background: linear-gradient(90deg, #a78bfa, transparent); }
.stat-number {
    font-family: 'Space Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1;
}
.stat-card.green  .stat-number { color: var(--accent); }
.stat-card.blue   .stat-number { color: var(--accent2); }
.stat-card.red    .stat-number { color: var(--danger); }
.stat-card.total  .stat-number { color: #a78bfa; }
.stat-label {
    color: var(--muted);
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.3rem;
    font-family: 'Space Mono', monospace;
}

/* ── Camera Panel ── */
.cam-panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    position: relative;
}
.cam-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.4rem;
    border-bottom: 1px solid var(--border);
}
.cam-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text);
}
.cam-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 0.5rem;
}
.cam-dot.live { background: var(--accent); box-shadow: 0 0 8px var(--accent); animation: blink 1.4s ease-in-out infinite; }
.cam-dot.off  { background: var(--muted); }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── Button ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--accent), #00cc6a) !important;
    color: #000 !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    box-shadow: 0 0 20px rgba(0,255,136,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 0 35px rgba(0,255,136,0.45) !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button {
    background: linear-gradient(135deg, var(--danger), #cc2244) !important;
    box-shadow: 0 0 20px rgba(255,68,102,0.25) !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button:hover {
    box-shadow: 0 0 35px rgba(255,68,102,0.45) !important;
}

/* ── Table Panel ── */
.table-panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
}
.table-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.4rem;
    border-bottom: 1px solid var(--border);
}
.table-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text);
}
.table-count {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--accent);
    background: rgba(0,255,136,0.1);
    border: 1px solid rgba(0,255,136,0.25);
    padding: 0.2rem 0.6rem;
    border-radius: 2rem;
}

/* ── DataFrame ── */
[data-testid="stDataFrame"] {
    background: transparent !important;
}
[data-testid="stDataFrame"] table {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
}
[data-testid="stDataFrame"] th {
    background: rgba(30,30,46,0.8) !important;
    color: var(--muted) !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border) !important;
    padding: 0.7rem 1rem !important;
}
[data-testid="stDataFrame"] td {
    color: var(--text) !important;
    border-bottom: 1px solid rgba(30,30,46,0.6) !important;
    padding: 0.65rem 1rem !important;
}

/* ── Status Indicator ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.6rem 1.2rem;
    background: rgba(0,255,136,0.05);
    border: 1px solid rgba(0,255,136,0.2);
    border-radius: 8px;
    margin: 0.8rem 0;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--accent);
}
.status-bar.inactive {
    background: rgba(90,90,122,0.1);
    border-color: rgba(90,90,122,0.3);
    color: var(--muted);
}

/* ── Download Button ── */
[data-testid="stDownloadButton"] > button {
    width: 100% !important;
    background: transparent !important;
    color: var(--accent2) !important;
    border: 1px solid rgba(0,207,255,0.4) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    border-radius: 8px !important;
    padding: 0.7rem !important;
    transition: all 0.2s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(0,207,255,0.1) !important;
    box-shadow: var(--glow2) !important;
    border-color: var(--accent2) !important;
}

/* ── Section Divider ── */
.section-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1.5rem 0;
}
.section-divider-line {
    flex: 1;
    height: 1px;
    background: var(--border);
}
.section-divider-text {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    white-space: nowrap;
}

/* ── Notification ── */
.notif {
    padding: 0.75rem 1.2rem;
    border-radius: 8px;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    margin: 0.5rem 0;
    border-left: 3px solid;
    animation: slideIn 0.3s ease;
}
.notif.success { background: rgba(0,255,136,0.08); border-color: var(--accent); color: var(--accent); }
.notif.info    { background: rgba(0,207,255,0.08); border-color: var(--accent2); color: var(--accent2); }
@keyframes slideIn { from{transform:translateX(-8px);opacity:0} to{transform:translateX(0);opacity:1} }

/* ── Hide stale elements ── */
[data-testid="stImage"] img { border-radius: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Hero ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⬡ AI-Powered · Real-Time · Automatic</div>
    <h1>FaceID Attendance</h1>
    <p class="hero-sub">LBPH Face Recognition  ·  OpenCV  ·  Auto CSV Export</p>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# ─── Load Model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces, labels, label_map = [], [], {}
    current_label = 0
    all_names = []
    base_path = "known_faces"

    if not os.path.exists(base_path):
        return None, None, [], {}

    for person_name in sorted(os.listdir(base_path)):
        person_folder = os.path.join(base_path, person_name)
        if not os.path.isdir(person_folder):
            continue
        label_map[current_label] = person_name
        all_names.append(person_name)
        for image_name in os.listdir(person_folder):
            image_path = os.path.join(person_folder, image_name)
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            detected = face_cascade.detectMultiScale(img, 1.1, 3)
            for (x, y, w, h) in detected:
                face = cv2.resize(img[y:y+h, x:x+w], (100, 100))
                faces.append(face)
                labels.append(current_label)
        current_label += 1

    if faces:
        recognizer.train(faces, np.array(labels))

    return face_cascade, recognizer, all_names, label_map

face_cascade, recognizer, all_names, label_map = load_model()
model_ready = face_cascade is not None and len(all_names) > 0

# ─── Session State ───────────────────────────────────────────────────────────────
if "attendance" not in st.session_state:
    st.session_state.attendance = {
        name: {"Status": "Absent", "Time": "--"} for name in all_names
    }
if "running" not in st.session_state:
    st.session_state.running = False
if "log" not in st.session_state:
    st.session_state.log = []

# ─── Stats Row ───────────────────────────────────────────────────────────────────
att = st.session_state.attendance
total   = len(all_names)
present = sum(1 for v in att.values() if v["Status"] == "Present")
absent  = total - present
rate    = f"{int(present/total*100)}%" if total else "0%"

st.markdown(f"""
<div class="stats-row">
    <div class="stat-card total">
        <div class="stat-number">{total}</div>
        <div class="stat-label">Total Enrolled</div>
    </div>
    <div class="stat-card green">
        <div class="stat-number">{present}</div>
        <div class="stat-label">Present</div>
    </div>
    <div class="stat-card red">
        <div class="stat-number">{absent}</div>
        <div class="stat-label">Absent</div>
    </div>
    <div class="stat-card blue">
        <div class="stat-number">{rate}</div>
        <div class="stat-label">Attendance Rate</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Status Bar ─────────────────────────────────────────────────────────────────
if not model_ready:
    st.markdown('<div class="notif info">⚠ No <code>known_faces/</code> folder found. Create it with subfolders named after each person containing their photos.</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="notif success">✓ Model loaded — {total} person(s) enrolled: {", ".join(all_names)}</div>', unsafe_allow_html=True)

# ─── Main Layout ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-divider"><div class="section-divider-line"></div><div class="section-divider-text">Live Recognition</div><div class="section-divider-line"></div></div>', unsafe_allow_html=True)

col_cam, col_data = st.columns([3, 2], gap="large")

with col_cam:
    # Camera panel header
    status_dot = '<span class="cam-dot live"></span>LIVE' if st.session_state.running else '<span class="cam-dot off"></span>STANDBY'
    st.markdown(f"""
    <div class="cam-panel">
        <div class="cam-header">
            <span class="cam-title">📷 Camera Feed</span>
            <span style="font-family:'Space Mono',monospace;font-size:0.7rem;color:{'#00ff88' if st.session_state.running else '#5a5a7a'}">{status_dot}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    frame_placeholder = st.empty()

    # Placeholder image when not running
    if not st.session_state.running:
        frame_placeholder.markdown("""
        <div style="background:#0d0d14;border:1px dashed #1e1e2e;border-radius:0 0 16px 16px;
                    height:320px;display:flex;flex-direction:column;align-items:center;
                    justify-content:center;gap:0.8rem;">
            <div style="font-size:3rem;opacity:0.3">📷</div>
            <div style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#3a3a5a;
                        letter-spacing:0.15em;text-transform:uppercase">
                Camera inactive
            </div>
            <div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#2a2a4a">
                Press START to begin recognition
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Buttons
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        start_btn = st.button("▶  START CAMERA", disabled=not model_ready)
    with btn_col2:
        stop_btn = st.button("■  STOP", disabled=not st.session_state.running)

    if stop_btn:
        st.session_state.running = False
        st.rerun()

with col_data:
    # Table panel
    present_count = sum(1 for v in att.values() if v["Status"] == "Present")
    st.markdown(f"""
    <div class="table-panel">
        <div class="table-header">
            <span class="table-title">📋 Attendance Register</span>
            <span class="table-count">{present_count}/{total} present</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    table_placeholder = st.empty()

    # Render table
    def render_table():
        df = pd.DataFrame.from_dict(st.session_state.attendance, orient="index")
        df.index.name = "Name"
        df = df.reset_index()
        # Add emoji status
        df["●"] = df["Status"].apply(lambda s: "🟢" if s == "Present" else "🔴")
        df = df[["●", "Name", "Status", "Time"]]
        table_placeholder.dataframe(df, use_container_width=True, hide_index=True, height=320)

    render_table()

    st.markdown("<br>", unsafe_allow_html=True)

    # Log
    if st.session_state.log:
        st.markdown('<div class="section-divider-text" style="font-family:\'Space Mono\',monospace;font-size:0.65rem;color:#5a5a7a;letter-spacing:0.15em;margin-bottom:0.5rem">RECENT ACTIVITY</div>', unsafe_allow_html=True)
        for entry in reversed(st.session_state.log[-4:]):
            st.markdown(f'<div class="notif success">✓ {entry}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Download
    df_export = pd.DataFrame.from_dict(st.session_state.attendance, orient="index")
    df_export.index.name = "Name"
    csv_bytes = df_export.to_csv().encode("utf-8")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="⬇  EXPORT ATTENDANCE CSV",
        data=csv_bytes,
        file_name=f"attendance_{timestamp}.csv",
        mime="text/csv"
    )

# ─── Camera Loop ─────────────────────────────────────────────────────────────────
if start_btn and model_ready:
    st.session_state.running = True
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.markdown('<div class="notif info">⚠ Could not open camera. Check permissions.</div>', unsafe_allow_html=True)
        st.session_state.running = False
    else:
        stop_placeholder = st.empty()

        while st.session_state.running:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detected_faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in detected_faces:
                face_roi = cv2.resize(gray[y:y+h, x:x+w], (100, 100))
                label, confidence = recognizer.predict(face_roi)
                name = "Unknown"

                if confidence < 100:
                    name = label_map[label]
                    if st.session_state.attendance[name]["Status"] == "Absent":
                        now = datetime.now()
                        st.session_state.attendance[name]["Status"] = "Present"
                        st.session_state.attendance[name]["Time"] = now.strftime("%H:%M:%S")
                        st.session_state.log.append(f"{name} marked present at {now.strftime('%H:%M:%S')}")

                        # Auto-save CSV
                        pd.DataFrame.from_dict(
                            st.session_state.attendance, orient="index"
                        ).to_csv("attendance.csv")

                # Draw bounding box
                color = (0, 255, 136) if name != "Unknown" else (255, 68, 102)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                # Name background
                label_bg_y = y - 30 if y > 30 else y + h
                cv2.rectangle(frame, (x, label_bg_y), (x + w, label_bg_y + 28), color, -1)
                cv2.putText(frame, name, (x + 6, label_bg_y + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

                # Confidence badge
                if name != "Unknown":
                    conf_text = f"{int(100-confidence)}%"
                    cv2.putText(frame, conf_text, (x + w - 45, label_bg_y + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 2)

            # HUD overlay
            h_frame, w_frame = frame.shape[:2]
            ts = datetime.now().strftime("%H:%M:%S")
            cv2.putText(frame, f"LIVE  {ts}", (10, 26),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 136), 2)
            cv2.putText(frame, f"Faces: {len(detected_faces)}", (10, h_frame - 14),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 207, 255), 1)

            # Show frame
            frame_placeholder.image(frame, channels="BGR", use_container_width=True)

            # Update table live
            render_table()

        cap.release()
        st.session_state.running = False
        st.rerun()