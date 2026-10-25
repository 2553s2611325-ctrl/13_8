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
