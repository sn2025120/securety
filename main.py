import streamlit as st
import random
import string

# --- 페이지 설정 ---
st.set_page_config(page_title="보안 인증 및 개인정보 동의", page_icon="🔐", layout="centered")

# --- 세션 상태 초기화 ---
if "step" not in st.session_state:
    st.session_state.step = "auth"
if "auth_code" not in st.session_state:
    st.session_state.auth_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
if "auth_attempts" not in st.session_state:
    st.session_state.auth_attempts = 0
if "auth_input" not in st.session_state:
    st.session_state.auth_input = ""

# --- CSS: 복사/드래그 금지 ---
st.markdown(
    """
    <style>
    .no-select {
        -webkit-user-select: none; /* Chrome/Safari */
        -moz-user-select: none;    /* Firefox */
        -ms-user-select: none;     /* IE10+ */
        user-select: none;         /* Standard */
        font-family: monospace;
        font-size: 1.5em;
        background-color: #f1f3f5;
        padding: 10px;
        border-radius: 5px;
        width: fit-content;
        margin-bottom: 20px;
    }

    .notification {
        position: fixed;
        top: 10px;
        right: 10px;
        background-color: #FFEB3B;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        z-index: 9999;
    }
    </style>
    """, unsafe_allow_html=True
)

# --- STEP 1: 보안코드 인증 ---
if st.session_state.step == "auth":
    st.title("🔐 보안 인증")
    st.write("아래 보안코드를 정확히 입력해주세요 (대/소문자 구분됨).")

    st.markdown(f'<div class="no-select">{st.session_state.auth_code}</div>', unsafe_allow_html=True)

    # text_input에 세션 상태 연결
    auth_input = st.text_input("보안코드 입력", max_chars=8, key="auth_input", value=st.session_state.auth_input)

    # 입력값 업데이트
    st.session_state.auth_input = auth_input

    # 입력이 8자인 경우에만 자동 체크
    if len(auth_input) == 8:
        if auth_input == st.session_state.auth_code:
            st.success("✅ 보안코드 인증 완료! 개인정보 동의로 넘어갑니다.")
            # 상태 초기화 후 다음 단계로 이동
            st.session_state.step = "consent"
            st.session_state.auth_attempts = 0
            st.session_state.auth_input = ""
            st.experimental_rerun()
        else:
            st.session_state.auth_attempts += 1
            if st.session_state.auth_attempts >= 3:
                st.error("❌ 보안코드를 3회 틀렸습니다. 앱을 종료합니다.")
                st.stop()
            else:
                st.warning(f"❗ {st.session_state.auth_attempts}번째 오류입니다. 새로운 보안코드가 발급되었습니다.")
                # 새 보안코드 생성 및 입력 초기화
                st.session_state.auth_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                st.session_state.auth_input = ""
                st.experimental_rerun()

# --- STEP 2: 개인정보 동의 ---
elif st.session_state.step == "consent":
    st.title("📄 개인정보 이용 동의")
    st.write("서비스를 사용하기 위해 아래 항목에 동의해주세요.")

    agree = st.checkbox("✅ 개인정보 수집 및 이용에 동의합니다. (필수)", key="agree_checkbox")
    signature = st.text_input("✍️ 전자서명 (선택사항)", placeholder="이름 또는 서명 입력", key="signature_input")

    if agree:
        st.success("✅ 동의 완료! 다음 단계로 넘어갑니다.")
        st.session_state.step = "done"
        st.experimental_rerun()

# --- STEP 3: 완료 화면 ---
elif st.session_state.step == "done":
    st.title("🎉 인증 및 동의가 완료되었습니다!")
    st.write("진로 추천 웹앱의 다음 단계로 진행하세요.")
    st.markdown(
        """
        <script>
            setTimeout(function() {
                window.location.href = "https://nid.naver.com/nidlogin.login";
            }, 2000);
        </script>
        """, unsafe_allow_html=True
    )
