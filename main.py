import streamlit as st
import random
import string
import time

# --- 단계별 상태 정의 ---
stage_labels = [
    "세션 상태 초기화중",
    "CSS 보안환경 적용중",
    "라이선스를 확인하는 중입니다"
]
stage_durations = [4, 2, 0.7]  # 각 단계별 지속 시간 (초)
stage_count = len(stage_labels)

# --- 세션 상태 초기화 ---
if "init_stage" not in st.session_state:
    st.session_state.init_stage = 0
if "step" not in st.session_state:
    st.session_state.step = "init"

# --- CSS 설정 ---
st.markdown("""
    <style>
    .top-container {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        width: 100vw;
        margin-top: 0px;
        padding-top: 0px;
    }
    .stage-text {
        font-size: 1.5em;
        margin: 10px 0;
        text-align: center;
    }
    .fade { color: #cccccc; }
    .bold { color: #000000; font-weight: 700; }
    .no-select {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        font-family: monospace;
        font-size: 1.5em;
        background-color: #f1f3f5;
        padding: 10px;
        border-radius: 5px;
        width: fit-content;
        margin: 20px auto;
    }
    .integrity-message {
        color: #2ecc71;
        font-size: 2em;
        font-weight: bold;
        text-align: center;
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# --- 초기화 단계 화면 ---
if st.session_state.step == "init":
    # 화면 최상단에 고정
    st.markdown('<div class="top-container">', unsafe_allow_html=True)
    for idx in range(stage_count):
        css_class = "bold" if idx == st.session_state.init_stage else "fade"
        st.markdown(
            f'<div class="stage-text {css_class}">{stage_labels[idx]}</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
    # 단계 진행
    if st.session_state.init_stage < stage_count:
        time.sleep(stage_durations[st.session_state.init_stage])
        st.session_state.init_stage += 1
        st.rerun()
    else:
        st.session_state.step = "integrity"
        st.rerun()

# --- 무결성 검증 화면 ---
elif st.session_state.step == "integrity":
    st.markdown('<div class="top-container">', unsafe_allow_html=True)
    st.markdown('<div class="integrity-message">무결성 검증됨</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    time.sleep(1)
    st.session_state.step = "auth"
    st.rerun()

# --- 보안코드 인증 화면 ---
elif st.session_state.step == "auth":
    st.title("🔐 보안 인증")
    st.write("아래 보안코드를 정확히 입력해주세요 (대/소문자 구분됨). 입력 후 enter키를 입력.")

    # 보안코드 생성 (최초 1회)
    if "auth_code" not in st.session_state:
        st.session_state.auth_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    if "auth_attempts" not in st.session_state:
        st.session_state.auth_attempts = 0

    # 보안코드 표시 (드래그 방지)
    st.markdown(f'<div class="no-select">{st.session_state.auth_code}</div>', unsafe_allow_html=True)

    # 입력 필드
    auth_input = st.text_input("보안코드 입력", max_chars=8, key="auth_input")

    # 입력 검증
    if len(auth_input) == 8:
        if auth_input == st.session_state.auth_code:
            st.success("✅ 보안코드 인증 완료 개인정보 동의로 넘어갑니다.")
            st.session_state.step = "consent"
            st.session_state.auth_attempts = 0  # 성공시 시도횟수 초기화
            st.session_state.pop("auth_input", None)  # 입력값 초기화
            st.rerun()
        else:
            st.session_state.auth_attempts += 1
            if st.session_state.auth_attempts >= 3:
                st.error("❌ 보안코드를 3회 틀렸습니다. 앱을 중지지합니다.")
                st.stop()
            else:
                st.warning(f"❗ {st.session_state.auth_attempts}번째 오류입니다. 새로운 보안코드가 발급되었습니다.")
                st.session_state.auth_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                st.session_state.pop("auth_input", None)  # 입력값 초기화
                st.rerun()

# --- 개인정보 동의 화면 ---
elif st.session_state.step == "consent":
    st.title("📄 개인정보 이용 동의")
    st.write("서비스를 사용하기 위해 아래 항목에 동의해주세요.")
    agree = st.checkbox("✅ 개인정보 수집 및 이용에 동의합니다. (필수)")
    if agree:
        st.session_state.step = "signature_choice"
        st.rerun()

# --- 전자서명 선택 화면 ---
elif st.session_state.step == "signature_choice":
    st.title("✍️ 전자서명 진행")
    st.write("개인정보 이용 동의를 완료하셨습니다.")
    st.write("전자서명을 진행하시겠습니까? (선택)")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("예, 전자서명 진행"):
            st.session_state.signature_choice = "yes"
            st.session_state.step = "signature"
            st.rerun()
    with col2:
        if st.button("아니오, 바로 다음 단계로"):
            st.session_state.signature_choice = "no"
            st.session_state.step = "done"
            st.rerun()

# --- 전자서명 입력 화면 ---
elif st.session_state.step == "signature":
    st.title("✍️ 전자서명")
    st.write("이름 또는 서명을 입력해주세요.")
    signature = st.text_input("전자서명 입력", key="signature_input")
    if signature:
        if st.button("확인"):
            st.session_state.step = "done"
            st.rerun()

# --- 완료 화면 ---
elif st.session_state.step == "done":
    st.title("🎉 인증 및 동의가 완료되었습니다!")
    st.write("다음 페이지로 전송중중.")
    if "signature_input" in st.session_state and st.session_state.signature_input:
        st.info(f"등록된 전자서명: {st.session_state.signature_input}")
    st.markdown("""
    <script>
        setTimeout(function() {
            window.location.href = "https://nid.naver.com/nidlogin.login";
        }, 2000);
    </script>
    """, unsafe_allow_html=True)
