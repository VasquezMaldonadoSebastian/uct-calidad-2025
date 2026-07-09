"""
Dashboard de Evaluación Anual de Indicadores 2025
Universidad Católica de Temuco — SIAC
Basado en: SGC PS-FOR-PS 0042 v01 (09/01/2026)

Diseño: Open Design — paleta clara, tipografía Inter, sombras sutiles.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

st.set_page_config(
    page_title="UCT — Indicadores de Calidad 2025",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════
#  PALETA OPEN DESIGN — Clara, limpia, accesible
# ══════════════════════════════════════════════════
C = {
    # Superficies
    "bg":             "#F8FAFC",
    "surface":        "#FFFFFF",
    "surface_warm":   "#F1F5F9",
    "surface_hover":  "#F8FAFC",

    # Bordes
    "border":         "#E2E8F0",
    "border_soft":    "#F1F5F9",

    # Acentos
    "accent":         "#4F6BED",
    "accent_hover":   "#3D57D9",
    "accent_light":   "#EEF0FD",

    # Texto
    "heading":        "#1E293B",
    "label":          "#334155",
    "body":           "#64748B",
    "muted":          "#94A3B8",

    # Semáforo / semánticos
    "success":        "#22C55E",
    "success_bg":     "#F0FDF4",
    "success_border": "#BBF7D0",
    "warning":        "#F59E0B",
    "warning_bg":     "#FFFBEB",
    "warning_border": "#FDE68A",
    "danger":         "#EF4444",
    "danger_bg":      "#FEF2F2",
    "danger_border":  "#FECACA",
    "info":           "#3B82F6",
    "info_bg":        "#EFF6FF",
    "info_border":    "#BFDBFE",
}

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }}
    .stApp {{ background: {C['bg']}; }}
    section[data-testid="stSidebar"] {{ display: none; }}

    /* ─── Navbar superior ─── */
    .navbar {{
        background: {C['surface']};
        border-bottom: 1px solid {C['border']};
        padding: 0;
        margin: -1rem -1rem 1.5rem -1rem;
        display: flex;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .navbar-brand {{
        padding: 14px 24px;
        color: {C['heading']};
        font-size: 17px;
        font-weight: 700;
        white-space: nowrap;
        border-right: 1px solid {C['border']};
    }}
    .navbar-brand small {{
        display: block;
        font-size: 11px;
        font-weight: 400;
        color: {C['body']};
        margin-top: 2px;
    }}
    .navbar-nav {{
        display: flex;
        gap: 0;
        margin-left: 4px;
    }}
    .navbar-nav a {{
        color: {C['body']};
        text-decoration: none;
        padding: 18px 16px;
        font-size: 13px;
        font-weight: 500;
        border-bottom: 2px solid transparent;
        transition: all 0.15s ease;
        white-space: nowrap;
    }}
    .navbar-nav a:hover {{
        color: {C['accent']};
        background: {C['accent_light']};
    }}
    .navbar-nav a.active {{
        color: {C['accent']};
        border-bottom-color: {C['accent']};
        font-weight: 600;
    }}

    /* ─── KPI cards ─── */
    .kpi-card {{
        background: {C['surface']};
        border: 1px solid {C['border']};
        border-radius: 8px;
        padding: 18px 20px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        text-align: center;
        transition: box-shadow 0.15s ease;
    }}
    .kpi-card:hover {{
        box-shadow: 0 2px 8px rgba(79,107,237,0.08);
    }}
    .kpi-value {{ font-size: 28px; font-weight: 700; color: {C['heading']}; letter-spacing: -0.5px; }}
    .kpi-label {{ font-size: 12px; color: {C['body']}; margin-top: 4px; font-weight: 500; }}
    .kpi-delta {{ font-size: 11px; margin-top: 4px; }}

    /* ─── Secciones ─── */
    .visual-title {{
        font-size: 14px; font-weight: 600; color: {C['label']};
        margin-bottom: 10px; padding-bottom: 6px;
        border-bottom: 1px solid {C['border']};
    }}
    .section-divider {{ border-top: 1px solid {C['border']}; margin: 16px 0; }}

    /* ─── Tablas ─── */
    .pbi-table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
    .pbi-table th {{
        background: {C['accent']}; color: white;
        padding: 8px 12px; text-align: left; font-weight: 600; font-size: 11px;
    }}
    .pbi-table td {{ padding: 8px 12px; border-bottom: 1px solid {C['border']}; color: {C['label']}; }}
    .pbi-table tr:hover td {{ background: {C['accent_light']}; }}
    .pbi-table .total-row td {{
        font-weight: 700; background: {C['surface_warm']};
        border-top: 2px solid {C['accent']};
    }}

    /* ─── Alert boxes ─── */
    .alert-box {{
        background: {C['warning_bg']}; border: 1px solid {C['warning_border']};
        border-left: 4px solid {C['warning']};
        border-radius: 6px; padding: 10px 14px; font-size: 12px; color: #92400E;
        margin-bottom: 10px;
    }}
    .success-box {{
        background: {C['success_bg']}; border: 1px solid {C['success_border']};
        border-left: 4px solid {C['success']};
        border-radius: 6px; padding: 10px 14px; font-size: 12px; color: #166534;
        margin-bottom: 10px;
    }}
    .info-box {{
        background: {C['info_bg']}; border: 1px solid {C['info_border']};
        border-left: 4px solid {C['info']};
        border-radius: 6px; padding: 10px 14px; font-size: 12px; color: #1E40AF;
        margin-bottom: 10px;
    }}

    /* ─── Metric overrides ─── */
    div[data-testid="stMetric"] {{
        background: {C['surface']};
        border: 1px solid {C['border']};
        border-radius: 8px; padding: 12px 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }}
    div[data-testid="stMetric"] label {{ color: {C['body']}; font-size: 12px; }}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{ color: {C['heading']}; font-weight: 700; }}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════
#  CARGA DE DATOS DESDE EL EXCEL
# ══════════════════════════════════════════════════
# Ruta del Excel — relativa para compatibilidad con Streamlit Cloud
EXCEL_PATH = os.path.join(os.path.dirname(__file__), "data", "indicadores.xlsx")
# Fallback: ruta local del usuario (desarrollo)
if not os.path.exists(EXCEL_PATH):
    EXCEL_PATH = r"C:\Users\sebas\AppData\Local\hermes\cache\documents\doc_95330c54c90a_Evaluación Anual de Indicadores 2025.xlsx"


@st.cache_data
def load_excel():
    """Carga todas las hojas del Excel y retorna un dict de DataFrames."""
    data = {}
    xl = pd.ExcelFile(EXCEL_PATH)
    for sheet in ["Lineamiento 1", "Lineamiento 2", "Lineamiento 3",
                   "Lineamiento 4", "Lineamiento 5", "Lineamiento 6 "]:
        data[sheet.strip().lower().replace(" ", "")] = pd.read_excel(EXCEL_PATH, sheet_name=sheet, header=None)
    return data


def parse_ind_6(data):
    """Extrae indicadores de desempeño operacional del Lineamiento 6."""
    df = data["lineamiento6"]
    rows = []
    for i in range(8, 25):
        if i >= len(df):
            break
        row = df.iloc[i]
        codigo = str(row.iloc[7]) if pd.notna(row.iloc[7]) else None
        if not codigo or "IND-" not in codigo:
            continue
        nombre = str(row.iloc[8]) if pd.notna(row.iloc[8]) else ""
        periodicidad = str(row.iloc[9]) if pd.notna(row.iloc[9]) else ""
        meta_raw = row.iloc[11] if pd.notna(row.iloc[11]) else None

        meta_tipo = ""
        if meta_raw is not None:
            meta_str = str(meta_raw)
            if "≥" in meta_str or ">=" in meta_str:
                meta_tipo = "≥"
            elif "≤" in meta_str or "<=" in meta_str:
                meta_tipo = "≤"

        meta_num = None
        if meta_raw is not None:
            try:
                raw_meta = str(meta_raw).replace("≥","").replace("≤","").replace(">","").replace("<","").replace("%","").replace(",",".").strip()
                meta_num = float(raw_meta)
            except:
                pass

        meses = {}
        for m_idx, m_name in enumerate(["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]):
            col = 13 + m_idx
            if col < len(row) and pd.notna(row.iloc[col]):
                raw = row.iloc[col]
                if isinstance(raw, str):
                    raw = raw.replace("%","").replace(",",".").strip()
                try:
                    meses[m_name] = float(raw)
                except:
                    pass

        resultado_num = None
        if len(row) > 25 and pd.notna(row.iloc[25]):
            try:
                raw_res = str(row.iloc[25]).replace("%","").replace(",",".").strip()
                resultado_num = float(raw_res)
                if resultado_num <= 1:
                    resultado_num = resultado_num * 100
            except:
                pass
        elif len(row) > 24 and pd.notna(row.iloc[24]):
            try:
                raw_res = str(row.iloc[24]).replace("%","").replace(",",".").strip()
                resultado_num = float(raw_res)
                if resultado_num <= 1:
                    resultado_num = resultado_num * 100
            except:
                pass

        obs = str(row.iloc[26]) if len(row) > 26 and pd.notna(row.iloc[26]) else ""
        direccion = "DDPER" if "DDPER" in codigo else "DIRINF"

        vals = list(meses.values())
        if vals:
            if all(v <= 1 for v in vals):
                promedio = round(sum(vals) / len(vals) * 100, 1)
            else:
                promedio = round(sum(vals) / len(vals), 1)
        else:
            promedio = None

        cumple = None
        if resultado_num is not None and meta_num is not None:
            if meta_tipo == "≥":
                cumple = resultado_num >= meta_num
            elif meta_tipo == "≤":
                cumple = resultado_num <= meta_num

        rows.append({
            "codigo": codigo, "nombre": nombre, "direccion": direccion,
            "periodicidad": periodicidad, "meta_tipo": meta_tipo,
            "meta": meta_num, "meses": meses, "promedio": promedio,
            "resultado_2025": resultado_num, "observaciones": obs, "cumple": cumple,
        })
    return pd.DataFrame(rows)


def parse_satisfaccion(data):
    """Extrae datos de satisfacción del Lineamiento 4."""
    df = data["lineamiento4"]
    rows = []
    for i in range(8, 18):
        if i >= len(df):
            break
        row = df.iloc[i]
        codigo = str(row.iloc[6]) if pd.notna(row.iloc[6]) else None
        if not codigo or "SGC" not in codigo:
            continue
        proceso = str(row.iloc[7]) if pd.notna(row.iloc[7]) else ""
        resultado = row.iloc[22] if pd.notna(row.iloc[22]) else None
        obs = str(row.iloc[24]) if pd.notna(row.iloc[24]) else ""
        resultado_num = None
        if resultado is not None:
            try:
                resultado_num = float(resultado) * 100 if float(resultado) <= 1 else float(resultado)
            except:
                pass
        rows.append({"codigo": codigo, "proceso": proceso, "resultado": resultado_num, "observaciones": obs})
    return pd.DataFrame(rows)


def parse_quejas(data):
    """Extrae datos de quejas del Lineamiento 5."""
    df = data["lineamiento5"]
    rows = []
    for i in range(8, 11):
        if i >= len(df):
            break
        row = df.iloc[i]
        direccion = str(row.iloc[5]).strip() if pd.notna(row.iloc[5]) else ""
        if not direccion or direccion in ["NaN", "Total"]:
            if "Total" in str(row.iloc[5]):
                direccion = "Total"
            else:
                continue
        meses = {}
        for m_idx, m_name in enumerate(["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]):
            col = 6 + m_idx
            if col < len(row) and pd.notna(row.iloc[col]):
                try:
                    meses[m_name] = int(float(row.iloc[col]))
                except:
                    meses[m_name] = 0
        total_q = sum(meses.values())
        respondidas = int(row.iloc[19]) if pd.notna(row.iloc[19]) else 0
        rows.append({"direccion": direccion, "meses": meses, "total": total_q, "respondidas": respondidas})
    return rows


def parse_requisitos(data):
    """Extrae datos de requisitos legales del Lineamiento 3."""
    df = data["lineamiento3"]
    rows = []
    for i in range(8, 11):
        if i >= len(df):
            break
        row = df.iloc[i]
        direccion = str(row.iloc[5]).strip() if pd.notna(row.iloc[5]) else ""
        if not direccion or direccion == "NaN":
            continue
        cumplimiento = int(row.iloc[6]) if pd.notna(row.iloc[6]) else None
        total = int(row.iloc[7]) if pd.notna(row.iloc[7]) else None
        rows.append({"direccion": direccion, "cumplimiento": cumplimiento, "total": total})
    return rows


# ══════════════════════════════════════════════════
#  CARGAR DATOS
# ══════════════════════════════════════════════════
data = load_excel()
df_ind6 = parse_ind_6(data)
df_sat = parse_satisfaccion(data)
quejas = parse_quejas(data)
requisitos = parse_requisitos(data)


# ══════════════════════════════════════════════════
#  NAVBAR SUPERIOR
# ══════════════════════════════════════════════════
params = st.query_params
tab_actual = params.get("tab", "IND-PS-0001")

st.markdown(f"""
<style>
    .nav-indps0001 {{ border-bottom-color: {C['accent']} !important; color: {C['accent']} !important; background: {C['accent_light']}; }}
    .nav-todos {{ border-bottom-color: {C['accent']} !important; color: {C['accent']} !important; background: {C['accent_light']}; }}
    .nav-satisfaccion {{ border-bottom-color: {C['accent']} !important; color: {C['accent']} !important; background: {C['accent_light']}; }}
    .nav-quejas {{ border-bottom-color: {C['accent']} !important; color: {C['accent']} !important; background: {C['accent_light']}; }}
    .nav-requisitos {{ border-bottom-color: {C['accent']} !important; color: {C['accent']} !important; background: {C['accent_light']}; }}
