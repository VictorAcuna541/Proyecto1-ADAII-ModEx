# 6. Solución mediante programación dinámica

## 6.1. Idea de la solución

La programación dinámica transforma el problema en una variante de la mochila
0/1. Cada agente representa un elemento que se puede seleccionar como máximo
una vez: moderarlo consume parte del presupuesto y reduce el extremismo de la
red.

Para un agente \(i\), el costo de moderación es

\[
c_i = \left\lceil |op_i|(1-rec_i)inf_i \right\rceil
\]

y el beneficio obtenido al moderarlo es la contribución que deja de aportar al
extremismo:

\[
b_i = op_i^2 \cdot inf_i.
\]

En efecto, para una estrategia \(E\), el extremismo es

\[
Ext(RS,E) =
\frac{1}{n}\sqrt{\sum_{i=0}^{n-1}(op_i(1-E_i))^2inf_i}.
\]

La raíz cuadrada y la división por \(n\) son funciones crecientes. Por tanto,
minimizar el extremismo equivale a maximizar la suma de los beneficios de los
agentes moderados, sujeto a que el esfuerzo total no supere \(R_{max}\).

## 6.2. Subproblema y recurrencia

Sea \(DP(i,r)\) el máximo beneficio que se puede obtener usando los primeros
\(i\) agentes, con un presupuesto disponible de hasta \(r\). El caso base es
\(DP(0,r)=0\): sin agentes no se puede obtener beneficio.

Para cada agente existen dos posibilidades:

- No moderarlo: se conserva el mejor beneficio \(DP(i-1,r)\).
- Moderarlo, si su costo cabe en el presupuesto: se suma \(b_i\) al mejor
  beneficio obtenido con el presupuesto restante \(DP(i-1,r-c_i)\).

Así, la recurrencia es

\[
DP(i,r) =
\begin{cases}
DP(i-1,r), & c_i > r,\\
\max(DP(i-1,r),\ DP(i-1,r-c_i)+b_i), & c_i \le r.
\end{cases}
\]

La implementación calcula estos valores con un vector unidimensional,
actualizando los presupuestos en orden descendente. Esto evita reutilizar un
mismo agente más de una vez. Para reconstruir la estrategia sin almacenar toda
la tabla de decisiones, divide recursivamente los agentes en dos mitades y
elige la distribución del presupuesto que maximiza la suma de los beneficios
de ambas partes.

## 6.3. Algoritmo

1. Calcular para cada agente su costo \(c_i\) y su beneficio \(b_i\).
2. Limitar el presupuesto de trabajo a
   \(\min(\lfloor R_{max}\rfloor,\sum_i c_i)\), ya que no se puede gastar más
   que el costo de moderar a todos los agentes.
3. Calcular los beneficios alcanzables para cada mitad de agentes y cada
   presupuesto posible.
4. Encontrar la distribución de presupuesto entre las mitades que maximiza el
   beneficio total.
5. Repetir el proceso en cada mitad hasta identificar los agentes que se deben
   moderar.
6. Calcular y devolver la estrategia, el esfuerzo utilizado y el extremismo
   resultante.

La función `modexPD(RS)` devuelve la misma estructura que las otras soluciones:
\((E,\ Esfuerzo(RS,E),\ Ext(Mod(RS,E)))\).

## 6.4. Correctitud y optimalidad

La recurrencia considera todas las alternativas posibles para el agente
actual: moderarlo o no moderarlo. En cada caso, utiliza la mejor solución del
subproblema correspondiente. Por inducción sobre la cantidad de agentes,
\(DP(i,r)\) contiene el beneficio máximo alcanzable con los primeros \(i\)
agentes y presupuesto \(r\).

La reconstrucción por mitades prueba las distribuciones de presupuesto que
pueden asignarse a cada mitad y escoge la que logra el beneficio máximo. Por
ello recupera una estrategia factible que alcanza el óptimo calculado por la
recurrencia. Como maximizar el beneficio eliminado equivale a minimizar el
extremismo restante, la estrategia devuelta es óptima para el problema.

Los agentes con costo cero también se consideran: la actualización descendente
los incorpora una vez y no aumenta el presupuesto utilizado. Si la red está
vacía, el algoritmo devuelve una estrategia vacía, esfuerzo cero y extremismo
cero.

## 6.5. Complejidad

Sea \(n\) el número de agentes y \(R\) el presupuesto entero efectivo usado por
el algoritmo.

El cálculo de beneficios para un intervalo de agentes y una capacidad dada
cuesta \(O(nR)\) en el peor caso. La reconstrucción divide los agentes en dos
mitades y repite esos cálculos en cada nivel recursivo; por tanto, el tiempo
total de esta implementación es \(O(nR\log n)\) en el peor caso.

Los vectores de beneficios temporales ocupan \(O(R)\) espacio y la estrategia,
los costos, los beneficios y las sumas prefijas ocupan \(O(n)\). Como los
vectores temporales se liberan antes de continuar con la recursión, el espacio
total es \(O(R+n)\).

La complejidad es pseudo-polinomial: depende del valor numérico del presupuesto,
no solo de la cantidad de agentes. Por ello, aunque es mucho más apropiada que
fuerza bruta para redes grandes con presupuestos moderados, puede resultar
costosa cuando el presupuesto efectivo es muy alto.

## 6.6. Validación y resultados

La implementación se probó con los dos ejemplos del enunciado y con casos
especiales, incluyendo una red vacía y agentes cuya moderación tiene costo
cero. Además, se comparó el extremismo obtenido por programación dinámica
contra fuerza bruta en 40 redes pequeñas generadas de forma reproducible. En
esas pruebas, ambas soluciones obtuvieron el mismo extremismo óptimo y la
estrategia de programación dinámica respetó el presupuesto.

| Caso | Estrategia \(E\) | Esfuerzo | Extremismo |
|---|---|---:|---:|
| Ejemplo 1 | \([1,0,0]\) | 50 | 33.50 |
| Ejemplo 2 | \([1,0,1]\) | 28 | 9.43 |

No se incluyen tiempos experimentales de programación dinámica porque no se
realizó un benchmark sistemático de este algoritmo. Sus tiempos dependen tanto
del número de agentes como del presupuesto efectivo.

## 6.7. Conclusión

La programación dinámica encuentra una solución óptima y, a diferencia de
fuerza bruta, no enumera explícitamente las \(2^n\) estrategias posibles.
Su principal limitación es que el tiempo y el espacio dependen del presupuesto:
si este crece mucho, los vectores de estados también crecen. Frente al enfoque
voraz, ofrece garantía de optimalidad, a cambio de un mayor costo
computacional.
