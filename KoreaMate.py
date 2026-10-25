import streamlit as st
from urllib.parse import quote_plus

st.set_page_config(
    page_title="Korea Mate | Your Easy Guide to Korea",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
    .stApp { background: #f7f9fc; }
    .block-container { max-width: 1100px; padding-top: 2rem; padding-bottom: 3rem; }
    .hero {
        background: linear-gradient(120deg, #e8f3ff 0%, #f4f0ff 100%);
        border: 1px solid #e1e8f5;
        border-radius: 22px;
        padding: 2rem 1.5rem;
        text-align: center;
        margin-bottom: 1.3rem;
    }
    .hero h1 { margin: 0; color: #172b4d; font-size: 2.35rem; }
    .hero p { color: #42526e; margin: .45rem 0 0 0; font-size: 1.08rem; }
    .welcome {
        background: white; border: 1px solid #e5eaf2; border-radius: 18px;
        padding: 1.1rem 1.3rem; text-align: center; margin-bottom: 1.2rem;
    }
    .welcome h2 { margin: 0 0 .3rem 0; color: #172b4d; font-size: 1.55rem; }
    .welcome p { margin: 0; color: #52627a; }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: white; border: 1px solid #e5eaf2; border-radius: 16px;
        padding: 1rem; height: 100%;
    }
    .feature-title { font-size: 1.18rem; font-weight: 700; color: #172b4d; margin-bottom: .25rem; }
    .feature-desc { color: #52627a; min-height: 2.8rem; }
    .small-note { color: #6b778c; font-size: .88rem; }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>🌏 Korea Mate</h1>
      <p>Your Easy Guide to Korea</p>
    </div>
    <div class="welcome">
      <h2>🇰🇷 Welcome to Korea!</h2>
      <p>Everything you need for your trip to Korea, all in one place.</p>
      <p>한국 여행에 필요한 정보를 한곳에서!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Language and quick phrasebook ----------
LANGUAGES = {
    "English": "en",
    "日本語 (Japanese)": "ja",
    "中文 (Chinese)": "zh-CN",
    "Español (Spanish)": "es",
    "Français (French)": "fr",
    "한국어 (Korean)": "ko",
}

PHRASES = {
    "Hello": {"English": "Hello", "日本語 (Japanese)": "こんにちは", "中文 (Chinese)": "你好", "Español (Spanish)": "Hola", "Français (French)": "Bonjour", "한국어 (Korean)": "안녕하세요"},
    "Thank you": {"English": "Thank you", "日本語 (Japanese)": "ありがとうございます", "中文 (Chinese)": "谢谢", "Español (Spanish)": "Gracias", "Français (French)": "Merci", "한국어 (Korean)": "감사합니다"},
    "Excuse me": {"English": "Excuse me", "日本語 (Japanese)": "すみません", "中文 (Chinese)": "不好意思", "Español (Spanish)": "Disculpe", "Français (French)": "Excusez-moi", "한국어 (Korean)": "실례합니다"},
    "How much is it?": {"English": "How much is it?", "日本語 (Japanese)": "いくらですか？", "中文 (Chinese)": "多少钱？", "Español (Spanish)": "¿Cuánto cuesta?", "Français (French)": "C’est combien ?", "한국어 (Korean)": "얼마예요?"},
    "Where is the restroom?": {"English": "Where is the restroom?", "日本語 (Japanese)": "トイレはどこですか？", "中文 (Chinese)": "洗手间在哪里？", "Español (Spanish)": "¿Dónde está el baño?", "Français (French)": "Où sont les toilettes ?", "한국어 (Korean)": "화장실이 어디예요?"},
}

st.subheader("✨ What do you need today?")
st.caption("Choose a service below to get started.")

left_top, right_top = st.columns(2, gap="large")
left_bottom, right_bottom = st.columns(2, gap="large")

# Translator card
with left_top:
    with st.container(border=True):
        st.markdown('<div class="feature-title">🔤 Translator · 번역기</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-desc">Choose your language and translate words or sentences for your trip.</div>', unsafe_allow_html=True)
        target_language = st.selectbox(
            "Translate into",
            list(LANGUAGES.keys()),
            index=0,
            key="translate_language",
        )
        translate_text = st.text_input(
