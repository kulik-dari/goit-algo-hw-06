"""
Завдання 3: Реалізація алгоритму Дейкстри для пошуку найкоротших шляхів

Додавання ваг до ребер графа та реалізація алгоритму Дейкстри
для знаходження найкоротших шляхів між всіма парами вершин.
"""

import networkx as nx
import matplotlib.pyplot as plt
import heapq
import numpy as np
import pandas as pd
from collections import defaultdict
import time

def load_and_prepare_weighted_graph():
    """
    Завантажує граф та додає/оновлює ваги ребер на основі відстані та типу транспорту.
    
    Returns:
        nx.Graph: Граф з вагами
    """
    try:
        G = nx.read_gml("city_transport_network.gml")
        print("✅ Граф завантажено з файлу")
    except FileNotFoundError:
        print("⚠️  Файл графа не знайдено, створюємо новий...")
        G = create_city_transport_network()
        nx.write_gml(G, "city_transport_network.gml")
    
    # Додаємо/оновлюємо ваги на основі відстані та типу транспорту
    for edge in G.edges():
        if 'distance' in G.edges[edge]:
            distance = G.edges[edge]['distance']
            transport_type = G.edges[edge].get('transport_type', 'bus')
            
            # Коефіцієнти для різних типів транспорту (час подорожі)
            transport_coefficients = {
                'metro': 1.0,    # Найшвидший
                'train': 1.2,    # Трохи повільніше через зупинки
                'bus': 1.8       # Найповільніше через трафік
            }
            
            # Обчислюємо вагу як час подорожі
            coefficient = transport_coefficients.get(transport_type, 1.5)
            weight = distance * coefficient
            
            G.edges[edge]['weight'] = weight
            G.edges[edge]['travel_time'] = weight  # час у хвилинах
        else:
            # Якщо відстань не вказана, встановлюємо базову вагу
            G.edges[edge]['weight'] = 5.0
            G.edges[edge]['travel_time'] = 5.0
    
    return G

def create_city_transport_network():
    """
    Створює граф транспортної мережі міста (копія для незалежності).
    """
    G = nx.Graph()
    
    stations = {
        'Центральна площа': {'district': 'Центр', 'type': 'metro', 'population': 50000},
        'Театральна': {'district': 'Центр', 'type': 'metro', 'population': 30000},
        'Університет': {'district': 'Центр', 'type': 'metro', 'population': 40000},
        'Північний вокзал': {'district': 'Північ', 'type': 'train', 'population': 35000},
        'Озерна': {'district': 'Північ', 'type': 'bus', 'population': 25000},
        'Лісопарк': {'district': 'Північ', 'type': 'bus', 'population': 15000},
        'Промислова': {'district': 'Схід', 'type': 'metro', 'population': 45000},
        'Заводська': {'district': 'Схід', 'type': 'bus', 'population': 20000},
        'Нова забудова': {'district': 'Схід', 'type': 'bus', 'population': 30000},
        'Аеропорт': {'district': 'Захід', 'type': 'train', 'population': 25000},
        'Торговий центр': {'district': 'Захід', 'type': 'metro', 'population': 40000},
        'Спортивний комплекс': {'district': 'Захід', 'type': 'bus', 'population': 20000},
        'Річковий порт': {'district': 'Південь', 'type': 'train', 'population': 30000},
        'Ринок': {'district': 'Південь', 'type': 'bus', 'population': 35000},
        'Житловий масив': {'district': 'Південь', 'type': 'bus', 'population': 40000}
    }
    
    for station, attributes in stations.items():
        G.add_node(station, **attributes)
    
    connections = [
        ('Центральна площа', 'Театральна', 'metro', 2.5),
        ('Центральна площа', 'Університет', 'metro', 3.0),
        ('Театральна', 'Університет', 'bus', 1.8),
        ('Центральна площа', 'Північний вокзал', 'metro', 4.5),
        ('Центральна площа', 'Промислова', 'metro', 5.2),
        ('Центральна площа', 'Торговий центр', 'metro', 6.0),
        ('Центральна площа', 'Річковий порт', 'bus', 7.5),
        ('Північний вокзал', 'Озерна', 'bus', 3.5),
        ('Озерна', 'Лісопарк', 'bus', 2.8),
        ('Північний вокзал', 'Лісопарк', 'train', 5.0),
        ('Промислова', 'Заводська', 'bus', 2.2),
        ('Заводська', 'Нова забудова', 'bus', 3.1),
        ('Промислова', 'Нова забудова', 'metro', 4.0),
        ('Торговий центр', 'Аеропорт', 'train', 8.5),
        ('Торговий центр', 'Спортивний комплекс', 'bus', 2.7),
        ('Аеропорт', 'Спортивний комплекс', 'bus', 6.3),
        ('Річковий порт', 'Ринок', 'bus', 2.0),
        ('Ринок', 'Житловий масив', 'bus', 2.5),
        ('Річковий порт', 'Житловий масив', 'train', 4.2),
        ('Університет', 'Промислова', 'bus', 4.8),
        ('Театральна', 'Торговий центр', 'bus', 5.5),
        ('Північний вокзал', 'Аеропорт', 'train', 12.0),
        ('Озерна', 'Спортивний комплекс', 'bus', 8.2),
        ('Заводська', 'Ринок', 'bus', 6.5),
        ('Нова забудова', 'Житловий масив', 'bus', 5.8),
    ]
    
    for station1, station2, transport_type, distance in connections:
        G.add_edge(station1, station2, 
                  transport_type=transport_type, 
                  distance=distance,
                  weight=distance)
    
    return G

