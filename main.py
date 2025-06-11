import streamlit as st
import random
import string
import base64
from captcha.image import ImageCaptcha
from io import BytesIO

# --- 페이지 설정 ---
st.set_page_config(page_title="MBTI 진로 추천", page_icon="🧭", layout="centered")

# --- 세션 상태 초기화 ---
if "step" not in st.session_state:
    st.session_state.step = "auth"
if "auth_code" not in st.session_state:
    st.session_state.auth_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
if "auth_attempts" not in st.session_state:
    st.session_state.auth_attempts = 0
if "captcha_code" not in st.session_state:
    st.session_state.captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
if "captcha_failed" not in st.session_state:
    st.session_state.captcha_failed = False



# --- STEP 1: 보안코드 입력 ---
if st.session_state.step == "auth":
    st.title("🔐 보안 인증")
    st.write("아래 보안코드를 정확히 입력해주세요 (대/소문자 구분)")

    st.markdown(
        f"""
        <div style="user-select: none; font-family: monospace; font-size: 1.5em; background-color: #f1f3f5; padding: 10px; border-radius: 5px;">
            {st.session_state.auth_code}
        </div>
        """,
        unsafe_allow_html=True
    )

    user_input = st.text_input("보안코드 입력", max_chars=8)

    if st.button("확인"):
        if user_input == st.session_state.auth_code:
            st.session_state.step = "captcha"
        else:
            st.session_state.auth_attempts += 1
            if st.session_state.auth_attempts >= 3:
                st.error("❌ 보안코드를 3회 틀렸습니다. 앱을 종료합니다.")
                st.markdown("<script>window.close();</script>", unsafe_allow_html=True)
                st.stop()
            else:
                st.warning(f"❗ {st.session_state.auth_attempts}번째 오류입니다. 새로운 보안코드가 발급되었습니다.")
                st.session_state.auth_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))


# --- STEP 2: 시각 CAPTCHA ---



# --- STEP 3: 개인정보 동의 ---
elif st.session_state.step == "consent":
    st.title("📄 개인정보 이용 동의")
    st.write("서비스를 사용하기 위해 아래 항목에 동의해주세요.")

    agree = st.checkbox("✅ 개인정보 수집 및 이용에 동의합니다. (필수)")
    signature = st.text_input("✍️ 전자서명 (선택사항)", placeholder="이름 또는 서명 입력")

    if st.button("확인"):
        if agree:
            st.session_state.step = "mbti"
        else:
            st.error("⚠️ 개인정보 이용에 동의해야 다음 단계로 넘어갈 수 있습니다.")



