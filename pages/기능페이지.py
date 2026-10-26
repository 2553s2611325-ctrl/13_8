"""Korea Culture Guide — a fully offline, rule-based Streamlit chat app."""

from __future__ import annotations

import streamlit as st

MAX_INPUT_CHARS = 600

WELCOME = (
    "Hi! I'm your Korea Culture Guide. 🇰🇷\n\n"
    "I answer common questions using a built-in collection of prepared explanations. "
    "No API key or external AI service is needed. Try asking about greetings, food, "
    "public transport, tipping, shoes, hanbok, or Korean phrases."
)

SUGGESTED_QUESTIONS = [
    "Why do people bow in Korea?",
    "How does Korean BBQ work?",
    "What should I know about subway manners?",
    "Is tipping expected in Korea?",
    "What Korean phrases should I learn?",
    "Tell me about hanbok.",
]

# Each entry has keywords and a prepared answer. Keyword matching is intentionally
# simple so the app has no external service dependency and is easy to maintain.
ANSWERS = [
    {
        "title": "Greetings and bowing",
        "keywords": ("bow", "greet", "hello", "greeting", "인사", "절", "고개 숙", "안녕"),
        "answer": (
            "### Greetings and bowing\n\n"
            "A small bow or nod is a common polite greeting in Korea. It can also show thanks or respect. "
            "You do not need to bow deeply in everyday situations. A friendly **안녕하세요 (annyeonghaseyo)** means ‘hello’ and is a useful place to start.\n\n"
            "**Travel tip:** A smile and a polite greeting are enough in most casual situations. Customs can vary by person and setting."
        ),
    },
    {
        "title": "Korean BBQ and dining",
        "keywords": ("bbq", "barbecue", "samgyeopsal", "restaurant", "dining", "eat", "food", "meal", "banchan", "고기", "음식", "식당", "반찬", "삼겹살"),
        "answer": (
            "### Korean BBQ and dining\n\n"
            "At Korean BBQ restaurants, diners often grill meat at the table and share side dishes. Small side dishes are called **반찬 (banchan)**. Rice, soup, vegetables, and sauces may also be served.\n\n"
            "**Travel tips:**\n"
            "- Check whether dishes are for sharing.\n"
            "- Use serving utensils when provided.\n"
            "- Ask staff about spice levels or ingredients if you have dietary needs.\n"
            "- Some restaurants expect each diner to order a main item; policies vary by restaurant."
        ),
    },
    {
        "title": "Public transport manners",
        "keywords": ("subway", "metro", "train", "bus", "transport", "transit", "t-money", "지하철", "버스", "교통", "대중교통"),
        "answer": (
            "### Public transport manners\n\n"
            "On buses and subways, let passengers exit before you board, keep doorways clear, and use headphones for audio. Speak quietly and follow signs and announcements.\n\n"
            "Some seats are designated for people who may need them, including older adults, disabled passengers, and pregnant passengers.\n\n"
            "**Travel tip:** Transit cards and fare rules can vary by city and service. Check station signs or official transit guidance for current details."
        ),
    },
    {
        "title": "Tipping",
        "keywords": ("tip", "tipping", "gratuity", "service charge", "팁", "봉사료"),
        "answer": (
            "### Tipping in Korea\n\n"
            "Tipping is **not generally expected** at most everyday restaurants and cafés in South Korea. Some tourist-focused services may have different practices, so check the bill or service information rather than assuming.\n\n"
            "A sincere **감사합니다 (gamsahamnida)** means ‘thank you’ and is always useful."
        ),
    },
    {
        "title": "Shoes indoors and at temples",
        "keywords": ("shoe", "shoes", "indoors", "house", "home", "temple", "remove shoes", "신발", "집", "절", "사찰"),
        "answer": (
            "### Shoes indoors\n\n"
            "You may be asked to remove your shoes in Korean homes and in some restaurants or spaces with floor seating. Look for a shoe rack or signs, and follow your host's instructions.\n\n"
            "At temples and cultural sites, follow posted instructions and photography rules. If you are unsure, politely ask staff."
        ),
    },
    {
        "title": "Hanbok",
        "keywords": ("hanbok", "traditional clothes", "traditional clothing", "한복"),
        "answer": (
            "### Hanbok\n\n"
            "**Hanbok (한복)** is traditional Korean clothing worn for occasions such as holidays, ceremonies, and celebrations. There are traditional and modern styles. Visitors can rent hanbok at some cultural and tourist areas.\n\n"
            "**Travel tips:** Follow the rental shop's instructions, treat historic spaces carefully, and ask before photographing other people."
        ),
    },
    {
        "title": "Hanok and traditional homes",
        "keywords": ("hanok", "traditional house", "architecture", "ondol", "한옥", "온돌"),
        "answer": (
            "### Hanok and traditional homes\n\n"
            "**Hanok (한옥)** refers to traditional Korean buildings. Depending on the building, you may see wooden frames, tiled roofs, courtyards, and **온돌 (ondol)**, a traditional underfloor heating system.\n\n"
            "Some hanok neighborhoods are still residential. Keep noise low and respect signs that mark private spaces."
        ),
    },
    {
        "title": "Useful Korean phrases",
        "keywords": ("phrase", "phrases", "korean words", "language", "speak korean", "how to say", "존댓말", "한국어", "표현", "말해"),
        "answer": (
            "### Useful Korean phrases\n\n"
            "| Korean | Pronunciation | Meaning |\n"
            "|---|---|---|\n"
            "| 안녕하세요 | an-nyeong-ha-se-yo | Hello |\n"
            "| 감사합니다 | gam-sa-ham-ni-da | Thank you |\n"
            "| 죄송합니다 | joe-song-ham-ni-da | I'm sorry / excuse me |\n"
            "| 얼마예요? | eol-ma-ye-yo? | How much is it? |\n"
            "| 화장실이 어디예요? | hwa-jang-sil-i eo-di-ye-yo? | Where is the restroom? |\n\n"
            "Polite forms are a good starting point when speaking with someone you have just met."
        ),
    },
    {
        "title": "Polite language and honorifics",
        "keywords": ("honorific", "speech level", "polite", "informal", "banmal", "oppa", "존댓말", "반말", "호칭"),
        "answer": (
            "### Polite Korean\n\n"
            "Korean speech changes with politeness, familiarity, and context. When meeting someone for the first time, polite expressions such as **안녕하세요** (hello) and **감사합니다** (thank you) are a safe starting point.\n\n"
            "Relationship words and titles can be context-specific. If you are unsure, use polite language and follow the other person's lead."
        ),
    },
    {
        "title": "Kimchi",
        "keywords": ("kimchi", "fermented", "김치"),
        "answer": (
            "### Kimchi\n\n"
            "**Kimchi (김치)** is a family of fermented vegetable dishes, often made with napa cabbage or radish and seasonings. Recipes and spice levels vary. It is commonly served as a side dish, but Korean food culture includes many other dishes too.\n\n"
            "If you avoid spicy food or have dietary restrictions, ask about the ingredients before ordering."
        ),
    },
    {
        "title": "Giving and receiving items",
        "keywords": ("gift", "giving", "receive", "receiving", "two hands", "선물", "두 손"),
        "answer": (
            "### Giving and receiving items\n\n"
            "In some Korean settings, using both hands—or supporting one arm with the other—when giving or receiving a gift or important item can show respect. It is a thoughtful gesture, not a strict rule in every situation.\n\n"
            "Follow the tone of the occasion and the other person's lead."
        ),
    },
    {
        "title": "Age and respect",
        "keywords": ("age", "older", "elder", "respect", "senior", "나이", "어른", "예의"),
        "answer": (
            "### Age and respect\n\n"
            "Age and social relationships can influence forms of address and speech levels in Korea, but people differ in their preferences. You do not need to know someone's age to be polite.\n\n"
            "Start with polite language, avoid overly personal questions with strangers, and follow the other person's cues."
        ),
    },
    {
        "title": "Cash, cards, and payments",
        "keywords": ("pay", "payment", "cash", "card", "credit card", "money", "결제", "현금", "카드"),
        "answer": (
            "### Paying in Korea\n\n"
            "Cards are widely accepted in many Korean shops and restaurants, but it is useful to keep a little cash for situations where card payment is unavailable. Payment options vary by business.\n\n"
            "For transport, check which transit cards or mobile payment options are supported by the service you plan to use."
        ),
    },
    {
        "title": "Korean holidays",
        "keywords": ("holiday", "seollal", "chuseok", "lunar new year", "설날", "추석", "명절"),
        "answer": (
            "### Korean holidays\n\n"
            "**Seollal (설날)**, the Lunar New Year holiday, and **Chuseok (추석)**, a harvest holiday, are important family-centered occasions for many Koreans. Traditions can include family gatherings, special foods, and honoring ancestors.\n\n"
            "Travel tip: transportation and business hours may change around major holidays, so check official information before making plans."
        ),
    },
    {
        "title": "Photography and etiquette",
        "keywords": ("photo", "photograph", "photography", "picture", "camera", "사진", "촬영"),
        "answer": (
            "### Photography etiquette\n\n"
            "Check signs before taking photos in museums, temples, performances, and private businesses. Ask permission before photographing people, especially children or workers. Avoid blocking walkways while taking pictures.\n\n"
            "Rules vary by venue, so posted instructions should take priority."
        ),
    },
]

