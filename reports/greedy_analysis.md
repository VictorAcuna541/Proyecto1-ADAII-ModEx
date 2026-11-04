# Análisis de la Solución Voraz - Proyecto ModEx

## 1. Descripción de la estrategia

El algoritmo voraz (`modexV`) implementa una estrategia heurística basada en la optimización local de la relación **beneficio/esfuerzo**. El procedimiento consta de las siguientes etapas:

1. **Evaluación marginal individual:** Para cada agente de la red, se calcula de manera independiente el esfuerzo requerido para moderarlo ($effort_i$) utilizando las funciones oficiales del módulo `core/calculations.py`.
2. **Cálculo de reducción de extremismo:** Se evalúa cuánto disminuye el extremismo global de la red al moderar únicamente a ese agente frente al extremismo inicial de la red sin moderación reducción_i = Extremismo inicial - Extremismo con agente i
3. **Criterio voraz (Ratio):** Se calcula un ratio de eficiencia para cada agente dividiendo la reducción de extremismo obtenida entre el esfuerzo consumido ratio_i = reducción_i / effort_i
4. **Selección iterativa:** Se ordenan los agentes de mayor a menor según su ratio de eficiencia. Posteriormente, se recorre la lista ordenada seleccionando (marcando con `1`) a los agentes de mayor beneficio marginal, acumulando el costo de moderación de forma que **nunca se supere el presupuesto máximo disponible ($R_{max}$)**.

Esta aproximación permite tomar decisiones rápidas priorizando a los agentes que ofrecen el mayor impacto de moderación al menor costo posible en recursos.

---

## 2. Complejidad temporal y espacial

* **Complejidad temporal (**O(n log n)**):** 
  El cálculo de las métricas individuales para los $n$ agentes toma un tiempo lineal O(n log n) El paso computacionalmente dominante es el **ordenamiento** de los agentes en función de su ratio de beneficio/esfuerzo, el cual requiere O(n log n) utilizando algoritmos de ordenamiento eficientes (como Timsort en Python). El ciclo final de selección toma tiempo lineal O(n). Por lo tanto, la complejidad temporal total es $\mathcal{O}(n \log n)$.

* **Complejidad espacial **O(n)**:** 
  El algoritmo almacena la lista binaria de resultados $E$ de tamaño $n$, una estructura auxiliar para guardar las métricas de los agentes (índice, ratio y esfuerzo) y variables de control que escalan linealmente con el número de agentes. Por ende, el uso de memoria es de O(n).

---

## 3. Optimalidad y viabilidad práctica

### ¿Garantiza una solución óptima?
**No necesariamente.** Al ser un enfoque voraz (*greedy*), el algoritmo toma decisiones óptimas a nivel local en cada paso basándose en la relación marginal inmediata, sin evaluar combinaciones globales de agentes. Debido a la naturaleza combinatoria no lineal del cálculo del extremismo de la red, la selección voraz puede dejar fuera combinaciones de agentes que en conjunto producirían un extremismo menor que el obtenido al elegir de manera estrictamente voraz. Por lo tanto, **no garantiza siempre el óptimo global** (a diferencia del algoritmo de fuerza bruta).

### Viabilidad práctica
A pesar de no asegurar la optimalidad en todos los escenarios, la solución voraz destaca por su **extraordinaria eficiencia computacional**. Mientras que la fuerza bruta presenta un crecimiento exponencial O(n * 2^n) que se vuelve intratable para redes con más de 18 o 20 agentes, el algoritmo voraz procesa redes de miles de agentes en fracciones de segundo (por ejemplo, redes de 1,000 agentes en aproximadamente $0.34$ segundos). Esto lo convierte en una herramienta altamente viable y útil en entornos reales con grafos y redes sociales de gran escala.

---

## 4. Pruebas y rendimiento experimental

El algoritmo fue validado exhaustivamente mediante una suite de pruebas automatizadas en `unittest`, verificando el cumplimiento estricto del contrato de la función (`modexV(RS)` retornando la tupla `(E, esfuerzo, extremismo)`), la consistencia matemática con los ejemplos oficiales del curso y el respeto riguroso del presupuesto máximo.

### Resultados de rendimiento comparativo:
Las pruebas de desempeño experimental demuestran el comportamiento del tiempo de ejecución frente al tamaño de la red ($n$):

| Agentes ($n$) | Tiempo de ejecución voraz (s) |
| :--- | :--- |
| 10 | $0.000102$ |
| 100 | $0.003322$ |
| 1,000 | $0.342145$ |

Los resultados confirman que el algoritmo escala de forma casi lineal-logarítmica, validando su robustez y su utilidad práctica frente a enfoques combinatorios exactos pero computacionalmente prohibitivos.