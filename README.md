
# Proyecto1-ADAII-ModEx

## Instrucciones de ejecución

### 1. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 2. Iniciar la interfaz gráfica

```bash
python -m streamlit run app.py
```

La aplicación estará disponible en:
http://localhost:8501

## Pruebas automatizadas

Para ejecutar las pruebas unitarias del proyecto:

```bash
python -m unittest discover -s tests -v
```

## Ejecución de la batería oficial

El proyecto incluye un ejecutor automático para los 35 casos
de prueba proporcionados por el profesor.

Para ejecutar la batería desde la raíz del proyecto:

```bash
python tests/run_official_battery.py
```

El programa evalúa los algoritmos, verifica la validez de las
estrategias y genera el archivo
`reports/official_battery_results.csv` con los resultados.

Debido a las diferencias de complejidad, algunas ejecuciones
pueden omitirse o interrumpirse por límites de recursos.

Estos casos se identifican como `SKIPPED` o `TIMEOUT`
y no se consideran pruebas aprobadas.