FALLBACK = (
    "I don't have a prepared answer for that question yet. This guide works with a fixed set of cultural topics, "
    "so it does not generate new answers like an AI chatbot.\n\n"
    "**Try asking about:** greetings and bowing, Korean BBQ, subway manners, tipping, shoes indoors, hanbok, "
    "hanok, useful Korean phrases, kimchi, polite language, holidays, or photography etiquette."
)


def get_answer(question: str) -> str:
    """Find a prepared answer using simple keyword matching."""
    normalized = question.casefold().strip()
    if not normalized:
        return "Please enter a question about Korean culture."

    # Score by number of matched keywords so a more specific topic can win.
    best_answer = None
    best_score = 0
    for item in ANSWERS:
        score = sum(1 for keyword in item["keywords"] if keyword.casefold() in normalized)
        if score > best_score:
            best_score = score
            best_answer = item["answer"]

    return best_answer if best_answer else FALLBACK


def reset_chat() -> None:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME}]


def render_message(message: dict[str, str]) -> None:
    role = "assistant" if message.get("role") == "assistant" else "user"
    avatar = "🤖" if role == "assistant" else "🧳"
    with st.chat_message(role, avatar=avatar):
        if role == "assistant":
            st.caption("KOREA CULTURE GUIDE · PREPARED ANSWERS")
        st.markdown(message.get("content", ""))


