"""
Завдання 2: Реалізація алгоритмів DFS та BFS для пошуку шляхів

Порівняння алгоритмів пошуку в глибину (DFS) та пошуку в ширину (BFS)
на транспортній мережі міста, створеній в першому завданні.
"""

import networkx as nx
import matplotlib.pyplot as plt
from collections import deque, defaultdict
import time

def load_graph():
    """
    Завантажує граф з файлу або створює новий, якщо файл не знайдено.
    
    Returns:
        nx.Graph: Граф транспортної мережі
    """
    try:
        G = nx.read_gml("city_transport_network.gml")
        print("✅ Граф завантажено з файлу 'city_transport_network.gml'")
        return G
    except FileNotFoundError:
        print("⚠️  Файл графа не знайдено, створюємо новий...")
        # Імпортуємо функцію з першого завдання
        from task1 import create_city_transport_network
        G = create_city_transport_network()
        nx.write_gml(G, "city_transport_network.gml")
        return G

def dfs_paths(graph, start, end, path=None):
    """
    Пошук усіх шляхів від початкової до кінцевої вершини за допомогою DFS.
    
    Args:
        graph (nx.Graph): Граф для пошуку
        start (str): Початкова вершина
        end (str): Кінцева вершина
        path (list): Поточний шлях (для рекурсії)
        
    Yields:
        list: Знайдені шляхи
    """
    if path is None:
        path = []
    
    path = path + [start]
    
    if start == end:
        yield path
    else:
        for neighbor in graph.neighbors(start):
            if neighbor not in path:  # Уникаємо циклів
                yield from dfs_paths(graph, neighbor, end, path)

def dfs_single_path(graph, start, end):
    """
    Знаходить один шлях за допомогою DFS з детальним логуванням.
    
    Args:
        graph (nx.Graph): Граф для пошуку
        start (str): Початкова вершина
        end (str): Кінцева вершина
        
    Returns:
        tuple: (шлях, порядок відвідування, статистика)
    """
    visited = set()
    path = []
    visit_order = []
    
    def dfs_recursive(node, target, current_path):
        visited.add(node)
        visit_order.append(node)
        current_path.append(node)
        
        if node == target:
            return True
        
        # Сортуємо сусідів для детермінованого результату
        neighbors = sorted(graph.neighbors(node))
        for neighbor in neighbors:
            if neighbor not in visited:
                if dfs_recursive(neighbor, target, current_path):
                    return True
        
        current_path.pop()  # Backtrack
        return False
    
    start_time = time.time()
    found = dfs_recursive(start, end, path)
    end_time = time.time()
    
    stats = {
        'found': found,
        'path_length': len(path) if found else 0,
        'nodes_visited': len(visit_order),
        'execution_time': end_time - start_time,
        'algorithm': 'DFS'
    }
    
    return path if found else None, visit_order, stats

def bfs_single_path(graph, start, end):
    """
    Знаходить найкоротший шлях за допомогою BFS з детальним логуванням.
    
    Args:
        graph (nx.Graph): Граф для пошуку
        start (str): Початкова вершина
        end (str): Кінцева вершина
        
    Returns:
        tuple: (шлях, порядок відвідування, статистика)
    """
    if start == end:
        return [start], [start], {'found': True, 'path_length': 1, 'nodes_visited': 1, 'execution_time': 0, 'algorithm': 'BFS'}
    
    visited = set([start])
    queue = deque([(start, [start])])
    visit_order = [start]
    
    start_time = time.time()
    
    while queue:
        current, path = queue.popleft()
        
        # Сортуємо сусідів для детермінованого результату
        neighbors = sorted(graph.neighbors(current))
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                visit_order.append(neighbor)
                new_path = path + [neighbor]
                
                if neighbor == end:
                    end_time = time.time()
                    stats = {
                        'found': True,
                        'path_length': len(new_path),
                        'nodes_visited': len(visit_order),
                        'execution_time': end_time - start_time,
                        'algorithm': 'BFS'
                    }
                    return new_path, visit_order, stats
                
                queue.append((neighbor, new_path))
    
    end_time = time.time()
    stats = {
        'found': False,
        'path_length': 0,
        'nodes_visited': len(visit_order),
        'execution_time': end_time - start_time,
        'algorithm': 'BFS'
    }
    
    return None, visit_order, stats

