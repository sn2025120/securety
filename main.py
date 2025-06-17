import streamlit as st
import random
import string
import re
import time

# --- 입력 유효성 검사 함수 ---
def is_valid_input(input_str):
    """영어 대소문자와 숫자만 허용"""
    return bool(re.fullmatch(r'^[A-Za-z0-9]*$', input_str))

# --- 페이지 설정 ---
st.set_page_config(page_title="보안 인증", layout="centered")

# --- 세션 상태 초기화 ---
if "step" not in st.session_state:
    st.session_state.step = "auth"
if "auth_code" not in st.session_state:
    st.session_state.auth_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
if "auth_attempts" not in st.session_state:
    st.session_state.auth_attempts = 0
if "auth_input" not in st.session_state:
    st.session_state.auth_input = ""

# --- CSS 설정 ---
st.markdown("""
    <style>
    .no-select {
        user-select: none;
        font-family: monospace;
        font-size: 1.5em;
        background-color: #f1f3f5;
        padding: 10px;
        border-radius: 5px;
        margin: 20px auto;
        width: fit-content;
    }
    </style>
""", unsafe_allow_html=True)

# --- 보안코드 인증 화면 ---
if st.session_state.step == "auth":
    st.title("🔐 보안 인증")
    st.write("아래 보안코드를 정확히 입력해주세요 (영어 대소문자, 숫자만 가능).")
    
    # 보안코드 표시
    st.markdown(f'<div class="no-select">{st.session_state.auth_code}</div>', unsafe_allow_html=True)
    
    # 입력 필드 (실시간 유효성 검사)
    input_code = st.text_input("보안코드 입력", 
                             max_chars=8,
                             value=st.session_state.auth_input,
                             on_change=lambda: st.session_state.update({"auth_input": st.session_state.auth_input}))
    
    # 입력 제한 검사
    if input_code and not is_valid_input(input_code):
        st.warning("⚠️ 영어와 숫자만 입력 가능합니다.")
        st.session_state.auth_input = re.sub(r'[^A-Za-z0-9]', '', input_code)  # 특수문자 자동 제거
        st.rerun()
    
    # 입력 완료 시 검증
    if len(input_code) == 8:
        if input_code == st.session_state.auth_code:
            st.success("✅ 인증 성공! 다음 단계로 이동합니다.")
            st.session_state.step = "consent"
            st.session_state.auth_attempts = 0
            st.rerun()
        else:
            st.session_state.auth_attempts += 1
            if st.session_state.auth_attempts >= 3:
                st.error("⛔ 3회 이상 오류로 프로그램을 종료합니다.")
                st.stop()
            else:
                # 새 보안코드 생성 및 입력 초기화
                st.session_state.auth_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                st.session_state.auth_input = ""
                st.warning(f"❌ {st.session_state.auth_attempts}번째 오류 - 새 보안코드가 발급되었습니다.")
                st.rerun()

# --- 개인정보 동의 화면 ---
elif st.session_state.step == "consent":
    st.title("📄 개인정보 동의")
    agree = st.checkbox("개인정보 수집 및 이용에 동의합니다 (필수)")
    if agree:
        st.success("✅ 동의 완료!")
        # 다음 단계 코드 추가
