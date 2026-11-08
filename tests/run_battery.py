import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.models import Agent, SocialNetwork
from algorithms.greedy import modexV

def parse_txt_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    n = int(lines[0])
    agents = []
    for i in range(1, n + 1):
        parts = lines[i].split(',')
        opinion = float(parts[0])
        receptivity = float(parts[1])
        influence = float(parts[2])
        agents.append(Agent(opinion=opinion, receptivity=receptivity, influence=influence))
    
    max_budget = float(lines[n + 1])
    return SocialNetwork(agents=agents, max_budget=max_budget)

def run_battery(directory_path):
    print(f"{'Archivo':<15} {'Agentes (n)':<12} {'Presupuesto':<12} {'Esfuerzo':<10} {'Extremismo':<12} {'Tiempo (s)':<12} {'Estado'}")
    print("-" * 90)
    
    success_count = 0
    total_files = 0
    
    for i in range(1, 36):
        filename = f"Prueba{i}.txt"
        filepath = os.path.join(directory_path, filename)
        
        if not os.path.exists(filepath):
            continue
            
        total_files += 1
        try:
            rs = parse_txt_file(filepath)
            
            start = time.perf_counter()
            E, effort, extremism = modexV(rs)
            elapsed = time.perf_counter() - start
            
            is_valid = effort <= rs.max_budget
            status = "PASS" if is_valid else "FAIL (Presupuesto superado)"
            
            if is_valid:
                success_count += 1
                
            print(f"{filename:<15} {len(rs.agents):<12} {rs.max_budget:<12} {effort:<10} {extremism:<12.2f} {elapsed:<12.6f} {status}")
        except Exception as e:
            print(f"{filename:<15} ERROR: {str(e)}")
            
    print("-" * 90)
    print(f"Pruebas superadas con éxito: {success_count}/{total_files}")

if __name__ == "__main__":
    battery_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../bateria_pruebas'))
    
    run_battery(battery_dir)