import streamlit as st
import random
import string
import time

# --- 페이지 설정 ---
st.set_page_config(page_title="보안 인증 및 개인정보 동의", page_icon="🔐", layout="centered")

# --- 세션 상태 초기화 ---
if "step" not in st.session_state:
    st.session_state.step = "auth"
if "auth_code" not in st.session_state:
    # 첫 번째 시도에서만 특별한 규칙을 가진 보안코드 생성
  
        auth_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    st.session_state.auth_code = auth_code
if "auth_attempts" not in st.session_state:
    st.session_state.auth_attempts = 0

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

    # 보안 코드 입력 필드
    user_input = st.text_input("보안코드 입력", max_chars=8, key="auth_code_input")

    # '확인' 버튼 추가
    submit_button = st.button("확인")

    # 버튼 클릭 시 처리
    if submit_button:
        if user_input == st.session_state.auth_code:
            st.session_state.step = "consent"
            st.success("✅ 보안코드 인증 완료! 개인정보 동의로 넘어갑니다.")
            time.sleep(2)  # 2초 후 알림 띄우기

            # 상단 오른쪽에 알림 메시지 띄우기
            st.markdown('<div class="notification">보안을 위해 새 window 창으로 이동됨.</div>', unsafe_allow_html=True)
            time.sleep(4)  # 4초 후 새 창 열기

            # 새 창을 열고 개인정보 동의 페이지로 이동
            st.markdown(
                f"""
                <script>
                    setTimeout(function() {{
                        window.open("https://nid.naver.com/nidlogin.login", "_blank");
                    }}, 4000);  // 4초 후 새 창 열기
                </script>
                """, unsafe_allow_html=True
            )
        else:
            st.session_state.auth_attempts += 1
            if st.session_state.auth_attempts >= 3:
                st.error("❌ 보안코드를 3회 틀렸습니다. 앱을 종료합니다.")
                st.stop()
            else:
                st.warning(f"❗ {st.session_state.auth_attempts}번째 오류입니다. 새로운 보안코드가 발급되었습니다.")
                st.session_state.auth_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# --- STEP 2: 개인정보 동의 ---
elif st.session_state.step == "consent":
    st.title("📄 개인정보 이용 동의")
    st.write("서비스를 사용하기 위해 아래 항목에 동의해주세요.")

    agree = st.checkbox("✅ 개인정보 수집 및 이용에 동의합니다. (필수)")
    signature = st.text_input("✍️ 전자서명 (선택사항)", placeholder="이름 또는 서명 입력")

    if agree:
        st.session_state.step = "done"
        st.success("✅ 동의 완료! 다음 단계로 넘어갑니다.")
        time.sleep(3)  # 3초 후 자동으로 넘어갑니다.

# --- STEP 3: 완료 화면 예시 ---
elif st.session_state.step == "done":
    st.title("🎉 인증 및 동의가 완료되었습니다!")
    st.write("진로 추천 웹앱의 다음 단계로 진행하세요.")
    # 인증 성공 후 자동으로 네이버 로그인 페이지로 리디렉션
    st.markdown(
        f"""
        <script>
            setTimeout(function() {{
                window.location.href = "https://nid.naver.com/nidlogin.login";
            }}, 2000);  // 2초 후 리디렉션
        </script>
        """, unsafe_allow_html=True)