def dijkstra_algorithm(graph, start):
    """
    Реалізація алгоритму Дейкстри для пошуку найкоротших шляхів від заданої вершини.
    
    Args:
        graph (nx.Graph): Зважений граф
        start (str): Початкова вершина
        
    Returns:
        tuple: (відстані, попередники, статистика)
    """
    # Ініціалізація
    distances = {node: float('infinity') for node in graph.nodes()}
    distances[start] = 0
    predecessors = {node: None for node in graph.nodes()}
    visited = set()
    
    # Купа для ефективного вибору наступної вершини
    heap = [(0, start)]
    iterations = 0
    
    start_time = time.time()
    
    while heap:
        iterations += 1
        current_distance, current = heapq.heappop(heap)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        # Перевіряємо всіх сусідів
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                # Отримуємо вагу ребра
                edge_weight = graph.edges[current, neighbor]['weight']
                new_distance = current_distance + edge_weight
                
                # Якщо знайшли коротший шлях
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current
                    heapq.heappush(heap, (new_distance, neighbor))
    
    end_time = time.time()
    
    stats = {
        'iterations': iterations,
        'execution_time': end_time - start_time,
        'nodes_processed': len(visited),
        'reachable_nodes': sum(1 for d in distances.values() if d != float('infinity'))
    }
    
    return distances, predecessors, stats

def reconstruct_path(predecessors, start, end):
    """
    Відновлює шлях від початкової до кінцевої вершини.
    
    Args:
        predecessors (dict): Словник попередників
        start (str): Початкова вершина
        end (str): Кінцева вершина
        
    Returns:
        list: Шлях від start до end
    """
    path = []
    current = end
    
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    path.reverse()
    
    # Перевіряємо, чи дійсно знайдено шлях
    if path[0] != start:
        return None
    
    return path

def find_all_shortest_paths(graph):
    """
    Знаходить найкоротші шляхи між всіма парами вершин.
    
    Args:
        graph (nx.Graph): Зважений граф
        
    Returns:
        dict: Словник з результатами для всіх пар вершин
    """
    all_paths = {}
    all_distances = {}
    nodes = list(graph.nodes())
    total_pairs = len(nodes) * (len(nodes) - 1)
    
    print(f"🔄 Обчислюємо найкоротші шляхи для {total_pairs} пар вершин...")
    
    for i, start in enumerate(nodes):
        print(f"   Обробка вершини {i+1}/{len(nodes)}: {start}")
        
        distances, predecessors, _ = dijkstra_algorithm(graph, start)
        
        for end in nodes:
            if start != end and distances[end] != float('infinity'):
                path = reconstruct_path(predecessors, start, end)
                if path:
                    all_paths[(start, end)] = path
                    all_distances[(start, end)] = distances[end]
    
    return all_paths, all_distances

