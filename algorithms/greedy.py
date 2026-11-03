from core.calculations import calculate_effort, calculate_extremism

def modexV(RS):
    
    agents = RS.agents
    n = len(agents)
    r_max = RS.max_budget  
    
    # Lista binaria de moderación inicializada en ceros
    E = [0] * n
    current_effort = 0
    
    # Calcular el extremismo inicial de la red sin moderar a nadie
    initial_extremism = calculate_extremism(RS, E)
    
    agent_metrics = []
    
    for i in range(n):
        # Crear una estrategia temporal moderando únicamente al agente i
        single_E = [0] * n
        single_E[i] = 1
        
        # Calcular esfuerzo y extremismo usando las funciones oficiales
        effort_i = calculate_effort(RS, single_E)
        
        if effort_i > 0:
            extremism_i = calculate_extremism(RS, single_E)
            reduction_i = initial_extremism - extremism_i
            
            # Ratio de beneficio (reducción de extremismo) por unidad de esfuerzo
            ratio = reduction_i / effort_i
        else:
            ratio = float('inf') if effort_i == 0 else 0
            
        agent_metrics.append({
            'index': i,
            'ratio': ratio,
            'effort': effort_i
        })
        
    # Ordenar los agentes de mayor a menor según el criterio voraz (ratio)
    agent_metrics.sort(key=lambda x: x['ratio'], reverse=True)
    
    # Seleccionar vorazmente mientras el presupuesto lo permita
    for item in agent_metrics:
        idx = item['index']
        effort_i = item['effort']
        
        if current_effort + effort_i <= r_max:
            E[idx] = 1
            current_effort += effort_i
            
    # Calcular el extremismo final con la estrategia voraz completa
    final_extremism = calculate_extremism(RS, E)
    
    return (E, current_effort, final_extremism)