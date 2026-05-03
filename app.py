import numpy as np
import pandas as pd
import altair as alt
import streamlit as st


st.set_page_config(
    page_title="Perceptron Gamificado",
    page_icon="⚙",
    layout="wide",
)


COMBINATIONS = pd.DataFrame(
    [
        {"x1": 0, "x2": 0},
        {"x1": 0, "x2": 1},
        {"x1": 1, "x2": 0},
        {"x1": 1, "x2": 1},
    ]
)

PRESETS = {
    "Personalizado": [1, 1, 1, 1],
    "AND": [0, 0, 0, 1],
    "OR": [0, 1, 1, 1],
    "NAND": [1, 1, 1, 0],
    "XOR": [0, 1, 1, 0],
}


def init_state():
    if "labels" not in st.session_state:
        st.session_state.labels = PRESETS["AND"].copy()
    if "selected_problem" not in st.session_state:
        st.session_state.selected_problem = "AND"
    if "active_idx" not in st.session_state:
        st.session_state.active_idx = 3
    if "w1" not in st.session_state:
        st.session_state.w1 = 0.0
    if "w2" not in st.session_state:
        st.session_state.w2 = 0.0
    if "bias" not in st.session_state:
        st.session_state.bias = 0.0


def apply_problem(problem_name):
    st.session_state.selected_problem = problem_name
    st.session_state.labels = PRESETS[problem_name].copy()
    for idx, value in enumerate(st.session_state.labels):
        st.session_state[f"label_{problem_name}_{idx}"] = bool(value)


def reset_knobs():
    st.session_state.w1 = 0.0
    st.session_state.w2 = 0.0
    st.session_state.bias = 0.0


def predict_row(x1, x2, w1, w2, bias):
    z_value = (x1 * w1) + (x2 * w2) + bias
    prediction = 1 if z_value >= 0 else 0
    return z_value, prediction


def build_results(w1, w2, bias):
    rows = []
    for idx, row in COMBINATIONS.iterrows():
        z_value, prediction = predict_row(row.x1, row.x2, w1, w2, bias)
        expected = st.session_state.labels[idx]
        rows.append(
            {
                "idx": idx,
                "x1": row.x1,
                "x2": row.x2,
                "deseado": expected,
                "z": z_value,
                "salida": prediction,
                "correcto": prediction == expected,
            }
        )
    return pd.DataFrame(rows)


