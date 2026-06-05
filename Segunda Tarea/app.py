import streamlit as st


st.set_page_config(
    page_title="Maquina de puntuacion para reconocer T",
    page_icon="T",
    layout="wide",
)


IMAGENES = {
    "T perfecta": {
        "tipo": "T",
        "matriz": [
            [1, 1, 1],
            [0, 1, 0],
            [0, 1, 0],
        ],
    },
    "T con base corta": {
        "tipo": "T",
        "matriz": [
            [1, 1, 1],
            [0, 1, 0],
            [0, 0, 0],
        ],
    },
    "T alta incompleta": {
        "tipo": "T",
        "matriz": [
            [1, 1, 1],
            [0, 1, 0],
            [1, 1, 0],
        ],
    },
    "Cruz": {
        "tipo": "No T",
        "matriz": [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ],
    },
    "L": {
        "tipo": "No T",
        "matriz": [
            [1, 0, 0],
            [1, 0, 0],
            [1, 1, 1],
        ],
    },
    "Linea vertical": {
        "tipo": "No T",
        "matriz": [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0],
        ],
    },
    "Personalizada": {
        "tipo": "Manual",
        "matriz": [
            [1, 1, 1],
            [0, 1, 0],
            [0, 1, 0],
        ],
    },
}


PESOS_INICIALES = [
    [2, 2, 2],
    [-1, 3, -1],
    [-1, 3, -1],
]


def calcular_puntaje(imagen, pesos):
    puntaje = 0
    detalles = []

    for fila in range(3):
        for columna in range(3):
            pixel = imagen[fila][columna]
            peso = pesos[fila][columna]
            producto = pixel * peso
            puntaje += producto
            detalles.append(
                {
                    "posicion": f"({fila + 1}, {columna + 1})",
                    "pixel": pixel,
                    "peso": peso,
                    "producto": producto,
                }
            )

    return puntaje, detalles


def copiar_matriz(matriz):
    return [[valor for valor in fila] for fila in matriz]


def mostrar_matriz(matriz, titulo):
    st.markdown(f"**{titulo}**")
    html = '<div class="pixel-grid">'
    for fila in matriz:
        for valor in fila:
            clase = "pixel-on" if valor == 1 else "pixel-off"
            html += f'<div class="pixel {clase}">{valor}</div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def mostrar_pesos(pesos):
    st.markdown("**Pesos actuales**")
    html = '<div class="weight-grid">'
    for fila in pesos:
        for valor in fila:
            html += f'<div class="weight-cell">{valor}</div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def construir_sliders_pesos():
    pesos = []
    st.markdown("**Ajusta los pesos**")
    for fila in range(3):
        columnas = st.columns(3)
        fila_pesos = []
        for columna in range(3):
            with columnas[columna]:
                valor = st.slider(
                    f"w{fila + 1}{columna + 1}",
                    min_value=-5,
                    max_value=8,
                    value=PESOS_INICIALES[fila][columna],
                    step=1,
                )
                fila_pesos.append(valor)
        pesos.append(fila_pesos)
    return pesos


def construir_imagen_personalizada(matriz_base):
    matriz = copiar_matriz(matriz_base)
    st.markdown("**Edita la imagen personalizada**")
    for fila in range(3):
        columnas = st.columns(3)
        for columna in range(3):
            with columnas[columna]:
                activo = st.checkbox(
                    f"x{fila + 1}{columna + 1}",
                    value=bool(matriz[fila][columna]),
                )
                matriz[fila][columna] = 1 if activo else 0
    return matriz


def formatear_calculo(detalles):
    terminos = []
    for detalle in detalles:
        terminos.append(f"({detalle['pixel']} x {detalle['peso']})")
    return " + ".join(terminos)


st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .pixel-grid,
    .weight-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(58px, 86px));
        gap: 8px;
        margin: 10px 0 18px;
    }
    .pixel,
    .weight-cell {
        aspect-ratio: 1;
        border: 1px solid #9aa4b2;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.45rem;
        font-weight: 700;
        border-radius: 6px;
    }
    .pixel-on {
        background: #1f2937;
        color: white;
    }
    .pixel-off {
        background: #f8fafc;
        color: #475569;
    }
    .weight-cell {
        background: #f1f5f9;
        color: #0f172a;
    }
    .formula-box {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 12px;
        font-family: monospace;
        overflow-wrap: anywhere;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("Maquina de puntuacion para reconocer la letra T")
st.write(
    "Cada imagen es una matriz binaria de 3 x 3. La maquina multiplica cada pixel por un peso, suma los productos y compara el puntaje con un threshold."
)

with st.sidebar:
    st.header("Controles")
    nombre_imagen = st.selectbox("Imagen de prueba", list(IMAGENES.keys()))
    threshold = st.slider("Threshold", min_value=-10, max_value=25, value=8, step=1)
    st.caption("Si el puntaje es mayor o igual al threshold, la maquina dice que parece una T.")

    pesos = construir_sliders_pesos()

imagen = copiar_matriz(IMAGENES[nombre_imagen]["matriz"])
tipo_real = IMAGENES[nombre_imagen]["tipo"]

if nombre_imagen == "Personalizada":
    with st.sidebar:
        imagen = construir_imagen_personalizada(imagen)

puntaje, detalles = calcular_puntaje(imagen, pesos)
clasificacion = "Parece una T" if puntaje >= threshold else "No parece una T"

col_izquierda, col_centro, col_derecha = st.columns([1, 1, 1.2])

with col_izquierda:
    mostrar_matriz(imagen, f"Imagen seleccionada: {nombre_imagen}")
    st.write(f"Etiqueta real: **{tipo_real}**")

with col_centro:
    mostrar_pesos(pesos)
    st.write("Formula usada: **y = sumatoria(wi xi)**")

with col_derecha:
    st.metric("Puntaje total", puntaje)
    st.metric("Threshold", threshold)
    if clasificacion == "Parece una T":
        st.success(clasificacion)
    else:
        st.warning(clasificacion)

st.divider()

st.subheader("Calculo paso a paso")
st.markdown(f'<div class="formula-box">{formatear_calculo(detalles)} = {puntaje}</div>', unsafe_allow_html=True)

tabla_detalles = []
for detalle in detalles:
    tabla_detalles.append(
        {
            "Posicion": detalle["posicion"],
            "Pixel x": detalle["pixel"],
            "Peso w": detalle["peso"],
            "x * w": detalle["producto"],
        }
    )
st.table(tabla_detalles)

st.subheader("Comparacion con todas las imagenes")
comparacion = []
for nombre, datos in IMAGENES.items():
    if nombre == "Personalizada":
        continue
    puntaje_imagen, _ = calcular_puntaje(datos["matriz"], pesos)
    comparacion.append(
        {
            "Imagen": nombre,
            "Tipo real": datos["tipo"],
            "Puntaje": puntaje_imagen,
            "Decision": "T" if puntaje_imagen >= threshold else "No T",
        }
    )
st.table(comparacion)

st.subheader("Guia de observacion")
st.write(
    "- Los pesos de la fila superior y de la columna central suelen ser los mas importantes para reconocer una T."
)
st.write(
    "- Si aumentas los pesos de posiciones que una T real tiene encendidas, su puntaje sube."
)
st.write(
    "- Si aumentas pesos en posiciones laterales o inferiores, algunas figuras que no son T pueden volverse ambiguas."
)
st.write(
    "- Esta actividad se relaciona con el aprendizaje porque ajustar pesos cambia la decision de la maquina."
)
