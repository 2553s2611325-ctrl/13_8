"""Korea Culture AI — a simple Streamlit chat app for travelers."""

from __future__ import annotations

import os
from typing import Any

import streamlit as st

# Keep the app usable in preview mode even if the SDK import fails.
try:
    from google import genai
    from google.genai import types
except Exception:  # pragma: no cover - exercised only in misconfigured deployments
    genai = None  # type: ignore[assignment]
    types = None  # type: ignore[assignment]

MODEL_NAME = "gemini-2.5-flash-lite"
MAX_INPUT_CHARS = 1200
MAX_CONTEXT_MESSAGES = 12

LANGUAGES = {
    "English": "English",
    "한국어": "Korean",
    "日本語": "Japanese",
    "简体中文": "Simplified Chinese",
    "Español": "Spanish",
    "Français": "French",
}

WELCOME_MESSAGES = {
    "English": (
        "Hi! I'm your Korea Culture AI guide. 🇰🇷\n\n"
        "Ask me about Korean customs, food, greetings, public transport, history, or everyday life. "
        "I'll explain the context and share practical tips for visitors."
    ),
    "한국어": (
        "안녕하세요! 한국 문화 여행 가이드 AI예요. 🇰🇷\n\n"
        "한국의 예절, 음식, 인사법, 대중교통, 역사와 일상생활에 대해 편하게 물어보세요. "
        "문화적 배경과 여행에 도움이 되는 팁을 설명해 드릴게요."
    ),
    "日本語": (
        "こんにちは！韓国文化を案内するAIガイドです。🇰🇷\n\n"
        "韓国のマナー、食べ物、あいさつ、公共交通機関、歴史、日常生活について気軽に質問してください。"
    ),
    "简体中文": (
        "你好！我是韩国文化旅行 AI 向导。🇰🇷\n\n"
        "可以问我韩国礼仪、美食、问候方式、公共交通、历史或日常生活，我会提供背景说明和旅行小贴士。"
    ),
    "Español": (
        "¡Hola! Soy tu guía de cultura coreana con IA. 🇰🇷\n\n"
        "Pregúntame sobre costumbres, comida, saludos, transporte público, historia o vida diaria en Corea."
    ),
    "Français": (
        "Bonjour ! Je suis votre guide IA de la culture coréenne. 🇰🇷\n\n"
        "Posez-moi des questions sur les coutumes, la cuisine, les salutations, les transports, l'histoire ou la vie quotidienne."
    ),
}

SUGGESTED_QUESTIONS = [
    "Why do people bow in Korea?",
    "How does Korean BBQ work?",
    "What should I know about subway manners?",
    "Is tipping expected in Korea?",
]

SYSTEM_PROMPT = """You are Korea Culture AI, a friendly, careful guide for international visitors to South Korea.
Answer in {language}. If the user asks for a Korean phrase, include Hangul and a simple pronunciation guide when useful.
Explain cultural context in plain language and give practical, respectful travel tips.
Do not present Korean people as all having the same views or habits. Explain that practices can vary by region, age, venue, family, and individual.
If a custom is uncertain or context-dependent, say so instead of inventing a rule. Distinguish common etiquette from strict requirements.
Keep responses organized and helpful, usually with a short explanation and a few practical tips. You may answer follow-up questions using the conversation history.
Stay focused on Korean culture and travel. For time-sensitive details such as opening hours, prices, transport changes, or current events, explain that the visitor should verify current information with an official source.
"""