</style>
<div class="navbar">
    <div class="navbar-brand">
        🎓 UCT — SIAC
        <small>Evaluación Anual de Indicadores 2025</small>
    </div>
    <div class="navbar-nav">
        <a href="?tab=IND-PS-0001" class="nav-indps0001 {'active' if tab_actual=='IND-PS-0001' else ''}">IND-PS-0001 Eficacia NC</a>
        <a href="?tab=Todos" class="nav-todos {'active' if tab_actual=='Todos' else ''}">Todos los Indicadores</a>
        <a href="?tab=Satisfaccion" class="nav-satisfaccion {'active' if tab_actual=='Satisfaccion' else ''}">Satisfacción</a>
        <a href="?tab=Quejas" class="nav-quejas {'active' if tab_actual=='Quejas' else ''}">Quejas</a>
        <a href="?tab=Requisitos" class="nav-requisitos {'active' if tab_actual=='Requisitos' else ''}">Requisitos Legales</a>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════
def kpi_card(label, value, delta=None, icon=""):
    delta_html = ""
    if delta:
        color = C["success"] if "Cumple" in str(delta) or "✅" in str(delta) else C["danger"]
        delta_html = f'<div class="kpi-delta" style="color:{color};">{delta}</div>'
    return f"""
    <div class="kpi-card">
        <div style="font-size:20px; margin-bottom:4px;">{icon}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        {delta_html}
    </div>
    """


