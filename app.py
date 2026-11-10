import streamlit as st
import pandas as pd
import time
import math

from core.models import Agent, SocialNetwork
from core.io import parse_input, format_output, social_network_to_input_format, generate_random_network

# Importación de los tres algoritmos
try:
    from algorithms.brute_force import modexFB
except ImportError:
    modexFB = None

try:
    from algorithms.greedy import modexV
except ImportError:
    modexV = None

try:
    from algorithms.dynamic_programming import modexPD
except ImportError:
    modexPD = None


def calculate_initial_extremism(rs: SocialNetwork) -> float:
    n = len(rs.agents)
    if n == 0:
        return 0.0
    s = sum((ag.opinion ** 2) * ag.influence for ag in rs.agents)
    return math.sqrt(s) / n


def get_agent_metrics(ag: Agent):
    cost = math.ceil(abs(ag.opinion) * (1.0 - ag.receptivity) * ag.influence)
    gain = (ag.opinion ** 2) * ag.influence
    ratio = gain / cost if cost > 0 else 0.0
    return cost, gain, ratio


# Configuración de página
st.set_page_config(page_title="ModEx Solver", page_icon="M", layout="wide")
st.title(" ModEx: Moderación de Extremismo en Redes Sociales")
st.markdown("Herramienta interactiva para análisis, comparación y verificación de soluciones.")

# ================= SIDEBAR =================
with st.sidebar:
    st.header(" Carga de Red Social")
    option = st.radio(
        "Seleccione origen:",
        ["Subir archivo .txt", "Generador de casos de prueba", "Ejemplos del enunciado"]
    )

    rs: SocialNetwork = None

    if option == "Subir archivo .txt":
        uploaded_file = st.file_uploader("Seleccione un archivo (.txt)", type=["txt"])
        if uploaded_file is not None:
            try:
                content = uploaded_file.read().decode("utf-8")
                rs = parse_input(content)
                st.success(f"Cargados {len(rs.agents)} agentes exitosamente.")
            except Exception as e:
                st.error(f"Error al leer el archivo: {e}")

    elif option == "Generador de casos de prueba":
        st.subheader("Parámetros del generador")
        n_val = st.slider("Número de agentes (n)", min_value=3, max_value=250, value=12)
        budget_pct = st.slider("Porcentaje de presupuesto disponible", 0.05, 0.90, 0.35, 0.05)
        
        if st.button(" Generar nueva red"):
            rs_gen = generate_random_network(n_val, budget_pct)
            st.session_state["generated_rs"] = rs_gen
        
        if "generated_rs" in st.session_state:
            rs = st.session_state["generated_rs"]
            st.download_button(
                " Descargar caso generado (.txt)",
                data=social_network_to_input_format(rs),
                file_name=f"caso_n{len(rs.agents)}.txt",
                mime="text/plain"
            )

    else: 
        ej = st.selectbox("Seleccione ejemplo:", ["Ejemplo 1 (n=3, R_max=55)", "Ejemplo 2 (n=3, R_max=35)"])
        if ej.startswith("Ejemplo 1"):
            rs = SocialNetwork(
                agents=[
                    Agent(opinion=100, receptivity=0.5, influence=1.0),
                    Agent(opinion=100, receptivity=0.1, influence=1.0),
                    Agent(opinion=-10, receptivity=0.1, influence=1.0),
                ],
                max_budget=55
            )
        else:
            rs = SocialNetwork(
                agents=[
                    Agent(opinion=-30, receptivity=0.9, influence=1.0),
                    Agent(opinion=20, receptivity=0.1, influence=2.0),
                    Agent(opinion=50, receptivity=0.5, influence=1.0),
                ],
                max_budget=35
            )

