import streamlit as st


st.set_page_config(
    page_title="Perceptron Gamificado",
    page_icon="P",
    layout="wide",
)


COMBINATIONS = [
    {"x1": 0, "x2": 0},
    {"x1": 0, "x2": 1},
    {"x1": 1, "x2": 0},
    {"x1": 1, "x2": 1},
]

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
        st.session_state[f"label_{idx}"] = bool(value)


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
    for idx, row in enumerate(COMBINATIONS):
        z_value, prediction = predict_row(row["x1"], row["x2"], w1, w2, bias)
        expected = st.session_state.labels[idx]
        rows.append(
            {
                "idx": idx,
                "x1": row["x1"],
                "x2": row["x2"],
                "deseado": expected,
                "z": z_value,
                "salida": prediction,
                "correcto": prediction == expected,
            }
        )
    return rows


def to_screen_x(x_value, width, pad, x_min=-0.25, x_max=1.25):
    return pad + ((x_value - x_min) / (x_max - x_min)) * (width - 2 * pad)


def to_screen_y(y_value, height, pad, y_min=-0.25, y_max=1.25):
    return height - pad - ((y_value - y_min) / (y_max - y_min)) * (height - 2 * pad)


def boundary_points(w1, w2, bias):
    x_min, x_max = -0.25, 1.25
    y_min, y_max = -0.25, 1.25
    points = []

    if abs(w2) > 1e-9:
        for x_value in (x_min, x_max):
            y_value = -(w1 * x_value + bias) / w2
            if y_min <= y_value <= y_max:
                points.append((x_value, y_value))

    if abs(w1) > 1e-9:
        for y_value in (y_min, y_max):
            x_value = -(w2 * y_value + bias) / w1
            if x_min <= x_value <= x_max:
                points.append((x_value, y_value))

    unique_points = []
    for point in points:
        rounded = (round(point[0], 6), round(point[1], 6))
        if rounded not in unique_points:
            unique_points.append(rounded)

    return unique_points[:2]


