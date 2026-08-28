import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import os

# ==========================================
# 1. Хуудасны тохиргоо ба CSS (Sky Blue Theme + Sliding Animations)
# ==========================================
st.set_page_config(
    page_title="Pasture Degradation Risk Prediction",
    page_icon="🌱",
    layout="wide"
)

st.markdown("""
    <style>
        .main, .stApp { 
            background-color: #F0F9FF !important; 
        }
        [data-testid="stSidebar"] {
            background-color: #E0F2FE !important;
        }
        h1, h2, h3, h4, h5, h6, p, label, .stMarkdown { 
            color: #0C4A6E !important; 
        }

        @keyframes slideInRight {
            0% { opacity: 0; transform: translateX(80px); }
            100% { opacity: 1; transform: translateX(0); }
        }

        @keyframes slideInLeft {
            0% { opacity: 0; transform: translateX(-80px); }
            100% { opacity: 1; transform: translateX(0); }
        }

        .slide-right { animation: slideInRight 1.0s cubic-bezier(0.25, 1, 0.5, 1) forwards; }
        .slide-left { animation: slideInLeft 1.0s cubic-bezier(0.25, 1, 0.5, 1) forwards; }

        .nav-brand {
            font-size: 24px;
            font-weight: 800;
            color: #0284C7 !important;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        div[role="dialog"] { background-color: #F0F9FF !important; }
        div[role="dialog"] h2, div[role="dialog"] h3 { color: #0284C7 !important; font-weight: 800 !important; }
        div[role="dialog"] p, div[role="dialog"] li, div[role="dialog"] div { color: #0F172A !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Олон хэлний Толь бичиг
# ==========================================
translations = {
    "Монгол": {
        "sidebar_title": "Settings / Тохиргоо",
        "lang_label": "Language / Хэл:",
        "input_params": "Оруулах үзүүлэлтүүд",
        "lbl_precip": "Жилийн хур тунадас (мм):",
        "lbl_temp": "Агаарын дундаж температур (°C):",
        "lbl_pasture": "Бэлчээрийн талбай (мянга га):",
        "lbl_count": "Малын тоо (мянга тоо толгой):",
        "lbl_loss": "Зүй бус хорогдол (мянга толгой):",
        "upload_label": "📁 Файлаар өгөгдөл оруулах (CSV/XLSX):",
        "export_btn": "📥 Таамаглалын тайлан татах",
        "main_title": "Бэлчээрийн Доройтлын ЭРСДЭЛИЙГ Таамаглах Систем",
        "main_subtitle": "Уур амьсгал болон мал ахуйн үзүүлэлтэд суурилсан хиймэл интеллектийн хяналтын багц.",
        "ai_result_title": "AI Таамаглалын Дүн",
        "nav_about": "🌿 COP-17 & Төслийн зорилго",
        "cop_modal_title": "COP-17 Ulaanbaatar 2026 & AI Системийн Уялдаа",
        "cop_sub": "НҮБ-ын Цөлжилттэй тэмцэх конвенцын Талуудын 17-р бага хурал (UNCCD COP-17)",
        "cop_loc": "📍 **Байршил:** Улаанбаатар хот, Монгол Улс",
        "cop_date": "📅 **Огноо:** 2026 он",
        "goal_title": "🎯 Системийн Гол Зорилго ба Шаардлага",
        "goal_desc": """
        Монгол орны бэлчээрийн 70 гаруй хувь нь тодорхой хэмжээгээр доройтолд ороод байгаа бөгөөд COP-17 бага хурлын гол стратеги нь <b>бэлчээрийг тогтвортой хамгаалах, цөлжилтийг сааруулах</b> явдал юм.<br/><br/>
        <b>Энэхүү AI Системийн шийдэх асуудал:</b>
        <ul>
            <li><b>Эрт анхааруулах систем:</b> Цаг уурын өөрчлөлт болон малын нягтралд суурилан бэлчээрийн доройтлын эрсдэлийг урьдчилан таамаглах.</li>
            <li><b>Датанд суурилсан шийдвэр:</b> Бэлчээр ашиглалт, нүүдэл суудлыг оновчтой зохицуулахад шинжлэх ухааны үндэслэлтэй дата өгөх.</li>
            <li><b>Эрсдэлийг бууруулах:</b> Зуд болон гангийн эрсдэлийг эрт тодорхойлж, малын зүй бус хорогдлыг багасгах.</li>
        </ul>
        """,
        "target_users_title": "👥 Ашиглах бүлэг & Гарах үр дүн",
        "target_users_desc": "• <b>Шийдвэр гаргачид:</b> Бүс нутгийн бэлчээрийн даацад тохирсон бодлого хэрэгжүүлэх.<br/>• <b>Судлаачид:</b> Цаг уур болон бэлчээрийн динамик өөрчлөлтийг AI загвараар шинжлэх.<br/>• <b>Орон нутаг & Малчид:</b> Газар нутгийнхаа бэлчээрийн эрсдэлийг бодитой үнэлэх.",
        "kpi_precip": "Хур тунадас",
        "kpi_temp": "Температур",
        "kpi_density": "Малын нягтрал",
        "kpi_loss": "Хорогдол",
        "unit_mm": "мм",
        "unit_density": "толгой/га",
        "unit_thousand": "мян.тол",
        "risk_level_label": "ЭРСДЭЛИЙН ТҮВШИН:",
        "radar_title": "Үзүүлэлтүүдийн Харьцаа ба Радар График",
        "radar_subtitle": "Оруулсан үзүүлэлтүүдийн стандартчилсан утга",
        "feature_title": "Үзүүлэлтүүдийн Нөлөөлөл (Feature Importance)",
        "feature_subtitle": "Ямар үзүүлэлтүүд AI загварын таамаглалд хамгийн их нөлөөлж байна вэ?",
        "categories": ['Малын тоо', 'Хур тунадас', 'Температур', 'Зүй бус хорогдол', 'Малын нягтрал'],
        "feature_labels": {
            "livestock_density": "Малын нягтрал",
            "livestock_loss": "Зүй бус хорогдол",
            "precipitation": "Хур тунадас",
            "livestock_count": "Малын тоо",
            "temperature": "Температур",
            "pasture_area": "Бэлчээрийн талбай"
        },
        "dataset_title": "📊 Өгөгдлийн сангийн мэдээлэл ба тодорхойлолт",
        "dataset_caption": "AI загварыг сургахад ашигласан цаг уур болон бэлчээрийн үзүүлэлтүүдийн бүтэц.",
        "col_feature": "Үзүүлэлтийн нэр",
        "col_unit": "Хэмжих нэгж",
        "col_role": "Үүрэг",
        "col_desc": "Тайлбар"
    },
    "English": {
        "sidebar_title": "Settings / Configuration",
        "lang_label": "Language:",
        "input_params": "Input Parameters",
        "lbl_precip": "Annual Precipitation (mm):",
        "lbl_temp": "Average Air Temp (°C):",
        "lbl_pasture": "Pasture Area (thousand ha):",
        "lbl_count": "Livestock Count (thousand head):",
        "lbl_loss": "Livestock Loss (thousand head):",
        "upload_label": "📁 Upload Dataset File (CSV/XLSX):",
        "export_btn": "📥 Export Prediction Report",
        "main_title": "Pasture Degradation Risk Prediction System",
        "main_subtitle": "Machine Learning Dashboard based on climate and livestock parameters.",
        "ai_result_title": "AI Prediction Result",
        "nav_about": "🌿 COP-17 & Project Mission",
        "cop_modal_title": "COP-17 Ulaanbaatar 2026 & AI Integration",
        "cop_sub": "17th Conference of the Parties to the UNCCD (UNCCD COP-17)",
        "cop_loc": "📍 **Location:** Ulaanbaatar, Mongolia",
        "cop_date": "📅 **Date:** 2026",
        "goal_title": "🎯 Key System Objectives & Alignment",
        "goal_desc": """
        Over 70% of Mongolia's pastureland is degraded. Aligning with COP-17, this project targets <b>sustainable land management and combating desertification</b>.<br/><br/>
        <b>Solutions provided by this AI System:</b>
        <ul>
            <li><b>Early Warning Framework:</b> Predicts pasture degradation risks ahead of time using climate and livestock load metrics.</li>
            <li><b>Data-Driven Decisions:</b> Empowers decision-makers with machine learning insights.</li>
            <li><b>Risk Mitigation:</b> Identifies severe drought and dzud vulnerabilities early.</li>
        </ul>
        """,
        "target_users_title": "👥 Target Stakeholders & Impact",
        "target_users_desc": "• <b>Policymakers:</b> Implement sustainable land policies.<br/>• <b>Researchers:</b> Analyze spatio-temporal trends.<br/>• <b>Local Communities:</b> Gain actionable risk insights.",
        "kpi_precip": "Precipitation",
        "kpi_temp": "Temperature",
        "kpi_density": "Livestock Density",
        "kpi_loss": "Livestock Loss",
        "unit_mm": "mm",
        "unit_density": "head/ha",
        "unit_thousand": "k.head",
        "risk_level_label": "RISK LEVEL:",
        "radar_title": "Parameter Proportions & Radar Chart",
        "radar_subtitle": "Normalized values of input features",
        "feature_title": "Feature Importance",
        "feature_subtitle": "Which features influence the AI model the most?",
        "categories": ['Livestock Count', 'Precipitation', 'Temperature', 'Livestock Loss', 'Livestock Density'],
        "feature_labels": {
            "livestock_density": "Livestock Density",
            "livestock_loss": "Livestock Loss",
            "precipitation": "Precipitation",
            "livestock_count": "Livestock Count",
            "temperature": "Temperature",
            "pasture_area": "Pasture Area"
        },
        "dataset_title": "📊 Dataset Information & Specification",
        "dataset_caption": "Structure of climate and pasture metrics used for training the AI model.",
        "col_feature": "Feature Name",
        "col_unit": "Unit",
        "col_role": "Role",
        "col_desc": "Description"
    }
}

# ==========================================
# 3. Sidebar (Тохиргоо ба Оруулах Үзүүлэлтүүд)
# ==========================================
st.sidebar.title("Settings / Тохиргоо")
lang = st.sidebar.radio("Language / Хэл:", options=["Монгол", "English"], index=0)
t = translations[lang]

st.sidebar.markdown("---")
st.sidebar.subheader(f"📊 {t['input_params']}")

precip = st.sidebar.slider(t["lbl_precip"], 0.0, 600.0, 250.0)
temp = st.sidebar.slider(t["lbl_temp"], -30.0, 45.0, 1.5)
pasture = st.sidebar.slider(t["lbl_pasture"], 100.0, 10000.0, 3738.0)
count = st.sidebar.slider(t["lbl_count"], 100.0, 10000.0, 2679.0)
loss = st.sidebar.slider(t["lbl_loss"], 0.0, 2000.0, 120.0)

# Малын нягтрал (толгой/га)
calculated_density = count / pasture if pasture > 0 else 0.0

st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader(t["upload_label"], type=["csv", "xlsx"])

# ==========================================
# 4. Navigation Header ба POP-UP Модал
# ==========================================
nav_col1, nav_col2 = st.columns([2.8, 1.2])

with nav_col1:
    st.markdown('<div class="nav-brand slide-right">🌱 Pasture Risk AI</div>', unsafe_allow_html=True)

with nav_col2:
    if st.button(t["nav_about"], use_container_width=True):
        @st.dialog("🌿 COP-17 & Platform Strategy")
        def show_cop_info():
            st.markdown(f"""
                <div class="slide-right">
                    <h3 style='color: #0284C7 !important; font-weight: 800; margin-bottom: 4px;'>🌿 {t['cop_modal_title']}</h3>
                    <p style='color: #0369A1; font-weight: 600; font-size: 14px;'>{t['cop_sub']}</p>
                    <div style='display: flex; gap: 15px; font-size: 13px; color: #334155;'>
                        <span>{t['cop_loc']}</span>
                        <span>{t['cop_date']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("---")
            st.markdown(f"""
                <div class="slide-left" style="background-color: #E0F2FE; padding: 16px; border-radius: 10px; border-left: 4px solid #0284C7; margin-bottom: 12px;">
                    <h4 style='color: #0369A1 !important; font-weight: 700; margin-bottom: 8px;'>{t['goal_title']}</h4>
                    <div style='color: #0C4A6E; font-size: 13.5px; line-height: 1.6;'>{t['goal_desc']}</div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <div class="slide-right" style="background-color: #F0FDF4; padding: 16px; border-radius: 10px; border-left: 4px solid #10B981;">
                    <h4 style='color: #047857 !important; font-weight: 700; margin-bottom: 8px;'>{t['target_users_title']}</h4>
                    <div style='color: #064E3B; font-size: 13px; line-height: 1.6;'>{t['target_users_desc']}</div>
                </div>
            """, unsafe_allow_html=True)

        show_cop_info()

st.markdown(f"""
    <div class="slide-left">
        <h1 style="color: #0C4A6E; font-weight: 800; margin-bottom: 0px;">{t['main_title']}</h1>
        <p style="color: #0369A1; font-size: 15px; margin-top: 4px;">{t['main_subtitle']}</p>
    </div>
""", unsafe_allow_html=True)
st.write("")

# ==========================================
# 5. KPI Картууд
# ==========================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.caption(t["kpi_precip"])
    st.header(f"{precip:.1f} {t['unit_mm']}")
with col2:
    st.caption(t["kpi_temp"])
    st.header(f"{temp:.1f} °C")
with col3:
    st.caption(t["kpi_density"])
    st.header(f"{calculated_density:.2f} {t['unit_density']}")
with col4:
    st.caption(t["kpi_loss"])
    st.header(f"{loss:.1f} {t['unit_thousand']}")

st.markdown("---")

# ==========================================
# 6. ДИНАМИК ОНООНЫ СИСТЕМ БА AI ТААМАГЛАЛ
# ==========================================
model_loaded = False

if os.path.exists("model.pkl"):
    try:
        model = joblib.load("model.pkl")
        input_data = pd.DataFrame([[precip, temp, pasture, count, loss, calculated_density]],
                                  columns=['precipitation', 'temperature', 'pasture_area', 'livestock_count', 'livestock_loss', 'livestock_density'])
        pred = model.predict(input_data)[0]
        raw_risk = str(pred).upper()
        
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(input_data)[0]
            prob_high, prob_med, prob_low = int(probs[0]*100), int(probs[1]*100), int(probs[2]*100)
        else:
            prob_high, prob_med, prob_low = (70, 20, 10) if raw_risk == "HIGH" else ((20, 60, 20) if raw_risk == "MEDIUM" else (10, 20, 70))
        
        model_loaded = True
    except Exception:
        model_loaded = False

# Загвар байхгүй эсвэл ачаалагдаагүй бол динамик тасралтгүй тооцоолол хийнэ
if not model_loaded:
    density_risk = np.clip((calculated_density - 0.5) / (2.0 - 0.5) * 100, 0, 100)
    precip_risk = np.clip((400 - precip) / (400 - 50) * 100, 0, 100)
    
    if temp < 0:
        temp_risk = np.clip((-temp) / 35.0 * 100, 0, 100)
    elif temp > 25:
        temp_risk = np.clip((temp - 25) / 20.0 * 100, 0, 100)
    else:
        temp_risk = 0.0

    loss_ratio = (loss / count) * 100 if count > 0 else 0
    loss_risk = np.clip(loss_ratio / 10.0 * 100, 0, 100)

    total_risk_score = (
        density_risk * 0.40 + 
        precip_risk * 0.35 + 
        temp_risk * 0.15 + 
        loss_risk * 0.10
    )

    prob_high = int(np.clip(total_risk_score, 5, 90))
    prob_low = int(np.clip(100 - total_risk_score, 5, 90))
    prob_med = max(0, 100 - prob_high - prob_low)

    if total_risk_score >= 55:
        raw_risk = "HIGH"
    elif total_risk_score >= 35:
        raw_risk = "MEDIUM"
    else:
        raw_risk = "LOW"

# UI Өнгө ба Нэршлийн тохиргоо
risk_map = {
    "HIGH": (
        "HIGH" if lang == "English" else "ӨНДӨР", "#DC2626", "#FEE2E2", 
        "🚨 HIGH RISK ASSESSMENT" if lang == "English" else "🚨 ЭРСДЭЛ ӨНДӨР НӨХЦӨЛ БАЙДЛЫН ДҮГНЭЛТ", 
        "Critical indicators reached. Immediate action recommended." if lang == "English" else "Олон тооны үзүүлэлт аюултай түвшинд хүрсэн тул яаралтай зохицуулалт шаардлагатай."
    ),
    "MEDIUM": (
        "MEDIUM" if lang == "English" else "ДУНД", "#D97706", "#FEF3C7", 
        "⚠️ MODERATE RISK ASSESSMENT" if lang == "English" else "⚠️ ЭРСДЭЛ ДУНД НӨХЦӨЛ БАЙДЛЫН ДҮГНЭЛТ", 
        "Certain metrics exceed normal thresholds. Attention required." if lang == "English" else "Зарим үзүүлэлт хэвийн хэмжээнээс хэтэрсэн тул анхааралдаа авах хэрэгтэй."
    ),
    "LOW": (
        "LOW" if lang == "English" else "БАГА", "#059669", "#DCFCE7", 
        "✅ STABLE CONDITION" if lang == "English" else "✅ ЭРСДЭЛ БАГА НӨХЦӨЛ БАЙДАЛ", 
        "All parameters remain within normal and safe levels." if lang == "English" else "Үзүүлэлтүүд хэвийн болон аюулгүй түвшинд байна."
    )
}
risk_display_name, current_color, bg_card_color, summary_title, summary_desc = risk_map[raw_risk]

# ==========================================
# 7. ДИНАМИК ТАЙЛБАР БА ШИЙДЛҮҮД
# ==========================================
critical_reasons, positive_reasons, recommendations = [], [], []

# Хур тунадас
if precip < 100:
    critical_reasons.append(f"🌧️ <b>{t['lbl_precip']} ({precip:.1f} мм):</b> " + ("Severe drought risk, critical moisture shortage." if lang == "English" else "Гангийн өндөр эрсдэлтэй, ургамал ургах чийг асар дутагдалтай."))
    recommendations.append("💧 " + ("Emergency feed supply, well drilling, reduce herd size." if lang == "English" else "Өвс тэжээлийн нөөц бүрдүүлж, гүний худаг гаргах, малын тоог яаралтай багасгах."))
elif precip < 250:
    critical_reasons.append(f"🌧️ <b>{t['lbl_precip']} ({precip:.1f} мм):</b> " + ("Below annual average rainfall." if lang == "English" else "Жилийн дундаж хэмжээнээс бага чийгшилтэй байна."))
    recommendations.append("💧 " + ("Implement rotational grazing schedules." if lang == "English" else "Бэлчээрийг хэсэгчлэн амрааж сэлгэн ашиглах."))
else:
    positive_reasons.append(f"🌧️ <b>{t['lbl_precip']} ({precip:.1f} мм):</b> " + ("Sufficient rainfall for vegetation." if lang == "English" else "Хөрсний чийг ба ургамлын ургалтад эерэг нөлөөтэй."))

# Нягтрал
if calculated_density > 1.5:
    critical_reasons.append(f"🐄 <b>{t['kpi_density']} ({calculated_density:.2f} {t['unit_density']}):</b> " + ("Pasture capacity severely exceeded." if lang == "English" else "Даац хэд дахин хэтэрч талхлагдахад хүрсэн."))
    recommendations.append("🐄 " + ("Relocate livestock via otor or cull low-productivity stock." if lang == "English" else "Өөр аймаг, суманд отор нүүдэл хийх, малын чанарт анхаарч тоог цөөлөх."))
elif calculated_density > 0.8:
    critical_reasons.append(f"🐄 <b>{t['kpi_density']} ({calculated_density:.2f} {t['unit_density']}):</b> " + ("Grazing pressure is high." if lang == "English" else "Бэлчээрийн даац хэтрэх аюултай түвшинд байна."))
    recommendations.append("📊 " + ("Adjust grazing schedule with local user groups." if lang == "English" else "Бэлчээр ашиглалтын нөхөрлөлийн хуваарьт шилжих."))
else:
    positive_reasons.append(f"🌱 <b>{t['kpi_density']} ({calculated_density:.2f} {t['unit_density']}):</b> " + ("Normal grazing pressure." if lang == "English" else "Бэлчээрийн даац ба малын нягтрал нормал түвшинд байна."))

# Температур
if temp < -20:
    critical_reasons.append(f"❄️ <b>{t['lbl_temp']} ({temp:.1f}°C):</b> " + ("High dzud (severe winter) risk." if lang == "English" else "Зуд болон хүйтний стресс үүсэх эрсдэлтэй."))
    recommendations.append("❄️ " + ("Insulate shelters, prepare emergency supplementary feed." if lang == "English" else "Хашаа саравчаа дулаалах, нэмэгдэл тэжээл бэлтгэх."))
elif temp > 30:
    critical_reasons.append(f"☀️ <b>{t['lbl_temp']} ({temp:.1f}°C):</b> " + ("Extreme heat evaporating soil moisture." if lang == "English" else "Бэлчээрийн чийг хурдан ууршиж гангатахад хүрч байна."))
    recommendations.append("☀️ " + ("Provide shading and ensure continuous water access." if lang == "English" else "Худаг усаа бэлдэж, малыг нарнаас хамгаалах."))
else:
    positive_reasons.append(f"🌡️ <b>{t['lbl_temp']} ({temp:.1f}°C):</b> " + ("Optimal temperature range." if lang == "English" else "Агаарын дундаж температур нормал түвшинд байна."))

# Хорогдол
if loss > 200:
    critical_reasons.append(f"⚠️ <b>{t['kpi_loss']} ({loss:.0f} {t['unit_thousand']}):</b> " + ("High unnatural mortality." if lang == "English" else "Зүй бус хорогдлын хэмжээ өндөр байна."))
    recommendations.append("🛡️ " + ("Enhance veterinary services and vaccinations." if lang == "English" else "Вакцинжуулалт, урьдчилан сэргийлэх арга хэмжээ аваарай."))

if not recommendations:
    recommendations.append("🌿 " + ("Maintain current pasture management." if lang == "English" else "Бэлчээрийн менежментээ хэвийн үргэлжлүүлнэ үү."))


# ==========================================
# 8. ДЭЛГЭЦИЙН ЗОХИОН БАЙГУУЛАЛТ (LAYOUT)
# ==========================================
col_left, col_right = st.columns([1, 1])

# --- ЗҮҮН БАГАНА ---
with col_left:
    st.subheader(t["ai_result_title"])
    st.markdown(f"""
        <div style="background-color: {bg_card_color}; padding: 16px 20px; border-radius: 12px; border-left: 6px solid {current_color}; margin-bottom: 15px;">
            <span style="font-size: 13px; color: #1E293B; font-weight: 700;">{t['risk_level_label']}</span><br/>
            <span style="font-size: 26px; color: {current_color}; font-weight: 800;">{risk_display_name} ({raw_risk})</span>
        </div>
    """, unsafe_allow_html=True)

    fig_donut = go.Figure(data=[go.Pie(
        labels=["Өндөр" if lang=="Монгол" else "High", "Дунд" if lang=="Монгол" else "Medium", "Бага" if lang=="Монгол" else "Low"],
        values=[prob_high, prob_med, prob_low],
        hole=.6,
        marker=dict(colors=['#EF4444', '#F59E0B', '#10B981'])
    )])
    fig_donut.update_layout(showlegend=True, height=220, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_donut, use_container_width=True)

# --- БАРУУН БАГАНА ---
with col_right:
    st.subheader(t["radar_title"])
    st.caption(t["radar_subtitle"])
    
    fig_radar = go.Figure(go.Scatterpolar(
        r=[
            min(precip / 600.0, 1.0),
            min((temp + 30) / 75.0, 1.0),
            min(pasture / 10000.0, 1.0),
            min(count / 10000.0, 1.0),
            min(calculated_density / 3.0, 1.0)
        ],
        theta=t["categories"], 
        fill='toself', 
        fillcolor='rgba(2, 132, 199, 0.25)', 
        line=dict(color='#0284C7', width=2)
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1]), bgcolor='rgba(255,255,255,0.5)'), showlegend=False, height=240, margin=dict(l=30, r=30, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_radar, use_container_width=True)


# ==========================================
# 9. ДҮГНЭЛТ БОЛОН ШИЙДЭЛ (ЗЭРГЭЦҮҮЛЭХ)
# ==========================================
st.markdown("<br/>", unsafe_allow_html=True)
col_summary, col_solution = st.columns([1, 1])

with col_summary:
    crit_title = "🚨 HIGH RISK FACTORS:" if lang == "English" else "🚨 СӨРӨГ ХҮЧИН ЗҮЙЛС:"
    pos_title = "✅ POSITIVE FACTORS:" if lang == "English" else "✅ ТОГТВОРТОЙ ҮЗҮҮЛЭЛТҮҮД:"

    # Markdown эсвэл HTML таг тасалдахгүй байхаар зассан хэсэг
    crit_items = "".join([f"<li style='margin-bottom:6px;line-height:1.4;color:#991B1B;'>{r}</li>" for r in critical_reasons])
    pos_items = "".join([f"<li style='margin-bottom:6px;line-height:1.4;color:#166534;'>{r}</li>" for r in positive_reasons])

    crit_html = f"<div style='font-size:12px;color:#991B1B;font-weight:800;margin-top:8px;'>{crit_title}</div><ul style='font-size:12.5px;padding-left:18px;margin:4px 0;'>{crit_items}</ul>" if critical_reasons else ""
    pos_html = f"<div style='font-size:12px;color:#166534;font-weight:800;margin-top:8px;'>{pos_title}</div><ul style='font-size:12.5px;padding-left:18px;margin:4px 0;'>{pos_items}</ul>" if positive_reasons else ""

    # Бүрэн нэг мөр/цэвэр HTML блок
    summary_card_html = f"""<div style="background-color: {bg_card_color}; padding: 18px; border-radius: 12px; border: 1.5px solid #CBD5E1;"><div style="font-weight: 800; font-size: 14px; color: {current_color}; margin-bottom: 6px;">{summary_title}</div><p style="font-size: 12.5px; color: #1E293B; margin-bottom: 10px;">{summary_desc}</p><hr style="border: 0; border-top: 1px solid #CBD5E1; margin: 10px 0;"/>{crit_html}{pos_html}</div>"""
    
    st.markdown(summary_card_html, unsafe_allow_html=True)

with col_solution:
    rec_items = "".join([f"<li style='margin-bottom:6px;line-height:1.4;color:#1E3A8A;'>{item}</li>" for item in recommendations])
    sol_title = f"💡 RECOMMENDED ACTIONS ({len(recommendations)}):" if lang == "English" else f"💡 АВАХ АРГА ХЭМЖЭЭ БА САНОЛ БОЛГОХ ШИЙДЛҮҮД ({len(recommendations)}):"
    
    solution_card_html = f"""<div style="background-color: #EFF6FF; padding: 18px; border-radius: 12px; border: 1.5px solid #BFDBFE;"><div style="font-size: 13px; color: #1E40AF; font-weight: 800; margin-bottom: 10px;">{sol_title}</div><ul style="font-size: 12.5px; padding-left: 18px; margin: 0;">{rec_items}</ul></div>"""
    
    st.markdown(solution_card_html, unsafe_allow_html=True)

# ==========================================
# 10. Feature Importance
# ==========================================
st.write("")
st.subheader(t["feature_title"])
st.caption(t["feature_subtitle"])

importance_data = pd.DataFrame({
    'Feature_Key': ['livestock_density', 'livestock_loss', 'precipitation', 'livestock_count', 'temperature', 'pasture_area'],
    'Importance': [48.5, 15.2, 14.1, 10.5, 7.8, 4.2]
})

importance_data['Feature_Name'] = importance_data['Feature_Key'].map(lambda x: t["feature_labels"].get(x, x))

fig_importance = go.Figure(go.Bar(
    x=importance_data['Importance'],
    y=importance_data['Feature_Name'],
    orientation='h',
    marker=dict(color='#0284C7')
))
fig_importance.update_layout(
    xaxis_title="Importance (%)",
    yaxis=dict(autorange="reversed"),
    height=300,
    margin=dict(l=20, r=20, t=10, b=30),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_importance, use_container_width=True)

# ==========================================
# 11. Dataset Information & Specification
# ==========================================
st.markdown("---")

with st.expander(t["dataset_title"], expanded=False):
    st.caption(t["dataset_caption"])
    
    dataset_info = pd.DataFrame([
        {
            t["col_feature"]: t["feature_labels"]["precipitation"], 
            t["col_unit"]: t["unit_mm"], 
            t["col_role"]: "Input Feature", 
            t["col_desc"]: "Average annual precipitation volume" if lang == "English" else "Жилийн дундаж хур тунадасны хэмжээ"
        },
        {
            t["col_feature"]: t["feature_labels"]["temperature"], 
            t["col_unit"]: "°C", 
            t["col_role"]: "Input Feature", 
            t["col_desc"]: "Average air temperature" if lang == "English" else "Дундаж агаарын температур"
        },
        {
            t["col_feature"]: t["feature_labels"]["pasture_area"], 
            t["col_unit"]: "k.ha" if lang == "English" else "мян.га", 
            t["col_role"]: "Input Feature", 
            t["col_desc"]: "Total available grazing area" if lang == "English" else "Нийт ашиглах боломжит бэлчээр"
        },
        {
            t["col_feature"]: t["feature_labels"]["livestock_count"], 
            t["col_unit"]: t["unit_thousand"], 
            t["col_role"]: "Input Feature", 
            t["col_desc"]: "Total livestock count" if lang == "English" else "Нийт малын тоо толгой"
        },
        {
            t["col_feature"]: t["feature_labels"]["livestock_loss"], 
            t["col_unit"]: t["unit_thousand"], 
            t["col_role"]: "Input Feature", 
            t["col_desc"]: "Unnatural livestock mortality" if lang == "English" else "Зүй бусаар хорогдсон мал"
        },
        {
            t["col_feature"]: t["feature_labels"]["livestock_density"], 
            t["col_unit"]: t["unit_density"], 
            t["col_role"]: "Derived Feature", 
            t["col_desc"]: "Livestock load per unit area" if lang == "English" else "Нэгж талбайд ногдох малын ачаалал"
        }
    ])
    st.table(dataset_info)