def visualize_path_comparison(graph, start, end, dfs_path, bfs_path, dfs_visit_order, bfs_visit_order):
    """
    Візуалізує порівняння шляхів DFS та BFS.
    
    Args:
        graph (nx.Graph): Граф
        start (str): Початкова вершина
        end (str): Кінцева вершина
        dfs_path (list): Шлях, знайдений DFS
        bfs_path (list): Шлях, знайдений BFS
        dfs_visit_order (list): Порядок відвідування DFS
        bfs_visit_order (list): Порядок відвідування BFS
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    pos = nx.spring_layout(graph, k=3, iterations=50, seed=42)
    
    # Функція для малювання графа з виділеним шляхом
    def draw_graph_with_path(ax, path, visit_order, title, algorithm):
        # Базові кольори вершин
        node_colors = []
        for node in graph.nodes():
            if node == start:
                node_colors.append('#FF4444')  # Червоний для початку
            elif node == end:
                node_colors.append('#44FF44')  # Зелений для кінця
            elif path and node in path:
                node_colors.append('#4444FF')  # Синій для шляху
            elif node in visit_order:
                node_colors.append('#FFAA44')  # Помаранчевий для відвіданих
            else:
                node_colors.append('#CCCCCC')  # Сірий для не відвіданих
        
        # Малюємо всі ребра сірим кольором
        nx.draw_networkx_edges(graph, pos, ax=ax, edge_color='lightgray', width=1, alpha=0.5)
        
        # Виділяємо ребра шляху
        if path and len(path) > 1:
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_edges(graph, pos, edgelist=path_edges, ax=ax,
                                 edge_color='red', width=3, alpha=0.8)
        
        # Малюємо вершини
        nx.draw_networkx_nodes(graph, pos, ax=ax,
                             node_color=node_colors,
                             node_size=500,
                             alpha=0.8,
                             edgecolors='black',
                             linewidths=1)
        
        # Додаємо підписи
        nx.draw_networkx_labels(graph, pos, ax=ax,
                              font_size=6,
                              font_weight='bold')
        
        ax.set_title(f'{title}\n{algorithm}', fontsize=14, fontweight='bold')
        ax.axis('off')
        
        # Додаємо легенду
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF4444', 
                      markersize=10, label='Початок'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#44FF44', 
                      markersize=10, label='Кінець'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4444FF', 
                      markersize=10, label='Шлях'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FFAA44', 
                      markersize=10, label='Відвідано'),
            plt.Line2D([0], [0], color='red', linewidth=3, label='Знайдений шлях')
        ]
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1))
    
    # Малюємо DFS
    draw_graph_with_path(ax1, dfs_path, dfs_visit_order, 
                        f'Пошук в глибину (DFS)\n{start} → {end}', 'DFS')
    
    # Малюємо BFS
    draw_graph_with_path(ax2, bfs_path, bfs_visit_order,
                        f'Пошук в ширину (BFS)\n{start} → {end}', 'BFS')
    
    plt.tight_layout()
    plt.show()

def analyze_algorithms_comparison(dfs_stats, bfs_stats, dfs_path, bfs_path):
    """
    Аналізує та порівнює результати алгоритмів DFS та BFS.
    
    Args:
        dfs_stats (dict): Статистика DFS
        bfs_stats (dict): Статистика BFS
        dfs_path (list): Шлях DFS
        bfs_path (list): Шлях BFS
    """
    print("\n" + "="*70)
    print("📊 ПОРІВНЯЛЬНИЙ АНАЛІЗ АЛГОРИТМІВ DFS ТА BFS")
    print("="*70)
    
    print(f"\n🔍 Результати пошуку:")
    print(f"{'Алгоритм':<10} {'Знайдено':<10} {'Довжина шляху':<15} {'Відвідано вузлів':<15} {'Час (мс)':<10}")
    print("-" * 70)
    
    dfs_time_ms = dfs_stats['execution_time'] * 1000
    bfs_time_ms = bfs_stats['execution_time'] * 1000
    
    print(f"{'DFS':<10} {'Так' if dfs_stats['found'] else 'Ні':<10} "
          f"{dfs_stats['path_length']:<15} {dfs_stats['nodes_visited']:<15} {dfs_time_ms:.3f}")
    print(f"{'BFS':<10} {'Так' if bfs_stats['found'] else 'Ні':<10} "
          f"{bfs_stats['path_length']:<15} {bfs_stats['nodes_visited']:<15} {bfs_time_ms:.3f}")
    
    print(f"\n📈 Детальне порівняння:")
    
    if dfs_stats['found'] and bfs_stats['found']:
        # Порівняння довжини шляхів
        if dfs_stats['path_length'] == bfs_stats['path_length']:
            print(f"   • Довжина шляхів: Однакова ({dfs_stats['path_length']} вузлів)")
        elif dfs_stats['path_length'] < bfs_stats['path_length']:
            diff = bfs_stats['path_length'] - dfs_stats['path_length']
            print(f"   • Довжина шляхів: DFS коротший на {diff} вузлів")
        else:
            diff = dfs_stats['path_length'] - bfs_stats['path_length']
            print(f"   • Довжина шляхів: BFS коротший на {diff} вузлів")
        
        # Порівняння кількості відвіданих вузлів
        if dfs_stats['nodes_visited'] == bfs_stats['nodes_visited']:
            print(f"   • Відвідано вузлів: Однаково ({dfs_stats['nodes_visited']})")
        elif dfs_stats['nodes_visited'] < bfs_stats['nodes_visited']:
            diff = bfs_stats['nodes_visited'] - dfs_stats['nodes_visited']
            print(f"   • Відвідано вузлів: DFS менше на {diff}")
        else:
            diff = dfs_stats['nodes_visited'] - bfs_stats['nodes_visited']
            print(f"   • Відвідано вузлів: BFS менше на {diff}")
        
        # Ефективність за часом
        if dfs_time_ms < bfs_time_ms:
            ratio = bfs_time_ms / dfs_time_ms if dfs_time_ms > 0 else float('inf')
            print(f"   • Швидкість: DFS швидший у {ratio:.2f} разів")
        elif bfs_time_ms < dfs_time_ms:
            ratio = dfs_time_ms / bfs_time_ms if bfs_time_ms > 0 else float('inf')
            print(f"   • Швидкість: BFS швидший у {ratio:.2f} разів")
        else:
            print(f"   • Швидкість: Приблизно однакова")
    
    print(f"\n📝 Знайдені шляхи:")
    if dfs_path:
        print(f"   DFS: {' → '.join(dfs_path)}")
    else:
        print(f"   DFS: Шлях не знайдено")
    
    if bfs_path:
        print(f"   BFS: {' → '.join(bfs_path)}")
    else:
        print(f"   BFS: Шлях не знайдено")

def explain_algorithm_differences():
    """
    Пояснює відмінності між алгоритмами DFS та BFS.
    """
    print(f"\n" + "="*70)
    print("🧠 ПОЯСНЕННЯ ВІДМІННОСТЕЙ МІЖ АЛГОРИТМАМИ")
    print("="*70)
    
    print(f"""