def main() -> None:
    st.set_page_config(
        page_title="Korea Culture Guide",
        page_icon="🇰🇷",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        .stApp { background: #f7f5ef; }
        .block-container { max-width: 900px; padding-top: 1.6rem; padding-bottom: 6rem; }
        [data-testid="stSidebar"] { background: #eeebe2; border-right: 1px solid #dfd9cc; }
        .hero { text-align: center; padding: 1.5rem 1.1rem 1.2rem; margin: .1rem 0 1rem; }
        .hero-kicker { display: inline-block; color: #8a604a; background: #efe2d6; border-radius: 100px; padding: .32rem .75rem; font-size: .74rem; font-weight: 800; letter-spacing: .12em; }
        .hero h1 { color: #203849; font-size: clamp(2rem, 5vw, 3rem); letter-spacing: -.04em; margin: .8rem 0 .45rem; }
        .hero p { color: #59656c; max-width: 620px; margin: 0 auto; font-size: 1.02rem; line-height: 1.65; }
        .mode-note { border: 1px solid #e3d9ca; background: #fffdf8; color: #685c4d; padding: .7rem .9rem; border-radius: 12px; font-size: .9rem; margin-bottom: 1rem; }
        .suggestion-title { font-weight: 750; color: #203849; margin: .5rem 0 .6rem; }
        [data-testid="stChatMessage"] { border: 1px solid #e7e1d7; border-radius: 16px; padding: .9rem 1rem; background: rgba(255,255,255,.82); }
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p { line-height: 1.65; }
        [data-testid="stChatInput"] { border-color: #d9d1c3; border-radius: 16px; background: #fffefa; }
        .stButton > button { min-height: 2.8rem; border-radius: 14px; border-color: #ddd5c8; background: #fffdf8; color: #203849; font-size: .91rem; }
        .stButton > button:hover { border-color: #bf8265; color: #7e4f3a; }
        hr { border-color: #ded8cd; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("## 🇰🇷 Korea Culture Guide")
        st.caption("A simple guide for international visitors")
        st.info("Offline mode: no API key or account connection needed.")
        st.divider()
        if st.button("Start a new chat", use_container_width=True):
            reset_chat()
            st.rerun()
        st.markdown("**Prepared topics**")
        st.markdown(
            "Greetings · Food · Public transport · Tipping · Shoes · Hanbok · Hanok · Korean phrases · Kimchi · Holidays"
        )
        st.divider()
        st.caption("Answers are prepared in advance and matched to keywords. Questions outside these topics may not be understood.")

    if "messages" not in st.session_state:
        reset_chat()

    st.markdown(
        """
        <div class="hero">
          <div class="hero-kicker">YOUR TRAVEL COMPANION</div>
          <h1>한국 문화 설명</h1>
          <p><strong>Korea Culture Guide</strong><br>Ask about Korean customs, food, etiquette, language, and everyday life.</p>
        </div>
        <div class="mode-note">🗨️ <strong>Ready to explore?</strong> Choose a suggested question or type a question below. Answers come from a built-in guide—no API key required.</div>
        """,
        unsafe_allow_html=True,
    )

    for message in st.session_state.messages:
        render_message(message)

    selected_prompt = ""
    if not any(message.get("role") == "user" for message in st.session_state.messages):
        st.markdown("<div class='suggestion-title'>Try asking</div>", unsafe_allow_html=True)
        columns = st.columns(2)
        for idx, question in enumerate(SUGGESTED_QUESTIONS):
            with columns[idx % 2]:
                if st.button(question, key=f"suggestion_{idx}", use_container_width=True):
                    selected_prompt = question

    typed_prompt = st.chat_input("Ask about Korean culture…", max_chars=MAX_INPUT_CHARS)
    if typed_prompt and typed_prompt.strip():
        selected_prompt = typed_prompt.strip()

    if selected_prompt:
        selected_prompt = selected_prompt[:MAX_INPUT_CHARS]
        st.session_state.messages.append({"role": "user", "content": selected_prompt})
        answer = get_answer(selected_prompt)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

    st.caption("Cultural practices vary by person and setting. For current prices, opening hours, or transport rules, check official sources.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        st.error("The app encountered an unexpected problem. Refresh the page and try again. If it continues, check the Streamlit app logs.")
