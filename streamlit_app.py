import streamlit as st
import cv2
from app import main as gesture_stream

st.set_page_config(page_title="Defendum", layout="wide")
st.title("🛡️ Defendum: Gesture-Controlled In-Car Assistant")

# Initialize session state
if "running" not in st.session_state:
    st.session_state.running = False

# Layout: Left - video & controls, Right - gesture info
left_col, right_col = st.columns([2, 1])

with left_col:
    b1, b2 = st.columns(2)
    with b1:
        if st.button("▶️ Start Webcam") and not st.session_state.running:
            st.session_state.running = True
    with b2:
        if st.button("⛔ Stop Webcam") and st.session_state.running:
            st.session_state.running = False

    frame_placeholder = st.empty()

with right_col:
    gesture_text = st.empty()
    action_text = st.empty()
    dyn_gesture_text = st.empty()
    dyn_action_text = st.empty()

# Run webcam if active
if st.session_state.running:
    gesture_feed = gesture_stream()
    while st.session_state.running:
        try:
            frame, gesture_name, action_name, dyn_label, dyn_action = next(gesture_feed)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame, channels="RGB")

            gesture_text.markdown(f"### 🤖 Gesture: `{gesture_name}`")
            action_text.markdown(f"### 🎯 Action: `{action_name}`")
            dyn_gesture_text.markdown(f"### 🔄 Dynamic Gesture: `{dyn_label}`")
            dyn_action_text.markdown(f"### 🕹️ Dynamic Action: `{dyn_action}`")

        except StopIteration:
            break
        except Exception as e:
            st.error(f"Camera error: {e}")
            break