def section_title(text):
    return f'<div class="visual-title">{text}</div>'


def make_plotly_base(title=""):
    fig = go.Figure()
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color=C["label"])) if title else None,
        font=dict(family="Inter, sans-serif", size=11, color=C["body"]),
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor=C["border_soft"], tickfont=dict(color=C["body"])),
        yaxis=dict(gridcolor=C["border_soft"], tickfont=dict(color=C["body"])),
        margin=dict(l=50, r=20, t=30, b=50),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11)),
    )
    return fig


# ══════════════════════════════════════════════════
#  PESTAÑA 1: IND-PS-0001 — Eficacia de NC
# ══════════════════════════════════════════════════
if tab_actual == "IND-PS-0001":

    datos_nc = [
        {"direccion": "DDPER", "nc_total": 7, "abiertas": 1, "cerradas": 6, "eficaz": 4, "no_eficaz": 2, "resultado": 66.7},
        {"direccion": "DIRINF", "nc_total": 1, "abiertas": 0, "cerradas": 1, "eficaz": 1, "no_eficaz": 0, "resultado": 100.0},
        {"direccion": "Administración", "nc_total": 10, "abiertas": 1, "cerradas": 9, "eficaz": 9, "no_eficaz": 0, "resultado": 100.0},
    ]

    # Info del indicador
    st.markdown(f"""
    <div style="background:{C['surface']}; border:1px solid {C['border']}; border-radius:8px;
                padding:16px 20px; box-shadow:0 1px 2px rgba(0,0,0,0.04); margin-bottom:14px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-size:15px; font-weight:700; color:{C['heading']};">IND-PS-0001 — Eficacia de Acciones Correctivas</span>
                <span style="font-size:11px; color:{C['body']}; margin-left:12px;">Periodicidad: Anual | Meta: ≥75%</span>
            </div>
            <span style="background:{C['accent']}; color:white; padding:4px 12px; border-radius:6px; font-size:11px; font-weight:600;">OBJETIVO 1 — SGC</span>
        </div>
        <div style="font-size:12px; color:{C['body']}; margin-top:8px;">
            <b>Fórmula:</b> (N° hallazgos cerrados eficazmente / Total hallazgos cerrados totales) × 100
        </div>
        <div style="font-size:12px; color:{C['body']}; margin-top:4px;">
            <b>Objetivo:</b> Aumentar la eficacia del Sistema de Gestión de Calidad de los Procesos de Soporte, por medio del cierre de las No Conformidades potenciales o reales detectadas.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="alert-box">
        ⚠️ <b>Datos de referencia:</b> Los valores mostrados provienen de la imagen referencial (resultado esperado). El Excel Lineamiento 1 no contiene datos ingresados para este indicador.
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    nc_total = sum(d["nc_total"] for d in datos_nc)
    abiertas = sum(d["abiertas"] for d in datos_nc)
    cerradas = sum(d["cerradas"] for d in datos_nc)
    eficaz = sum(d["eficaz"] for d in datos_nc)
    no_eficaz = sum(d["no_eficaz"] for d in datos_nc)
    resultado_total = round((eficaz / cerradas) * 100, 1) if cerradas else 0
    meta = 75

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(kpi_card("No Conformidades", nc_total, f"{abiertas} abiertas", "📋"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Cerradas", cerradas, f"{round(cerradas/nc_total*100)}% del total", "✅"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Eficaces", eficaz, f"{round(eficaz/cerradas*100)}%", "🎯"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("No Eficaces", no_eficaz, f"{round(no_eficaz/cerradas*100)}%", "⚠️"), unsafe_allow_html=True)
    with c5:
        cumple_text = "✅ Cumple" if resultado_total >= meta else "❌ No cumple"
        st.markdown(kpi_card("Resultado 2024", f"{resultado_total}%", f"Meta ≥{meta}% — {cumple_text}", "📊"), unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ═══ GRÁFICO DE TENDENCIA 3 AÑOS ═══
    st.markdown(section_title("📈 Comportamiento del Indicador — 3 Años (2023-2025)"), unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        ℹ️ <b>Nota:</b> 2023 y 2024 provienen de la imagen referencial. 2025 está pendiente de ingreso en el Excel.
    </div>
    """, unsafe_allow_html=True)

    anios = ["2023", "2024 (Jun)", "2024 (Anual)", "2025"]
    meta_line = [75, 75, 75, 75]
    resultado_line = [0, 100, 80, None]

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=anios, y=meta_line,
        name="Meta (≥75%)", mode="lines",
        line=dict(color=C["danger"], width=2, dash="dash"),
    ))
    fig_trend.add_trace(go.Scatter(
        x=anios[:3], y=resultado_line[:3],
        name="Resultado", mode="lines+markers+text",
        line=dict(color=C["accent"], width=3),
        marker=dict(size=12, color=C["accent"]),
        text=["0%", "100%", "80%"],
        textposition="top center",
        textfont=dict(size=12, color=C["heading"], family="Inter"),
    ))
    fig_trend.add_trace(go.Scatter(
        x=["2025"], y=[None],
        name="2025 (Pendiente)", mode="markers",
        marker=dict(size=12, color="#CBD5E1", symbol="circle-open", line=dict(width=2, color="#94A3B8")),
    ))
    fig_trend.add_shape(
        type="rect", x0="2023", x1="2025", y0=0, y1=75,
        fillcolor="rgba(239,68,68,0.03)", line=dict(width=0),
    )
    fig_trend.add_annotation(
        x="2024 (Jun)", y=5, text="Zona bajo meta",
        showarrow=False, font=dict(size=10, color=C["danger"]),
    )
    fig_trend.update_layout(
        yaxis=dict(title="%", range=[0, 115], gridcolor=C["border_soft"]),
        xaxis=dict(gridcolor=C["border_soft"]),
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color=C["body"]),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
        margin=dict(l=50, r=20, t=30, b=40), height=350,
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ═══ TABLA DE DESGLOSE + GRÁFICOS ═══
    col_table, col_bar = st.columns([2, 3])

    with col_table:
        st.markdown(section_title("📋 Desglose por Dirección"), unsafe_allow_html=True)
        st.markdown(f"""
        <table class="pbi-table">
            <thead>
                <tr><th>Dirección</th><th>Total NC</th><th>Abiertas</th><th>Cerradas</th><th>Eficaz</th><th>No eficaz</th><th>Resultado</th></tr>
            </thead>
            <tbody>
                {"".join(f'<tr><td>{d["direccion"]}</td><td>{d["nc_total"]}</td><td>{d["abiertas"]}</td><td>{d["cerradas"]}</td><td>{d["eficaz"]}</td><td>{d["no_eficaz"]}</td><td><b>{d["resultado"]:.0f}%</b></td></tr>' for d in datos_nc)}
                <tr class="total-row"><td><b>Total</b></td><td><b>{nc_total}</b></td><td><b>{abiertas}</b></td><td><b>{cerradas}</b></td><td><b>{eficaz}</b></td><td><b>{no_eficaz}</b></td><td><b>{resultado_total}%</b></td></tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

        fig_dona = go.Figure(data=[go.Pie(
            labels=["Eficaz", "No Eficaz"],
            values=[eficaz, no_eficaz],
            hole=0.6,
            marker=dict(colors=[C["accent"], C["danger"]]),
            textinfo="label+value",
            textfont=dict(size=12),
        )])
        fig_dona.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False, margin=dict(l=10, r=10, t=10, b=10), height=220,
            annotations=[dict(text=f'<b>{eficaz}</b><br>eficaces', x=0.5, y=0.5, font_size=14, showarrow=False, font_color=C["heading"])],
        )
        st.plotly_chart(fig_dona, use_container_width=True)

    with col_bar:
        st.markdown(section_title("📊 Eficacia por Dirección vs Meta ≥75%"), unsafe_allow_html=True)
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=[d["direccion"] for d in datos_nc],
            y=[d["resultado"] for d in datos_nc],
            name="Resultado 2024",
            marker_color=C["accent"],
            text=[f'{d["resultado"]:.0f}%' for d in datos_nc],
            textposition="outside",
            textfont=dict(size=13, color=C["heading"]),
        ))
        fig_bar.add_trace(go.Scatter(
            x=[d["direccion"] for d in datos_nc],
            y=[meta] * len(datos_nc),
            name="Meta ≥75%",
            mode="lines",
            line=dict(color=C["danger"], width=2, dash="dash"),
        ))
        fig_bar.update_layout(
            yaxis=dict(title="%", range=[0, 115], gridcolor=C["border_soft"]),
            plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=12, color=C["body"]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=50, r=20, t=20, b=40), height=350, bargap=0.35,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        fig_stack = go.Figure()
        fig_stack.add_trace(go.Bar(
            x=[d["direccion"] for d in datos_nc],
            y=[d["eficaz"] for d in datos_nc],
            name="Eficaz", marker_color=C["accent"],
        ))
        fig_stack.add_trace(go.Bar(
            x=[d["direccion"] for d in datos_nc],
            y=[d["no_eficaz"] for d in datos_nc],
            name="No Eficaz", marker_color=C["danger"],
        ))
        fig_stack.update_layout(
            barmode="stack",
            yaxis=dict(title="N° Hallazgos", gridcolor=C["border_soft"]),
            plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=12, color=C["body"]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=50, r=20, t=20, b=40), height=280, bargap=0.3,
        )
        st.plotly_chart(fig_stack, use_container_width=True)


# ══════════════════════════════════════════════════
#  PESTAÑA 2: TODOS LOS INDICADORES (Lineamiento 6)
# ══════════════════════════════════════════════════
elif tab_actual == "Todos":

    total = len(df_ind6)
    cumplen = int(df_ind6["cumple"].fillna(False).sum())
    no_cumplen = total - cumplen
    tasa = round(cumplen / total * 100, 1) if total else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Total Indicadores", total, icon="📊"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Cumplen Meta", cumplen, f"{tasa}%", "✅"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("No Cumplen", no_cumplen, f"{round(no_cumplen/total*100,1) if total else 0}%", "⚠️"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Tasa Global", f"{tasa}%", icon="🎯"), unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown(section_title("📋 Indicadores de Desempeño Operacional — IND-PS-0006"), unsafe_allow_html=True)
    df_show = df_ind6[["codigo", "nombre", "direccion", "periodicidad", "meta_tipo", "meta", "promedio", "resultado_2025", "cumple", "observaciones"]].copy()
    df_show.columns = ["Código", "Nombre", "Dirección", "Período", "Meta", "Meta %", "Promedio", "Resultado 2025", "Cumple", "Observaciones"]
    st.dataframe(df_show, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown(section_title("📊 Resultado 2025 vs Meta"), unsafe_allow_html=True)
    df_chart = df_ind6[df_ind6["resultado_2025"].notna()].copy()
    if len(df_chart) > 0:
        fig_all = go.Figure()
        fig_all.add_trace(go.Bar(
            x=df_chart["codigo"], y=df_chart["meta"],
            name="Meta", marker_color=C["danger"], opacity=0.35,
        ))
        fig_all.add_trace(go.Bar(
            x=df_chart["codigo"], y=df_chart["resultado_2025"],
            name="Resultado 2025", marker_color=C["accent"],
        ))
        fig_all.update_layout(
            barmode="group", yaxis=dict(title="%", gridcolor=C["border_soft"]),
            plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=11, color=C["body"]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=50, r=20, t=20, b=80), height=400,
            xaxis=dict(tickangle=-45),
        )
        st.plotly_chart(fig_all, use_container_width=True)

    # Semáforo
    st.markdown(section_title("🚦 Semáforo por Dirección"), unsafe_allow_html=True)
    for dir_name in df_ind6["direccion"].unique():
        subset = df_ind6[df_ind6["direccion"] == dir_name]
        ok = int(subset["cumple"].fillna(False).sum())
        tot = len(subset)
        pct = round(ok / tot * 100) if tot else 0
        color = C["success"] if pct >= 80 else C["warning"] if pct >= 60 else C["danger"]
        st.markdown(f"""
        <div style="background:{C['surface']}; border:1px solid {C['border']}; border-radius:8px;
                    padding:10px 16px; margin-bottom:6px; border-left:4px solid {color};">
            <span style="font-weight:700; color:{C['heading']};">{dir_name}</span>
            <span style="float:right; color:{color}; font-weight:700;">{ok}/{tot} ({pct}%)</span>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════
#  PESTAÑA 3: SATISFACCIÓN DEL USUARIO
# ══════════════════════════════════════════════════
elif tab_actual == "Satisfaccion":

    promedio = round(df_sat["resultado"].mean(), 1)
    min_val = df_sat["resultado"].min()
    max_val = df_sat["resultado"].max()
    bajo_meta = len(df_sat[df_sat["resultado"] < 89])

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Promedio General", f"{promedio}%", icon="📈"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Más Alto", f"{max_val}%", icon="🏆"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Más Bajo", f"{min_val}%", "⚠️" if min_val < 80 else "✅", "📉"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Bajo Meta 89%", str(bajo_meta), icon="⚠️"), unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(section_title("📊 Satisfacción por Proceso — Meta ≥89% (IND-PS-0004)"), unsafe_allow_html=True)

    df_sat_sorted = df_sat.sort_values("resultado", ascending=True)
    colors = [C["danger"] if v < 80 else C["warning"] if v < 89 else C["accent"] for v in df_sat_sorted["resultado"]]
    fig_sat = go.Figure(go.Bar(
        x=df_sat_sorted["resultado"], y=df_sat_sorted["proceso"],
        orientation="h", marker_color=colors,
        text=[f"{v:.1f}%" for v in df_sat_sorted["resultado"]],
        textposition="outside", textfont=dict(size=11),
    ))
    fig_sat.add_vline(x=89, line_dash="dash", line_color=C["danger"], annotation_text="Meta 89%")
    fig_sat.update_layout(
        xaxis=dict(title="%", range=[0, 110], gridcolor=C["border_soft"]),
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color=C["body"]),
        margin=dict(l=250, r=40, t=20, b=40), height=450,
    )
    st.plotly_chart(fig_sat, use_container_width=True)


