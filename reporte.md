# Reporte corto: Perceptron Gamificado

## 1. Objetivo

El objetivo fue construir una aplicacion interactiva para entender como funciona un perceptron de dos entradas. La app permite modificar manualmente los pesos `w1`, `w2` y el bias, observar la suma ponderada y visualizar la frontera de decision en el plano 2D.

## 2. Problema resuelto facilmente

Problema elegido: AND.

Captura: pegar aqui una captura de la app cuando el contador marque 4/4.

Explicacion breve:

El problema AND se resolvio facilmente porque sus puntos son linealmente separables. La combinacion `(1, 1)` pertenece a la clase positiva y las otras tres combinaciones pertenecen a la clase negativa. Una linea puede separar ese punto de los demas.

Un ejemplo de configuracion que suele funcionar:

```text
w1 = 1.0
w2 = 1.0
b  = -1.5
```

## 3. Segundo problema resuelto

Problema elegido: OR o NAND.

Captura: pegar aqui una captura de la app cuando el contador marque 4/4.

Explicacion breve:

Este problema tambien es linealmente separable, por lo que una sola frontera de decision puede dividir correctamente los patrones positivos y negativos.

## 4. Problema que no pude resolver

Problema elegido: XOR.

Captura: pegar aqui una captura donde se vea que el contador no llega a 4/4.

Explicacion:

XOR no puede resolverse con un unico perceptron porque sus clases no son linealmente separables. Los puntos positivos son `(0, 1)` y `(1, 0)`, mientras que los negativos son `(0, 0)` y `(1, 1)`. No existe una sola linea recta que separe esos dos grupos sin cometer errores.

## 5. Reflexion personal

Al mover manualmente las perillas se entiende que una maquina aprende ajustando parametros. Cada peso cambia la importancia de una entrada y el bias mueve la frontera de decision. Cuando los pesos son adecuados, el perceptron clasifica correctamente los patrones. Sin embargo, tambien se observa una limitacion importante: un perceptron simple solo puede resolver problemas separables linealmente. Para problemas como XOR se necesitan modelos con mas capas o transformaciones adicionales.
