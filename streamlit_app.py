import streamlit as st
import cv2
from app import main as gesture_stream

st.set_page_config(page_title="Defendum", layout="wide")
st.title("🛡️ Defendum: Gesture-Controlled In-Car Assistant")

# Initialize state
if "running" not in st.session_state:
    st.session_state.running = False

# Layout setup
left_col, right_col = st.columns([2, 1])  # Video left, gestures right

with left_col:
    # Start/Stop buttons in the same row
    b1, b2 = st.columns(2)
    with b1:
        if st.button("▶️ Start Webcam") and not st.session_state.running:
            st.session_state.running = True
    with b2:
        if st.button("⛔ Stop Webcam") and st.session_state.running:
            st.session_state.running = False

    frame_placeholder = st.empty()

# Right column for gesture/action display
with right_col:
    gesture_text = st.empty()
    action_text = st.empty()

# Run webcam if active
if st.session_state.running:
    gesture_feed = gesture_stream()  # Start fresh each time
    while st.session_state.running:
        try:
            frame, gesture_name, action_name = next(gesture_feed)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame, channels="RGB")

            gesture_text.markdown(f"### 🤖 Gesture: `{gesture_name}`")
            action_text.markdown(f"### 🎯 Action: `{action_name}`")

        except StopIteration:
            break
        except Exception as e:
            st.error(f"Camera error: {e}")
            break