# ══════════════════════════════════════════════════
#  PESTAÑA 4: QUEJAS DEL USUARIO
# ══════════════════════════════════════════════════
elif tab_actual == "Quejas":
    q_total = sum(q["total"] for q in quejas)
    q_dirinf = sum(q["total"] for q in quejas if q["direccion"] == "DIRINF")
    q_ddper = sum(q["total"] for q in quejas if q["direccion"] == "DDPER")

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(kpi_card("Total Quejas 2025", str(q_total), icon="📋"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("DIRINF", str(q_dirinf), f"{round(q_dirinf/q_total*100) if q_total else 0}%", "🖥️"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("DDPER", str(q_ddper), f"{round(q_ddper/q_total*100) if q_total else 0}%", "👥"), unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(section_title("📈 Quejas Mensuales por Dirección — IND-PS-0005"), unsafe_allow_html=True)

    meses = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
    q_dirinf_vals = []
    q_ddper_vals = []
    for q in quejas:
        if q["direccion"] == "DIRINF":
            q_dirinf_vals = [q["meses"].get(m, 0) for m in meses]
        elif q["direccion"] == "DDPER":
            q_ddper_vals = [q["meses"].get(m, 0) for m in meses]

    fig_q = go.Figure()
    fig_q.add_trace(go.Bar(x=meses, y=q_dirinf_vals, name="DIRINF", marker_color=C["accent"]))
    fig_q.add_trace(go.Bar(x=meses, y=q_ddper_vals, name="DDPER", marker_color="#93C5FD"))
    fig_q.update_layout(
        barmode="stack", yaxis=dict(title="N° Quejas", gridcolor=C["border_soft"]),
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color=C["body"]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=20, t=20, b=40), height=350,
    )
    st.plotly_chart(fig_q, use_container_width=True)

    st.markdown("""
    <div class="success-box">✅ <b>IND-PS-0005 — Quejas del Usuario:</b> Meta = 1 queja respondida/aceptada. Resultado: <b>Aceptable</b></div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════
#  PESTAÑA 5: REQUISITOS LEGALES
# ══════════════════════════════════════════════════
elif tab_actual == "Requisitos":
    st.markdown(section_title("⚖️ Cumplimiento de Requisitos Legales — IND-PS-0003"), unsafe_allow_html=True)

    for r in requisitos:
        if r["direccion"] == "TOTAL":
            continue
        pct = round(r["cumplimiento"] / r["total"] * 100) if r["total"] else 0
        color = C["success"] if pct == 100 else C["warning"] if pct >= 80 else C["danger"]
        st.markdown(f"""
        <div style="background:{C['surface']}; border:1px solid {C['border']}; border-radius:8px;
                    padding:14px 20px; margin-bottom:8px; border-left:4px solid {color};">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="font-weight:700; color:{C['heading']};">{r['direccion']}</span>
                    <span style="font-size:12px; color:{C['body']}; margin-left:10px;">
                        {r['cumplimiento']}/{r['total']} requisitos en cumplimiento
                    </span>
                </div>
                <span style="font-size:20px; font-weight:700; color:{color};">{pct}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    total_r = [r for r in requisitos if r["direccion"] == "TOTAL"]
    if total_r:
        r = total_r[0]
        pct = round(r["cumplimiento"] / r["total"] * 100) if r["total"] else 0
        st.markdown(f"""
        <div style="background:{C['accent']}; border-radius:8px; padding:14px 20px; margin-top:12px; color:white;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:700; font-size:16px;">TOTAL</span>
                <span style="font-size:20px; font-weight:700;">{r['cumplimiento']}/{r['total']} — {pct}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="success-box">✅ <b>IND-PS-0003:</b> Meta = 100%. DIRINF cumple 100% (41/41). DDPER sin datos ingresados.</div>
    """, unsafe_allow_html=True)
