
import streamlit as st

st.set_page_config(
    page_title="K-Travel Translator",
    page_icon="🇰🇷",
    layout="centered",
)

# -----------------------------
# 기본 디자인
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #f3f7ff 0%, #ffffff 48%);
}
.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
.hero {
    background: linear-gradient(135deg, #3457d5, #7195ff);
    padding: 30px 26px;
    border-radius: 22px;
    color: white;
    margin-bottom: 22px;
}
.hero h1 {
    color: white;
    font-size: 2.2rem;
    margin-bottom: 8px;
}
.hero p {
    color: #eef2ff;
    margin-bottom: 0;
}
.result {
    background: #f0f4ff;
    border: 1px solid #dce5ff;
    padding: 20px;
    border-radius: 15px;
    margin: 12px 0;
}
.small-note {
    color: #687386;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 여행 표현 데이터
# 형식: 한국어, 영어, 일본어, 중국어
# -----------------------------
LANGUAGES = {
    "English 🇺🇸": "en",
    "日本語 🇯🇵": "ja",
    "中文 🇨🇳": "zh",
}

PHRASES = [
    ("안녕하세요", "Hello.", "こんにちは。", "你好。", "기본 표현"),
    ("감사합니다", "Thank you.", "ありがとうございます。", "谢谢。", "기본 표현"),
    ("죄송합니다", "I'm sorry.", "すみません。", "对不起。", "기본 표현"),
    ("영어 할 수 있어요?", "Can you speak English?", "英語を話せますか？", "你会说英语吗？", "기본 표현"),
    ("화장실이 어디예요?", "Where is the restroom?", "トイレはどこですか？", "洗手间在哪里？", "길 찾기"),
    ("여기 어떻게 가요?", "How do I get there?", "ここへはどう行けばいいですか？", "怎么去这里？", "길 찾기"),
    ("지하철역이 어디예요?", "Where is the subway station?", "地下鉄の駅はどこですか？", "地铁站在哪里？", "길 찾기"),
    ("이 주소로 가 주세요", "Please take me to this address.", "この住所までお願いします。", "请带我去这个地址。", "교통"),
    ("이 역에서 내려 주세요", "Please let me off at this station.", "この駅で降ろしてください。", "请让我在这个站下车。", "교통"),
    ("이거 하나 주세요", "One of these, please.", "これを一つください。", "请给我一个这个。", "식당·카페"),
    ("메뉴판 주세요", "May I have the menu, please?", "メニューをください。", "请给我菜单。", "식당·카페"),
    ("물 주세요", "Water, please.", "お水をください。", "请给我水。", "식당·카페"),
    ("맵지 않게 해 주세요", "Please make it not spicy.", "辛くしないでください。", "请做得不辣。", "식당·카페"),
    ("계산해 주세요", "Could I have the bill, please?", "お会計をお願いします。", "请结账。", "식당·카페"),
    ("포장해 주세요", "Takeout, please.", "持ち帰りでお願いします。", "请打包。", "식당·카페"),
    ("얼마예요?", "How much is it?", "いくらですか？", "多少钱？", "쇼핑"),
    ("카드로 결제할 수 있어요?", "Can I pay by card?", "カードで払えますか？", "可以刷卡吗？", "쇼핑"),
    ("조금 더 저렴한 것이 있어요?", "Do you have something cheaper?", "もう少し安いものはありますか？", "有更便宜一点的吗？", "쇼핑"),
    ("예약했어요", "I have a reservation.", "予約しています。", "我有预约。", "숙소"),
    ("체크인하고 싶어요", "I'd like to check in.", "チェックインをお願いします。", "我想办理入住。", "숙소"),
    ("와이파이 비밀번호가 뭐예요?", "What's the Wi-Fi password?", "Wi-Fiのパスワードは何ですか？", "Wi-Fi密码是什么？", "숙소"),
    ("도와주세요", "Please help me.", "助けてください。", "请帮帮我。", "긴급 상황"),
    ("경찰을 불러 주세요", "Please call the police.", "警察を呼んでください。", "请帮我叫警察。", "긴급 상황"),
    ("병원이 어디예요?", "Where is the hospital?", "病院はどこですか？", "医院在哪里？", "긴급 상황"),
]

CATEGORIES = [
    "전체",
    "기본 표현",
    "길 찾기",
    "교통",
    "식당·카페",
    "쇼핑",
    "숙소",
    "긴급 상황",
]

# -----------------------------
# 화면 상단
# -----------------------------
st.markdown("""
<div class="hero">
    <h1>🇰🇷 K-Travel Translator</h1>
    <p>한국 여행에서 필요한 말을 쉽고 빠르게 찾아보세요.</p>
    <p>Easy Korean travel phrases at your fingertips.</p>
</div>
""", unsafe_allow_html=True)

st.caption("여행자를 위한 간편 번역 · API 키 불필요")

# -----------------------------
# 언어 선택
# -----------------------------
st.subheader("🌏 번역 언어")

language = st.selectbox(
    "어떤 언어로 번역할까요?",
    list(LANGUAGES.keys()),
    label_visibility="collapsed",
)

lang_index = list(LANGUAGES.keys()).index(language) + 1

# -----------------------------
# 문장 검색
# -----------------------------
st.subheader("🔎 여행 표현 찾기")

keyword = st.text_input(
    "한국어 문장 또는 키워드",
    placeholder="예: 화장실, 감사합니다, 얼마예요?",
)

category = st.selectbox("여행 상황", CATEGORIES)

filtered = []
for phrase in PHRASES:
    korean = phrase[0]
    translated = phrase[lang_index]
    phrase_category = phrase[4]

    matches_keyword = (
        not keyword.strip()
        or keyword.strip().lower() in korean.lower()
        or keyword.strip().lower() in translated.lower()
    )
    matches_category = category == "전체" or phrase_category == category

    if matches_keyword and matches_category:
        filtered.append(phrase)

# -----------------------------
# 번역 결과
# -----------------------------
st.subheader("💬 번역 결과")

if filtered:
    options = [
        f"{p[0]}  ·  {p[4]}"
        for p in filtered
    ]

    selected_label = st.selectbox(
        "번역할 문장을 선택하세요",
        options,
    )

    selected_index = options.index(selected_label)
    selected = filtered[selected_index]

    korean_text = selected[0]
    translated_text = selected[lang_index]

    st.markdown(
        f"""
        <div class="result">
            <p style="color:#53627c; margin-bottom:5px;">🇰🇷 한국어</p>
            <h3 style="margin-top:0;">{korean_text}</h3>
            <hr>
            <p style="color:#53627c; margin-bottom:5px;">{language}</p>
            <h3 style="margin-top:0;">{translated_text}</h3>
            <p class="small-note">상황: {selected[4]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.code(translated_text, language=None)
    st.caption("위 번역문을 선택해 복사한 뒤 여행 중 사용하세요.")

else:
    st.info("검색 결과가 없어요. 다른 키워드나 여행 상황을 선택해 보세요.")

# -----------------------------
# 빠른 문장 모음
# -----------------------------
st.divider()
st.subheader("✨ 바로 쓰는 필수 표현")

quick_phrases = [
    ("감사합니다", "Thank you.", "ありがとうございます。", "谢谢。"),
    ("얼마예요?", "How much is it?", "いくらですか？", "多少钱？"),
    ("도와주세요", "Please help me.", "助けてください。", "请帮帮我。"),
    ("화장실이 어디예요?", "Where is the restroom?", "トイレはどこですか？", "洗手间在哪里？"),
]

quick_index = list(LANGUAGES.keys()).index(language) + 1

for korean, english, japanese, chinese in quick_phrases:
    translations = [korean, english, japanese, chinese]
    with st.container(border=True):
        left, right = st.columns([1, 2])
        with left:
            st.write(f"🇰🇷 {korean}")
        with right:
            st.write(translations[quick_index])

# -----------------------------
# 안내
# -----------------------------
st.divider()
st.markdown("""
<div class="small-note">
<strong>이용 안내</strong><br>
이 앱은 미리 준비한 여행 표현을 번역합니다.
자유롭게 입력한 새로운 문장을 자동 번역하는 기능은 포함되어 있지 않습니다.
긴급 상황에서는 주변 직원이나 현지 긴급 지원 기관에도 도움을 요청하세요.
</div>
""", unsafe_allow_html=True)