def decision_figure(results, w1, w2, bias):
    x_min, x_max = -0.25, 1.25
    y_min, y_max = -0.25, 1.25
    steps = 70
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, steps),
        np.linspace(y_min, y_max, steps),
    )
    zz = (xx * w1) + (yy * w2) + bias
    dx = (x_max - x_min) / steps
    dy = (y_max - y_min) / steps
    region_df = pd.DataFrame(
        {
            "x": xx.ravel(),
            "x2_end": (xx + dx).ravel(),
            "y": yy.ravel(),
            "y2_end": (yy + dy).ravel(),
            "region": np.where(zz.ravel() >= 0, "positiva", "negativa"),
        }
    )

    region_chart = (
        alt.Chart(region_df)
        .mark_rect(opacity=0.35)
        .encode(
            x=alt.X("x:Q", title="Entrada x1", scale=alt.Scale(domain=[x_min, x_max])),
            x2="x2_end:Q",
            y=alt.Y("y:Q", title="Entrada x2", scale=alt.Scale(domain=[y_min, y_max])),
            y2="y2_end:Q",
            color=alt.Color(
                "region:N",
                scale=alt.Scale(
                    domain=["negativa", "positiva"],
                    range=["#7f1d1d", "#065f46"],
                ),
                legend=None,
            ),
        )
    )

    layers = [region_chart]

    if abs(w2) > 1e-9:
        xs = np.array([x_min, x_max])
        ys = -(w1 * xs + bias) / w2
        line_df = pd.DataFrame({"x": xs, "y": ys})
        layers.append(
            alt.Chart(line_df)
            .mark_line(color="#60a5fa", strokeWidth=4)
            .encode(x="x:Q", y="y:Q")
        )
    elif abs(w1) > 1e-9:
        line_df = pd.DataFrame({"x": [-bias / w1, -bias / w1], "y": [y_min, y_max]})
        layers.append(
            alt.Chart(line_df)
            .mark_line(color="#60a5fa", strokeWidth=4)
            .encode(x="x:Q", y="y:Q")
        )

    point_df = results.copy()
    point_df["etiqueta"] = point_df["deseado"].map({1: "positiva", 0: "negativa"})
    point_df["estado"] = point_df["correcto"].map({True: "correcto", False: "error"})
    point_df["coord"] = point_df.apply(lambda row: f"({row.x1}, {row.x2})", axis=1)

    layers.append(
        alt.Chart(point_df)
        .mark_point(size=360, filled=True, stroke="#e2e8f0", strokeWidth=2)
        .encode(
            x="x1:Q",
            y="x2:Q",
            color=alt.Color(
                "etiqueta:N",
                scale=alt.Scale(
                    domain=["negativa", "positiva"],
                    range=["#ef4444", "#10b981"],
                ),
                legend=alt.Legend(title="Etiqueta"),
            ),
            shape=alt.Shape(
                "estado:N",
                scale=alt.Scale(domain=["correcto", "error"], range=["circle", "cross"]),
                legend=alt.Legend(title="Clasificacion"),
            ),
            tooltip=[
                "x1:Q",
                "x2:Q",
                "deseado:Q",
                alt.Tooltip("z:Q", format=".2f"),
                "salida:Q",
                "correcto:N",
            ],
        )
    )

    layers.append(
        alt.Chart(point_df)
        .mark_text(dy=-22, color="#e2e8f0", fontSize=13, fontWeight="bold")
        .encode(x="x1:Q", y="x2:Q", text="coord:N")
    )

    return (
        alt.layer(*layers)
        .properties(height=460)
        .configure_axis(
            gridColor="#2a3550",
            labelColor="#e2e8f0",
            titleColor="#e2e8f0",
        )
        .configure_view(stroke="#2a3550")
        .configure_legend(labelColor="#e2e8f0", titleColor="#e2e8f0")
    )


