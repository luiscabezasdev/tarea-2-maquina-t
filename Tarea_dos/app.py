import streamlit as st


IMAGES = {
    "T perfecta 3x3": {
        "kind": "T",
        "matrix": [
            [1, 1, 1],
            [0, 1, 0],
            [0, 1, 0],
        ],
    },
    "T con base corta": {
        "kind": "T",
        "matrix": [
            [1, 1, 1],
            [0, 1, 0],
            [0, 0, 0],
        ],
    },
    "T con pixel extra": {
        "kind": "T",
        "matrix": [
            [1, 1, 1],
            [0, 1, 0],
            [1, 1, 0],
        ],
    },
    "Cruz": {
        "kind": "No T",
        "matrix": [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ],
    },
    "L": {
        "kind": "No T",
        "matrix": [
            [1, 0, 0],
            [1, 0, 0],
            [1, 1, 1],
        ],
    },
    "Linea horizontal abajo": {
        "kind": "No T",
        "matrix": [
            [0, 0, 0],
            [0, 1, 0],
            [1, 1, 1],
        ],
    },
}

DEFAULT_WEIGHTS = [
    [2, 2, 2],
    [-1, 3, -1],
    [-1, 3, -1],
]


def copy_matrix(matrix):
    return [row[:] for row in matrix]


def score_image(image, weights):
    total = 0
    terms = []

    for row in range(3):
        for col in range(3):
            pixel = image[row][col]
            weight = weights[row][col]
            product = pixel * weight
            total += product
            terms.append(
                {
                    "posicion": f"x{row + 1}{col + 1}",
                    "pixel": pixel,
                    "peso": weight,
                    "producto": product,
                }
            )

    return total, terms


def init_state():
    if "weights" not in st.session_state:
        st.session_state.weights = copy_matrix(DEFAULT_WEIGHTS)

    if "selected_image" not in st.session_state:
        st.session_state.selected_image = "T perfecta 3x3"

    if "custom_image" not in st.session_state:
        st.session_state.custom_image = copy_matrix(
            IMAGES[st.session_state.selected_image]["matrix"]
        )
        sync_pixel_widgets(st.session_state.custom_image)


def set_image_from_example():
    selected = st.session_state.selected_image
    st.session_state.custom_image = copy_matrix(IMAGES[selected]["matrix"])
    sync_pixel_widgets(st.session_state.custom_image)


def sync_pixel_widgets(matrix):
    for row in range(3):
        for col in range(3):
            st.session_state[f"pixel_{row}_{col}"] = bool(matrix[row][col])


def render_binary_image(matrix):
    html = '<div class="pixel-grid">'
    for row in matrix:
        for value in row:
            class_name = "pixel on" if value else "pixel off"
            html += f'<div class="{class_name}">{value}</div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_weight_matrix(weights):
    html = '<div class="weight-grid">'
    for row in weights:
        for value in row:
            html += f'<div class="weight-cell">{value}</div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_styles():
    st.markdown(
        """
        <style>
            .main .block-container {
                max-width: 1040px;
                padding-top: 2rem;
            }

            .pixel-grid,
            .weight-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(56px, 76px));
                gap: 8px;
                margin: 8px 0 18px;
            }

            .pixel,
            .weight-cell {
                aspect-ratio: 1 / 1;
                border: 1px solid #1f2937;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.4rem;
                font-weight: 700;
            }

            .pixel.on {
                color: #f8fafc;
                background: #111827;
            }

            .pixel.off {
                color: #334155;
                background: #f8fafc;
            }

            .weight-cell {
                color: #111827;
                background: #e0f2fe;
            }

            .result-box {
                border: 1px solid #cbd5e1;
                padding: 16px;
                border-radius: 8px;
                background: #f8fafc;
                margin-top: 8px;
            }

            .score {
                font-size: 2.1rem;
                font-weight: 800;
                color: #0f172a;
                line-height: 1.2;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(page_title="Maquina de puntuacion T", page_icon="T")
    render_styles()
    init_state()

    st.title("Maquina de puntuacion para reconocer una T")
    st.write(
        "Cada pixel se multiplica por un peso. Luego se suman todos los "
        "productos para obtener un puntaje: y = suma(w_i x_i)."
    )

    image_col, controls_col = st.columns([1, 1])

    with image_col:
        st.subheader("Imagen binaria")
        st.selectbox(
            "Ejemplo",
            list(IMAGES.keys()),
            key="selected_image",
            on_change=set_image_from_example,
        )
        st.caption(f"Etiqueta esperada: {IMAGES[st.session_state.selected_image]['kind']}")

        st.write("Activa o apaga pixeles para probar variaciones:")
        for row in range(3):
            cols = st.columns(3)
            for col in range(3):
                with cols[col]:
                    value = st.checkbox(
                        f"x{row + 1}{col + 1}",
                        value=bool(st.session_state.custom_image[row][col]),
                        key=f"pixel_{row}_{col}",
                    )
                    st.session_state.custom_image[row][col] = 1 if value else 0

        render_binary_image(st.session_state.custom_image)

    with controls_col:
        st.subheader("Pesos ajustables")
        st.write("Mueve las perillas para cambiar la importancia de cada posicion.")

        for row in range(3):
            cols = st.columns(3)
            for col in range(3):
                with cols[col]:
                    st.session_state.weights[row][col] = st.slider(
                        f"w{row + 1}{col + 1}",
                        min_value=-5,
                        max_value=5,
                        value=int(st.session_state.weights[row][col]),
                        step=1,
                    )

        render_weight_matrix(st.session_state.weights)

        threshold = st.slider("Threshold de decision", -10, 20, 7, 1)

    score, terms = score_image(st.session_state.custom_image, st.session_state.weights)
    decision = "Probablemente es T" if score >= threshold else "Probablemente NO es T"

    st.divider()
    score_col, calc_col = st.columns([1, 1.4])

    with score_col:
        st.subheader("Resultado")
        st.markdown(
            f"""
            <div class="result-box">
                <div>Puntaje total</div>
                <div class="score">{score}</div>
                <div>Threshold: {threshold}</div>
                <strong>{decision}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("Matriz de pesos actual:")
        st.code(st.session_state.weights, language="python")

    with calc_col:
        st.subheader("Calculo paso a paso")
        st.dataframe(terms, use_container_width=True, hide_index=True)
        expression = " + ".join(str(term["producto"]) for term in terms)
        st.code(f"y = {expression}\ny = {score}", language="text")

    st.divider()
    st.subheader("Preguntas de reflexion")
    st.markdown(
        """
        - Las posiciones mas importantes suelen ser la fila superior y la columna central.
        - Si aumentas pesos en pixeles que pertenecen a la T, las T obtienen mas puntaje.
        - Si aumentas pesos laterales o inferiores, algunas imagenes que no son T pueden confundirse.
        - Las imagenes ambiguas aparecen cuando comparten muchos pixeles con una T, como una cruz.
        - La relacion con aprendizaje es que ajustar numeros cambia la decision de la maquina.
        - Si los pesos estan bien elegidos, una maquina puede reconocer patrones simples usando solo numeros.
        """
    )


if __name__ == "__main__":
    main()