OFFLINE_ANSWERS = [
    (("bow", "greet", "인사", "절", "고개"),
     "A small bow or nod is a common polite greeting in Korea, and it can also show appreciation. You do not need to bow deeply in everyday situations. A friendly “안녕하세요” (annyeonghaseyo, hello) is a useful place to start. Customs vary by setting and person."),
    (("bbq", "barbecue", "samgyeopsal", "food", "meal", "banchan", "반찬", "고기", "음식"),
     "Korean meals may include rice, soup, and small side dishes called banchan. At Korean BBQ restaurants, diners commonly cook meat at the table and share some dishes. Check whether a dish is shared, use serving utensils when provided, and ask staff about ingredients or spice if needed."),
    (("subway", "metro", "train", "bus", "transport", "지하철", "버스", "교통"),
     "On Korean public transport, let passengers exit before boarding, stand clear of the doors, and keep audio private with headphones. Some seats are designated for people who need them, such as older adults, disabled passengers, or pregnant passengers. Transit-card rules vary by system, so follow station signs and announcements."),
    (("tip", "tipping", "gratuity", "팁"),
     "Tipping is not generally expected in most everyday restaurants and cafés in South Korea. Some tourist-focused services may have different practices, so check the bill or service information rather than assuming. A sincere “감사합니다” (gamsahamnida, thank you) is always useful."),
    (("shoe", "shoes", "home", "house", "temple", "신발", "집", "사찰", "절"),
     "Remove your shoes when a host or sign asks you to—this is common in homes and some floor-seating spaces. At temples and cultural sites, follow posted instructions and photography rules. If you are unsure, pause and look for signs or politely ask staff."),
    (("hanbok", "한복"),
     "Hanbok is traditional Korean clothing worn for occasions such as holidays, ceremonies, and celebrations. Modern and contemporary versions also exist. If you rent hanbok for photos, follow the rental shop's instructions and ask before photographing other people."),
    (("hanok", "한옥", "architecture", "house"),
     "Hanok refers to traditional Korean buildings. Depending on the building, you may notice wooden frames, tiled roofs, courtyards, and ondol-style floor heating. In residential hanok neighborhoods, keep noise low and respect signs that mark private spaces."),
    (("honorific", "speech level", "polite korean", "oppa", "언어", "존댓말", "반말"),
     "Korean speech changes with politeness, familiarity, and context. When meeting someone for the first time, polite forms such as “안녕하세요” (hello) and “감사합니다” (thank you) are a safe starting point. Titles and relationship words can be context-specific, so it is fine to use a person's name and polite language when unsure."),
    (("kimchi", "김치"),
     "Kimchi is a broad family of fermented vegetable dishes, often made with napa cabbage or radish and seasonings. Recipes and spice levels vary. It is commonly served as a side dish, but it is not the only part of Korean food culture."),
    (("gift", "giving", "받다", "선물"),
     "In some Korean settings, using both hands—or supporting one arm with the other—when giving or receiving a gift or important item can show respect. It is a thoughtful gesture rather than a universal strict rule; follow the tone of the occasion."),
]


def get_api_key() -> str:
    """Read the API key from Streamlit secrets first, then environment variables."""
    key: Any = ""
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        # Local preview works when no secrets file has been created.
        key = ""
    if not key:
        key = os.environ.get("GEMINI_API_KEY", "")
    return key.strip() if isinstance(key, str) else ""


def welcome_message(language_label: str) -> str:
    return WELCOME_MESSAGES.get(language_label, WELCOME_MESSAGES["English"])


def get_offline_answer(question: str) -> str:
    """Return a small built-in answer so the app still runs without an API key."""
    normalized = question.casefold()
    for keywords, answer in OFFLINE_ANSWERS:
        if any(word.casefold() in normalized for word in keywords):
            return answer + "\n\n*Preview mode:* add `GEMINI_API_KEY` in Streamlit Secrets to enable full AI conversation."
    return (
        "I'm currently in preview mode, so I can only answer a few common culture questions without an API key. "
        "Try asking about bowing, Korean BBQ, subway manners, tipping, shoes, hanbok, hanok, kimchi, or polite Korean.\n\n"
        "To enable open-ended AI answers, add `GEMINI_API_KEY` in your Streamlit app's Secrets settings."
    )


