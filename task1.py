"""
Завдання 1: Створення графа для моделювання реальної мережі

Моделюємо транспортну мережу міста з різними районами та транспортними маршрутами.
Використовуємо NetworkX для створення, візуалізації та аналізу графа.
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

def create_city_transport_network():
    """
    Створює граф транспортної мережі міста.
    
    Returns:
        nx.Graph: Граф транспортної мережі
    """
    # Створюємо порожній граф
    G = nx.Graph()
    
    # Визначаємо станції/зупинки в різних районах міста
    stations = {
        # Центральний район
        'Центральна площа': {'district': 'Центр', 'type': 'metro', 'population': 50000},
        'Театральна': {'district': 'Центр', 'type': 'metro', 'population': 30000},
        'Університет': {'district': 'Центр', 'type': 'metro', 'population': 40000},
        
        # Північний район
        'Північний вокзал': {'district': 'Північ', 'type': 'train', 'population': 35000},
        'Озерна': {'district': 'Північ', 'type': 'bus', 'population': 25000},
        'Лісопарк': {'district': 'Північ', 'type': 'bus', 'population': 15000},
        
        # Східний район
        'Промислова': {'district': 'Схід', 'type': 'metro', 'population': 45000},
        'Заводська': {'district': 'Схід', 'type': 'bus', 'population': 20000},
        'Нова забудова': {'district': 'Схід', 'type': 'bus', 'population': 30000},
        
        # Західний район
        'Аеропорт': {'district': 'Захід', 'type': 'train', 'population': 25000},
        'Торговий центр': {'district': 'Захід', 'type': 'metro', 'population': 40000},
        'Спортивний комплекс': {'district': 'Захід', 'type': 'bus', 'population': 20000},
        
        # Південний район
        'Річковий порт': {'district': 'Південь', 'type': 'train', 'population': 30000},
        'Ринок': {'district': 'Південь', 'type': 'bus', 'population': 35000},
        'Житловий масив': {'district': 'Південь', 'type': 'bus', 'population': 40000}
    }
    
    # Додаємо вершини до графа
    for station, attributes in stations.items():
        G.add_node(station, **attributes)
    
    # Визначаємо з'єднання (ребра) між станціями
    # Формат: (станція1, станція2, тип_транспорту, відстань_км)
    connections = [
        # Центральні з'єднання
        ('Центральна площа', 'Театральна', 'metro', 2.5),
        ('Центральна площа', 'Університет', 'metro', 3.0),
        ('Театральна', 'Університет', 'bus', 1.8),
        
        # З'єднання з центром
        ('Центральна площа', 'Північний вокзал', 'metro', 4.5),
        ('Центральна площа', 'Промислова', 'metro', 5.2),
        ('Центральна площа', 'Торговий центр', 'metro', 6.0),
        ('Центральна площа', 'Річковий порт', 'bus', 7.5),
        
        # Північний район
        ('Північний вокзал', 'Озерна', 'bus', 3.5),
        ('Озерна', 'Лісопарк', 'bus', 2.8),
        ('Північний вокзал', 'Лісопарк', 'train', 5.0),
        
        # Східний район
        ('Промислова', 'Заводська', 'bus', 2.2),
        ('Заводська', 'Нова забудова', 'bus', 3.1),
        ('Промислова', 'Нова забудова', 'metro', 4.0),
        
        # Західний район
        ('Торговий центр', 'Аеропорт', 'train', 8.5),
        ('Торговий центр', 'Спортивний комплекс', 'bus', 2.7),
        ('Аеропорт', 'Спортивний комплекс', 'bus', 6.3),
        
        # Південний район
        ('Річковий порт', 'Ринок', 'bus', 2.0),
        ('Ринок', 'Житловий масив', 'bus', 2.5),
        ('Річковий порт', 'Житловий масив', 'train', 4.2),
        
        # Міжрайонні з'єднання
        ('Університет', 'Промислова', 'bus', 4.8),
        ('Театральна', 'Торговий центр', 'bus', 5.5),
        ('Північний вокзал', 'Аеропорт', 'train', 12.0),
        ('Озерна', 'Спортивний комплекс', 'bus', 8.2),
        ('Заводська', 'Ринок', 'bus', 6.5),
        ('Нова забудова', 'Житловий масив', 'bus', 5.8),
    ]
    
    # Додаємо ребра до графа
    for station1, station2, transport_type, distance in connections:
        G.add_edge(station1, station2, 
                  transport_type=transport_type, 
                  distance=distance,
                  weight=distance)  # Вага = відстань для алгоритмів пошуку
    
    return G

def visualize_graph(G):
    """
    Візуалізує граф транспортної мережі.
    
    Args:
        G (nx.Graph): Граф для візуалізації
    """
    plt.figure(figsize=(16, 12))
    
    # Створюємо layout для розташування вершин
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    
    # Визначаємо кольори для різних районів
    district_colors = {
        'Центр': '#FF6B6B',      # Червоний
        'Північ': '#4ECDC4',     # Бірюзовий
        'Схід': '#45B7D1',       # Синій
        'Захід': '#96CEB4',      # Зелений
        'Південь': '#FECA57'     # Жовтий
    }
    
    # Визначаємо розміри вершин на основі населення
    node_sizes = []
    node_colors = []
    for node in G.nodes():
        population = G.nodes[node]['population']
        district = G.nodes[node]['district']
        
        # Розмір пропорційний населенню
        size = population / 1000 + 200  # Мінімальний розмір 200
        node_sizes.append(size)
        node_colors.append(district_colors[district])
    
    # Малюємо вершини
    nx.draw_networkx_nodes(G, pos, 
                          node_color=node_colors,
                          node_size=node_sizes,
                          alpha=0.8,
                          edgecolors='black',
                          linewidths=1.5)
    
    # Визначаємо кольори та стилі ребер за типом транспорту
    edge_colors = []
    edge_styles = []
    edge_widths = []
    
    for edge in G.edges():
        transport_type = G.edges[edge]['transport_type']
        if transport_type == 'metro':
            edge_colors.append('#2C3E50')  # Темно-сірий
            edge_styles.append('-')        # Суцільна лінія
            edge_widths.append(3)
        elif transport_type == 'train':
            edge_colors.append('#8E44AD')  # Фіолетовий
            edge_styles.append('--')       # Пунктирна лінія
            edge_widths.append(2.5)
        else:  # bus
            edge_colors.append('#E67E22')  # Помаранчевий
            edge_styles.append(':')        # Крапкова лінія
            edge_widths.append(2)
    
    # Малюємо ребра
    for i, edge in enumerate(G.edges()):
        nx.draw_networkx_edges(G, pos,
                             edgelist=[edge],
                             edge_color=edge_colors[i],
                             style=edge_styles[i],
                             width=edge_widths[i],
                             alpha=0.7)
    
    # Додаємо підписи до вершин
    labels = {}
    for node in G.nodes():
        # Коротка назва для кращого відображення
        short_name = node.replace(' ', '\n')
        labels[node] = short_name
    
    nx.draw_networkx_labels(G, pos, labels, 
                           font_size=8, 
                           font_weight='bold',
                           font_color='white',
                           bbox=dict(boxstyle='round,pad=0.3', 
                                   facecolor='black', 
                                   alpha=0.7))
    
    # Створюємо легенду
    legend_elements = []
    for district, color in district_colors.items():
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                        markerfacecolor=color, markersize=10, 
                                        label=f'Район: {district}'))
    
    # Додаємо легенду для типів транспорту
    transport_legend = [
        plt.Line2D([0], [0], color='#2C3E50', linewidth=3, label='Метро'),
        plt.Line2D([0], [0], color='#8E44AD', linewidth=2.5, linestyle='--', label='Поїзд'),
        plt.Line2D([0], [0], color='#E67E22', linewidth=2, linestyle=':', label='Автобус')
    ]
    
    # Розміщуємо легенди
    legend1 = plt.legend(handles=legend_elements, loc='upper left', title='Райони')
    plt.legend(handles=transport_legend, loc='upper right', title='Транспорт')
    plt.gca().add_artist(legend1)
    
    plt.title('Транспортна мережа міста\nРозмір вершин пропорційний населенню районів', 
              fontsize=16, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def analyze_graph_characteristics(G):
    """
    Аналізує основні характеристики графа.
    
    Args:
        G (nx.Graph): Граф для аналізу
    """
    print("🔍 АНАЛІЗ ХАРАКТЕРИСТИК ТРАНСПОРТНОЇ МЕРЕЖІ")
    print("=" * 60)
    
    # Основні характеристики
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    
    print(f"📊 Основні характеристики:")
    print(f"   • Кількість станцій (вершин): {num_nodes}")
    print(f"   • Кількість з'єднань (ребер): {num_edges}")
    print(f"   • Щільність графа: {nx.density(G):.3f}")
    print(f"   • Чи є граф зв'язним: {'Так' if nx.is_connected(G) else 'Ні'}")
    
    # Аналіз ступенів вершин
    degrees = dict(G.degree())
    avg_degree = sum(degrees.values()) / len(degrees)
    max_degree_node = max(degrees.keys(), key=lambda x: degrees[x])
    min_degree_node = min(degrees.keys(), key=lambda x: degrees[x])
    
    print(f"\n🔗 Аналіз з'єднань (ступінь вершин):")
    print(f"   • Середній ступінь вершини: {avg_degree:.2f}")
    print(f"   • Максимальний ступінь: {degrees[max_degree_node]} (станція: {max_degree_node})")
    print(f"   • Мінімальний ступінь: {degrees[min_degree_node]} (станція: {min_degree_node})")
    
    # Топ-5 найбільш зв'язаних станцій
    top_connected = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"   • Топ-5 найбільш зв'язаних станцій:")
    for i, (station, degree) in enumerate(top_connected, 1):
        print(f"     {i}. {station}: {degree} з'єднань")
    
    # Аналіз за районами
    print(f"\n🏘️  Аналіз за районами:")
    districts = {}
    for node in G.nodes():
        district = G.nodes[node]['district']
        if district not in districts:
            districts[district] = []
        districts[district].append(node)
    
    for district, stations in districts.items():
        district_population = sum(G.nodes[station]['population'] for station in stations)
        avg_connections = sum(degrees[station] for station in stations) / len(stations)
        print(f"   • {district}:")
        print(f"     - Станцій: {len(stations)}")
        print(f"     - Населення: {district_population:,}")
        print(f"     - Середня кількість з'єднань: {avg_connections:.1f}")
    
    # Аналіз за типами транспорту
    print(f"\n🚊 Аналіз транспортних типів:")
    transport_types = Counter()
    total_distance = 0
    
    for edge in G.edges():
        transport_type = G.edges[edge]['transport_type']
        distance = G.edges[edge]['distance']
        transport_types[transport_type] += 1
        total_distance += distance
    
    print(f"   • Загальна довжина мережі: {total_distance:.1f} км")
    for transport_type, count in transport_types.items():
        percentage = (count / num_edges) * 100
        print(f"   • {transport_type.title()}: {count} з'єднань ({percentage:.1f}%)")
    
    # Аналіз за типами станцій
    print(f"\n🚉 Аналіз типів станцій:")
    station_types = Counter()
    for node in G.nodes():
        station_type = G.nodes[node]['type']
        station_types[station_type] += 1
    
    for station_type, count in station_types.items():
        percentage = (count / num_nodes) * 100
        print(f"   • {station_type.title()}: {count} станцій ({percentage:.1f}%)")
    
    # Центральність вершин
    print(f"\n🎯 Аналіз центральності:")
    
    # Центральність за близькістю
    closeness_centrality = nx.closeness_centrality(G)
    most_central = max(closeness_centrality.keys(), key=lambda x: closeness_centrality[x])
    print(f"   • Найбільш центральна станція (за близькістю): {most_central}")
    print(f"     Значення центральності: {closeness_centrality[most_central]:.3f}")
    
    # Центральність за посередництвом
    betweenness_centrality = nx.betweenness_centrality(G)
    most_between = max(betweenness_centrality.keys(), key=lambda x: betweenness_centrality[x])
    print(f"   • Найважливіша станція (за посередництвом): {most_between}")
    print(f"     Значення центральності: {betweenness_centrality[most_between]:.3f}")
    
    # Діаметр графа
    if nx.is_connected(G):
        diameter = nx.diameter(G)
        radius = nx.radius(G)
        center = nx.center(G)
        print(f"\n📏 Геометричні характеристики:")
        print(f"   • Діаметр графа: {diameter} (максимальна відстань між станціями)")
        print(f"   • Радіус графа: {radius}")
        print(f"   • Центр графа: {', '.join(center)}")
    
    # Кластеризація
    clustering_coefficient = nx.average_clustering(G)
    print(f"   • Коефіцієнт кластеризації: {clustering_coefficient:.3f}")
    
    return {
        'num_nodes': num_nodes,
        'num_edges': num_edges,
        'density': nx.density(G),
        'is_connected': nx.is_connected(G),
        'avg_degree': avg_degree,
        'most_central': most_central,
        'clustering': clustering_coefficient
    }

def main():
    """
    Головна функція для створення, візуалізації та аналізу графа.
    """
    print("🏙️  Створення моделі транспортної мережі міста")
    print("=" * 50)
    
    # Створюємо граф
    G = create_city_transport_network()
    print(f"✅ Граф створено успішно!")
    
    # Візуалізуємо граф
    print(f"\n📊 Візуалізація графа...")
    visualize_graph(G)
    
    # Аналізуємо характеристики
    print(f"\n🔬 Аналіз характеристик графа...")
    characteristics = analyze_graph_characteristics(G)
    
    # Зберігаємо граф для використання в наступних завданнях
    nx.write_gml(G, "city_transport_network.gml")
    print(f"\n💾 Граф збережено у файл 'city_transport_network.gml'")
    
    print(f"\n✅ Завдання 1 завершено!")
    print(f"📋 Створено реалістичну модель транспортної мережі міста")
    print(f"📈 Проаналізовано основні характеристики мережі")
    print(f"🎨 Візуалізовано граф з використанням різних кольорів та стилів")
    
    return G

if __name__ == "__main__":
    # Створюємо та аналізуємо граф
    city_graph = main()
