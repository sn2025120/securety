import streamlit as st
import random
import string
import time

# --- 페이지 설정 ---
st.set_page_config(page_title="MBTI 진로 추천", page_icon="🧭", layout="centered")

# --- 세션 상태 초기화 ---
if "step" not in st.session_state:
    st.session_state.step = "auth"
if "auth_code" not in st.session_state:
    st.session_state.auth_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
if "auth_attempts" not in st.session_state:
    st.session_state.auth_attempts = 0
if "auth_success" not in st.session_state:
    st.session_state.auth_success = False
if "agreed" not in st.session_state:
    st.session_state.agreed = False

# --- 진로 추천 데이터 ---
mbti_career = {
    "INTJ": ["전략 컨설턴트 🧠", "데이터 과학자 📊", "연구원 🔬"],
    "INTP": ["개발자 👨‍💻", "이론물리학자 📚", "UX 디자이너 🎨"],
    "ENTJ": ["CEO 💼", "프로젝트 매니저 📂", "변호사 ⚖️"],
    "ENTP": ["창업가 🚀", "마케터 📢", "기획자 🧩"],
    "INFJ": ["상담사 🧑‍⚕️", "작가 ✍️", "사회복지사 💗"],
    "INFP": ["예술가 🎨", "심리학자 🧠", "시나리오 작가 🎬"],
    "ENFJ": ["교사 👩‍🏫", "HR 전문가 🧑‍💼", "컨설턴트 📘"],
    "ENFP": ["방송인 🎤", "홍보 담당자 🗣️", "여행 가이드 🌍"],
    "ISTJ": ["회계사 📒", "공무원 🏛️", "엔지니어 🛠️"],
    "ISFJ": ["간호사 🏥", "초등교사 📚", "사서 📖"],
    "ESTJ": ["경영 관리자 🧾", "군인 🪖", "재무 담당자 💹"],
    "ESFJ": ["이벤트 플래너 🎉", "세일즈 매니저 🛍️", "교육 코디네이터 📆"],
    "ISTP": ["기계공 🛠️", "파일럿 ✈️", "보안 전문가 🕵️"],
    "ISFP": ["플로리스트 🌸", "사진작가 📸", "헤어 디자이너 💇‍♀️"],
    "ESTP": ["응급 구조사 🚑", "운동 트레이너 🏋️", "여행 작가 ✈️"],
    "ESFP": ["배우 🎭", "MC 🎙️", "패션 디자이너 👗"]
}


# --- STEP 1: 보안코드 인증 ---
if st.session_state.step == "auth":
    st.title("🔐 보안 인증")
    st.write("아래 보안코드를 정확히 입력하십시요.")
    st.code(st.session_state.auth_code, language="text")

    user_input = st.text_input("보안코드 입력", max_chars=8)

    if st.button("확인"):
        if user_input.strip().upper() == st.session_state.auth_code:
            st.session_state.auth_success = True
            st.session_state.step = "consent"
        else:
            st.session_state.auth_attempts += 1
            if st.session_state.auth_attempts >= 5:
                st.error("❌ 보안코드를 5회 틀렸습니다. 앱을 종료합니다.")
                st.stop()
            else:
                st.warning(f"❗ {st.session_state.auth_attempts}번째 오류입니다. 새로운 보안코드가 발급되었습니다.")
                st.session_state.auth_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# --- STEP 2: 개인정보 동의 ---
elif st.session_state.step == "consent":
    st.title("📄 개인정보 이용 동의 안내")
    st.write("서비스를 이용하기 위해 아래 항목에 동의해주세요. 거절할수 있으며, 불이익이 발생할수 있습니다.")

    agree = st.checkbox("개인정보 수집 및 이용에 동의")

    if agree:
        st.session_state.agreed = True
        st.session_state.step = "mbti"

# --- STEP 3: MBTI 진로 추천 ---
elif st.session_state.step == "mbti":
    st.title("💼 MBTI 진로 추천 웹앱")
    st.write("당신의 **MBTI** 유형을 선택하면, 어울리는 진로를 추천해드릴게요! 😊")

    selected_mbti = st.selectbox("당신의 MBTI를 선택해주세요:", [""] + list(mbti_career.keys()))

    if selected_mbti != "":
        st.markdown("---")
        st.subheader(f"🎯 {selected_mbti} 유형에게 어울리는 진로는?")
        for job in mbti_career[selected_mbti]:
            st.markdown(f"- {job}")
        st.markdown("---")
        st.success("당신의 강점을 살릴 수 있는 분야를 탐색해보세요! 🚀")

    st.caption("ⓒ 2025 진로탐색 EduApp - MBTI 기반 추천 시스템 🧭")
