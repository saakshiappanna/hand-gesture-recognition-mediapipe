import streamlit as st
import cv2
from app import main as gesture_stream

st.set_page_config(page_title="QuietCommute", layout="wide")

# Title and subtitle
st.markdown("""
    <div style='text-align: left; margin-bottom: 20px;'>
        <h1 style='font-size: 3em; margin-bottom: 0;'>🛡️ QuietCommute</h1>
        <h4 style='color: gray; margin-top: 0;'>True luxury is defined by its inclusivity</h4>
    </div>
""", unsafe_allow_html=True)

# Session state
if "running" not in st.session_state:
    st.session_state.running = False
if "temp" not in st.session_state:
    st.session_state.temp = 22
if "frame_counter" not in st.session_state:
    st.session_state.frame_counter = 0

# Layout
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
    action_text = st.empty()
    dyn_action_text = st.empty()
    emoji_col, dyn_col = st.columns([1, 2])  # 1:2 ratio for better room for blocks
    with emoji_col:
        emoji_box = st.empty()
    with dyn_col:
        dyn_action_box = st.empty()
    dict_box = st.empty()
    



# Mappings
emoji_map = {
    "Help": "🆘", "OK": "✅", "Open": "🔓", "Close": "🔒",
    "Pointer": "👉", "Temperature Ctrl": "🌡️", "Vent Ctrl": "🌬️",
    "Lights Ctrl": "💡", "Open Manual": "📖", "Open Navigation": "🧭",
    "None": "❔"
}

gesture_action_dict = {
    "🔓": "Open System", "🔒": "Close System", "👉": "Pointer Mode",
    "✅": "Confirm (OK)", "🆘": "Call Help / SOS", "🌡️": "Adjust Temperature",
    "🌬️": "Control Vents", "💡": "Control Lights", "📖": "Manual Override",
    "🧭": "Open Navigation"
}

def map_action_to_emoji(action_name):
    mapping = {
        "Open System": "Open", "Close System": "Close", "Pointer Mode": "Pointer",
        "Confirm (OK)": "OK", "Call Help / SOS": "Help", "Adjust Temperature": "Temperature Ctrl",
        "Control Vents": "Vent Ctrl", "Control Lights": "Lights Ctrl",
        "Manual Override": "Open Manual", "Open Navigation": "Open Navigation"
    }
    return mapping.get(action_name, "None")

# Webcam loop
if st.session_state.running:
    gesture_feed = gesture_stream()
    while st.session_state.running:
        try:
            st.session_state.frame_counter += 1
            update_this_frame = st.session_state.frame_counter % 3 == 0

            frame, gesture_name, action_name, dyn_label, dyn_action = next(gesture_feed)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame, channels="RGB")

            action_text.markdown(f"### 🎯 Action: `{action_name}`")
            dyn_action_text.markdown(f"### 🕹️ Dynamic Action: `{dyn_action}`")

            # Static gesture emoji display
            emoji_key = map_action_to_emoji(action_name)
            emoji = emoji_map.get(emoji_key, " ")
            emoji_box.markdown(f"""
               <div style="
                   width: 100%;
                   height: 120px;
                   border: 2px solid #ddd;
                   border-radius: 10px;
                   display: flex;
                   align-items: center;
                   justify-content: center;
                   font-size: 48px;
                   margin: 10px 0;
                   background-color: #fff;
               ">{emoji}</div>
           """, unsafe_allow_html=True)
            
            # Dynamic visual feedback with temperature block logic
            max_blocks = 5
            temp_range = 28 - 16
            filled_blocks = round((st.session_state.temp - 16) / temp_range * max_blocks)
            empty_blocks = max_blocks - filled_blocks

            if dyn_action == "Rotate Vent Clockwise":
                if st.session_state.temp < 28 and update_this_frame:
                    st.session_state.temp += 1
                temp_bar = "🟥" * filled_blocks + "⬜" * empty_blocks
                dyn_action_box.markdown(f"""
                    <div style='padding: 10px; background: #fff; border: 1px solid #aaa; border-radius: 10px;'>
                        <div style="height: 1px;"></div>
                        <p><strong>{st.session_state.temp}°C</strong></p>
                        <div style='font-size: 26px; letter-spacing: 5px;'>{temp_bar}</div>
                    </div>
                """, unsafe_allow_html=True)

            elif dyn_action == "Rotate Vent Counter-Clockwise":
                if st.session_state.temp > 16 and update_this_frame:
                    st.session_state.temp -= 1
                temp_bar = "🟦" * filled_blocks + "⬜" * empty_blocks
                dyn_action_box.markdown(f"""
                    <div style='padding: 10px; background: #fff; border: 1px solid #aaa; border-radius: 10px;'>
                        <div style="height: 1px;"></div>
                        <p><strong>{st.session_state.temp}°C</strong></p>
                        <div style='font-size: 26px; letter-spacing: 5px;'>{temp_bar}</div>
                    </div>
                """, unsafe_allow_html=True)
            elif dyn_action == "Slide Display Right":
                dyn_action_box.markdown(f"""
                    <div style='padding: 10px; background: #f0f9ff; border: 1px solid #aaa; border-radius: 10px;'>
                        <div style="height: 1px;"></div>
                        <div style='font-size: 28px;'>➡️ ➡️ ➡️</div>
                    </div>
                """, unsafe_allow_html=True)
            
            elif dyn_action == "Slide Display Left":
                dyn_action_box.markdown(f"""
                    <div style='padding: 10px; background: #f0f9ff; border: 1px solid #aaa; border-radius: 10px;'>
                        <div style="height: 1px;"></div>
                        <div style='font-size: 28px;'>⬅️ ⬅️ ⬅️</div>
                    </div>
                """, unsafe_allow_html=True)    

            else:
                dyn_action_box.markdown(f"""
                    <div style='
                    width: 100%;
                    height: 120px;
                    background: #fff;
                    border: 2px solid #ddd;
                    border-radius: 10px;
                    padding: 10px;
                    overflow: hidden;
                    margin: 10px 0;
                '>
                        <p> </p>
                    </div>
                """, unsafe_allow_html=True)

            # Manual / Navigation visualizations
            if gesture_name == "Open Manual":
                dict_box.markdown(
                    "<div style='padding: 1rem; background-color: #f1f3f6; border-radius: 10px; border: 1px solid #ccc'><h4>📖 Gesture-Action Dictionary</h4><ul style='line-height: 1.6'>" +
                    "".join([f"<li><strong>{emoji}</strong>: {desc}</li>" for emoji, desc in gesture_action_dict.items()]) +
                    "</ul></div>", unsafe_allow_html=True)

            elif gesture_name == "Open Navigation":
                dict_box.image("Maps_screenshot.png", caption="Navigation Map", use_container_width=True)

            elif gesture_name == "Close":
                dict_box.empty()

        except StopIteration:
            break
        except Exception as e:
            st.error(f"Camera error: {e}")
            break
