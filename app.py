import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="FraudShield AI | Banking Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --navy:      #050d1a;
    --blue-mid:  #0e4d8f;
    --blue-acc:  #1e7de0;
    --cyan:      #00d4ff;
    --green:     #00e676;
    --orange:    #ff9f43;
    --red:       #ff4757;
    --text-1:    #e8f0fe;
    --text-2:    #8ba3c7;
    --text-3:    #4a6080;
    --border:    rgba(30,125,224,0.18);
}

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-1) !important;
}

.stApp {
    background: linear-gradient(135deg, #020810 0%, #050d1a 50%, #060f1e 100%) !important;
    background-attachment: fixed !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020810 0%, #060f1e 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-1) !important; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.kpi-card {
    background: linear-gradient(135deg, rgba(14,32,64,0.85), rgba(10,22,40,0.95));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.2rem 1.3rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 16px 16px 0 0;
}
.kpi-card.blue::before   { background: linear-gradient(90deg, var(--blue-acc), var(--cyan)); }
.kpi-card.green::before  { background: linear-gradient(90deg, var(--green), #00bcd4); }
.kpi-card.red::before    { background: linear-gradient(90deg, var(--red), #ff6b81); }
.kpi-card.orange::before { background: linear-gradient(90deg, var(--orange), #ffd32a); }
.kpi-card.purple::before { background: linear-gradient(90deg, #a29bfe, #6c5ce7); }
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.6);
}
.kpi-icon  { font-size: 1.5rem; margin-bottom: 0.4rem; }
.kpi-label { font-size: 0.68rem; color: var(--text-2); text-transform: uppercase; letter-spacing: 0.08em; font-weight: 500; }
.kpi-value { font-size: 1.65rem; font-weight: 700; color: var(--text-1); line-height: 1.1; margin: 0.1rem 0; }
.kpi-sub   { font-size: 0.7rem; color: var(--text-3); margin-top: 0.2rem; }

.panel-title {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-2);
    font-weight: 600;
    margin-bottom: 1.25rem;
}

.result-banner {
    border-radius: 16px;
    padding: 1.4rem 1.75rem;
    display: flex;
    align-items: center;
    gap: 1.25rem;
    margin: 1rem 0;
    border: 1px solid;
    animation: fadeUp 0.4s ease;
}
.result-banner.legit { background: rgba(0,230,118,0.1);  border-color: rgba(0,230,118,0.3); }
.result-banner.fraud { background: rgba(255,71,87,0.12); border-color: rgba(255,71,87,0.35); }
.result-emoji    { font-size: 2.2rem; }
.result-title    { font-size: 1.2rem; font-weight: 700; }
.result-subtitle { font-size: 0.8rem; color: var(--text-2); margin-top: 0.15rem; }

.risk-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.3rem 0.85rem;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-left: auto;
}
.risk-badge.low    { background: rgba(0,230,118,0.18);  color: var(--green);  border: 1px solid rgba(0,230,118,0.35); }
.risk-badge.medium { background: rgba(255,159,67,0.18); color: var(--orange); border: 1px solid rgba(255,159,67,0.35); }
.risk-badge.high   { background: rgba(255,71,87,0.18);  color: var(--red);    border: 1px solid rgba(255,71,87,0.35); }

.prob-bar-wrap {
    background: rgba(14,32,64,0.6);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin: 0.75rem 0;
}
.prob-label { font-size: 0.72rem; color: var(--text-2); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem; }
.prob-value { font-size: 2rem; font-weight: 700; margin-bottom: 0.6rem; }
.prob-track {
    height: 8px;
    background: rgba(255,255,255,0.06);
    border-radius: 4px;
    overflow: hidden;
}
.prob-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.6s ease;
}

.alert-card {
    display: flex;
    align-items: flex-start;
    gap: 0.7rem;
    padding: 0.85rem 1rem;
    border-radius: 12px;
    margin-bottom: 0.55rem;
    border-left: 3px solid;
    transition: transform 0.2s ease;
}
.alert-card:hover { transform: translateX(4px); }
.alert-card.danger  { background: rgba(255,71,87,0.1);  border-color: var(--red); }
.alert-card.warning { background: rgba(255,159,67,0.1); border-color: var(--orange); }
.alert-card.success { background: rgba(0,230,118,0.1);  border-color: var(--green); }
.alert-title { font-size: 0.83rem; font-weight: 600; }
.alert-body  { font-size: 0.75rem; color: var(--text-2); margin-top: 0.12rem; }

.sb-logo {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 1.2rem 1rem 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}
.sb-icon {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, var(--blue-acc), var(--cyan));
    border-radius: 11px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
}
.sb-name { font-size: 0.95rem; font-weight: 700; }
.sb-sub  { font-size: 0.62rem; color: var(--text-3) !important; text-transform: uppercase; letter-spacing: 0.08em; }

@keyframes fadeUp { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }

.sec-head { font-size: 1.55rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 0.2rem; }
.sec-sub  { font-size: 0.82rem; color: var(--text-2); margin-bottom: 1.4rem; }

.stButton > button {
    background: linear-gradient(135deg, var(--blue-mid), var(--blue-acc)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    padding: 0.6rem 1.5rem !important;
    box-shadow: 0 4px 20px rgba(30,125,224,0.35) !important;
    transition: all 0.25s ease !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(30,125,224,0.55) !important;
    background: linear-gradient(135deg, var(--blue-acc), var(--cyan)) !important;
}

.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: rgba(10,22,40,0.9) !important;
    border-color: var(--border) !important;
    color: var(--text-1) !important;
    border-radius: 10px !important;
}

hr { border-color: var(--border) !important; margin: 1.25rem 0 !important; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: #0f2040; border-radius: 3px; }

.stRadio label {
    background: rgba(14,32,64,0.4) !important;
    border: 1px solid rgba(30,125,224,0.12) !important;
    border-radius: 10px !important;
    padding: 0.5rem 0.85rem !important;
    transition: all 0.2s ease !important;
    font-size: 0.84rem !important;
    color: var(--text-2) !important;
}
.stRadio label:hover {
    border-color: rgba(30,125,224,0.4) !important;
    color: var(--text-1) !important;
    background: rgba(14,77,143,0.25) !important;
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_artifacts():
    model         = joblib.load("models/fraud_detection_xgboost.pkl")
    scaler        = joblib.load("models/scaler.pkl")
    feature_names = joblib.load("models/feature_name.pkl")
    return model, scaler, feature_names

model, scaler, feature_names = load_artifacts()


with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-icon">🛡️</div>
        <div>
            <div class="sb-name">FraudShield AI</div>
            <div class="sb-sub">Banking Security</div>
        </div>
    </div>""", unsafe_allow_html=True)

    page = st.radio("", [
        "🔍  Transaction Analysis",
        "ℹ️  About"
    ], label_visibility="collapsed")

page = page.split("  ")[1].strip()


if page == "Transaction Analysis":

    st.markdown('<div class="sec-head">🔍 Transaction Fraud Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Enter transaction details below and run the XGBoost model to detect fraud</div>', unsafe_allow_html=True)

    with st.form("fraud_form"):
        st.markdown('<div class="panel-title">📋 Transaction Details</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            amount = st.number_input(
                "💰 Transaction Amount ($)",
                min_value=0.0, max_value=100000.0, value=100.0, step=0.01
            )
            transaction_hour = st.slider(
                "🕐 Transaction Hour (0 – 23)",
                min_value=0, max_value=23, value=12
            )
            foreign_transaction = st.selectbox(
                "🌍 Foreign Transaction",
                options=[0, 1],
                format_func=lambda x: "Yes (1)" if x == 1 else "No (0)"
            )
            location_mismatch = st.selectbox(
                "📍 Location Mismatch",
                options=[0, 1],
                format_func=lambda x: "Yes (1)" if x == 1 else "No (0)"
            )

        with col2:
            device_trust_score = st.slider(
                "📱 Device Trust Score (0.0 – 1.0)",
                min_value=0.0, max_value=1.0, value=0.5, step=0.01
            )
            velocity_last_24h = st.number_input(
                "⚡ Transactions in Last 24 Hours",
                min_value=0, max_value=100, value=1
            )
            cardholder_age = st.number_input(
                "👤 Cardholder Age",
                min_value=18, max_value=100, value=30
            )
            merchant_category = st.selectbox(
                "🏪 Merchant Category",
                ["Electronics", "Food", "Grocery", "Travel"]
            )

        submitted = st.form_submit_button("🔮  ANALYSE TRANSACTION", use_container_width=True)

    if submitted:
        electronics = 1 if merchant_category == "Electronics" else 0
        food        = 1 if merchant_category == "Food"        else 0
        grocery     = 1 if merchant_category == "Grocery"     else 0
        travel      = 1 if merchant_category == "Travel"      else 0

        input_data = pd.DataFrame([{
            "amount":                        amount,
            "transaction_hour":              transaction_hour,
            "foreign_transaction":           foreign_transaction,
            "location_mismatch":             location_mismatch,
            "device_trust_score":            device_trust_score,
            "velocity_last_24h":             velocity_last_24h,
            "cardholder_age":                cardholder_age,
            "merchant_category_Electronics": electronics,
            "merchant_category_Food":        food,
            "merchant_category_Grocery":     grocery,
            "merchant_category_Travel":      travel,
        }])

        input_data   = input_data[feature_names]
        input_scaled = scaler.transform(input_data)

        prediction  = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1]
        prob_pct    = probability * 100

        if prob_pct < 30:
            risk_label, risk_cls = "LOW RISK",    "low"
        elif prob_pct < 70:
            risk_label, risk_cls = "MEDIUM RISK", "medium"
        else:
            risk_label, risk_cls = "HIGH RISK",   "high"

        is_fraud     = prediction == 1
        banner_cls   = "fraud" if is_fraud else "legit"
        verdict_text = "🚨 FRAUD DETECTED" if is_fraud else "✅ LEGITIMATE TRANSACTION"
        verdict_sub  = (f"This transaction was flagged with {prob_pct:.1f}% fraud probability."
                        if is_fraud
                        else f"Transaction appears legitimate — fraud probability {prob_pct:.1f}%.")

        st.markdown(f"""
        <div class="result-banner {banner_cls}">
            <div class="result-emoji">{"🚨" if is_fraud else "✅"}</div>
            <div>
                <div class="result-title">{verdict_text}</div>
                <div class="result-subtitle">{verdict_sub}</div>
            </div>
            <span class="risk-badge {risk_cls}">{risk_label}</span>
        </div>""", unsafe_allow_html=True)

        bar_color = ("#ff4757" if prob_pct >= 70
                     else "#ff9f43" if prob_pct >= 30
                     else "#00e676")

        st.markdown(f"""
        <div class="prob-bar-wrap">
            <div class="prob-label">Fraud Probability</div>
            <div class="prob-value" style="color:{bar_color};">{prob_pct:.1f}%</div>
            <div class="prob-track">
                <div class="prob-fill" style="width:{prob_pct:.1f}%;background:{bar_color};"></div>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="panel-title">🧠 Explainable AI — Risk Factors</div>', unsafe_allow_html=True)

        reasons = []

        if location_mismatch == 1:
            reasons.append(("danger",  "📍 Location Mismatch Detected",
                             "Transaction origin does not match the cardholder's registered region."))
        if foreign_transaction == 1:
            reasons.append(("warning", "🌍 Foreign Transaction",
                             "Transaction originated outside the cardholder's home country."))
        if device_trust_score < 0.30:
            reasons.append(("danger",  "📱 Low Device Trust Score",
                             f"Score of {device_trust_score:.2f} is well below the 0.30 safety threshold."))
        if transaction_hour < 5:
            reasons.append(("warning", "🕐 Unusual Transaction Hour",
                             f"Transactions at {transaction_hour}:00 are associated with elevated fraud rates."))
        if velocity_last_24h > 10:
            reasons.append(("warning", "⚡ High Transaction Velocity",
                             f"{velocity_last_24h} transactions in 24 hours — significantly above normal."))
        if amount > 5000:
            reasons.append(("warning", "💰 High Transaction Amount",
                             f"${amount:,.2f} is above the high-risk amount threshold."))
        if merchant_category in ["Electronics", "Travel"]:
            reasons.append(("warning", f"🏪 Elevated-Risk Category: {merchant_category}",
                             "This merchant category shows higher-than-average fraud incidence."))

        if reasons:
            for severity, title, body in reasons:
                st.markdown(f"""
                <div class="alert-card {severity}">
                    <div>
                        <div class="alert-title">{title}</div>
                        <div class="alert-body">{body}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-card success">
                <div>
                    <div class="alert-title">✅ No Significant Risk Factors Detected</div>
                    <div class="alert-body">This transaction matches the behavioural profile of legitimate activity.</div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="panel-title">📋 Input Summary</div>', unsafe_allow_html=True)

        kpi_html  = '<div class="kpi-grid">'
        kpi_html += f'<div class="kpi-card blue"><div class="kpi-icon">💰</div><div class="kpi-label">Amount</div><div class="kpi-value">${amount:,.2f}</div></div>'
        kpi_html += f'<div class="kpi-card {"red" if prob_pct >= 70 else "orange" if prob_pct >= 30 else "green"}"><div class="kpi-icon">🎯</div><div class="kpi-label">Fraud Prob</div><div class="kpi-value">{prob_pct:.1f}%</div></div>'
        kpi_html += f'<div class="kpi-card purple"><div class="kpi-icon">🕐</div><div class="kpi-label">Hour</div><div class="kpi-value">{transaction_hour}:00</div></div>'
        kpi_html += f'<div class="kpi-card {"red" if device_trust_score < 0.3 else "green"}"><div class="kpi-icon">📱</div><div class="kpi-label">Device Trust</div><div class="kpi-value">{device_trust_score:.2f}</div></div>'
        kpi_html += f'<div class="kpi-card {"orange" if velocity_last_24h > 10 else "blue"}"><div class="kpi-icon">⚡</div><div class="kpi-label">Velocity 24h</div><div class="kpi-value">{velocity_last_24h}</div></div>'
        kpi_html += '</div>'
        st.markdown(kpi_html, unsafe_allow_html=True)


elif page == "About":

    st.markdown('<div class="sec-head">ℹ️ About This Project</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Model details, features, and technology stack</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(14,32,64,0.7),rgba(10,22,40,0.85));
                    border:1px solid var(--border);border-radius:16px;padding:1.5rem;margin-bottom:1rem;">
            <div class="panel-title">🎯 Project Overview</div>
            <div style="font-size:0.84rem;color:var(--text-2);line-height:1.75;">
                <b style="color:var(--text-1);">FraudShield AI</b> uses a trained XGBoost model to
                classify banking transactions as fraudulent or legitimate in real time.
                <br><br>
                The model was trained on labelled transaction data with behavioural,
                contextual, and temporal features.
                <br><br>
                Predictions are accompanied by explainable AI risk factors so analysts
                understand <i>why</i> a transaction was flagged, not just <i>that</i> it was.
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(14,32,64,0.7),rgba(10,22,40,0.85));
                    border:1px solid var(--border);border-radius:16px;padding:1.5rem;">
            <div class="panel-title">💻 Technology Stack</div>
            <div style="display:flex;flex-wrap:wrap;gap:0.5rem;margin-top:0.25rem;">
                <span style="background:rgba(14,77,143,0.35);border:1px solid rgba(30,125,224,0.3);
                             border-radius:8px;padding:0.3rem 0.75rem;font-size:0.74rem;
                             font-weight:600;color:#2b9af3;font-family:'JetBrains Mono',monospace;">Python</span>
                <span style="background:rgba(14,77,143,0.35);border:1px solid rgba(30,125,224,0.3);
                             border-radius:8px;padding:0.3rem 0.75rem;font-size:0.74rem;
                             font-weight:600;color:#2b9af3;font-family:'JetBrains Mono',monospace;">Streamlit</span>
                <span style="background:rgba(14,77,143,0.35);border:1px solid rgba(30,125,224,0.3);
                             border-radius:8px;padding:0.3rem 0.75rem;font-size:0.74rem;
                             font-weight:600;color:#2b9af3;font-family:'JetBrains Mono',monospace;">XGBoost</span>
                <span style="background:rgba(14,77,143,0.35);border:1px solid rgba(30,125,224,0.3);
                             border-radius:8px;padding:0.3rem 0.75rem;font-size:0.74rem;
                             font-weight:600;color:#2b9af3;font-family:'JetBrains Mono',monospace;">scikit-learn</span>
                <span style="background:rgba(14,77,143,0.35);border:1px solid rgba(30,125,224,0.3);
                             border-radius:8px;padding:0.3rem 0.75rem;font-size:0.74rem;
                             font-weight:600;color:#2b9af3;font-family:'JetBrains Mono',monospace;">Pandas</span>
                <span style="background:rgba(14,77,143,0.35);border:1px solid rgba(30,125,224,0.3);
                             border-radius:8px;padding:0.3rem 0.75rem;font-size:0.74rem;
                             font-weight:600;color:#2b9af3;font-family:'JetBrains Mono',monospace;">joblib</span>
            </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(14,32,64,0.7),rgba(10,22,40,0.85));
                    border:1px solid var(--border);border-radius:16px;padding:1.5rem;">
            <div class="panel-title">📦 Model Features (11 inputs)</div>
            <div style="display:flex;flex-direction:column;gap:0.4rem;font-size:0.8rem;">
                <div style="background:rgba(14,77,143,0.2);border:1px solid var(--border);border-radius:8px;
                             padding:0.45rem 0.8rem;color:var(--text-2);">
                    <b style="color:var(--text-1);">amount</b> — Transaction value in USD
                </div>
                <div style="background:rgba(14,77,143,0.2);border:1px solid var(--border);border-radius:8px;
                             padding:0.45rem 0.8rem;color:var(--text-2);">
                    <b style="color:var(--text-1);">transaction_hour</b> — Hour of day (0–23)
                </div>
                <div style="background:rgba(14,77,143,0.2);border:1px solid var(--border);border-radius:8px;
                             padding:0.45rem 0.8rem;color:var(--text-2);">
                    <b style="color:var(--text-1);">foreign_transaction</b> — 0 / 1 binary flag
                </div>
                <div style="background:rgba(14,77,143,0.2);border:1px solid var(--border);border-radius:8px;
                             padding:0.45rem 0.8rem;color:var(--text-2);">
                    <b style="color:var(--text-1);">location_mismatch</b> — 0 / 1 binary flag
                </div>
                <div style="background:rgba(14,77,143,0.2);border:1px solid var(--border);border-radius:8px;
                             padding:0.45rem 0.8rem;color:var(--text-2);">
                    <b style="color:var(--text-1);">device_trust_score</b> — Float 0.0 → 1.0
                </div>
                <div style="background:rgba(14,77,143,0.2);border:1px solid var(--border);border-radius:8px;
                             padding:0.45rem 0.8rem;color:var(--text-2);">
                    <b style="color:var(--text-1);">velocity_last_24h</b> — Transaction count
                </div>
                <div style="background:rgba(14,77,143,0.2);border:1px solid var(--border);border-radius:8px;
                             padding:0.45rem 0.8rem;color:var(--text-2);">
                    <b style="color:var(--text-1);">cardholder_age</b> — Age (18–100)
                </div>
                <div style="background:rgba(14,77,143,0.2);border:1px solid var(--border);border-radius:8px;
                             padding:0.45rem 0.8rem;color:var(--text-2);">
                    <b style="color:var(--text-1);">merchant_category_*</b> — One-hot (4 columns)
                </div>
            </div>
        </div>""", unsafe_allow_html=True)