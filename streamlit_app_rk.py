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
    emoji_box = st.empty()
    dyn_gesture_text = st.empty()
    dyn_action_text = st.empty()
    dict_box = st.empty()

# Emoji and dictionary mapping
emoji_map = {
    "Help": "🆘",
    "OK": "✅",
    "Open": "🔓",
    "Close": "🔒",
    "Pointer": "👉",
    "Temperature Ctrl": "🌡️",
    "Vent Ctrl": "🌬️",
    "Lights Ctrl": "💡",
    "Open Manual": "📖",
    "Open Navigation": "🧭",
    "None": "❔"
}

gesture_action_dict = {
    "🔓": "Open System",
    "🔒": "Close System",
    "👉": "Pointer Mode",
    "✅": "Confirm (OK)",
    "🆘": "Call Help / SOS",
    "🌡️": "Adjust Temperature",
    "🌬️": "Control Vents",
    "💡": "Control Lights",
    "📖": "Manual Override",
    "🧭": "Open Navigation"
}

def map_action_to_emoji(action_name):
    mapping = {
        "Open System": "Open",
        "Close System": "Close",
        "Pointer Mode": "Pointer",
        "Confirm (OK)": "OK",
        "Call Help / SOS": "Help",
        "Adjust Temperature": "Temperature Ctrl",
        "Control Vents": "Vent Ctrl",
        "Control Lights": "Lights Ctrl",
        "Manual Override": "Open Manual",
        "Open Navigation": "Open Navigation"
    }
    return mapping.get(action_name, "None")

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

            # Get the emoji key and display the corresponding emoji
            emoji_key = map_action_to_emoji(action_name)
            emoji = emoji_map.get(emoji_key, "❔")
            emoji_box.markdown(
                f"""
                <div style="
                    width: 3cm;
                    height: 3cm;
                    border: 2px solid #ddd;
                    border-radius: 5px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 48px;
                    margin: 10px 0;
                ">
                    {emoji}
                </div>
                """,
                unsafe_allow_html=True
            )

            dyn_gesture_text.markdown(f"### 🔄 Dynamic Gesture: `{dyn_label}`")
            dyn_action_text.markdown(f"### 🕹️ Dynamic Action: `{dyn_action}`")

            # Show dictionary and stop webcam if 'Open Manual' detected
            if gesture_name == "Open Manual":
                # st.session_state.running = False
                dict_box.markdown(
                    """
                    <div style='padding: 1rem; background-color: #f1f3f6; border-radius: 10px; border: 1px solid #ccc'>
                        <h4>📖 Gesture-Action Dictionary</h4>
                        <ul style='line-height: 1.6'>
                    """ + "".join(
                        [f"<li><strong>{emoji}</strong>: {desc}</li>" for emoji, desc in gesture_action_dict.items()]
                    ) + "</ul></div>", unsafe_allow_html=True)
                
            if gesture_name == "Open Navigation":
                dict_box.image("Maps_screenshot.png", caption="Navigation Map", use_column_width=True)

            if gesture_name == "Close":
                dict_box.empty()

        except StopIteration:
            break
        except Exception as e:
            st.error(f"Camera error: {e}")
            break