def visualize_shortest_path(graph, start, end, path, distances):
    """
    Візуалізує найкоротший шлях між двома вершинами.
    """
    plt.figure(figsize=(14, 10))
    
    pos = nx.spring_layout(graph, k=3, iterations=50, seed=42)
    
    # Кольори вершин на основі відстані від початкової точки
    node_colors = []
    max_distance = max(d for d in distances.values() if d != float('infinity'))
    
    for node in graph.nodes():
        if node == start:
            node_colors.append('#FF4444')  # Червоний для початку
        elif node == end:
            node_colors.append('#44FF44')  # Зелений для кінця
        elif path and node in path:
            node_colors.append('#4444FF')  # Синій для шляху
        else:
            # Градієнт на основі відстані
            if distances[node] == float('infinity'):
                node_colors.append('#CCCCCC')  # Сірий для недосяжних
            else:
                intensity = 1 - (distances[node] / max_distance)
                node_colors.append(plt.cm.YlOrRd(intensity))
    
    # Малюємо всі ребра
    nx.draw_networkx_edges(graph, pos, edge_color='lightgray', width=1, alpha=0.3)
    
    # Виділяємо ребра найкоротшого шляху
    if path and len(path) > 1:
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        
        # Різні кольори для різних типів транспорту в шляху
        for edge in path_edges:
            transport_type = graph.edges[edge]['transport_type']
            if transport_type == 'metro':
                color = '#2C3E50'
                width = 4
            elif transport_type == 'train':
                color = '#8E44AD'
                width = 3.5
            else:  # bus
                color = '#E67E22'
                width = 3
            
            nx.draw_networkx_edges(graph, pos, edgelist=[edge],
                                 edge_color=color, width=width, alpha=0.9)
    
    # Малюємо вершини
    nx.draw_networkx_nodes(graph, pos,
                         node_color=node_colors,
                         node_size=600,
                         alpha=0.8,
                         edgecolors='black',
                         linewidths=1.5)
    
    # Додаємо підписи з відстанями
    labels = {}
    for node in graph.nodes():
        if distances[node] == float('infinity'):
            labels[node] = f"{node[:8]}...\n∞"
        else:
            labels[node] = f"{node[:8]}...\n{distances[node]:.1f}"
    
    nx.draw_networkx_labels(graph, pos, labels,
                          font_size=7,
                          font_weight='bold')
    
    # Додаємо ваги ребер для шляху
    if path and len(path) > 1:
        edge_labels = {}
        for i in range(len(path)-1):
            edge = (path[i], path[i+1])
            weight = graph.edges[edge]['weight']
            edge_labels[edge] = f"{weight:.1f}"
        
        nx.draw_networkx_edge_labels(graph, pos, edge_labels,
                                   font_size=8, font_color='red')
    
    total_distance = distances[end] if distances[end] != float('infinity') else "∞"
    plt.title(f'Найкоротший шлях від "{start}" до "{end}"\n'
              f'Загальна відстань: {total_distance}\n'
              f'Шлях: {" → ".join(path) if path else "Не знайдено"}',
              fontsize=12, fontweight='bold')
    
    # Легенда
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF4444', 
                  markersize=10, label='Початок'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#44FF44', 
                  markersize=10, label='Кінець'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4444FF', 
                  markersize=10, label='Шлях'),
        plt.Line2D([0], [0], color='#2C3E50', linewidth=4, label='Метро'),
        plt.Line2D([0], [0], color='#8E44AD', linewidth=3.5, label='Поїзд'),
        plt.Line2D([0], [0], color='#E67E22', linewidth=3, label='Автобус')
    ]
    plt.legend(handles=legend_elements, loc='upper left')
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def create_distance_matrix(graph, all_distances):
    """
    Створює матрицю відстаней між всіма парами вершин.
    
    Args:
        graph (nx.Graph): Граф
        all_distances (dict): Відстані між всіма парами
        
    Returns:
        pd.DataFrame: Матриця відстаней
    """
    nodes = list(graph.nodes())
    matrix = np.full((len(nodes), len(nodes)), np.inf)
    
    # Заповнюємо матрицю
    for i, start in enumerate(nodes):
        matrix[i, i] = 0  # Відстань до самого себе = 0
        for j, end in enumerate(nodes):
            if (start, end) in all_distances:
                matrix[i, j] = all_distances[(start, end)]
    
    # Створюємо DataFrame для красивого відображення
    df = pd.DataFrame(matrix, index=nodes, columns=nodes)
    return df

