import streamlit as st
import numpy as np
import streamlit_authenticator as stauth
from datetime import datetime
import os
import yaml
from yaml.loader import SafeLoader

# 1. Page Configuration
st.set_page_config(
    page_title="ChannelX AI - Cross-Platform Algorithm Diagnostics",
    page_icon="🚦",
    layout="centered"
)

# 2. Database Handling: Read and verify config.yaml structure
if not os.path.exists('config.yaml'):
    default_config = {
        "cookie": {"expiry_days": 30, "key": "abcdef_secret_key", "name": "channelx_cookie"},
        "credentials": {
            "usernames": {
                "sujit": {"email": "sujit@gmail.com", "first_name": "Sujit", "last_name": "Kumar", "password": "sujit123"},
                "creator1": {"email": "creator@gmail.com", "first_name": "Rohan", "last_name": "Sharma", "password": "sharma123"}
            }
        }
    }
    with open('config.yaml', 'w') as file:
        yaml.dump(default_config, file, default_flow_style=False, allow_unicode=True)

with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=SafeLoader)

# 🛠️ Auto-Hash plain passwords natively
for username_key in config['credentials']['usernames']:
    raw_password = config['credentials']['usernames'][username_key]['password']
    if not str(raw_password).startswith('$2b$') and not str(raw_password).startswith('$2a$'):
        hashed_password = stauth.Hasher([raw_password]).generate()
        config['credentials']['usernames'][username_key]['password'] = hashed_password

# 3. Initialize Authenticator Engine safely
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Helper Function to Log User Activity
def log_user_activity(username, name):
    log_file = "login_logs.txt"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{current_time} | Username: {username} | Name: {name}\n")

# 4. Render Login & Sign-Up Interface in Tabs
tab1, tab2 = st.tabs(["🔒 Login", "📝 Sign Up / Register"])

with tab1:
    authenticator.login(location='main')

with tab2:
    try:
        if authenticator.register_user(location='main'):
            st.success('User registered successfully! Please switch to the Login tab. 🎉')
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
    except Exception as e:
        st.error(f"Registration Error: {e}")

# 5. Retrieve login status safely from Streamlit Session State
authentication_status = st.session_state.get('authentication_status')
username = st.session_state.get('username')
name = st.session_state.get('name')

# 6. Check Authentication Logic
if authentication_status == False:
    st.error("🚨 Username/password is incorrect. / यूजरनेम या पासवर्ड गलत है।")

elif authentication_status == None:
    st.warning("🔒 Please enter your username and password to unlock ChannelX AI.")