def generate_ai_answer(messages: list[dict[str, Any]], language: str, api_key: str) -> str:
    """Generate an answer with the Gemini SDK using recent chat messages as context."""
    if genai is None or types is None:
        raise RuntimeError("The Google GenAI SDK is not installed correctly.")

    client = genai.Client(api_key=api_key)
    # Do not send the initial welcome message as conversation context.
    conversation = [m for m in messages if not m.get("is_welcome")]
    conversation = conversation[-MAX_CONTEXT_MESSAGES:]
    # A conversation sent to the model should begin with a user message.
    while conversation and conversation[0].get("role") != "user":
        conversation.pop(0)

    contents = []
    for item in conversation:
        text = str(item.get("content", "")).strip()
        if not text:
            continue
        role = "user" if item.get("role") == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=text)],
            )
        )

    if not contents:
        raise ValueError("There is no question to send to the AI service.")

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT.format(language=LANGUAGES.get(language, "English")),
            max_output_tokens=850,
            temperature=0.6,
        ),
    )
    answer = getattr(response, "text", None)
    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("The AI service returned an empty response.")
    return answer.strip()


def friendly_error_message(error: Exception) -> str:
    """Translate common API failures into an understandable next step."""
    detail = str(error).casefold()
    if any(term in detail for term in ("api key", "unauthenticated", "permission denied", "forbidden", "401", "403")):
        return (
            "I couldn't authenticate with the AI service. Please check that the `GEMINI_API_KEY` secret is correct, "
            "and that your Google AI Studio project has access to the requested model."
        )
    if any(term in detail for term in ("quota", "resource exhausted", "429", "rate limit")):
        return (
            "The AI service has reached a usage limit or is temporarily busy. Please try again later. "
            "You can still use the built-in culture answers in preview mode."
        )
    if any(term in detail for term in ("timeout", "timed out", "connection", "unavailable", "503")):
        return (
            "I couldn't reach the AI service just now. Check the connection and try again. "
            "You can still use the built-in culture answers in preview mode."
        )
    return (
        "Sorry, the AI service could not complete that request. Check the API key, model access, and usage quota, "
        "then try again. You can also try one of the suggested culture questions."
    )


def reset_chat(language_label: str) -> None:
    st.session_state.messages = [
        {"role": "assistant", "content": welcome_message(language_label), "is_welcome": True}
    ]
    st.session_state.pending_prompt = ""


def render_chat_message(message: dict[str, Any]) -> None:
    role = "assistant" if message.get("role") == "assistant" else "user"
    avatar = "🤖" if role == "assistant" else "🧳"
    with st.chat_message(role, avatar=avatar):
        if role == "assistant":
            st.caption("AI CULTURE GUIDE")
        st.markdown(str(message.get("content", "")))