def analyze_shortest_paths(graph, all_paths, all_distances):
    """
    Аналізує результати пошуку найкоротших шляхів.
    
    Args:
        graph (nx.Graph): Граф
        all_paths (dict): Всі знайдені шляхи
        all_distances (dict): Всі відстані
    """
    print("\n" + "="*80)
    print("📊 АНАЛІЗ НАЙКОРОТШИХ ШЛЯХІВ (АЛГОРИТМ ДЕЙКСТРИ)")
    print("="*80)
    
    # Загальна статистика
    total_possible_paths = len(graph.nodes()) * (len(graph.nodes()) - 1)
    found_paths = len(all_paths)
    
    print(f"\n📈 Загальна статистика:")
    print(f"   • Загальна кількість можливих шляхів: {total_possible_paths}")
    print(f"   • Знайдено шляхів: {found_paths}")
    print(f"   • Відсоток досяжності: {(found_paths/total_possible_paths)*100:.1f}%")
    
    # Аналіз довжин шляхів
    if all_distances:
        distances_list = list(all_distances.values())
        avg_distance = np.mean(distances_list)
        min_distance = min(distances_list)
        max_distance = max(distances_list)
        
        print(f"\n📏 Аналіз відстаней:")
        print(f"   • Середня відстань: {avg_distance:.2f}")
        print(f"   • Мінімальна відстань: {min_distance:.2f}")
        print(f"   • Максимальна відстань: {max_distance:.2f}")
        
        # Знаходимо найкоротший та найдовший шляхи
        min_path = min(all_distances.keys(), key=lambda x: all_distances[x])
        max_path = max(all_distances.keys(), key=lambda x: all_distances[x])
        
        print(f"   • Найкоротший шлях: {min_path[0]} → {min_path[1]} ({min_distance:.2f})")
        print(f"   • Найдовший шлях: {max_path[0]} → {max_path[1]} ({max_distance:.2f})")
    
    # Аналіз центральності станцій
    print(f"\n🎯 Аналіз доступності станцій:")
    
    # Підрахунок кількості шляхів від кожної станції
    outgoing_paths = defaultdict(int)
    incoming_paths = defaultdict(int)
    avg_outgoing_distance = defaultdict(list)
    
    for (start, end), distance in all_distances.items():
        outgoing_paths[start] += 1
        incoming_paths[end] += 1
        avg_outgoing_distance[start].append(distance)
    
    # Топ-5 найбільш доступних станцій (з яких можна дістатися до багатьох місць)
    top_accessible = sorted(outgoing_paths.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"   • Топ-5 станцій з найбільшою доступністю:")
    for i, (station, count) in enumerate(top_accessible, 1):
        avg_dist = np.mean(avg_outgoing_distance[station]) if avg_outgoing_distance[station] else 0
        print(f"     {i}. {station}: {count} напрямків, середня відстань {avg_dist:.2f}")
    
    # Центральні станції (до яких легко дістатися)
    top_central = sorted(incoming_paths.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"   • Топ-5 найбільш центральних станцій:")
    for i, (station, count) in enumerate(top_central, 1):
        print(f"     {i}. {station}: {count} шляхів ведуть сюди")

