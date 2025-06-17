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
stage_count = len(stage_labels)

# --- 세션 상태 초기화 ---
if "init_stage" not in st.session_state:
    st.session_state.init_stage = 0   # 0~3 (3이면 무결성 검증)
if "step" not in st.session_state:
    st.session_state.step = "init"    # "init" -> "auth" 등

# --- 초기화 단계 화면 ---
if st.session_state.step == "init":
    st.markdown("<style>.fade{color:#bbb;font-size:1.2em;}.bold{color:#222;font-weight:bold;font-size:1.2em;}</style>", unsafe_allow_html=True)
    # 단계별로 색상 변경
    for idx, label in enumerate(stage_labels):
        if st.session_state.init_stage == idx:
            st.markdown(f"<div class='bold'>{label}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='fade'>{label}</div>", unsafe_allow_html=True)
    # 단계 진행
    if st.session_state.init_stage < stage_count:
        time.sleep(2)  # 2초 대기
        st.session_state.init_stage += 1
        st.rerun()
    else:
        # 3단계 끝나면 문구 지우고 '무결성 검증됨' 표시
        st.session_state.step = "integrity"
        st.rerun()

# --- 무결성 검증됨 화면 (1초) ---
elif st.session_state.step == "integrity":
    st.markdown("<style>.integrity{color:#1abc9c;font-size:1.3em;font-weight:bold;}</style>", unsafe_allow_html=True)
    st.markdown("<div class='integrity'>무결성 검증됨</div>", unsafe_allow_html=True)
    time.sleep(1)
    st.session_state.step = "auth"
    st.rerun()

# --- 보안코드 인증 이후 기존 코드 이어서 ---
elif st.session_state.step == "auth":
    # ... (여기서부터 기존 보안코드 인증 코드 시작)
    st.title("🔐 보안 인증")
    st.write("아래 보안코드를 정확히 입력해주세요 (대/소문자 구분됨).")
    if "auth_code" not in st.session_state:
        st.session_state.auth_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    if "auth_attempts" not in st.session_state:
        st.session_state.auth_attempts = 0
    if "auth_input" not in st.session_state:
        st.session_state.auth_input = ""
    st.markdown(f'<div class="no-select">{st.session_state.auth_code}</div>', unsafe_allow_html=True)
    st.text_input("보안코드 입력", max_chars=8, key="auth_input")
    auth_input = st.session_state.auth_input
    if len(auth_input) == 8:
        if auth_input == st.session_state.auth_code:
            st.success("✅ 보안코드 인증 완료! 개인정보 동의로 넘어갑니다.")
            st.session_state.step = "consent"
            st.session_state.auth_attempts = 0
            st.rerun()
        else:
            st.session_state.auth_attempts += 1
            if st.session_state.auth_attempts >= 3:
                st.error("❌ 보안코드를 3회 틀렸습니다. 앱을 종료합니다.")
                st.stop()
            else:
                st.warning(f"❗ {st.session_state.auth_attempts}번째 오류입니다. 새로운 보안코드가 발급되었습니다.")
                st.session_state.auth_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                st.rerun()

# --- STEP 2: 개인정보 동의 ---
elif st.session_state.step == "consent":
    st.title("📄 개인정보 이용 동의")
    st.write("서비스를 사용하기 위해 아래 항목에 동의해주세요.")

    agree = st.checkbox("✅ 개인정보 수집 및 이용에 동의합니다. (필수)", key="agree_checkbox")

    if agree:
        st.session_state.step = "signature_choice"
        st.rerun()

# --- STEP 2.5: 전자서명 선택 ---
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

# --- STEP 2.6: 전자서명 입력 ---
elif st.session_state.step == "signature":
    st.title("✍️ 전자서명")
    st.write("이름 또는 서명을 입력해주세요.")
    signature = st.text_input("전자서명 입력", key="signature_input")
    if signature:
        if st.button("확인"):
            st.session_state.step = "done"
            st.rerun()

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