# ================= CUERPO PRINCIPAL =================
if rs is not None:
    n = len(rs.agents)
    ext_init = calculate_initial_extremism(rs)

    col1, col2, col3 = st.columns(3)
    col1.metric("Número de agentes (n)", n)
    col2.metric("Presupuesto (R_max)", rs.max_budget)
    col3.metric("Extremismo Inicial", f"{ext_init:.4f}")

    with st.expander(" Ver agentes y análisis de costos individuales", expanded=False):
        table_data = []
        for i, ag in enumerate(rs.agents):
            cost, gain, ratio = get_agent_metrics(ag)
            table_data.append({
                "Agente": f"a_{i}",
                "Opinión (o_i)": ag.opinion,
                "Receptividad (r_i)": ag.receptivity,
                "Influencia (inf_i)": ag.influence,
                "Esfuerzo necesario (c_i)": cost,
                "Ganancia de reducción (v_i)": gain,
                "Ratio (v_i / c_i)": round(ratio, 2)
            })
        st.dataframe(pd.DataFrame(table_data), use_container_width=True)

    st.markdown("###  Ejecución de Algoritmos")
    
    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    run_fb = col_b1.button("Fuerza Bruta", disabled=(n > 22))
    run_v = col_b2.button("Voraz")
    run_pd = col_b3.button("Programación Dinámica")
    run_all = col_b4.button(" Comparar los 3", type="primary")

    if n > 22:
        st.warning(" **Fuerza Bruta deshabilitada** para n > 22 para evitar el congelamiento de la aplicación (complejidad O(n · 2^n)).")

    def run_algorithm(func, name):
        if func is None:
            st.error(f"La función {name} no está disponible.")
            return None
        start = time.perf_counter()
        E, effort, ext = func(rs)
        duration = time.perf_counter() - start
        return {
            "Algoritmo": name,
            "E": E,
            "Esfuerzo": effort,
            "Extremismo": ext,
            "Tiempo (s)": duration,
            "Factible": effort <= rs.max_budget
        }

    executions = []

    if run_fb and n <= 22:
        res = run_algorithm(modexFB, "Fuerza Bruta")
        if res: executions.append(res)
    if run_v:
        res = run_algorithm(modexV, "Voraz")
        if res: executions.append(res)
    if run_pd:
        res = run_algorithm(modexPD, "Prog. Dinámica")
        if res: executions.append(res)
    if run_all:
        if n <= 22:
            res_fb = run_algorithm(modexFB, "Fuerza Bruta")
            if res_fb: executions.append(res_fb)
        res_v = run_algorithm(modexV, "Voraz")
        if res_v: executions.append(res_v)
        res_pd = run_algorithm(modexPD, "Prog. Dinámica")
        if res_pd: executions.append(res_pd)

    if executions:
        st.markdown("###  Tabla Comparativa de Resultados")
        
        best_ext = min(e["Extremismo"] for e in executions if e["Factible"])

        summary = []
        for e in executions:
            is_optimal = math.isclose(e["Extremismo"], best_ext, abs_tol=1e-4)
            summary.append({
                "Algoritmo": e["Algoritmo"],
                "Extremismo Obtenido": f"{e['Extremismo']:.4f}",
                "Esfuerzo Invertido": f"{e['Esfuerzo']} / {rs.max_budget}",
                "Factible": " Sí" if e["Factible"] else " No",
                "¿Es Óptimo?": " Óptimo" if is_optimal else "Subóptimo",
                "Agentes Moderados": sum(e["E"]),
                "Tiempo de Ejecución (s)": f"{e['Tiempo (s)']:.6f}"
            })

        st.dataframe(pd.DataFrame(summary), use_container_width=True)

        st.markdown("###  Exportación de Solución Oficial")
        selected_name = st.selectbox("Seleccione el resultado que desea inspeccionar y descargar:", [e["Algoritmo"] for e in executions])
        selected_res = next(e for e in executions if e["Algoritmo"] == selected_name)

        st.write(f"**Estrategia binaria E resultante:** `{selected_res['E']}`")

        out_txt = format_output(selected_res["E"], selected_res["Esfuerzo"], selected_res["Extremismo"])
        
        with st.expander(" Ver contenido del archivo de salida"):
            st.code(out_txt, language="text")

        st.download_button(
            label=f" Descargar salida de {selected_name} (.txt)",
            data=out_txt,
            file_name=f"salida_{selected_name.lower().replace(' ', '_').replace('.', '')}.txt",
            mime="text/plain"
        )
else:
    st.info(" Cargue un archivo `.txt`, use el generador o seleccione un ejemplo en el panel izquierdo para comenzar.")