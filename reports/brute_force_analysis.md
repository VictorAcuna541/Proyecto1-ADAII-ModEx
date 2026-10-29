# Análisis de fuerza bruta — ModEx

## 1. Descripción

El algoritmo de fuerza bruta (`modexFB`) busca minimizar el extremismo de una red social sin superar el presupuesto disponible.

Para ello, genera todas las combinaciones posibles de agentes que pueden ser moderados y selecciona la estrategia factible que produce el menor extremismo.

## 2. Funcionamiento

1. Inicializa una estrategia donde ningún agente es moderado.
2. Genera las \(2^n\) combinaciones posibles.
3. Calcula el esfuerzo de cada combinación.
4. Descarta las estrategias que superan el presupuesto.
5. Calcula el extremismo de las estrategias válidas.
6. Devuelve la estrategia con el menor extremismo, su esfuerzo y el extremismo resultante.

## 3. Corrección y optimalidad

El algoritmo garantiza una solución óptima porque examina todas las estrategias posibles.

Como solamente descarta aquellas que superan el presupuesto y conserva la estrategia factible de menor extremismo, al finalizar habrá seleccionado una solución óptima.

## 4. Complejidad

**Tiempo:** \(O(n \cdot 2^n)\).

Existen \(2^n\) combinaciones y evaluar cada una requiere recorrer hasta \(n\) agentes.

**Espacio auxiliar:** \(O(n)\).

Las combinaciones se generan iterativamente y únicamente se almacenan la estrategia actual y la mejor encontrada, sin guardar todas las combinaciones.

## 5. Pruebas

La implementación fue verificada mediante 10 pruebas automatizadas con `unittest`, incluyendo los ejemplos oficiales y casos límite.

Todas las pruebas finalizaron correctamente.

## 6. Conclusión

La fuerza bruta garantiza encontrar una estrategia óptima para ModEx, pero su complejidad exponencial limita su uso en redes grandes.

Su principal utilidad en este proyecto es servir como referencia para verificar la optimalidad de los algoritmos voraz y de programación dinámica.