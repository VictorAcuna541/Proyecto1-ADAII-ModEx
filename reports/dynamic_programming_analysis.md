# Análisis de programación dinámica — ModEx

## 1. Formulación

Moderarlo elimina la contribución \(op_i^2 \cdot inf_i\) del extremismo y cuesta
\(c_i = \lceil |op_i|(1-rec_i)inf_i \rceil\). Como la raíz cuadrada y la división
por \(n\) preservan el orden, minimizar el extremismo equivale a maximizar la
suma de contribuciones eliminadas bajo el presupuesto disponible.

## 2. Subproblema y recurrencia

Sea \(DP(i,b)\) el máximo beneficio que se puede obtener usando los primeros
\(i\) agentes con un presupuesto de hasta \(b\). Para el agente \(i\):

\[
DP(i,b) =
\begin{cases}
DP(i-1,b), & c_i > b \\
\max(DP(i-1,b), DP(i-1,b-c_i) + op_i^2 inf_i), & c_i \le b
\end{cases}
\]

La estrategia se reconstruye dividiendo los agentes en dos mitades y buscando
la distribución de presupuesto que maximiza la suma de los beneficios óptimos
de ambas mitades. La recurrencia permite tomar o no tomar cada agente una sola
vez; los agentes de costo cero también se consideran correctamente.

## 3. Corrección

Para cada agente, toda solución factible lo deja sin moderar o lo modera. Si no
se modera, el mejor beneficio es el subproblema anterior con el mismo
presupuesto. Si se modera, se suma su beneficio al mejor subproblema con el
costo restante. La recurrencia considera ambas posibilidades y, por inducción
en el número de agentes, obtiene el beneficio óptimo.

La reconstrucción por mitades prueba todas las distribuciones posibles del
presupuesto entre ambas partes; por tanto recupera una estrategia que alcanza
el valor calculado por la recurrencia.

## 4. Complejidad

Con presupuesto entero \(R\) y \(n\) agentes, el tiempo es \(O(nR)\) en el peor
caso. La reconstrucción usa vectores de beneficios temporales, por lo que el
espacio auxiliar es \(O(R+n)\), incluyendo los datos por agente y la estrategia.
Es una complejidad pseudo-polinomial: entradas con presupuestos muy grandes
pueden ser costosas aunque el número de agentes no cambie.

## 5. Validación

Las pruebas comparan el extremismo resultante de programación dinámica con
fuerza bruta para los ejemplos del enunciado y redes aleatorias pequeñas.
También verifican la factibilidad del presupuesto, redes vacías y moderaciones
de costo cero.
