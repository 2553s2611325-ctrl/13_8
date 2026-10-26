import streamlit as st
import pandas as pd
import json

# ---------------------------------------------------------
# 1. 페이지 설정 및 다국어 텍스트 데이터베이스 (i18n)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Korea Transit Guide for Foreigners",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 다국어 지원 Dictionary
I18N = {
    "English": {
        "title": "🇰🇷 K-Transit Helper: Korea Public Transit Guide",
        "subtitle": "Easy transit routing, subway maps, T-money card guides & emergency phrases for travelers!",
        "nav_search": "🔍 Route & Transfer Finder",
        "nav_cards": "💳 T-Money & Payment Guide",
        "nav_subway": "🗺️ City Subway Maps",
        "nav_phrases": "🗣️ Essential Korean Phrases",
        "nav_tips": "💡 Useful Tips & FAQs",
        "from_city": "Departure City / Region",
        "to_city": "Destination City / Region",
        "trans_type": "Preferred Transit",
        "all_trans": "All Transits",
        "subway": "Subway / Metro",
        "bus": "Bus",
        "ktx": "KTX / Train",
        "search_btn": "Find Route Options",
        "duration": "Duration",
        "cost": "Est. Cost",
        "transfers": "Transfers",
        "steps": "Step-by-Step Directions",
        "card_title": "💳 T-Money & Transit Cards Guide",
        "buy_location": "Where to Buy & Recharge",
        "buy_desc": "You can purchase and reload T-Money cards at any convenience store (GS25, CU, Seven-Eleven) or subway station ticket machines using CASH (KRW).",
        "tag_rules": "Important: Always Tag On & Tag Off!",
        "tag_desc": "Tap your card on the sensors when entering AND exiting buses/subways to get transfer discounts and avoid penalty fares.",
        "refund_info": "Refunds",
        "refund_desc": "Remaining balances under 20,000 KRW can be refunded instantly at convenience stores for a small fee (~500 KRW).",
        "phrases_title": "🗣️ Emergency & Station Korean Helper",
        "show_card_driver": "Show this screen to bus drivers, taxi drivers, or station staff:",
        "maps_title": "🗺️ Major City Subway Network Maps",
        "select_city": "Select City",
        "tips_title": "💡 Pro Travel Tips for Korea",
        "tip1_title": "🗺️ Google Maps doesn't give walking/driving routes in Korea?",
        "tip1_desc": "Due to local security laws, Google Maps walking navigation is limited. Use Naver Map or KakaoMap for 100% accurate walking and bus routes!",
        "tip2_title": "🚌 Bus Colors in Seoul",
        "tip2_desc": "• Blue Buses: Main routes connecting outer areas to downtown.\n• Green Buses: Branch routes connecting subway stations.\n• Red Buses: Express buses connecting satellite cities.\n• Yellow Buses: Circular routes inside downtown.",
        "tip3_title": "🚇 Express vs All-stop Trains (AREX)",
        "tip3_desc": "From Incheon Airport to Seoul Station:\n• Express Train: 43 mins direct (Reserved seating, higher fee).\n• All-Stop Train: ~59 mins (Standard subway fare, stops at all stations).",
    },
    "日本語": {
        "title": "🇰🇷 K-Transit Helper: 韓国公共交通機関ガイド",
        "subtitle": "外国人旅行者のための乗り환・路線検索、T-moneyカード使い方、緊急韓国語会話！",
        "nav_search": "🔍 経路＆乗り換え検索",
        "nav_cards": "💳 T-Money・決済ガイド",
        "nav_subway": "🗺️ 都市別地下鉄路線図",
        "nav_phrases": "🗣️ 交通必修韓国語フレーズ",
        "nav_tips": "💡 旅行のお役立ちヒント",
        "from_city": "出発地",
        "to_city": "目的地",
        "trans_type": " preferred 交通手段",
        "all_trans": "すべての交通手段",
        "subway": "地下鉄",
        "bus": "バス",
        "ktx": "KTX / 列車",
        "search_btn": "経路を検索する",
        "duration": "所要時間",
        "cost": "予想料金",
        "transfers": "乗り換え",
        "steps": " detailed 案内",
        "card_title": "💳 T-Moneyカード利用ガイド",
        "buy_location": "購入・チャージ場所",
        "buy_desc": "コンビニ（GS25、CU、セブンイレブン）や地下鉄駅の automatic 券売機にて現金（KRW）で購入・チャージが可能です。",
        "tag_rules": "重要：乗車・降車時のタッチ（Tag On & Tag Off）",
        "tag_desc": "乗車時と降車時の両方で端末にカードをタッチしてください。乗り換え割引が適用され、追加料金を防げます。",
        "refund_info": "払い戻し",
        "refund_desc": "残高が20,000ウォン未満の場合、コンビニで手数料（約500ウォン）を引いて即時払い戻し可能です。",
        "phrases_title": "🗣️ 駅・ドライバーに見せる緊急韓国語",
        "show_card_driver": "バスの運転手や駅員、タクシーで見せてください：",
        "maps_title": "🗺️ 主要都市地下鉄路線図",
        "select_city": "都市を選択",
        "tips_title": "💡 韓国旅行の交通コツ",
        "tip1_title": "🗺️ Googleマップの徒歩ナビが動かない？",
        "tip1_desc": "韓国の法律上の理由によりGoogleマップの徒歩ナビは制限されています。Naver Map（ナビマップ）やKakaoMapをご 이용ください。",
        "tip2_title": "🚌 ソウルバスの色と意味",
        "tip2_desc": "• 青バス：郊外と translation 都市を結ぶ幹線バス\n• 緑バス：地下鉄駅や主要スポットを結ぶ支線バス\n• 赤バス：広域急行バス\n• 黄色バス：都心循環バス",
        "tip3_title": "🚇 空港鉄道（AREX）直通 vs 一般",
        "tip3_desc": "仁川空港 ↔ ソウル駅:\n• 直通列車：約43分（全席指定、専用ホーム）\n• 一般列車：約59分（각駅停車、一般地下鉄料金）",
    },
    "中文(简体)": {
        "title": "🇰🇷 K-Transit Helper: 韩国公共交通指南",
        "subtitle": "为外国游客提供一站式换乘指南、地铁图、交通卡使用及实用韩语！",
        "nav_search": "🔍 路线与换乘查询",
        "nav_cards": "💳 T-Money交通卡指南",
        "nav_subway": "🗺️ 城市地铁线路图",
        "nav_phrases": "🗣️ 交通必备韩语卡片",
        "nav_tips": "💡 实用出行小贴士",
        "from_city": "出发地",
        "to_city": "目的地",
        "trans_type": "交通工具偏好",
        "all_trans": "全部交通工具",
        "subway": "地铁",
        "bus": "公交车",
        "ktx": "KTX / 火车",
        "search_btn": "查找路线",
        "duration": "预计时间",
        "cost": "预计费用",
        "transfers": "换乘次数",
        "steps": "详细步骤",
        "card_title": "💳 T-Money 交通卡指南",
        "buy_location": "购买与充值",
        "buy_desc": "您可以在任意便利店（GS25、CU、7-Eleven）或地铁站售票机使用韩元现金购买和充值。",
        "tag_rules": "重要：上下车必须刷卡！",
        "tag_desc": "乘坐公交车和地铁时，上下车均须刷卡，才能享受换乘优惠并避免被扣除罚款。",
        "refund_info": "余额退款",
        "refund_desc": "卡内余额少于20,000韩元时，可在便利店扣除小额手续费（约500韩元）后退还现金。",
        "phrases_title": "🗣️ 紧急与求助韩语卡片",
        "show_card_driver": "向公交车司机、出租车司机或工作人员出示此屏幕：",
        "maps_title": "🗺️ 韩国主要城市地铁图",
        "select_city": "选择城市",
        "tips_title": "💡 韩国出行秘籍",
        "tip1_title": "🗺️ 为什么谷歌地图在韩国无法步行导航？",
        "tip1_desc": "由于韩国地图数据相关法律，谷歌地图步行导航受限。推荐下载 Naver Map 或 KakaoMap 获得精准导航！",
        "tip2_title": "🚌 首尔公交车颜色含义",
        "tip2_desc": "• 蓝色公交：连接郊区与市中心的主干线\n• 绿色公交：连接地铁站与社区的支线\n• 红色公交：跨市城际直达快车\n• 黄色公交：市中心循环线",
        "tip3_title": "🚇 仁川机场铁路（AREX）直通 vs 普通",
        "tip3_desc": "仁川机场 ↔ 首尔站：\n• 直达列车：43分钟直达（对号入座，独立车厢）\n• 普通列车：约59分钟（每站必停，普通地铁票价）",
    }
}