def main() -> None:
    st.set_page_config(
        page_title="Korea Culture AI",
        page_icon="🇰🇷",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        .stApp { background: #f7f5ef; }
        .block-container { max-width: 900px; padding-top: 1.6rem; padding-bottom: 7rem; }
        [data-testid="stSidebar"] { background: #eeebe2; border-right: 1px solid #dfd9cc; }
        .hero { text-align: center; padding: 1.8rem 1.25rem 1.25rem; margin: .1rem 0 1.2rem; }
        .hero-kicker { display: inline-block; color: #8a604a; background: #efe2d6; border-radius: 100px; padding: .32rem .75rem; font-size: .74rem; font-weight: 800; letter-spacing: .12em; }
        .hero h1 { color: #203849; font-size: clamp(2rem, 5vw, 3rem); letter-spacing: -.04em; margin: .8rem 0 .45rem; }
        .hero p { color: #59656c; max-width: 620px; margin: 0 auto; font-size: 1.02rem; line-height: 1.65; }
        .mode-note { border: 1px solid #e3d9ca; background: #fffdf8; color: #685c4d; padding: .7rem .9rem; border-radius: 12px; font-size: .88rem; margin-bottom: 1rem; }
        .suggestion-title { font-weight: 750; color: #203849; margin: .5rem 0 .6rem; }
        [data-testid="stChatMessage"] { border: 1px solid #e7e1d7; border-radius: 16px; padding: .9rem 1rem; background: rgba(255,255,255,.78); }
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
        st.markdown("## 🇰🇷 Korea Culture AI")
        st.caption("A friendly culture guide for travelers")
        language_label = st.selectbox(
            "Answer language",
            options=list(LANGUAGES.keys()),
            index=0,
            help="Choose the language used by the AI replies.",
            key="answer_language",
        )
        st.divider()
        if st.button("Start a new chat", use_container_width=True):
            reset_chat(language_label)
            st.rerun()
        st.markdown("**What you can ask about**")
        st.markdown("Food and dining · Everyday manners · Korean phrases · History and traditions · Modern culture")
        st.divider()
        api_key = get_api_key()
        if api_key and genai is not None:
            st.success("AI mode enabled")
            st.caption(f"Model: `{MODEL_NAME}`")
        else:
            st.info("Preview mode")
            st.caption("Add `GEMINI_API_KEY` in Secrets to enable open-ended AI answers. Built-in answers work without a key.")
        st.markdown("[Get a Gemini API key](https://aistudio.google.com/app/apikey)")

    if "messages" not in st.session_state:
        reset_chat(language_label)
    elif st.session_state.get("last_language") != language_label:
        # Keep the conversation, but clear the first-turn welcome if that is all it contains.
        if len(st.session_state.messages) == 1 and st.session_state.messages[0].get("is_welcome"):
            reset_chat(language_label)
    st.session_state.last_language = language_label

    st.markdown(
        """
        <div class="hero">
          <div class="hero-kicker">YOUR TRAVEL COMPANION</div>
          <h1>한국 문화 설명</h1>
          <p><strong>Korea Culture AI</strong><br>Ask about Korean customs, food, etiquette, language, and everyday life.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not api_key or genai is None:
        st.markdown(
            "<div class='mode-note'>✨ <strong>Preview mode:</strong> common culture questions have built-in answers. Add your API key to unlock open-ended AI conversation.</div>",
            unsafe_allow_html=True,
        )

    messages = st.session_state.messages
    for message in messages:
        render_chat_message(message)

    selected_prompt = ""
    if not any(message.get("role") == "user" for message in messages):
        st.markdown("<div class='suggestion-title'>Try asking</div>", unsafe_allow_html=True)
        cols = st.columns(2)
        for idx, question in enumerate(SUGGESTED_QUESTIONS):
            with cols[idx % 2]:
                if st.button(question, key=f"suggestion_{idx}", use_container_width=True):
                    selected_prompt = question

    typed_prompt = st.chat_input(
        "Type your question about Korean culture…",
        max_chars=MAX_INPUT_CHARS,
    )
    if typed_prompt and typed_prompt.strip():
        selected_prompt = typed_prompt.strip()

    if selected_prompt:
        # Prevent empty or overlong input even if the prompt comes from a button.
        selected_prompt = selected_prompt.strip()[:MAX_INPUT_CHARS]
        st.session_state.messages.append({"role": "user", "content": selected_prompt})
        render_chat_message(st.session_state.messages[-1])

        with st.spinner("Preparing an answer…"):
            if api_key and genai is not None:
                try:
                    answer = generate_ai_answer(st.session_state.messages, language_label, api_key)
                except Exception as exc:
                    st.warning(friendly_error_message(exc))
                    answer = get_offline_answer(selected_prompt)
            else:
                answer = get_offline_answer(selected_prompt)

        assistant_message = {"role": "assistant", "content": answer}
        st.session_state.messages.append(assistant_message)
        render_chat_message(assistant_message)

    st.caption("Cultural practices can vary by person and setting. When in doubt, observe local guidance and ask politely.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Last-resort guard: show a friendly error rather than an unhandled traceback.
        st.error("The app encountered an unexpected problem. Refresh the page and try again. If it continues, check the Streamlit app logs.")

