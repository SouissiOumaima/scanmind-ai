import requests
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="ScanMind AI — Brain Tumor Detection",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Figtree:wght@300;400;500;600&display=swap');

            :root {
                --bg:        #f4f7fb;
                --surface:   #ffffff;
                --surface2:  #f0f4f9;
                --border:    #dce4ef;
                --border2:   #b8cce4;
                --accent:    #1a56db;
                --accent2:   #0891b2;
                --text:      #0f172a;
                --muted:     #64748b;
                --ok:        #059669;
                --warn:      #d97706;
                --danger:    #dc2626;
            }

            html, body, [class*="st-"], .stApp {
                background-color: var(--bg) !important;
                color: var(--text) !important;
                font-family: 'Figtree', sans-serif !important;
            }

            /* ── Sidebar ── */
            [data-testid="stSidebar"] {
                background: var(--surface) !important;
                border-right: 1px solid var(--border) !important;
            }
            [data-testid="stSidebar"] * { color: var(--text) !important; }
            [data-testid="stSidebar"] .stTextInput input {
                background: var(--surface2) !important;
                border: 1px solid var(--border2) !important;
                color: var(--text) !important;
                border-radius: 8px !important;
                font-family: 'Figtree', sans-serif !important;
            }

            .main .block-container { padding: 2rem 2.5rem !important; max-width: 1380px; }

            /* ── Hero ── */
            .hero {
                background: linear-gradient(120deg, #eef4ff 0%, #f0f9ff 50%, #ecfdf5 100%);
                border: 1px solid #c7d9f5;
                border-radius: 20px;
                padding: 34px 40px 30px;
                margin-bottom: 28px;
                position: relative;
                overflow: hidden;
            }
            .hero::after {
                content: '🧠';
                position: absolute;
                right: 40px; top: 50%;
                transform: translateY(-50%);
                font-size: 5rem;
                opacity: 0.08;
                filter: grayscale(1);
            }
            .hero-tag {
                display: inline-block;
                background: #dbeafe;
                border: 1px solid #93c5fd;
                color: #1d4ed8;
                font-size: 0.7rem;
                font-weight: 600;
                letter-spacing: 2px;
                text-transform: uppercase;
                padding: 4px 12px;
                border-radius: 100px;
                margin-bottom: 14px;
            }
            .hero h1 {
                font-family: 'Syne', sans-serif !important;
                font-size: 2.3rem !important;
                font-weight: 800 !important;
                color: #0f172a !important;
                margin: 0 0 10px !important;
                letter-spacing: -0.5px;
                line-height: 1.2;
            }
            .hero h1 span { color: #1a56db; }
            .hero p {
                color: var(--muted) !important;
                font-size: 0.97rem;
                margin: 0;
                font-weight: 400;
                max-width: 540px;
            }

            /* ── Card ── */
            .card {
                background: var(--surface);
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 22px 24px;
                height: 100%;
                box-shadow: 0 1px 4px rgba(15,23,42,0.05);
            }
            .card-title {
                font-family: 'Syne', sans-serif;
                font-size: 0.68rem;
                font-weight: 700;
                letter-spacing: 2px;
                text-transform: uppercase;
                color: var(--muted);
                margin-bottom: 16px;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .card-title::before {
                content: '';
                display: inline-block;
                width: 6px; height: 6px;
                border-radius: 50%;
                background: var(--accent2);
                flex-shrink: 0;
            }

            /* ── File uploader — style the native dropzone only, no HTML overlay ── */
            [data-testid="stFileUploader"] section {
                background: var(--surface2) !important;
                border: 2px dashed var(--border2) !important;
                border-radius: 12px !important;
                padding: 28px 20px !important;
                transition: border-color 0.2s, background 0.2s;
            }
            [data-testid="stFileUploader"] section:hover {
                border-color: var(--accent) !important;
                background: #eef4ff !important;
            }
            /* Hide only the redundant label above the dropzone, keep dropzone text intact */
            [data-testid="stFileUploader"] > label {
                display: none !important;
            }

            /* ── Badge ── */
            .badge {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 7px 16px;
                border-radius: 100px;
                font-size: 0.82rem;
                font-weight: 600;
                margin-bottom: 18px;
            }
            .badge-ok     { background: #d1fae5; color: #065f46; border: 1px solid #6ee7b7; }
            .badge-warn   { background: #fef3c7; color: #92400e; border: 1px solid #fcd34d; }
            .badge-danger { background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }
            .badge-dot {
                width: 8px; height: 8px;
                border-radius: 50%;
                background: currentColor;
                display: inline-block;
                animation: blink 2s infinite;
            }
            @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.35} }

            /* ── Metrics ── */
            .metric-row {
                display: grid;
                grid-template-columns: repeat(3,1fr);
                gap: 10px;
                margin: 4px 0 18px;
            }
            .metric-box {
                background: var(--surface2);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 14px 12px;
                text-align: center;
            }
            .metric-label {
                font-size: 0.68rem;
                color: var(--muted);
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 6px;
                font-weight: 600;
            }
            .metric-val {
                font-family: 'Syne', sans-serif;
                font-size: 1.3rem;
                font-weight: 700;
                color: var(--text);
            }
            .metric-val.ok     { color: var(--ok); }
            .metric-val.warn   { color: var(--warn); }
            .metric-val.danger { color: var(--danger); }

            /* ── Probability bars ── */
            .prob-item { margin: 11px 0; }
            .prob-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 5px;
            }
            .prob-name {
                font-size: 0.86rem;
                font-weight: 500;
                color: var(--text);
                text-transform: capitalize;
            }
            .prob-pct {
                font-family: 'Syne', sans-serif;
                font-size: 0.84rem;
                font-weight: 700;
                color: var(--accent);
            }
            .prob-track {
                width: 100%;
                height: 7px;
                background: var(--surface2);
                border-radius: 100px;
                overflow: hidden;
                border: 1px solid var(--border);
            }
            .prob-fill {
                height: 100%;
                border-radius: 100px;
                background: linear-gradient(90deg, #3b82f6, #06b6d4);
            }
            .prob-fill.top {
                background: linear-gradient(90deg, #1a56db, #0891b2);
            }

            /* ── Separator ── */
            .sep { height: 1px; background: var(--border); margin: 16px 0; }

            /* ── API status ── */
            .api-box {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 9px 14px;
                border-radius: 10px;
                font-size: 0.82rem;
                font-weight: 600;
                margin: 6px 0;
            }
            .api-on  { background: #d1fae5; border: 1px solid #6ee7b7; color: #065f46; }
            .api-off { background: #fee2e2; border: 1px solid #fca5a5; color: #991b1b; }
            .dot-s   { width: 8px; height: 8px; border-radius: 50%; background: currentColor; flex-shrink: 0; animation: blink 1.8s infinite; }

            /* ── Clinical note ── */
            .note {
                border-radius: 0 10px 10px 0;
                padding: 10px 14px;
                margin-top: 6px;
                font-size: 0.82rem;
                font-weight: 500;
            }
            .note-ok     { background: #ecfdf5; border-left: 3px solid #059669; color: #065f46; }
            .note-warn   { background: #fffbeb; border-left: 3px solid #d97706; color: #92400e; }
            .note-danger { background: #fff1f2; border-left: 3px solid #dc2626; color: #991b1b; }

            .stImage img { border-radius: 10px !important; }

            .footer {
                text-align: center;
                margin-top: 32px;
                padding-top: 16px;
                border-top: 1px solid var(--border);
                font-size: 0.74rem;
                color: #94a3b8;
            }

            h2, h3 { font-family: 'Syne', sans-serif !important; color: var(--text) !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_badge(status: str):
    s = status.lower()
    if "sain" in s or "notumor" in s:
        return "badge-ok", "Tissu Sain Confirmé"
    if "suspect" in s or "uncertain" in s:
        return "badge-warn", "Résultat Incertain"
    return "badge-danger", "Anomalie Détectée"


def get_metric_class(prediction: str, confidence: float):
    if "notumor" in prediction.lower():
        return "ok"
    if confidence < 70:
        return "warn"
    return "danger"


def render_probs(probabilities: dict, top_class: str):
    ordered = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
    for cls, prob in ordered:
        val = max(0.0, min(100.0, float(prob)))
        is_top = cls.lower() == top_class.lower()
        fill_cls = "prob-fill top" if is_top else "prob-fill"
        prefix = "▸ " if is_top else ""
        st.markdown(
            f"""
            <div class="prob-item">
                <div class="prob-header">
                    <span class="prob-name">{prefix}{cls}</span>
                    <span class="prob-pct">{val:.1f}%</span>
                </div>
                <div class="prob-track">
                    <div class="{fill_cls}" style="width:{val:.2f}%"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Init ───────────────────────────────────────────────────────────────────────
inject_styles()

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <div class="hero-tag">Deep Learning · Medical Imaging · v2.0</div>
        <h1>Scan<span>Mind</span> AI</h1>
        <p>Système de détection et classification des tumeurs cérébrales par IRM — pipeline CNN + Autoencodeur hybride.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<p style='font-family:Syne,sans-serif;font-size:1.05rem;font-weight:700;color:#0f172a;margin-bottom:2px'>Configuration</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='sep'></div>", unsafe_allow_html=True)

    api_url     = st.text_input("Endpoint API", "http://127.0.0.1:8000", label_visibility="collapsed")
    predict_url = f"{api_url.rstrip('/')}/predict"
    health_url  = f"{api_url.rstrip('/')}/health"

    st.markdown("<div style='margin-top:6px'></div>", unsafe_allow_html=True)
    try:
        r = requests.get(health_url, timeout=5)
        r.raise_for_status()
        payload = r.json()
        cls_ok = "✓" if payload.get("classifier_ready") else "✗"
        ae_ok  = "✓" if payload.get("autoencoder_ready") else "✗"
        st.markdown("<div class='api-box api-on'><span class='dot-s'></span>API connectée</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size:0.78rem;color:#64748b;margin-top:6px;line-height:2;padding-left:4px'>"
            f"{cls_ok} Classifier CNN<br>{ae_ok} Autoencodeur AE</div>",
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.markdown("<div class='api-box api-off'><span class='dot-s'></span>API hors ligne</div>", unsafe_allow_html=True)
        st.caption(str(e))

    st.markdown("<div class='sep' style='margin-top:18px'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='font-size:0.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#94a3b8;margin-bottom:8px'>Classes détectées</p>
        <div style='font-size:0.82rem;color:#475569;line-height:2.1'>
            🔵 &nbsp;Gliome<br>
            🟠 &nbsp;Méningiome<br>
            🟢 &nbsp;Tissu sain<br>
            🟣 &nbsp;Hypophyse
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='sep' style='margin-top:18px'></div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.72rem;color:#94a3b8;line-height:1.6'>⚠ Usage académique uniquement.<br>Non destiné à un usage clinique réel.</p>",
        unsafe_allow_html=True,
    )

# ── Main layout ────────────────────────────────────────────────────────────────
col_img, col_res = st.columns([1, 1.3], gap="large")

with col_img:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>Image IRM</div>", unsafe_allow_html=True)

    # Widget natif Streamlit — drag & drop fonctionnel, label masqué via CSS (> label)
    uploaded_file = st.file_uploader(
        "Déposer une image IRM ici (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
    )

    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, use_container_width=True)
        st.markdown(
            f"<p style='font-size:0.76rem;color:#94a3b8;text-align:center;margin-top:6px'>"
            f"{uploaded_file.name} &nbsp;·&nbsp; {img.size[0]}×{img.size[1]} px</p>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

with col_res:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>Analyse & Résultat</div>", unsafe_allow_html=True)

    if not uploaded_file:
        st.markdown(
            """
            <div style='text-align:center;padding:52px 0'>
                <p style='font-size:2.2rem;margin-bottom:10px'>🧬</p>
                <p style='color:#94a3b8;font-size:0.88rem'>En attente d'une image IRM...</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        with st.spinner("Analyse en cours..."):
            image_bytes = uploaded_file.getvalue()
            try:
                response = requests.post(
                    predict_url,
                    files={"file": (uploaded_file.name, image_bytes, "application/octet-stream")},
                    timeout=90,
                )
            except Exception as e:
                st.error(f"Impossible de joindre l'API : {e}")
                st.stop()

        if response.status_code != 200:
            st.error(f"Erreur API ({response.status_code})")
            st.code(response.text)
        else:
            result      = response.json()
            status      = result.get("status", "Anomalie détectée")
            prediction  = str(result.get("prediction", "N/A"))
            confidence  = float(result.get("confidence", 0.0))
            recon_error = float(result.get("reconstruction_error", 0.0))
            probs       = result.get("probabilities", {})

            badge_cls, badge_text = get_badge(status)
            mc = get_metric_class(prediction, confidence)

            st.markdown(
                f'<span class="badge {badge_cls}"><span class="badge-dot"></span>{badge_text}</span>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="metric-row">
                    <div class="metric-box">
                        <div class="metric-label">Prédiction</div>
                        <div class="metric-val {mc}">{prediction}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Confiance</div>
                        <div class="metric-val {mc}">{confidence:.1f}%</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Erreur AE</div>
                        <div class="metric-val">{recon_error:.5f}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<div class='sep'></div>", unsafe_allow_html=True)

            st.markdown(
                "<p style='font-size:0.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;"
                "color:#94a3b8;margin-bottom:10px'>Distribution par classe</p>",
                unsafe_allow_html=True,
            )
            render_probs(probs, prediction)

            st.markdown("<div class='sep'></div>", unsafe_allow_html=True)

            if "notumor" in prediction.lower():
                note_cls  = "note-ok"
                note_text = "✓ Aucune anomalie structurelle détectée. Résultat conforme à un tissu sain."
            elif confidence < 70:
                note_cls  = "note-warn"
                note_text = "⚠ Confiance modérée — une révision par un spécialiste est recommandée."
            else:
                note_cls  = "note-danger"
                note_text = "! Anomalie détectée avec forte confiance. Consultation médicale urgente conseillée."

            st.markdown(f'<div class="note {note_cls}">{note_text}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='footer'>ScanMind AI · Système d'aide au diagnostic — Usage académique uniquement · Non destiné à un usage clinique</div>",
    unsafe_allow_html=True,
)