# ---------------------------------------------------------
# 2. 샘플 픽스처 데이터 (주요 Tourist Route 10선)
# ---------------------------------------------------------
ROUTES_DATA = [
    {
        "id": 1,
        "from": "Incheon Intl Airport (ICN T1)",
        "to": "Seoul Station / Myeongdong",
        "mode": "Subway / Metro",
        "duration": "43 - 60 mins",
        "cost": "₩4,750 - ₩11,000",
        "transfers": "0 or 1 Transfer",
        "eng_steps": [
            "1. Take AREX (Airport Railroad Express) from Incheon Airport T1 Station.",
            "2. For Express (43 mins, reserved seat): Buy ticket at Express counter (₩11,000).",
            "3. For All-stop Train (59 mins): Tap T-Money card at gate (₩4,750).",
            "4. Arrive at Seoul Station. Transfer to Subway Line 4 for Myeongdong (2 stops)."
        ],
        "kor_steps": [
            "1. 인천공항 T1역에서 공항철도(AREX) 탑승",
            "2. 직통열차(43분): 전용 창구에서 승차권 구매 (11,000원)",
            "3. 일반열차(59분): T-Money 카드로 태그 승차 (4,750원)",
            "4. 서울역 도착 후 4호선 명동역 방향 환승(2개 정거장)"
        ]
    },
    {
        "id": 2,
        "from": "Myeongdong",
        "to": "Gyeongbokgung Palace",
        "mode": "Subway / Metro",
        "duration": "15 mins",
        "cost": "₩1,400",
        "transfers": "1 Transfer",
        "eng_steps": [
            "1. Board Subway Line 4 at Myeongdong Station (towards Chungmuro).",
            "2. Transfer to Line 3 at Chungmuro Station (towards 3호선 경복궁역).",
            "3. Get off at Gyeongbokgung Station (Exit 5 for palace entrance)."
        ],
        "kor_steps": [
            "1. 명동역에서 4호선 탑승 (충무로역 방향)",
            "2. 충무로역에서 3호선 환승 (경복궁역 방향)",
            "3. 경복궁역 하차 (5번 출구로 나가면 경복궁 연결)"
        ]
    },
    {
        "id": 3,
        "from": "Hongdae (Hongik Univ.)",
        "to": "Gangnam Station",
        "mode": "Subway / Metro",
        "duration": "38 mins",
        "cost": "₩1,500",
        "transfers": "Direct (0 Transfer)",
        "eng_steps": [
            "1. Enter Hongik Univ. Station.",
            "2. Take Subway Line 2 (Green Line, Inner Circle bound for Sinchon/City Hall).",
            "3. Ride for 18 stations directly to Gangnam Station without transfers."
        ],
        "kor_steps": [
            "1. 홍대입구역 2호선 승차",
            "2. 2호선 내선순환(신촌/시청 방면) 탑승",
            "3. 환승 없이 18개 정거장 이동 후 강남역 하차"
        ]
    },
    {
        "id": 4,
        "from": "Seoul Station",
        "to": "Busan Station",
        "mode": "KTX / Train",
        "duration": "2 hrs 40 mins",
        "cost": "₩59,800",
        "transfers": "0 Transfer",
        "eng_steps": [
            "1. Go to KTX Ticket Counter / Kiosk or KorailTalk app at Seoul Station.",
            "2. Purchase KTX Economy ticket to Busan Station.",
            "3. Proceed to Track platform 10-15 minutes prior to departure.",
            "4. Board train according to Car and Seat number on your ticket."
        ],
        "kor_steps": [
            "1. 서울역 KTX 창구/무인발권기 또는 코레일톡 앱 예약",
            "2. 부산역행 KTX 일반실 승차권 발권",
            "3. 출발 10~15분 전 해당 타는 곳(플랫폼)으로 이동",
            "4. 티켓의 호차 및 좌석 번호 확인 후 탑승"
        ]
    },
    {
        "id": 5,
        "from": "Namsan Cable Car / N Seoul Tower",
        "to": "Hongdae",
        "mode": "Bus",
        "duration": "30 mins",
        "cost": "₩1,400",
        "transfers": "1 Transfer",
        "eng_steps": [
            "1. Take Namsan Shuttle Bus No. 01A/01B down to Namsan Yejang Park / Myeongdong.",
            "2. Walk 3 mins to Myeongdong Subway Line 4 or nearby bus stop.",
            "3. Take Bus 604 or Metro Line 4 -> Line 2 to Hongik Univ Station."
        ],
        "kor_steps": [
            "1. 남산 예장공원/명동 방향 남산순환버스(01A/01B) 탑승",
            "2. 명동 부근 하차 후 604번 버스 또는 지하철 이동",
            "3. 홍대입구역 하차"
        ]
    }
]