elif authentication_status == True:
    if 'logged_in_recorded' not in st.session_state:
        log_user_activity(username, name)
        st.session_state['logged_in_recorded'] = True

    # Sidebar Config
    with st.sidebar:
        st.write(f"Welcome, **{name}**! 👋")
        authenticator.logout('Logout', 'sidebar')
        st.markdown("---")
        
        if username == "sujit":
            st.header("👑 Admin Panel")
            show_logs = st.checkbox("View Login History")
            st.markdown("---")
            
        lang = st.radio("Choose Language / भाषा चुनें", ["English", "हिंदी"])

    # --- 👑 ADMIN PANEL UI LOGIC ---
    if username == "sujit" and show_logs:
        st.title("📂 User Login History Logs")
        if os.path.exists("login_logs.txt"):
            with open("login_logs.txt", "r", encoding="utf-8") as f:
                logs = f.readlines()
            for log in reversed(logs):
                st.text(log.strip())
        else:
            st.info("No login logs found yet.")
        st.markdown("---")

    # --- 🚦 MAIN CORE APP INTERFACE ---
    st.title("🚦 ChannelX AI 2.0")
    st.subheader("Cross-Platform Algorithm Diagnostics Engine 🌐")
    st.write("Select your digital platform to analyze content fatigue and algorithmic reach suppression.")
    st.markdown("---")

    # Platform Selector Configuration Dropdown
    if lang == "English":
        platform = st.selectbox("Target Social Media Platform:", options=["YouTube Video/Shorts", "Instagram Reels/Post", "Facebook Post/Reels", "LinkedIn Article/Post"])
    else:
        platform = st.selectbox("टारगेट सोशल मीडिया प्लेटफॉर्म चुनें:", options=["YouTube Video/Shorts", "Instagram Reels/Post", "Facebook Post/Reels", "LinkedIn Article/Post"])

    st.markdown("---")
    st.header(f"📊 Enter {platform} Analytics Metrics")

    # Dynamic Field Processing Engine
    if lang == "English":
        topic_shift_input = st.selectbox("Did you change your core content theme/niche for this specific upload?", options=["No (Consistent Niche)", "Yes (Heavy Topic Shift)"])
        
        if "YouTube" in platform:
            ctr_label, ctr_help = "Click-Through Rate (CTR) after 3 hours (%)", "Percentage of viewers who clicked your thumbnail."
            ret_label = "Audience Retention Rate (%)"
            ratio_label = "Initial Views-to-Subscriber Ratio"
        elif "Instagram" in platform:
            ctr_label, ctr_help = "Hook Rate / First 3s View Rate (%)", "Percentage of users who didn't immediately scroll away."
            ret_label = "Average Watch Time Percentage (%)"
            ratio_label = "Non-Follower Reach Ratio (Explore Matrix)"
        elif "Facebook" in platform:
            ctr_label, ctr_help = "Link/Image Click Rate (%)", "Percentage of users interacting with post assets."
            ret_label = "Dwell Retention Index (%)"
            ratio_label = "Initial Feed Engagement Share Ratio"
        else:
            ctr_label, ctr_help = "'See More' Expansion Click Rate (%)", "Percentage of users who expanded your textual post."
            ret_label = "Text Reading Time vs Average Matrix (%)"
            ratio_label = "Profile Visit-to-Connection Ratio Index"

        ctr_input = st.slider(ctr_label, 0.0, 20.0, 6.5, step=0.1, help=ctr_help)
        retention_input = st.slider(ret_label, 0.0, 100.0, 35.0, step=0.5)
        views_input = st.slider(ratio_label, 0.00, 1.00, 0.05, step=0.01)
        submit_btn = st.button("🚀 Run Algorithm Pulse Check")
        
    else:
        topic_shift_input = st.selectbox("क्या आपने इस विशिष्ट पोस्ट/वीडियो के लिए अपना मुख्य टॉपिक बदला है?", options=["नहीं (समान केटेगरी है)", "हाँ (अचानक नया टॉपिक डाला है)"])
        
        if "YouTube" in platform:
            ctr_label = "3 घंटे के बाद क्लिक-थ्रू रेट (CTR) (%)"
            ret_label = "ऑडियंस रिटेंशन index (%)"
            ratio_label = "शुरुआती व्यूज और सब्सक्राइबर्स का अनुपात (Ratio)"
        elif "Instagram" in platform:
            ctr_label = "शुरुआती 3 सेकंड हुक रेट (Hook Rate) (%)"
            ret_label = "औसत रील वॉच-टाइम प्रतिशत (%)"
            ratio_label = "नॉन-फॉलोअर्स रीच अनुपात (Explore Ratio)"
        elif "Facebook" in platform:
            ctr_label = "लिंक/इमेज क्लिक इंटरेक्शन रेट (%)"
            ret_label = "पेज स्टे रिटेंशन इंडेक्स (%)"
            ratio_label = "फ़ीड इंगेजमेंट और शेयर अनुपात"
        else:
            ctr_label = "'See More' टेक्स्ट एक्सपेंशन क्लिक रेट (%)"
            ret_label = "PRO रीडिंग टाइम अनुपात (%)"
            ratio_label = "प्रोफाइल विज़िट और कनेक्शन अनुपात सूचकांक"

        ctr_input = st.slider(ctr_label, 0.0, 20.0, 6.5, step=0.1)
        retention_input = st.slider(ret_label, 0.0, 100.0, 35.0, step=0.5)
        views_input = st.slider(ratio_label, 0.00, 1.00, 0.05, step=0.01)
        submit_btn = st.button("🚀 एल्गोरिदम पल्स की जांच करें")

    # 7. Unified Logistic Regression Predictive Backend Execution
    if submit_btn:
        topic_shift_encoded = 1 if "Yes" in topic_shift_input or "हाँ" in topic_shift_input else 0
        w_topic_shift, w_ctr, w_retention, w_views_ratio, intercept = 3.5124, -0.4102, -0.1054, -5.0211, 2.0145
        
        z = (w_topic_shift * topic_shift_encoded) + (w_ctr * ctr_input) + (w_retention * retention_input) + (w_views_ratio * views_input) + intercept
        probability_dead = 1 / (1 + np.exp(-z))
        probability_healthy = 1 - probability_dead
        
        st.markdown("---")
        st.header("🎯 Algorithm Diagnostic Analysis Report")
        
        # 👑 THE BULLETPROOF FLAT LOGIC: No sub-blocks, no elifs, strictly straight if codes!
        if probability_dead >= 0.5 and lang == "English" and topic_shift_encoded == 1:
            st.error(f"🚨 **Status: ALGORITHMIC SUPPRESSION DETECTED** (Probability of Failure: {probability_dead * 100:.2f}%)")
            st.warning(f"💡 **Reason:** Shifting your niche on {platform} heavily fractured your core user behavior data model. The system suppressed the impressions!")
            
        if probability_dead >= 0.5 and lang == "English" and topic_shift_encoded == 0:
            st.error(f"🚨 **Status: ALGORITHMIC SUPPRESSION DETECTED** (Probability of Failure: {probability_dead * 100:.2f}%)")
            st.warning("💡 **Action Item:** Content niche is safe, but conversion rates are too low to trigger the platform's recommendation engine. Optimize your assets instantly!")
            
        if probability_dead >= 0.5 and lang != "English" and topic_shift_encoded == 1:
            st.error(f"🚨 **स्थिति: एल्गोरिदम द्वारा रीच रोक दी गई है** (असफल होने की संभावना: {probability_dead * 100:.2f}%)")
            st.warning(f"💡 **मुख्य कारण:** {platform} पर अचानक केटेगरी बदलने से यूजर बिहेवियर डेटा मॉडल टूट गया है। सिस्टम ने आपकी post की रीच रोक दी है!")
            