def compare_with_networkx(graph, start, end):
    """
    Порівнює нашу реалізацію алгоритму Дейкстри з вбудованою в NetworkX.
    
    Args:
        graph (nx.Graph): Граф
        start (str): Початкова вершина
        end (str): Кінцева вершина
    """
    print(f"\n🔬 ПОРІВНЯННЯ З NETWORKX")
    print("="*50)
    
    # Наша реалізація
    start_time = time.time()
    distances, predecessors, stats = dijkstra_algorithm(graph, start)
    our_path = reconstruct_path(predecessors, start, end)
    our_time = time.time() - start_time
    our_distance = distances[end] if distances[end] != float('infinity') else None
    
    # NetworkX реалізація
    start_time = time.time()
    try:
        nx_path = nx.shortest_path(graph, start, end, weight='weight')
        nx_distance = nx.shortest_path_length(graph, start, end, weight='weight')
        nx_time = time.time() - start_time
    except nx.NetworkXNoPath:
        nx_path = None
        nx_distance = None
        nx_time = time.time() - start_time
    
    print(f"Маршрут: {start} → {end}")
    print(f"\n{'Реалізація':<15} {'Відстань':<12} {'Час (мс)':<10} {'Шлях'}")
    print("-" * 70)
    print(f"{'Наша':<15} {our_distance if our_distance else 'Не знайдено':<12} {our_time*1000:.3f} "
          f"{' → '.join(our_path) if our_path else 'Не знайдено'}")
    print(f"{'NetworkX':<15} {nx_distance if nx_distance else 'Не знайдено':<12} {nx_time*1000:.3f} "
          f"{' → '.join(nx_path) if nx_path else 'Не знайдено'}")
    
    # Перевірка правильності
    if our_distance is not None and nx_distance is not None:
        if abs(our_distance - nx_distance) < 0.001:
            print("\n✅ Результати співпадають - реалізація правильна!")
        else:
            print(f"\n❌ Результати не співпадають! Різниця: {abs(our_distance - nx_distance):.3f}")
    elif our_distance is None and nx_distance is None:
        print("\n✅ Обидві реалізації не знайшли шлях - правильно!")

def main():
    """
    Головна функція для виконання завдання 3.
    """
    print("⚡ Завдання 3: Алгоритм Дейкстри для пошуку найкоротших шляхів")
    print("="*70)
    
    # Завантажуємо та підготовлюємо граф
    print("📊 Завантаження та підготовка зваженого графа...")
    G = load_and_prepare_weighted_graph()
    
    # Демонструємо алгоритм на конкретному прикладі
    start_station = 'Центральна площа'
    end_station = 'Аеропорт'
    
    print(f"\n🎯 Демонстрація алгоритму Дейкстри:")
    print(f"Пошук найкоротшого шляху: {start_station} → {end_station}")
    
    # Виконуємо алгоритм Дейкстри
    distances, predecessors, stats = dijkstra_algorithm(G, start_station)
    path = reconstruct_path(predecessors, start_station, end_station)
    
    print(f"\n📊 Результати:")
    if path:
        print(f"   • Знайдений шлях: {' → '.join(path)}")
        print(f"   • Загальна відстань: {distances[end_station]:.2f}")
        print(f"   • Кількість станцій: {len(path)}")
    else:
        print(f"   • Шлях не знайдено")
    
    print(f"   • Час виконання: {stats['execution_time']*1000:.3f} мс")
    print(f"   • Ітерацій: {stats['iterations']}")
    print(f"   • Оброблено вузлів: {stats['nodes_processed']}")
    
    # Візуалізуємо результат
    print(f"\n📈 Візуалізація найкоротшого шляху...")
    visualize_shortest_path(G, start_station, end_station, path, distances)
    
    # Знаходимо всі найкоротші шляхи
    print(f"\n🔄 Пошук найкоротших шляхів між всіма парами станцій...")
    all_paths, all_distances = find_all_shortest_paths(G)
    
    # Створюємо матрицю відстаней
    print(f"\n📋 Створення матриці відстаней...")
    distance_matrix = create_distance_matrix(G, all_distances)
    
    # Виводимо частину матриці для демонстрації
    print(f"\nМатриця відстаней (перші 5x5 елементів):")
    print(distance_matrix.iloc[:5, :5].round(2))
    
    # Аналізуємо результати
    analyze_shortest_paths(G, all_paths, all_distances)
    
    # Порівнюємо з NetworkX
    compare_with_networkx(G, start_station, end_station)
    
    # Зберігаємо результати
    print(f"\n💾 Збереження результатів...")
    distance_matrix.to_csv('distance_matrix.csv')
    print(f"   • Матриця відстаней збережена в 'distance_matrix.csv'")
    
    print(f"\n✅ Завдання 3 завершено!")
    print(f"📋 Реалізовано алгоритм Дейкстри")
    print(f"📊 Знайдено найкоротші шляхи між всіма парами вершин")
    print(f"📈 Проаналізовано характеристики найкоротших шляхів")
    print(f"🔬 Порівняно з реалізацією NetworkX")
    
    return G, all_paths, all_distances, distance_matrix

if __name__ == "__main__":
    graph, paths, distances, matrix = main()