def render_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background:
              radial-gradient(ellipse at top left, rgba(59,130,246,.13), transparent 45%),
              radial-gradient(ellipse at bottom right, rgba(167,139,250,.10), transparent 45%),
              #0a0e1a;
            color: #e2e8f0;
        }
        [data-testid="stHeader"] { background: rgba(10,14,26,.82); }
        .block-container { padding-top: 2rem; }
        .hero {
            border: 1px solid #2a3550;
            background: linear-gradient(180deg, #111827, #0d1424);
            border-radius: 8px;
            padding: 22px 24px;
            margin-bottom: 18px;
        }
        .hero h1 {
            font-size: 2.1rem;
            margin: 0 0 8px 0;
            letter-spacing: .04em;
            color: #60a5fa;
        }
        .hero p { margin: 0; color: #94a3b8; line-height: 1.6; }
        .metric-card {
            border: 1px solid #2a3550;
            background: #111827;
            border-radius: 8px;
            padding: 14px 16px;
            min-height: 94px;
        }
        .metric-label {
            color: #94a3b8;
            font-size: .78rem;
            letter-spacing: .08em;
            text-transform: uppercase;
        }
        .metric-value {
            color: #e2e8f0;
            font-size: 1.8rem;
            font-weight: 800;
            margin-top: 4px;
        }
        .ok { color: #34d399; }
        .bad { color: #f87171; }
        .pattern-row {
            border: 1px solid #2a3550;
            background: #111827;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
        }
        .stSlider [data-baseweb="slider"] { margin-top: 8px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


init_state()
render_styles()

st.markdown(
    """
    <div class="hero">
      <h1>PERCEPTRON GAMIFICADO</h1>
      <p>
        Ajusta manualmente las perillas w1, w2 y bias para separar patrones de dos entradas.
        La regla es la misma máquina conceptual: z = x1*w1 + x2*w2 + b.
        No hay entrenamiento automático.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Panel de control")
    problem = st.selectbox(
        "Problema",
        list(PRESETS.keys()),
        index=list(PRESETS.keys()).index(st.session_state.selected_problem),
    )
    if problem != st.session_state.selected_problem:
        apply_problem(problem)
        st.rerun()

    st.divider()
    st.subheader("Perillas manuales")
    w1 = st.slider("Peso w1", -5.0, 5.0, 0.0, 0.1, key="w1")
    w2 = st.slider("Peso w2", -5.0, 5.0, 0.0, 0.1, key="w2")
    bias = st.slider("Bias b", -5.0, 5.0, 0.0, 0.1, key="bias")

    st.divider()
    st.button("Reiniciar perillas", use_container_width=True, on_click=reset_knobs)

results = build_results(w1, w2, bias)
correct_count = int(results["correcto"].sum())
total = len(results)
score_pct = int(round((correct_count / total) * 100))

top_a, top_b, top_c, top_d = st.columns(4)
top_a.markdown(
    f"""
    <div class="metric-card">
      <div class="metric-label">Correctos</div>
      <div class="metric-value {'ok' if correct_count == total else 'bad'}">{correct_count}/{total}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
top_b.markdown(
    f"""
    <div class="metric-card">
      <div class="metric-label">Precisión</div>
      <div class="metric-value">{score_pct}%</div>
    </div>
    """,
    unsafe_allow_html=True,
)
top_c.markdown(
    f"""
    <div class="metric-card">
      <div class="metric-label">w1, w2</div>
      <div class="metric-value">{w1:.1f}, {w2:.1f}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
top_d.markdown(
    f"""
    <div class="metric-card">
      <div class="metric-label">Bias</div>
      <div class="metric-value">{bias:.1f}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.progress(correct_count / total)

left, right = st.columns([0.92, 1.08], gap="large")

with left:
    st.subheader("Patrones y etiquetas deseadas")
    st.caption("Cambia la etiqueta esperada para cada una de las 4 combinaciones.")

    for idx, row in COMBINATIONS.iterrows():
        current = st.session_state.labels[idx]
        z_value, prediction = predict_row(row.x1, row.x2, w1, w2, bias)
        is_ok = prediction == current
        state_text = "correcto" if is_ok else "incorrecto"
        state_class = "ok" if is_ok else "bad"

        st.markdown(
            f"""
            <div class="pattern-row">
              <strong>x1={row.x1}, x2={row.x2}</strong><br>
              <span class="{state_class}">salida={prediction} | deseado={current} | z={z_value:.2f} | {state_text}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.session_state.labels[idx] = 1 if st.toggle(
            f"Etiqueta positiva para ({row.x1}, {row.x2})",
            value=bool(current),
            key=f"label_{st.session_state.selected_problem}_{idx}",
        ) else 0

    active_options = [
        f"({row.x1}, {row.x2})" for row in COMBINATIONS.itertuples(index=False)
    ]
    active_label = st.radio(
        "Patrón activo para revisar el cálculo",
        active_options,
        index=st.session_state.active_idx,
        horizontal=True,
    )
    st.session_state.active_idx = active_options.index(active_label)

with right:
    st.subheader("Frontera de decisión")
    st.altair_chart(decision_figure(results, w1, w2, bias), use_container_width=True)

    active_row = COMBINATIONS.iloc[st.session_state.active_idx]
    active_z, active_prediction = predict_row(
        active_row.x1,
        active_row.x2,
        w1,
        w2,
        bias,
    )
    st.subheader("Cálculo en tiempo real")
    st.code(
        f"z = ({active_row.x1} * {w1:.2f}) + ({active_row.x2} * {w2:.2f}) + ({bias:.2f}) = {active_z:.2f}\n"
        f"salida = 1 si z >= 0, si no 0\n"
        f"salida actual = {active_prediction}",
        language="text",
    )

st.divider()
st.subheader("Tabla de evaluación")
st.dataframe(
    results.drop(columns=["idx"]).rename(
        columns={
            "x1": "x1",
            "x2": "x2",
            "deseado": "etiqueta deseada",
            "z": "suma ponderada",
            "salida": "salida perceptron",
            "correcto": "clasificacion correcta",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

if correct_count == total:
    st.success("Reto resuelto: todas las combinaciones están clasificadas correctamente.")
elif st.session_state.selected_problem == "XOR":
    st.warning(
        "XOR no puede resolverse con un único perceptrón porque sus clases no son linealmente separables."
    )
else:
    st.info("Sigue moviendo las perillas hasta que el contador llegue a 4/4.")