# 한국어 서바이벌 다국어 카드 데이터
PHRASES_DATA = [
    {
        "category": "🚌 Bus / Taxi Destination",
        "eng": "Please take me to Gyeongbokgung Palace.",
        "kor_script": "경복궁으로 가주세요.",
        "pronunciation": "[Gyeong-bok-gung-eu-ro ga-ju-se-yo]"
    },
    {
        "category": "🚌 Bus / Taxi Destination",
        "eng": "Please go to Seoul Station.",
        "kor_script": "서울역으로 가주세요.",
        "pronunciation": "[Seo-ul-yeok-eu-ro ga-ju-se-yo]"
    },
    {
        "category": "💳 T-Money & Payment",
        "eng": "Please recharge 10,000 KRW on this T-Money card.",
        "kor_script": "티머니 카드 만 원 충전해 주세요.",
        "pronunciation": "[T-money card man-won chung-jeon-hae ju-se-yo]"
    },
    {
        "category": "❓ Station Directions",
        "eng": "Where is the subway station / bus stop?",
        "kor_script": "지하철역 / 버스 정류장이 어디에 있나요?",
        "pronunciation": "[Ji-ha-cheol-yeok / bus jeong-ryu-jang-i eo-di-e in-na-yo?]"
    },
    {
        "category": "🚨 Emergency Help",
        "eng": "I missed my stop! How can I go back?",
        "kor_script": "내리는 곳을 놓쳤어요! 어떻게 반대편으로 가나요?",
        "pronunciation": "[Nae-ri-neun got-eul no-chyeoss-eo-yo! Ban-dae-pyeon-eu-ro eo-tteok-he ga-na-yo?]"
    }
]


