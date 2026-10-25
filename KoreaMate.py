import streamlit as st
from urllib.parse import quote_plus

st.set_page_config(
    page_title="Korea Mate | Your Easy Guide to Korea",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

LANGUAGES = {
    "English": "en",
    "日本語 (Japanese)": "ja",
    "中文 (Chinese)": "zh-CN",
    "Español (Spanish)": "es",
    "Français (French)": "fr",
    "한국어 (Korean)": "ko",
}

PHRASES = {
    "Hello": {
        "English": "Hello",
        "日本語 (Japanese)": "こんにちは",
        "中文 (Chinese)": "你好",
        "Español (Spanish)": "Hola",
        "Français (French)": "Bonjour",
        "한국어 (Korean)": "안녕하세요",
    },
    "Thank you": {
        "English": "Thank you",
        "日本語 (Japanese)": "ありがとうございます",
        "中文 (Chinese)": "谢谢",
        "Español (Spanish)": "Gracias",
        "Français (French)": "Merci",
        "한국어 (Korean)": "감사합니다",
    },
    "Excuse me": {
        "English": "Excuse me",
        "日本語 (Japanese)": "すみません",
        "中文 (Chinese)": "不好意思",
        "Español (Spanish)": "Disculpe",
        "Français (French)": "Excusez-moi",
        "한국어 (Korean)": "실례합니다",
    },
    "How much is it?": {
        "English": "How much is it?",
        "日本語 (Japanese)": "いくらですか？",
        "中文 (Chinese)": "多少钱？",
        "Español (Spanish)": "¿Cuánto cuesta?",
        "Français (French)": "C’est combien ?",
        "한국어 (Korean)": "얼마예요?",
    },
    "Where is the restroom?": {
        "English": "Where is the restroom?",
        "日本語 (Japanese)": "トイレはどこですか？",
        "中文 (Chinese)": "洗手间在哪里？",
        "Español (Spanish)": "¿Dónde está el baño?",
        "Français (French)": "Où sont les toilettes ?",
        "한국어 (Korean)": "화장실이 어디예요?",
    },
}

st.markdown(
    """
    <style>
    .stApp { background: #f7f9fc; }
    .block-container { max-width: 1100px; padding-top: 2rem; padding-bottom: 3rem; }
    .hero {
        background: linear-gradient(120deg, #e8f3ff 0%, #f4f0ff 100%);
        border: 1px solid #e1e8f5; border-radius: 22px;
        padding: 2rem 1.5rem; text-align: center; margin-bottom: 1.2rem;
    }
    .hero h1 { margin: 0; color: #172b4d; font-size: 2.35rem; }
    .hero p { color: #42526e; margin: .45rem 0 0 0; font-size: 1.08rem; }
    .welcome {
        background: white; border: 1px solid #e5eaf2; border-radius: 18px;
        padding: 1.1rem 1.3rem; text-align: center; margin-bottom: 1.2rem;
    }
    .welcome h2 { margin: 0 0 .3rem 0; color: #172b4d; font-size: 1.55rem; }
    .welcome p { margin: .2rem 0; color: #52627a; }
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

st.subheader("✨ What do you need today?")
st.caption("Choose a service below to get started.")

left_top, right_top = st.columns(2, gap="large")
left_bottom, right_bottom = st.columns(2, gap="large")

# 1. Translator
with left_top:
    with st.container(border=True):
        st.markdown('<div class="feature-title">🔤 Translator · 번역기</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="feature-desc">Choose your language and translate words or sentences for your trip.</div>',
            unsafe_allow_html=True,
        )
        target_language = st.selectbox(
            "Translate into",
            options=list(LANGUAGES.keys()),
            index=0,
            key="translate_language",
        )
        translate_text = st.text_input(
            "Text to translate",
            placeholder="Type a word or sentence...",
            key="translate_text",
        )
        translate_url = (
            "https://translate.google.com/?sl=auto&tl="
            + LANGUAGES[target_language]
            + "&text="
            + quote_plus(translate_text)
            + "&op=translate"
        )
        st.link_button("Open Google Translate ↗", translate_url, use_container_width=True)
        with st.expander("Useful Korean phrases"):
            phrase = st.selectbox("Choose a phrase", options=list(PHRASES.keys()), key="phrase")
            st.success("Korean: " + PHRASES[phrase]["한국어 (Korean)"])
            st.write(target_language + ": " + PHRASES[phrase][target_language])

# 2. Directions
with right_top:
    with st.container(border=True):
        st.markdown('<div class="feature-title">🗺️ Directions · 길안내</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="feature-desc">Enter a destination and open directions in Google Maps.</div>',
            unsafe_allow_html=True,
        )
        destination = st.text_input(
            "Destination",
            placeholder="e.g. Gyeongbokgung Palace, Seoul",
            key="destination",
        )
        travel_mode = st.selectbox(
            "Travel mode",
            options=["Transit", "Walking", "Driving", "Bicycling"],
            key="travel_mode",
        )
        mode_values = {
            "Transit": "transit",
            "Walking": "walking",
            "Driving": "driving",
            "Bicycling": "bicycling",
        }
        if destination.strip():
            directions_url = (
                "https://www.google.com/maps/dir/?api=1&destination="
                + quote_plus(destination.strip())
                + "&travelmode="
                + mode_values[travel_mode]
            )
            st.link_button("Find my route ↗", directions_url, use_container_width=True)
        else:
            st.info("Enter a destination to create your directions link.")

# 3. Facility search
with left_bottom:
    with st.container(border=True):
        st.markdown('<div class="feature-title">🏪 Find Facilities · 시설 찾기</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="feature-desc">Find useful places such as convenience stores, restrooms, and pharmacies.</div>',
            unsafe_allow_html=True,
        )
        facility = st.selectbox(
            "Choose a facility",
            options=["Convenience store", "Restroom", "Pharmacy", "Hospital", "ATM", "Cafe"],
            key="facility",
        )
        facility_terms = {
            "Convenience store": "convenience store",
            "Restroom": "public restroom",
            "Pharmacy": "pharmacy",
            "Hospital": "hospital",
            "ATM": "ATM",
            "Cafe": "cafe",
        }
        facility_url = "https://www.google.com/maps/search/" + quote_plus(
            facility_terms[facility] + " in South Korea"
        )
        st.link_button("Search on Google Maps ↗", facility_url, use_container_width=True)
        st.caption("Tip: Allow location access on your device for more relevant nearby results.")

# 4. Korean culture
with right_bottom:
    with st.container(border=True):
        st.markdown('<div class="feature-title">🎎 Korean Culture · 한국 문화</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="feature-desc">Learn useful things about Korean customs before you explore.</div>',
            unsafe_allow_html=True,
        )
        culture_topic = st.selectbox(
            "Explore a topic",
            options=["Greetings & manners", "Food culture", "Public transportation", "Paying & shopping"],
            key="culture_topic",
        )
        culture_info = {
            "Greetings & manners": "A small bow is a common way to greet someone. In formal situations, use both hands when giving or receiving something from an older person.",
            "Food culture": "Meals often include rice, soup, and side dishes called banchan. At a shared meal, follow the host or other diners when deciding when to start.",
            "Public transportation": "Subways and buses are widely used in cities. Keep your transit card ready, follow signs, and leave priority seats for people who need them.",
            "Paying & shopping": "Cards are accepted in many places, but a little cash can be useful at some small shops or markets. Check prices before paying.",
        }
        st.info(culture_info[culture_topic])

st.divider()
st.markdown("### 💡 Travel tip")
st.write("Save important addresses before you go out, and check official travel or emergency information when needed.")
st.markdown(
    '<p class="small-note">Korea Mate is a student project demo. Translation and maps open external services; results depend on those services.</p>',
    unsafe_allow_html=True,
)