🔍 ПОШУК В ГЛИБИНУ (DFS - Depth-First Search):
   Характеристики:
   • Досліджує граф "вглиб" - йде якомога далі по одному напрямку
   • Використовує стек (рекурсію або явний стек)
   • Може знайти довший шлях, якщо він існує
   • Потребує менше пам'яті
   
   Переваги:
   • Ефективний за пам'яттю O(h), де h - висота дерева
   • Простий у реалізації
   • Добре підходить для пошуку всіх рішень
   
   Недоліки:
   • Не гарантує найкоротший шлях
   • Може "застрягти" в глибоких гілках
   • У найгіршому випадку може обійти весь граф

🔍 ПОШУК В ШИРИНУ (BFS - Breadth-First Search):
   Характеристики:
   • Досліджує граф "вшир" - перевіряє всіх сусідів на поточному рівні
   • Використовує чергу (FIFO)
   • Завжди знаходить найкоротший шлях (за кількістю ребер)
   • Потребує більше пам'яті
   
   Переваги:
   • Гарантує найкоротший шлях в незваженому графі
   • Систематично досліджує граф рівень за рівнем
   • Оптимальний для пошуку найкоротшого шляху
   
   Недоліки:
   • Потребує більше пам'яті O(w), де w - максимальна ширина
   • Може бути повільнішим для глибоких графів
   • Досліджує багато "непотрібних" вузлів

🎯 ЧОМУ АЛГОРИТМИ ОБИРАЮТЬ РІЗНІ ШЛЯХИ:

1. DFS слідує першому доступному шляху до кінця, потім повертається назад
2. BFS досліджує всі можливості на кожному рівні перед переходом далі
3. В транспортній мережі:
   • DFS може знайти прямий, але не обов'язково найкоротший маршрут
   • BFS знаходить маршрут з мінімальною кількістю пересадок
   • Для пасажирів BFS зазвичай кращий (менше пересадок)
   • Для аналізу зв'язності DFS може бути достатнім
    """)

def test_multiple_paths(graph):
    """
    Тестує алгоритми на різних парах станцій.
    
    Args:
        graph (nx.Graph): Граф для тестування
    """
    print(f"\n" + "="*70)
    print("🧪 ТЕСТУВАННЯ НА РІЗНИХ МАРШРУТАХ")
    print("="*70)
    
    # Вибираємо цікаві пари станцій для тестування
    test_pairs = [
        ('Центральна площа', 'Аеропорт'),
        ('Північний вокзал', 'Річковий порт'),
        ('Університет', 'Житловий масив'),
        ('Лісопарк', 'Заводська'),
        ('Театральна', 'Нова забудова')
    ]
    
    summary_results = []
    
    for start, end in test_pairs:
        if start in graph.nodes() and end in graph.nodes():
            print(f"\n🚇 Маршрут: {start} → {end}")
            print("-" * 50)
            
            # Виконуємо пошук
            dfs_path, dfs_visit_order, dfs_stats = dfs_single_path(graph, start, end)
            bfs_path, bfs_visit_order, bfs_stats = bfs_single_path(graph, start, end)
            
            # Короткий звіт
            if dfs_stats['found'] and bfs_stats['found']:
                print(f"DFS: {len(dfs_path)} станцій, {dfs_stats['nodes_visited']} відвідано")
                print(f"BFS: {len(bfs_path)} станцій, {bfs_stats['nodes_visited']} відвідано")
                
                if len(dfs_path) == len(bfs_path):
                    print("✅ Однакова довжина шляху")
                elif len(bfs_path) < len(dfs_path):
                    print(f"✅ BFS знайшов коротший шлях на {len(dfs_path) - len(bfs_path)} станцій")
                else:
                    print(f"⚠️  DFS знайшов коротший шлях на {len(bfs_path) - len(dfs_path)} станцій")
            
            summary_results.append({
                'route': f"{start} → {end}",
                'dfs_length': len(dfs_path) if dfs_path else None,
                'bfs_length': len(bfs_path) if bfs_path else None,
                'dfs_visited': dfs_stats['nodes_visited'],
                'bfs_visited': bfs_stats['nodes_visited']
            })
    
    # Підсумок всіх тестів
    print(f"\n📊 ПІДСУМОК ТЕСТУВАННЯ:")
    print("-" * 70)
    bfs_wins = sum(1 for r in summary_results 
                   if r['bfs_length'] is not None and r['dfs_length'] is not None 
                   and r['bfs_length'] < r['dfs_length'])
    dfs_wins = sum(1 for r in summary_results 
                   if r['bfs_length'] is not None and r['dfs_length'] is not None 
                   and r['dfs_length'] < r['bfs_length'])
    ties = sum(1 for r in summary_results 
               if r['bfs_length'] is not None and r['dfs_length'] is not None 
               and r['bfs_length'] == r['dfs_length'])
    
    print(f"BFS знайшов коротші шляхи: {bfs_wins} разів")
    print(f"DFS знайшов коротші шляхи: {dfs_wins} разів")
    print(f"Однакова довжина: {ties} разів")

def main():
    """
    Головна функція для виконання завдання 2.
    """
    print("🔍 Завдання 2: Порівняння алгоритмів DFS та BFS")
    print("="*60)
    
    # Завантажуємо граф
    G = load_graph()
    
    # Вибираємо станції для демонстрації
    start_station = 'Центральна площа'
    end_station = 'Аеропорт'
    
    print(f"\n🎯 Основна демонстрація:")
    print(f"Маршрут: {start_station} → {end_station}")
    
    # Виконуємо пошук DFS
    print(f"\n🔍 Виконуємо пошук в глибину (DFS)...")
    dfs_path, dfs_visit_order, dfs_stats = dfs_single_path(G, start_station, end_station)
    
    # Виконуємо пошук BFS
    print(f"🔍 Виконуємо пошук в ширину (BFS)...")
    bfs_path, bfs_visit_order, bfs_stats = bfs_single_path(G, start_station, end_station)
    
    # Візуалізуємо результати
    print(f"\n📊 Візуалізація результатів...")
    visualize_path_comparison(G, start_station, end_station, 
                            dfs_path, bfs_path, dfs_visit_order, bfs_visit_order)
    
    # Аналізуємо результати
    analyze_algorithms_comparison(dfs_stats, bfs_stats, dfs_path, bfs_path)
    
    # Пояснюємо відмінності
    explain_algorithm_differences()
    
    # Тестуємо на додаткових маршрутах
    test_multiple_paths(G)
    
    print(f"\n✅ Завдання 2 завершено!")
    print(f"📋 Реалізовано та порівняно алгоритми DFS та BFS")
    print(f"📊 Проаналізовано відмінності в знайдених шляхах")
    print(f"🧠 Пояснено причини різних результатів алгоритмів")
    
    return G, dfs_path, bfs_path

if __name__ == "__main__":
    graph, dfs_result, bfs_result = main()
