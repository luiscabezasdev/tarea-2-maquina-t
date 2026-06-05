# Tarea 2 - Maquina que reconoce patrones

Esta solucion implementa una aplicacion interactiva en Streamlit para asignar
puntajes a mini-imagenes binarias de 3x3 y estimar si se parecen a una letra T.

No se usan librerias de Machine Learning ni Deep Learning. La clasificacion se
calcula manualmente con listas, matrices y operaciones aritmeticas basicas.

## Como ejecutar

```bash
streamlit run app.py
```

Si Streamlit no esta instalado:

```bash
pip install streamlit
streamlit run app.py
```

## Funcionamiento

Cada imagen es una matriz binaria. Un `1` representa un pixel activo y un `0`
representa un pixel apagado.

Ejemplo de T:

```text
1 1 1
0 1 0
0 1 0
```

Cada posicion tiene un peso ajustable:

```python
[
    [2, 2, 2],
    [-1, 3, -1],
    [-1, 3, -1],
]
```

La aplicacion calcula:

```text
y = suma(w_i x_i)
```

Es decir, multiplica cada pixel por su peso y suma los resultados. Tambien
permite ajustar un threshold para decidir si el puntaje es suficiente para
clasificar la imagen como una T.

## Imagenes incluidas

Imagenes tipo T:

- T perfecta 3x3
- T con base corta
- T con pixel extra

Imagenes que no son T:

- Cruz
- L
- Linea horizontal abajo

## Reflexion conceptual

Las partes mas importantes de la imagen son la fila superior y la columna
central, porque forman la estructura principal de una T. Cuando se aumentan sus
pesos, las imagenes que tienen esa forma reciben mayor puntaje.

Modificar ciertos pesos cambia directamente la decision. Por ejemplo, si se
asignan pesos altos a las esquinas inferiores, una figura que no es T podria
recibir un puntaje alto por error. Las imagenes ambiguas suelen ser las que
comparten varios pixeles con una T, como una cruz.

La actividad se relaciona con la idea de aprendizaje porque muestra que una
maquina puede cambiar su comportamiento ajustando numeros. En este caso el
ajuste es manual; en un sistema de aprendizaje real, esos pesos se ajustarian
automaticamente a partir de ejemplos.

Una maquina si puede reconocer patrones simples usando solo numeros, siempre
que la representacion y los pesos sean adecuados para el patron buscado.