# ---------------------------------------------------------
# 3. 사이드바 메인 구성 (언어 선택 & 메뉴)
# ---------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/subway.png", width=70)
st.sidebar.title("K-Transit Helper")

lang = st.sidebar.selectbox(
    "🌐 Select Language / 言語選択 / 语言选择",
    ["English", "日本語", "中文(简体)"]
)

txt = I18N[lang]

st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigation Menu",
    [
        txt["nav_search"],
        txt["nav_cards"],
        txt["nav_subway"],
        txt["nav_phrases"],
        txt["nav_tips"]
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("🇰🇷 Korea Tourism Helper v1.0 | Streamlit Ready")


# ---------------------------------------------------------
# 4. 화면별 로직 구현
# ---------------------------------------------------------

# 앱 헤더
st.title(txt["title"])
st.caption(txt["subtitle"])
st.markdown("---")

# ==========================================
# [화면 1] 🔍 노선 및 환승 정보 검색
# ==========================================
if menu == txt["nav_search"]:
    st.subheader(txt["nav_search"])
    
    col1, col2, col3 = st.columns([2, 2, 1.5])
    
    with col1:
        # 출발지 선택
        from_cities = sorted(list(set([r["from"] for r in ROUTES_DATA])))
        selected_from = st.selectbox(txt["from_city"], ["All"] + from_cities)
        
    with col2:
        # 도착지 선택
        to_cities = sorted(list(set([r["to"] for r in ROUTES_DATA])))
        selected_to = st.selectbox(txt["to_city"], ["All"] + to_cities)
        
    with col3:
        # 交通手段 픽
        mode_filter = st.selectbox(
            txt["trans_type"],
            [txt["all_trans"], txt["subway"], txt["bus"], txt["ktx"]]
        )
        
    st.markdown("##### 📌 Available Route Guide")
    
    # 데이터 필터링
    filtered_routes = ROUTES_DATA
    if selected_from != "All":
        filtered_routes = [r for r in filtered_routes if r["from"] == selected_from]
    if selected_to != "All":
        filtered_routes = [r for r in filtered_routes if r["to"] == selected_to]
        
    if mode_filter != txt["all_trans"]:
        if mode_filter == txt["subway"]:
            filtered_routes = [r for r in filtered_routes if "Subway" in r["mode"]]
        elif mode_filter == txt["bus"]:
            filtered_routes = [r for r in filtered_routes if "Bus" in r["mode"]]
        elif mode_filter == txt["ktx"]:
            filtered_routes = [r for r in filtered_routes if "KTX" in r["mode"]]

    if not filtered_routes:
        st.warning("No preset route matches your filter. Try clearing filters!")
    else:
        for route in filtered_routes:
            with st.expander(f"🚩 {route['from']} ➔ {route['to']} ({route['mode']})", expanded=True):
                m_col1, m_col2, m_col3 = st.columns(3)
                m_col1.metric(txt["duration"], route["duration"])
                m_col2.metric(txt["cost"], route["cost"])
                m_col3.metric(txt["transfers"], route["transfers"])
                
                st.markdown(f"**{txt['steps']}:**")
                steps_to_show = route["eng_steps"] if lang == "English" else route["eng_steps"]
                
                for step in steps_to_show:
                    st.write(f"- {step}")
                
                # Show Korean guide for drivers/staff
                st.info(f"💡 **Korean Direction Note for Drivers/Staff:**\n\n" + "\n".join(route["kor_steps"]))

# ==========================================
# [화면 2] 💳 T-Money 및 교통카드 이용 안내
# ==========================================
elif menu == txt["nav_cards"]:
    st.subheader(txt["card_title"])
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.success(f"🛒 **{txt['buy_location']}**")
        st.write(txt["buy_desc"])
        st.image("https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=600&q=80", caption="Convenience Stores in Korea")

    with col_b:
        st.warning(f"🏷️ **{txt['tag_rules']}**")
        st.write(txt["tag_desc"])
        st.info(f"💰 **{txt['refund_info']}**: {txt['refund_desc']}")

    st.markdown("---")
    st.markdown("### 🚌 Public Transport Fee Matrix")
    df_fees = pd.DataFrame({
        "Transport Type": ["Seoul Subway (Basic)", "City Bus (Blue/Green)", "Express Bus (Red)", "T-Money Card Discount"],
        "Adult Fare (Cash)": ["₩1,500", "₩1,500", "₩3,000", "N/A"],
        "Adult Fare (T-Money)": ["₩1,400", "₩1,400", "₩3,000", "₩100 Discount + Free Transfers"],
        "Transfer Discount": ["Included up to 4 times", "Included up to 4 times", "Included up to 4 times", "Must Tag Off within 30 mins!"]
    })
    st.table(df_fees)

# ==========================================
# [화면 3] 🗺️ 도시별 지하철 노선도
# ==========================================
elif menu == txt["nav_subway"]:
    st.subheader(txt["maps_title"])
    
    city = st.selectbox(txt["select_city"], ["Seoul Metro (서울)", "Busan Metro (부산)", "Daegu Metro (대구)"])
    
    if "Seoul" in city:
        st.markdown("#### 🚇 Seoul Metropolitan Subway Map")
        st.write("Seoul subway system is color-coded by line number. Transfers are clearly marked with multi-color circles.")
        # Seoul Map Image
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Seoul_Subway_Map_EN.png/1200px-Seoul_Subway_Map_EN.png", use_container_width=True)
    elif "Busan" in city:
        st.markdown("#### 🚇 Busan Metro Map")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Busan_subway_map_en.svg/1200px-Busan_subway_map_en.svg.png", use_container_width=True)
    else:
        st.markdown("#### 🚇 Daegu Metro Map")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Daegu_Metro_Map_En.svg/1200px-Daegu_Metro_Map_En.svg.png", use_container_width=True)

# ==========================================
# [화면 4] 🗣️ 한국어 한마디 / 생존 소통 카드리스트
# ==========================================
elif menu == txt["nav_phrases"]:
    st.subheader(txt["phrases_title"])
    st.caption(txt["show_card_driver"])
    
    for item in PHRASES_DATA:
        with st.container():
            st.markdown(f"#### `{item['category']}`")
            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown(f"**English / Selected Lang:**\n### {item['eng']}")
                st.caption(f"Pronunciation guide: {item['pronunciation']}")
            with c2:
                # 외국인이 화면을 보여줄 수 있도록 크게 표시
                st.success(f"🇰🇷 **Show this to Korean Driver / Staff:**\n# {item['kor_script']}")
            st.markdown("---")

# ==========================================
# [화면 5] 💡 여행 꿀팁 & FAQ
# ==========================================
elif menu == txt["nav_tips"]:
    st.subheader(txt["tips_title"])
    
    with st.expander(txt["tip1_title"], expanded=True):
        st.write(txt["tip1_desc"])
        st.markdown("- **Recommended Apps for Foreigners:** Naver Map (Supports EN/JP/CN), KakaoMap, Subway Korea.")

    with st.expander(txt["tip2_title"]):
        st.write(txt["tip2_desc"])

    with st.expander(txt["tip3_title"]):
        st.write(txt["tip3_desc"])
        
    st.markdown("---")
    st.info("🆘 **Emergency Transit Contacts in Korea:**\n- Korea Travel Hotline: **1330** (24/7, English/Japanese/Chinese supported)\n- Emergency Services: **112** (Police) / **119** (Fire & Medical)")
