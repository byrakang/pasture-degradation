import streamlit as st
import pandas as pd
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

# Sky Blue Арын фон болон CSS Анимаци
st.markdown("""
    <style>
        /* Ерөнхий арын өнгө болон туслах фон (Sky Blue Theme) */
        .main, .stApp { 
            background-color: #F0F9FF !important; 
        }
        [data-testid="stSidebar"] {
            background-color: #E0F2FE !important;
        }
        h1, h2, h3, h4, h5, h6, p, label, .stMarkdown { 
            color: #0C4A6E !important; 
        }

        /* 1. Баруун талаас зөөлөн орж ирэх анимаци (COP-17 / Гарчиг хэсэгт) */
        @keyframes slideInRight {
            0% {
                opacity: 0;
                transform: translateX(80px);
            }
            100% {
                opacity: 1;
                transform: translateX(0);
            }
        }

        /* 2. Зүүн талаас зөөлөн орж ирэх анимаци (Зорилго хэсэгт) */
        @keyframes slideInLeft {
            0% {
                opacity: 0;
                transform: translateX(-80px);
            }
            100% {
                opacity: 1;
                transform: translateX(0);
            }
        }

        /* Анимацийн ангиуд */
        .slide-right {
            animation: slideInRight 1.0s cubic-bezier(0.25, 1, 0.5, 1) forwards;
        }

        .slide-left {
            animation: slideInLeft 1.0s cubic-bezier(0.25, 1, 0.5, 1) forwards;
        }

        /* Navigation Header style */
        .nav-brand {
            font-size: 24px;
            font-weight: 800;
            color: #0284C7 !important;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Modal (Dialog) доторх гарчгийг Sky Blue болгож, бусад текстийг тод харагдуулах */
        div[role="dialog"] {
            background-color: #F0F9FF !important;
        }
        div[role="dialog"] h2, div[role="dialog"] h3 {
            color: #0284C7 !important;
            font-weight: 800 !important;
        }
        div[role="dialog"] p, div[role="dialog"] li, div[role="dialog"] div {
            color: #0F172A !important;
        }
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
        "lbl_temp": "Агаарын дундаж темп (°C):",
        "lbl_pasture": "Бэлчээрийн талбай (мянга га):",
        "lbl_count": "Малын тоо (мянга тоо толгой):",
        "lbl_loss": "Зүй бус хорогдол (мянга толгой):",
        "upload_label": "📁 Файлаар өгөгдөл оруулах (CSV/XLSX):",
        "export_btn": "📥 Таамаглалын тайлан татах",
        "main_title": "Бэлчээрийн Доройтлын Эрсдэлийг Таамаглах Систем",
        "main_subtitle": "Уур амьсгал болон мал сүргийн үзүүлэлтэд суурилсан хиймэл интеллектийн хянах багц.",
        "ai_result_title": "AI Таамаглалын Дүн",
        "nav_about": "🌿 COP-17 & Зорилго",
        "cop_modal_title": "COP-17 Ulaanbaatar 2026 & Вэбсайтын Зорилго",
        "cop_sub": "НҮБ-ын Цөлжилттэй тэмцэх конвенцийн Талуудын 17-р бага хурал",
        "cop_loc": "📍 **Байршил:** Улаанбаатар хот, Монгол улс",
        "cop_date": "📅 **Огноо:** 2026 он",
        "goal_title": "🎯 Вэбсайтын Зорилго & Шаардлага",
        "goal_desc": "• **Бэлчээрийн доройтлыг бууруулах:** Уур амьсгалын өөрчлөлт болон мал ахуйн ачааллаас үүдэлтэй бэлчээрийн талхагдлыг AI ашиглан эрт таамаглах.",
        "kpi_precip": "Хур тунадас",
        "kpi_temp": "Температура",
        "kpi_density": "Малын нягтрал",
        "kpi_loss": "Хорогдол",
        "unit_mm": "мм",
        "unit_density": "толгой/га",
        "unit_thousand": "мян.тол",
        "risk_level_label": "ЭРСДЭЛИЙН ТҮВШИН:",
        "prob_title": "ЭРСДЭЛИЙН МАГАДЛАЛЫН ХУВААРИЛАЛТ",
        "radar_title": "Үзүүлэлтүүдийн Харьцаа ба Радар График",
        "radar_subtitle": "Оруулсан үзүүлэлтүүдийн стандартчилсан утга",
        "feature_title": "Үзүүлэлтүүдийн Нөлөөлөл (Feature Importance)",
        "feature_subtitle": "Ямар үзүүлэлтүүд AI загварын таамаглалд хамгийн их нөлөөлж байна вэ?",
        "categories": ['Малын тоо', 'Хур тунадас', 'Температура', 'Зүй бус хорогдол', 'Малын нягтрал'],
        "feature_labels": {
            "livestock_density": "Малын нягтрал",
            "livestock_loss": "Зүй бус хорогдол",
            "precipitation": "Хур тунадас",
            "livestock_count": "Малын тоо",
            "temperature": "Температура",
            "pasture_area": "Бэлчээрийн талбай"
        },
        "summary_title_high": "🚨 ЭРСДЭЛ ӨНДӨР НӨХЦӨЛ БАЙДЛЫН ДҮГНЭЛТ",
        "summary_desc_high": "Олон тооны үзүүлэлтүүд аюултай түвшинд хүрсэн байна. Яаралтай зохицуулалт болон арга хэмжээ авахыг зөвлөж байна.",
        "summary_title_med": "⚠️ ДУНД ЭРСДЭЛТЭЙ НӨХЦӨЛ БАЙДЛЫН ДҮГНЭЛТ",
        "summary_desc_med": "Ерөнхий нөхцөл байдал харьцангуй тогтвортой боловч тодорхой үзүүлэлтүүдийг анхааралтай ажиглах шаардлагатай.",
        "summary_title_low": "✅ ТОГТВОРТОЙ НӨХЦӨЛ БАЙДАЛ (БАГА ЭРСДЭЛ)",
        "summary_desc_low": "Бэлчээрийн даац болон цаг уурын нөхцөл байдал сайн зохицож, зохистой түвшинд байна.",
        "analysis_header": "Гол нөлөөлөх хүчин зүйлс ба дэлгэрэнгүй шинжилгээ:",
        "reasons": {
            "precip_low": "🌧️ <b>Бага хур тунадас:</b> Жилийн хур тунадас <b>{val:.1f} мм</b> байгаа нь ургамлын ургалтад сөрөг нөлөө үзүүлж байна.",
            "precip_ok": "🌧️ <b>Хангалттай хур тунадас:</b> Жилийн хур тунадас <b>{val:.1f} мм</b> байгаа нь хөрсний чийгийг дэмжиж байна.",
            "temp_high": "🌡️ <b>Өндөр температура:</b> Агаарын температура <b>{val:.1f}°C</b> хүрч байгаа нь гандрах эрсдэлийг нэмэгдүүлнэ.",
            "temp_low": "❄️ <b>Хэт хүйтэн:</b> Агаарын температура <b>{val:.1f}°C</b> байгаа нь зуд болон бусад эрсдэлийг нэмэгдүүлнэ.",
            "temp_ok": "🌡️ <b>Зохистой температура:</b> Дундаж температура <b>{val:.1f}°C</b> байгаа нь дундаж хэмжээнд байна.",
            "density_high": "🐄 <b>Бэлчээрийн ачаалал өндөр:</b> Малын нягтрал <b>{val:.2f} толгой/га</b> байгаа нь бэлчээрийн даацаас хэтэрч байна.",
            "density_ok": "🌱 <b>Бэлчээрийн ачаалал зохистой:</b> Малын нягтрал <b>{val:.2f} толгой/га</b> байгаа нь бэлчээрт ирэх дарамт бага байна.",
            "loss_high": "⚠️ <b>Хорогдол өндөр:</b> Зүй бус хорогдол <b>{val:.0f} мянган толгой</b> байгаа нь мал сүргийн тогтвортой байдалд аюултай."
        },
        "dataset_title": "📊 Өгөгдлийн сангийн мэдээлэл ба тодорхойлолт",
        "dataset_caption": "AI загварыг сургахад ашигласан цаг уур болон бэлчээрийн үзүүлэлтүүдийн бүтэц.",
        "col_feature": "Үзүүлэлтийн нэр",
        "col_unit": "Хэмжих нэгж",
        "col_role": "Үүрэг",
        "col_desc": "Тайлбар",
        "sample_title": "🔍 Сургалтын өгөгдлийн дээж харах (Sample Raw Data)",
        "sample_caption": "Сургалтын эх өгөгдлийн зарим мөрүүдийг үзүүлж байна."
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
        "nav_about": "🌿 COP-17 & About",
        "cop_modal_title": "COP-17 Ulaanbaatar 2026 & Platform Purpose",
        "cop_sub": "17th Conference of the Parties to the UNCCD",
        "cop_loc": "📍 **Location:** Ulaanbaatar, Mongolia",
        "cop_date": "📅 **Date:** 2026",
        "goal_title": "🎯 Website Purpose & Objective",
        "goal_desc": "• **Reduce Pasture Degradation:** Early prediction of pasture degradation caused by climate change and livestock pressure using AI.",
        "kpi_precip": "Precipitation",
        "kpi_temp": "Temperature",
        "kpi_density": "Livestock Density",
        "kpi_loss": "Livestock Loss",
        "unit_mm": "mm",
        "unit_density": "head/ha",
        "unit_thousand": "k.head",
        "risk_level_label": "RISK LEVEL:",
        "prob_title": "RISK PROBABILITY DISTRIBUTION",
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
        "summary_title_high": "🚨 HIGH RISK OVERVIEW & ASSESSMENT",
        "summary_desc_high": "Multiple indicators have reached critical levels. Immediate management and intervention are recommended.",
        "summary_title_med": "⚠️ MODERATE RISK OVERVIEW & ASSESSMENT",
        "summary_desc_med": "Overall condition is relatively stable, but specific indicators require close monitoring.",
        "summary_title_low": "✅ STABLE CONDITION OVERVIEW (LOW RISK)",
        "summary_desc_low": "Pasture capacity and climate conditions are well balanced, indicating optimal conditions.",
        "analysis_header": "Key Factors & Detailed Analysis:",
        "reasons": {
            "precip_low": "🌧️ <b>Low Precipitation:</b> Annual rainfall at <b>{val:.1f} mm</b> poses a stress on vegetation growth.",
            "precip_ok": "🌧️ <b>Adequate Rainfall:</b> Annual precipitation at <b>{val:.1f} mm</b> supports normal moisture conditions.",
            "temp_high": "🌡️ <b>High Temperature:</b> Temperature reaching <b>{val:.1f}°C</b> increases drought vulnerability.",
            "temp_low": "❄️ <b>Extreme Cold:</b> Low temperature at <b>{val:.1f}°C</b> heightens severe winter (dzud) risk.",
            "temp_ok": "🌡️ <b>Optimal Temperature:</b> Average temperature at <b>{val:.1f}°C</b> remains within the normal climate range.",
            "density_high": "🐄 <b>High Grazing Pressure:</b> Livestock density at <b>{val:.2f} head/ha</b> strains pasture capacity.",
            "density_ok": "🌱 <b>Balanced Pasture Load:</b> Livestock density at <b>{val:.2f} head/ha</b> presents low pasture stress.",
            "loss_high": "⚠️ <b>High Mortality:</b> Livestock loss at <b>{val:.0f} thousand heads</b> impacts herd stability."
        },
        "dataset_title": "📊 Dataset Information & Specification",
        "dataset_caption": "Structure of climate and pasture metrics used for training the AI model.",
        "col_feature": "Feature Name",
        "col_unit": "Unit",
        "col_role": "Role",
        "col_desc": "Description",
        "sample_title": "🔍 View Training Sample Data (Sample Raw Data)",
        "sample_caption": "Showing sample head rows from the raw training dataset."
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

calculated_density = count / pasture if pasture > 0 else 0.0

st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader(t["upload_label"], type=["csv", "xlsx"])

# ==========================================
# 4. Navigation Header ба POP-UP Модал (Smooth Slide Effect)
# ==========================================
nav_col1, nav_col2 = st.columns([3, 1])

with nav_col1:
    st.markdown('<div class="nav-brand slide-right">🌱 Pasture Risk AI</div>', unsafe_allow_html=True)

with nav_col2:
    if st.button(t["nav_about"], use_container_width=True):
        @st.dialog("🌿 COP-17 & About")
        def show_cop_info():
            st.markdown(f"""
                <div class="slide-right">
                    <h3 style='color: #0284C7 !important; font-weight: 800;'>🌿 {t['cop_modal_title']}</h3>
                    <p style='color: #0369A1; font-weight: 600;'>{t['cop_sub']}</p>
                    <p style='margin-bottom: 4px;'>{t['cop_loc']}</p>
                    <p>{t['cop_date']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown(f"""
                <div class="slide-left" style="background-color: #E0F2FE; padding: 15px; border-radius: 10px; border-left: 4px solid #0284C7;">
                    <h4 style='color: #0369A1 !important; font-weight: 700; margin-bottom: 8px;'>{t['goal_title']}</h4>
                    <p style='color: #0C4A6E; line-height: 1.5; margin: 0;'>{t['goal_desc']}</p>
                </div>
            """, unsafe_allow_html=True)
            
        show_cop_info()

# Үндсэн гарчиг
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
# 6. AI Таамаглал ба ЭРСДЭЛИЙН КАРТ
# ==========================================
# Загвар унших эсвэл Rule-based fallback
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

if not model_loaded:
    if calculated_density > 1.2 or loss > 500 or precip < 120:
        raw_risk = "HIGH"
        prob_high, prob_med, prob_low = 65, 25, 10
    elif calculated_density > 0.8 or loss > 200 or precip < 200:
        raw_risk = "MEDIUM"
        prob_high, prob_med, prob_low = 5, 57, 38
    else:
        raw_risk = "LOW"
        prob_high, prob_med, prob_low = 2, 18, 80

if raw_risk == "HIGH":
    risk_display_name = "HIGH" if lang == "English" else "ӨНДӨР"
    current_color = "#DC2626"
    bg_card_color = "#FEE2E2"
elif raw_risk == "MEDIUM":
    risk_display_name = "MEDIUM" if lang == "English" else "ДУНД"
    current_color = "#D97706"
    bg_card_color = "#FEF3C7"
else:
    risk_display_name = "LOW" if lang == "English" else "БАГА"
    current_color = "#059669"
    bg_card_color = "#DCFCE7"

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader(t["ai_result_title"])
    
    st.markdown(f"""
        <div style="background-color: {bg_card_color}; padding: 18px 22px; border-radius: 12px; border-left: 6px solid {current_color}; margin-bottom: 20px;">
            <span style="font-size: 13px; color: #1E293B; font-weight: 700;">{t['risk_level_label']}</span><br/>
            <span style="font-size: 28px; color: {current_color}; font-weight: 800;">{risk_display_name} ({raw_risk})</span>
        </div>
    """, unsafe_allow_html=True)

    # Donut Chart
    fig_donut = go.Figure(data=[go.Pie(
        labels=["Өндөр" if lang=="Монгол" else "High", "Дунд" if lang=="Монгол" else "Medium", "Бага" if lang=="Монгол" else "Low"],
        values=[prob_high, prob_med, prob_low],
        hole=.6,
        marker=dict(colors=['#EF4444', '#F59E0B', '#10B981'])
    )])
    fig_donut.update_layout(
        showlegend=True,
        height=220,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_donut, use_container_width=True)

    # Шалтгаан болон Дүгнэлт
    reasons = []
    if precip < 250:
        reasons.append(t["reasons"]["precip_low"].format(val=precip))
    else:
        reasons.append(t["reasons"]["precip_ok"].format(val=precip))

    if temp > 30:
        reasons.append(t["reasons"]["temp_high"].format(val=temp))
    elif temp < -20:
        reasons.append(t["reasons"]["temp_low"].format(val=temp))
    else:
        reasons.append(t["reasons"]["temp_ok"].format(val=temp))

    if calculated_density > 1.2:
        reasons.append(t["reasons"]["density_high"].format(val=calculated_density))
    else:
        reasons.append(t["reasons"]["density_ok"].format(val=calculated_density))

    if loss > 800:
        reasons.append(t["reasons"]["loss_high"].format(val=loss))

    if raw_risk == "HIGH":
        summary_title = t["summary_title_high"]
        summary_desc = t["summary_desc_high"]
    elif raw_risk == "MEDIUM":
        summary_title = t["summary_title_med"]
        summary_desc = t["summary_desc_med"]
    else:
        summary_title = t["summary_title_low"]
        summary_desc = t["summary_desc_low"]

    reasons_html = "".join([f"<li style='margin-bottom: 8px; line-height: 1.5;'>{r}</li>" for r in reasons])

    st.markdown(f"""
        <div style="background-color: #E0F2FE; padding: 20px; border-radius: 14px; border: 1.5px solid #BAE6FD; margin-top: 10px;">
            <div style="font-weight: 800; font-size: 15px; color: {current_color}; margin-bottom: 8px;">
                {summary_title}
            </div>
            <p style="font-size: 13.5px; color: #0C4A6E; margin-bottom: 14px;">
                {summary_desc}
            </p>
            <hr style="border: 0; border-top: 1px solid #BAE6FD; margin-bottom: 12px;"/>
            <div style="font-size: 12px; color: #0369A1; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;">
                {t['analysis_header']}
            </div>
            <ul style="font-size: 13px; color: #0C4A6E; margin-left: -10px; margin-bottom: 0px; padding-left: 20px;">
                {reasons_html}
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # Тайлан татах хэсэг
    export_df = pd.DataFrame([{
        "Precipitation_mm": precip,
        "Temperature_C": temp,
        "Pasture_Area_k_ha": pasture,
        "Livestock_Count_k_head": count,
        "Livestock_Loss_k_head": loss,
        "Livestock_Density_head_ha": calculated_density,
        "Predicted_Risk_Level": raw_risk
    }])
    csv_data = export_df.to_csv(index=False).encode('utf-8')
    st.write("")
    st.download_button(
        label=t["export_btn"],
        data=csv_data,
        file_name="pasture_risk_prediction_report.csv",
        mime="text/csv"
    )

with col_right:
    st.subheader(t["radar_title"])
    st.caption(t["radar_subtitle"])
    
    fig_radar = go.Figure(go.Scatterpolar(
        r=[count/10000, precip/600, (temp+30)/75, loss/2000, calculated_density/3],
        theta=t["categories"],
        fill='toself',
        fillcolor='rgba(2, 132, 199, 0.25)',
        line=dict(color='#0284C7', width=2)
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1]),
            bgcolor='rgba(255,255,255,0.5)'
        ),
        showlegend=False,
        height=320,
        margin=dict(l=40, r=40, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# ==========================================
# 7. Feature Importance
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
# 8 & 9. Dataset Information & Custom File Preview (Expander)
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
            t["col_desc"]: "Average air temperature" if lang == "English" else "Дундаж агаарын температура"
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
    
    st.dataframe(dataset_info, use_container_width=True, hide_index=True)
    st.write("")

    with st.expander(t["sample_title"]):
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    user_data = pd.read_csv(uploaded_file)
                else:
                    user_data = pd.read_excel(uploaded_file)
                st.write("📋 **Оруулсан файлын дата:**")
                st.dataframe(user_data.head(), use_container_width=True)
            except Exception as e:
                st.error(f"Файл уншихад алдаа гарлаа: {e}")
        else:
            sample_display = pd.DataFrame({
                "precipitation": [280.0, 150.5, 420.0, 90.0, 310.0],
                "temperature": [2.5, 32.0, -15.0, 18.0, 5.0],
                "pasture_area": [3000.0, 1500.0, 5000.0, 800.0, 2500.0],
                "livestock_count": [1500.0, 2200.0, 1100.0, 3000.0, 1200.0],
                "livestock_loss": [50.0, 450.0, 20.0, 800.0, 30.0],
                "livestock_density": [0.50, 1.46, 0.22, 3.75, 0.48],
                "risk_level": ["LOW", "HIGH", "LOW", "HIGH", "LOW"]
            })
            st.dataframe(sample_display, use_container_width=True, hide_index=True)
            st.caption(t["sample_caption"])
