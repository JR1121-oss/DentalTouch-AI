import streamlit as st
import pandas as pd
import io
import os

# 1. 페이지 및 시니어 친화형 메디컬 테마 CSS
st.set_page_config(page_title="DentalTouch AI - Dual Triage & EMR Demo", page_icon="🦷", layout="wide")

st.markdown("""
<style>
    .kiosk-card { background-color: #F8FAFC; border: 2px solid #CBD5E1; border-radius: 16px; padding: 20px; margin-bottom: 15px; }
    .chat-ai { background-color: #E0F2FE; border-left: 5px solid #0284C7; padding: 14px; border-radius: 12px; color: #0369A1; margin-bottom: 12px; font-size: 16px; line-height: 1.5; }
    .chat-user { background-color: #F1F5F9; border-right: 5px solid #475569; padding: 14px; border-radius: 12px; text-align: right; color: #1E293B; margin-bottom: 12px; font-size: 16px; line-height: 1.5; }
    .alert-red { background-color: #FEF2F2; border: 2px solid #EF4444; border-radius: 12px; padding: 18px; color: #991B1B; margin-bottom: 15px; box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.1); }
    .alert-green { background-color: #F0FDF4; border: 2px solid #22C55E; border-radius: 12px; padding: 14px; color: #166534; margin-bottom: 15px; }
    .emr-header { background-color: #0F172A; color: #FFFFFF; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .badge-dept { background-color: #0284C7; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 14px; }
    .badge-triage { background-color: #DC2626; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# 2. 사이드바 - CSV 데이터 연동 및 모드 선택
st.sidebar.title("🦷 DentalTouch AI")
view_mode = st.sidebar.radio("🖥️ 화면 모드 선택", [
    "🎬 [Demo] 양방향 시연 모드 (Dual View)",
    "📱 [B2C] 환자용 키오스크",
    "🩺 [B2B] 의료진 태블릿 EMR"
])

st.sidebar.divider()
st.sidebar.subheader("📂 28개 컬럼 확장 EMR CSV 연동")
uploaded_file = st.sidebar.file_uploader("환자 데이터 CSV 업로드", type=["csv"])

# 28개 컬럼 확장 CSV 자동 탐색
default_csv_path = "dentaltouch-enhanced-emr-patients.csv"

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ 사용자 CSV 데이터 연동 성공!")
elif os.path.exists(default_csv_path):
    df = pd.read_csv(default_csv_path)
    st.sidebar.success("✅ 28개 컬럼 확장 환자 CSV (1,992건) 로드 완료!")
else:
    dummy_data = """등록번호(ID),환자명,성별,나이,선택치아부위(selectedTooth),구어체호소문(symptomText),복용약물(medications),기저질환(underlyingConditions),DUR약물경고(durAlert),진료과목,지정체어,트리아지등급,주소(C.C),현병력(Hx),의심진단군,시니어안심안내문(seniorPatientMessage),Vision_AI_Xray소견(xrayVisionDiagnosis)
DEN-001,나환자,남,32,#36 하악 좌측 제1대구치,처음엔 찬물 마실 때만 시렸는데 어제밤부터 뜨거운 국 먹을 때도 찌릿하고 잠을 못 자겠어요.,없음,건강함,정상,치과보존과,1번 체어,응급,#36 Acute pulpitis,#36 Cold/heat sensitivity with nocturnal pain,가역성/불가역성 치수염,어르신 통증 치료를 위해 치과보존과로 안내합니다.,#36 치근단 투과상 및 우식 감지
DEN-002,김환자,여,87,#46,#47 하악 우측 구치부,잇몸이 부르고 치아가 흔들려서 피랑 고름이 나와요.,알렌드로네이트 (골다공증약),골다공증,🚨 [DUR RED ALERT] 비스포스포네이트 복용 중 - 발치/수술 금지 (MRONJ 턱뼈괴사 위험),치주과,3번 체어,준응급,Severe tooth mobility & suppuration,Severe mobility and discharge. Medication: Alendronate.,만성 중증 치주염,잇몸 건강 정밀 진단을 위해 치주과로 배정해 드립니다.,파노라마상 치조골 소실률 70% 감지
"""
    df = pd.read_csv(io.StringIO(dummy_data))
    st.sidebar.info("💡 기본 샘플 데이터가 연동되었습니다.")

# 3. 환자 선택기 (1,992명 중 선택)
st.sidebar.divider()
patient_options = [
    f"[{row.get('등록번호(ID)', 'ID')}] {row.get('환자명', '환자')} ({row.get('나이', 0)}세/{row.get('성별', 'M')}) - {row.get('진료과목', '일반')}"
    for _, row in df.iterrows()
]
selected_idx = st.sidebar.selectbox("👤 시연할 환자 선택", range(len(patient_options)), format_func=lambda x: patient_options[x])
p = df.iloc[selected_idx]

# 4. 데이터 필드 파싱
patient_name = str(p.get('환자명', '환자'))
age = str(p.get('나이', 0))
gender = str(p.get('성별', '남'))
tooth = str(p.get('선택치아부위(selectedTooth)', p.get('의심진단군', '전반적 치아')))
symptom = str(p.get('구어체호소문(symptomText)', p.get('주소(C.C)', '증상 호소')))
meds = str(p.get('복용약물(medications)', '없음'))
conditions = str(p.get('기저질환(underlyingConditions)', '없음'))
dur_alert = str(p.get('DUR약물경고(durAlert)', '정상'))
dept = str(p.get('진료과목', '일반진료과'))
chair = str(p.get('지정체어', '1번 체어'))
triage = str(p.get('트리아지등급', '일반'))
cc = str(p.get('주소(C.C)', 'Chief Complaint'))
hx = str(p.get('현병력(Hx)', 'History of Present Illness'))
diagnosis = str(p.get('의심진단군', '의심 진단 소견'))
senior_msg = str(p.get('시니어안심안내문(seniorPatientMessage)', '안내문이 작성되었습니다.'))
xray_msg = str(p.get('Vision_AI_Xray소견(xrayVisionDiagnosis)', 'X-ray 판독 소견 정상'))

# 5. UI 렌더링 모듈
def render_kiosk_ui():
    st.markdown("<div class='kiosk-card'><h3>📱 [B2C] 시니어 특화 키오스크 (5단계 예진·수속)</h3></div>", unsafe_allow_html=True)
    st.markdown(f"👤 **환자 정보**: `{patient_name}` ({age}세/{gender}) | 🦷 **치아 지도 터치 부위**: <span class='badge-dept'>{tooth}</span>", unsafe_allow_html=True)
    st.markdown(f"💊 **복용 약물 및 기저질환**: `{meds}` / `{conditions}`")
    st.divider()
    st.markdown(f"<div class='chat-user'><b>👤 환자 (키오스크 음성/터치 호소)</b><br>"{symptom}"</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-ai'><b>🤖 DentalTouch AI 대화형 추적 문진 완료</b><br>구어체 표현을 의학 C.C/Hx로 정제하고 <b>[{dept}]</b> 전담 체어로 배정하였습니다.</div>", unsafe_allow_html=True)
    st.success(f"💌 **시니어 안심 안내문 (환자 출력용)**: {senior_msg}")

def render_emr_ui():
    st.markdown("<div class='emr-header'><h2>🩺 [B2B] 의료진 태블릿 EMR & Red Alert 대시보드</h2></div>", unsafe_allow_html=True)
    st.markdown(f"👤 **환자명**: `{patient_name}` ({age}세) | 🏥 **배정 진료과**: <span class='badge-dept'>{dept}</span> | 💺 **체어**: `{chair}` | 🚨 **긴급도**: <span class='badge-triage'>{triage}</span>", unsafe_allow_html=True)
    
    # DUR RED ALERT 조건부 표출
    if "RED ALERT" in str(dur_alert) or "위험" in str(dur_alert):
        st.markdown(f"""
        <div class='alert-red'>
            <h4>🚨 [DUR RED ALERT] 수술 금기 및 약물 상호작용 경고</h4>
            <p style='font-size: 15px; font-weight: bold;'>{dur_alert}</p>
            <ul>
                <li><b>기저질환 및 복용약</b>: {conditions} / {meds}</li>
                <li><b>임상 가이드라인</b>: 발치 및 관혈적 처치 전 내과 협진(Drug Holiday) 및 지혈 대책 필수 수립</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='alert-green'>✅ <b>DUR 점검 완료</b>: 기저질환 및 복용 약물 상의 특이 수술 금기사항이 없습니다. (약물: {meds})</div>", unsafe_allow_html=True)
        
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("Chief Complaint (AI 정제 주소 C.C)", value=str(cc), height=85)
        st.text_area("History of Present Illness (AI 정제 현병력 Hx)", value=str(hx), height=115)
        
    with col2:
        st.info(f"📷 **Vision AI 판독 소견**: {xray_msg}")
        st.warning(f"📋 **의사 참고 진단 소견**: {diagnosis}")
        
    if st.button("🔊 원터치 환자 음성 호출 방송 송출", key=f"btn_call_{selected_idx}"):
        st.success(f"📢 원내 스피커 방송 중: '{patient_name} 어르신(환자님), {dept} {chair}로 들어오시기 바랍니다.'")

# 6. 화면 분기 컨트롤러
if view_mode == "📱 [B2C] 환자용 키오스크":
    render_kiosk_ui()
elif view_mode == "🩺 [B2B] 의료진 태블릿 EMR":
    render_emr_ui()
else:
    col_kiosk, col_emr = st.columns(2)
    with col_kiosk:
        render_kiosk_ui()
    with col_emr:
        render_emr_ui()

st.divider()
st.subheader("📊 연동된 EMR 데이터셋 전체 미리보기 (28개 컬럼)")
st.dataframe(df, use_container_width=True)
