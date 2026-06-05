# Maquina de puntuacion para reconocer la letra T

Este proyecto implementa una pequena aplicacion interactiva en Streamlit para puntuar mini-imagenes binarias de `3 x 3` y decidir si se parecen a una letra T.

No usa librerias de Machine Learning ni Deep Learning. La decision se calcula manualmente con listas, pesos y operaciones matematicas basicas.

## Como ejecutar

Instalar Streamlit:

```bash
pip install -r requirements.txt
```

Ejecutar la aplicacion:

```bash
streamlit run app.py
```

Luego abrir la URL local que Streamlit muestra en la terminal.

## Funcionamiento

Cada imagen se representa como una matriz binaria:

```text
1 1 1
0 1 0
0 1 0
```

Cada posicion tiene un peso ajustable:

```text
 2  2  2
-1  3 -1
-1  3 -1
```

La maquina calcula el puntaje multiplicando cada pixel por su peso y sumando todos los resultados:

```text
y = sumatoria(wi xi)
```

Si el puntaje es mayor o igual al `threshold`, la aplicacion clasifica la imagen como una posible T. Si no, la clasifica como No T.

## Imagenes incluidas

La aplicacion incluye:

- 3 imagenes tipo T
- 3 imagenes que no son T
- 1 imagen personalizada editable con checkboxes

## Reflexion conceptual

Las partes mas importantes para reconocer una T son la fila superior y la columna central. Si esos pesos son altos, las imagenes tipo T obtienen mayor puntaje.

Cuando se modifican los pesos, cambia la forma en que la maquina interpreta la imagen. Por ejemplo, si se asignan pesos altos a pixeles laterales o inferiores, algunas imagenes que no son T pueden recibir puntajes altos y volverse ambiguas.

Las imagenes ambiguas son aquellas que comparten algunas partes con una T, como una linea vertical central o una cruz. Esto muestra que reconocer patrones no depende de un solo pixel, sino de la combinacion de varios valores.

La relacion con el aprendizaje esta en el ajuste de los pesos. Aunque aqui el estudiante los modifica manualmente, la idea es parecida: cambiar numeros internos para mejorar las decisiones.

Si, una maquina puede reconocer patrones simples ajustando numeros. Para patrones mas complejos se necesitarian mas datos, mas parametros y metodos de entrenamiento mas avanzados.