def decision_svg(results, w1, w2, bias):
    width, height, pad = 720, 460, 54
    x_min, x_max = -0.25, 1.25
    y_min, y_max = -0.25, 1.25
    cells = []
    steps = 34
    dx = (x_max - x_min) / steps
    dy = (y_max - y_min) / steps

    for ix in range(steps):
        for iy in range(steps):
            x_value = x_min + ix * dx
            y_value = y_min + iy * dy
            z_value = (x_value * w1) + (y_value * w2) + bias
            color = "#064e3b" if z_value >= 0 else "#7f1d1d"
            x_screen = to_screen_x(x_value, width, pad, x_min, x_max)
            y_screen = to_screen_y(y_value + dy, height, pad, y_min, y_max)
            cell_w = ((width - 2 * pad) / steps) + 1
            cell_h = ((height - 2 * pad) / steps) + 1
            cells.append(
                f'<rect x="{x_screen:.2f}" y="{y_screen:.2f}" '
                f'width="{cell_w:.2f}" height="{cell_h:.2f}" fill="{color}" opacity="0.42"/>'
            )

    grid_lines = []
    for tick in (-0.25, 0, 0.5, 1, 1.25):
        x = to_screen_x(tick, width, pad, x_min, x_max)
        y = to_screen_y(tick, height, pad, y_min, y_max)
        grid_lines.append(f'<line x1="{x:.2f}" y1="{pad}" x2="{x:.2f}" y2="{height-pad}" stroke="#2a3550"/>')
        grid_lines.append(f'<line x1="{pad}" y1="{y:.2f}" x2="{width-pad}" y2="{y:.2f}" stroke="#2a3550"/>')

    boundary = ""
    b_points = boundary_points(w1, w2, bias)
    if len(b_points) == 2:
        x1 = to_screen_x(b_points[0][0], width, pad, x_min, x_max)
        y1 = to_screen_y(b_points[0][1], height, pad, y_min, y_max)
        x2 = to_screen_x(b_points[1][0], width, pad, x_min, x_max)
        y2 = to_screen_y(b_points[1][1], height, pad, y_min, y_max)
        boundary = (
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            'stroke="#60a5fa" stroke-width="5" stroke-linecap="round"/>'
        )

    points = []
    for row in results:
        x = to_screen_x(row["x1"], width, pad, x_min, x_max)
        y = to_screen_y(row["x2"], height, pad, y_min, y_max)
        fill = "#10b981" if row["deseado"] == 1 else "#ef4444"
        mark = "OK" if row["correcto"] else "X"
        mark_color = "#0a0e1a" if row["correcto"] else "#ffffff"
        points.append(
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="19" fill="{fill}" stroke="#e2e8f0" stroke-width="3"/>'
            f'<text x="{x:.2f}" y="{y+5:.2f}" text-anchor="middle" font-size="13" '
            f'font-weight="800" fill="{mark_color}">{mark}</text>'
            f'<text x="{x:.2f}" y="{y-28:.2f}" text-anchor="middle" font-size="14" '
            f'font-weight="700" fill="#e2e8f0">({row["x1"]},{row["x2"]})</text>'
        )

    axis_labels = f"""
      <text x="{width / 2}" y="{height - 12}" text-anchor="middle" fill="#e2e8f0" font-size="14">Entrada x1</text>
      <text x="18" y="{height / 2}" text-anchor="middle" fill="#e2e8f0" font-size="14" transform="rotate(-90 18 {height / 2})">Entrada x2</text>
      <text x="{pad}" y="{height - pad + 24}" text-anchor="middle" fill="#94a3b8" font-size="12">0</text>
      <text x="{to_screen_x(1, width, pad, x_min, x_max)}" y="{height - pad + 24}" text-anchor="middle" fill="#94a3b8" font-size="12">1</text>
      <text x="{pad - 24}" y="{to_screen_y(0, height, pad, y_min, y_max) + 4}" text-anchor="middle" fill="#94a3b8" font-size="12">0</text>
      <text x="{pad - 24}" y="{to_screen_y(1, height, pad, y_min, y_max) + 4}" text-anchor="middle" fill="#94a3b8" font-size="12">1</text>
    """

    return f"""
    <div class="chart-wrap">
      <svg viewBox="0 0 {width} {height}" role="img" aria-label="Frontera de decision del perceptron">
        <rect x="0" y="0" width="{width}" height="{height}" rx="8" fill="#0a0e1a"/>
        {''.join(cells)}
        {''.join(grid_lines)}
        <rect x="{pad}" y="{pad}" width="{width - 2 * pad}" height="{height - 2 * pad}" fill="none" stroke="#3a4870" stroke-width="2"/>
        {boundary}
        {''.join(points)}
        {axis_labels}
      </svg>
      <div class="legend">
        <span><b class="good"></b>Region positiva</span>
        <span><b class="bad"></b>Region negativa</span>
        <span><i></i>Linea z = 0</span>
      </div>
    </div>
    """


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
        .chart-wrap {
            border: 1px solid #2a3550;
            border-radius: 8px;
            background: #0a0e1a;
            padding: 8px 8px 12px;
        }
        .chart-wrap svg {
            display: block;
            width: 100%;
            height: auto;
        }
        .legend {
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            color: #94a3b8;
            font-size: 13px;
            padding: 0 12px;
        }
        .legend b, .legend i {
            display: inline-block;
            width: 13px;
            height: 13px;
            margin-right: 6px;
            vertical-align: -2px;
            border-radius: 3px;
        }
        .legend .good { background: #065f46; }
        .legend .bad { background: #7f1d1d; }
        .legend i { background: #60a5fa; height: 4px; vertical-align: 2px; }
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
        La regla es: z = x1*w1 + x2*w2 + b. No hay entrenamiento automatico.
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
correct_count = sum(1 for row in results if row["correcto"])
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
      <div class="metric-label">Precision</div>
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

    for idx, row in enumerate(COMBINATIONS):
        current = st.session_state.labels[idx]
        z_value, prediction = predict_row(row["x1"], row["x2"], w1, w2, bias)
        is_ok = prediction == current
        state_text = "correcto" if is_ok else "incorrecto"
        state_class = "ok" if is_ok else "bad"

        st.markdown(
            f"""
            <div class="pattern-row">
              <strong>x1={row["x1"]}, x2={row["x2"]}</strong><br>
              <span class="{state_class}">salida={prediction} | deseado={current} | z={z_value:.2f} | {state_text}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.session_state.labels[idx] = 1 if st.toggle(
            f"Etiqueta positiva para ({row['x1']}, {row['x2']})",
            value=bool(current),
            key=f"label_{idx}",
        ) else 0

    active_options = [f"({row['x1']}, {row['x2']})" for row in COMBINATIONS]
    active_label = st.radio(
        "Patron activo para revisar el calculo",
        active_options,
        index=st.session_state.active_idx,
        horizontal=True,
    )
    st.session_state.active_idx = active_options.index(active_label)

with right:
    st.subheader("Frontera de decision")
    st.markdown(decision_svg(results, w1, w2, bias), unsafe_allow_html=True)

    active_row = COMBINATIONS[st.session_state.active_idx]
    active_z, active_prediction = predict_row(
        active_row["x1"],
        active_row["x2"],
        w1,
        w2,
        bias,
    )
    st.subheader("Calculo en tiempo real")
    st.code(
        f"z = ({active_row['x1']} * {w1:.2f}) + ({active_row['x2']} * {w2:.2f}) + ({bias:.2f}) = {active_z:.2f}\n"
        f"salida = 1 si z >= 0, si no 0\n"
        f"salida actual = {active_prediction}",
        language="text",
    )

st.divider()
st.subheader("Tabla de evaluacion")
st.dataframe(
    [
        {
            "x1": row["x1"],
            "x2": row["x2"],
            "etiqueta deseada": row["deseado"],
            "suma ponderada": round(row["z"], 2),
            "salida perceptron": row["salida"],
            "clasificacion correcta": row["correcto"],
        }
        for row in results
    ],
    use_container_width=True,
    hide_index=True,
)

if correct_count == total:
    st.success("Reto resuelto: todas las combinaciones estan clasificadas correctamente.")
elif st.session_state.selected_problem == "XOR":
    st.warning(
        "XOR no puede resolverse con un unico perceptron porque sus clases no son linealmente separables."
    )
else:
    st.info("Sigue moviendo las perillas hasta que el contador llegue a 4/4.")
