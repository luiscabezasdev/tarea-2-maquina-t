# Perceptron Gamificado

Aplicacion interactiva en Streamlit para la tarea de perceptron manual inspirado en la maquina fisica de Welch Labs.

La app usa un perceptron de 2 entradas y bias:

```text
z = x1*w1 + x2*w2 + b
salida = 1 si z >= 0, si no 0
```

No implementa entrenamiento automatico. Los pesos `w1`, `w2` y el bias `b` se ajustan manualmente con sliders.

## Archivos

- `app.py`: aplicacion principal de Streamlit.
- `reporte.md`: plantilla de reporte corto para completar con capturas y reflexion.

## Ejecutar localmente

```bash
pip install streamlit
streamlit run app.py
```

Streamlit abrira una URL local, normalmente:

```text
http://localhost:8501
```

## Desplegar en Streamlit Community Cloud

1. Sube estos archivos a un repositorio de GitHub.
2. Entra a `https://streamlit.io/cloud`.
3. Crea una nueva app.
4. Selecciona el repositorio.
5. En `Main file path`, escribe:

```text
app.py
```

6. Despliega la app y copia el link publico para la entrega.

Nota: no se incluye `requirements.txt` porque Streamlit Community Cloud ya instala `streamlit` por defecto y la app no usa librerias externas.

## Como usar la app

1. Selecciona un problema: AND, OR, NAND, XOR o Personalizado.
2. Cambia las etiquetas deseadas si quieres crear tu propio problema.
3. Ajusta manualmente las perillas `w1`, `w2` y `bias`.
4. Observa en tiempo real:
   - suma ponderada `z`,
   - salida del perceptron,
   - frontera de decision,
   - contador de patrones correctos.
5. Toma capturas cuando logres 4/4 en problemas separables.
6. Prueba XOR y documenta por que no llega a 4/4 con un solo perceptron.
