import streamlit as st
from PIL import Image
import time
import random

# --- [페이지 설정] ---
st.set_page_config(
    page_title="K-Food Guide (No API Ver.)",
    page_icon="🍲",
    layout="centered"
)

# --- [커스텀 스타일] ---
st.markdown("""
    <style>
    .main-title { text-align: center; color: #FF4B4B; font-weight: bold; }
    .sub-title { text-align: center; color: #555555; margin-bottom: 25px; }
    .demo-badge { text-align: center; color: #0083B8; font-size: 14px; font-weight: bold; margin-top: -15px; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🍲 K-Food Guide for Travelers</h1>", unsafe_allow_html=True)
st.markdown("<p class='demo-badge'>🚀 Demo Version (No API Key Required)</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Snap or upload a photo of Korean food to learn what it is and how to enjoy it!</p>", unsafe_allow_html=True)

# --- [모의(Mock) 데이터베이스 구축] ---
# 실제 AI 대신 출력될 대표적인 한국 음식 데이터베이스입니다.
mock_database = [
    {
        "korean_name": "비빔밥 (Bibimbap)",
        "english_name": "Mixed Rice with Meat and Assorted Vegetables",
        "description": "A healthy and colorful dish made of warm white rice topped with sautéed and seasoned vegetables, chili pepper paste (Gochujang), and sliced meat. It offers a perfect harmony of flavors.",
        "spiciness_level": "Mild 🌶️",
        "contains_pork": False,
        "main_ingredients": ["Rice", "Assorted Vegetables", "Gochujang (Chili Paste)", "Beef", "Egg"],
        "how_to_eat": "Mix all the ingredients thoroughly with the Gochujang sauce before eating! You can adjust the amount of sauce based on your spice tolerance.",
        "allergens": ["Egg", "Sesame"]
    },
    {
        "korean_name": "떡볶이 (Tteokbokki)",
        "english_name": "Spicy Stir-fried Rice Cakes",
        "description": "A highly popular Korean street food made with chewy rice cakes and fish cakes cooked in a sweet and spicy chili paste sauce.",
        "spiciness_level": "Spicy 🌶️🌶️🌶️",
        "contains_pork": False,
        "main_ingredients": ["Rice Cakes", "Fish Cakes", "Gochujang (Chili Paste)", "Green Onions"],
        "how_to_eat": "It's best enjoyed hot! Try dipping fried snacks (Twigim) or boiled eggs into the spicy sauce.",
        "allergens": ["Fish", "Wheat", "Soybean"]
    },
    {
        "korean_name": "삼겹살 (Samgyeopsal)",
        "english_name": "Grilled Pork Belly",
        "description": "Thick, fatty slices of pork belly meat grilled on a pan at the diners' table. It's the most beloved BBQ dish in Korea.",
        "spiciness_level": "Non-spicy 🚫",
        "contains_pork": True,
        "main_ingredients": ["Pork Belly", "Garlic", "Ssamjang (Dipping Sauce)"],
        "how_to_eat": "Make a 'Ssam' (wrap): Place a piece of grilled meat on a lettuce leaf, add a dab of Ssamjang, grilled garlic, and kimchi, then wrap it up and eat it in one bite!",
        "allergens": ["Soybean", "Pork"]
    },
    {
        "korean_name": "김치찌개 (Kimchi Jjigae)",
        "english_name": "Kimchi Stew",
        "description": "A hearty, spicy, and savory stew made with well-fermented Kimchi, pork or tuna, and tofu. A staple comfort food for Koreans.",
        "spiciness_level": "Medium 🌶️🌶️",
        "contains_pork": True, # 돼지고기 베이스인 경우
        "main_ingredients": ["Aged Kimchi", "Pork (or Tuna)", "Tofu", "Green Onions"],
        "how_to_eat": "Eat it with a bowl of warm white rice. The sourness of the aged Kimchi goes perfectly with the savory broth.",
        "allergens": ["Soybean", "Pork"]
    }
]

# --- [UI: 이미지 입력 부분] ---
st.subheader("📷 Step 1: Provide a Food Photo")
input_option = st.radio("Choose photo input method:", ["Upload Photo", "Take Photo (Camera)"], horizontal=True)

image_to_analyze = None

if input_option == "Take Photo (Camera)":
    camera_file = st.camera_input("Take a picture of Korean food")
    if camera_file:
        image_to_analyze = Image.open(camera_file)
else:
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "webp"])
    if uploaded_file:
        image_to_analyze = Image.open(uploaded_file)

# --- [UI: 분석 및 결과 출력 부분] ---
if image_to_analyze:
    st.image(image_to_analyze, caption="Selected Food Image", use_column_width=True)
    
    st.markdown("---")
    st.subheader("🔍 Step 2: Food Analysis (Simulation)")
    
    if st.button("🚀 Analyze K-Food", type="primary", use_container_width=True):
        
        # AI 분석하는 척하는 로직 (프로그레스 바 & 스피너)
        with st.spinner("AI is inspecting your food... Please wait a second! 🥢"):
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.015)  # 시각적 효과를 위한 딜레이
                progress_bar.progress(percent_complete + 1)
        
        # 무작위로 음식 데이터 하나 선택 (API 연결 없이 결과를 보여줌)
        result = random.choice(mock_database)
        
        # 결과 화면 출력
        st.success("✨ Analysis Complete!")
        
        st.markdown(f"### 🍽️ {result['english_name']}")
        st.markdown(f"**Korean:** `{result['korean_name']}`")
        
        # 지표 (Metrics)
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Spiciness Level", value=result["spiciness_level"])
        with col2:
            pork_status = "Yes 🐷" if result["contains_pork"] else "No ❌"
            st.metric(label="Contains Pork", value=pork_status)

        # 상세 설명
        st.markdown("#### 📝 Description")
        st.info(result["description"])

        # 주요 재료
        st.markdown("#### 🥬 Main Ingredients")
        st.write(", ".join(result["main_ingredients"]))

        # 먹는 방법
        st.markdown("#### 💡 How to Eat Like a Local")
        st.success(result["how_to_eat"])

        # 알레르기 주의사항
        if result["allergens"]:
            st.warning(f"⚠️ **Potential Allergens:** {', '.join(result['allergens'])}")

# --- [사이드바] ---
with st.sidebar:
    st.markdown("### ℹ️ About this App")
    st.info("This is a functional UI Demo page. It does NOT require an API key. When an image is uploaded, it simulates an AI analysis by selecting a famous Korean dish from a predefined database.")
    st.markdown("---")
    st.markdown("### 💡 Tips for Best Results")
    st.markdown("""
    - Try uploading any picture!
    - The app will 'guess' the food instantly.
    - Perfect for showcasing Streamlit app designs.
    """)
