import xmlparser
import graph
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import math

def main():

    g = graph.getGraphList()
    #wtf
    # ================================== КРАТЧАЙШИЕ ПУТИ ====================================

    buildings_list = xmlparser.getBuildingsNodes()
    hospitals_list = xmlparser.getHospitalsNodes()
    N = 10
    M = 10
    buildings = []
    hospitals = []
    coords = xmlparser.getNodesCoords()

    for i in range(N):
        hospitals.append(graph.NearestNode(g, coords, hospitals_list[i]))

    while (len(buildings) < M):
        buildings.append(graph.NearestNode(g, coords, random.choice(buildings_list)))

    building_trees = {}
    hospital_trees = {}

    for node in hospitals:
        hospital_trees[node] = graph.Dijkstra(g, node)

    for node in buildings:
        building_trees[node] = graph.Dijkstra(g, node)

    buildings_to_hospitals = {}
    hospitals_to_buildings = {}

    for node_h in hospitals:
        hospitals_to_buildings[node_h] = {}
        for node_b in buildings:
            (D, Parent) = hospital_trees[node_h]
            hospitals_to_buildings[node_h][node_b] = D[node_b]

    for node_b in buildings:
        buildings_to_hospitals[node_b] = {}
        for node_h in hospitals:
            (D, Parent) = building_trees[node_b]
            buildings_to_hospitals[node_b][node_h] = D[node_h]

     # ============================= 1.1 =====================================

    print('Задание 1')

    building_nearest_objects = {}
    for node_b in buildings:
        building_nearest_objects[node_b] = {}

        min_dist = math.inf
        nearest_from = ''
        for node_h in hospitals:
            if buildings_to_hospitals[node_b][node_h] < min_dist:
                nearest_from = node_h
                min_dist = buildings_to_hospitals[node_b][node_h]
        building_nearest_objects[node_b]['from'] = nearest_from

        min_dist = math.inf
        nearest_to = ''
        for node_h in hospitals:
            if hospitals_to_buildings[node_h][node_b] < min_dist:
                nearest_to = node_h
                min_dist = hospitals_to_buildings[node_h][node_b]
        building_nearest_objects[node_b]['to'] = nearest_to

        min_dist = math.inf
        nearest_fromto = ''
        for node_h in hospitals:
            if buildings_to_hospitals[node_b][node_h] + hospitals_to_buildings[node_h][node_b] < min_dist:
                nearest_fromto = node_h
                min_dist = buildings_to_hospitals[node_b][node_h] + hospitals_to_buildings[node_h][node_b]
        building_nearest_objects[node_b]['fromto'] = nearest_fromto


    print('Ближайшие больницы для каждого дома: ')
    print(building_nearest_objects)

    # ============================= 1.2 =====================================

    print('Задание 2. Определить, какой из объектов расположен так, что время/расстояние между ним и самым дальним домом минимально')

    object_furthest_buildings = {}
    for node_h in hospitals:
        object_furthest_buildings[node_h] = {}

        max_dist = 0
        furthest_from = ''
        for node_b in buildings:
            if hospitals_to_buildings[node_h][node_b] > max_dist:
                furthest_from = node_b
                max_dist = hospitals_to_buildings[node_h][node_b]
        object_furthest_buildings[node_h]['from'] = furthest_from

        max_dist = 0
        furthest_to = ''
        for node_b in buildings:
            if buildings_to_hospitals[node_b][node_h] > max_dist:
                furthest_to = node_b
                max_dist = buildings_to_hospitals[node_b][node_h]
        object_furthest_buildings[node_h]['to'] = furthest_to

        max_dist = 0
        furthest_fromto = ''
        for node_b in buildings:
            if hospitals_to_buildings[node_h][node_b] + buildings_to_hospitals[node_b][node_h] > max_dist:
                furthest_fromto = node_b
                max_dist = hospitals_to_buildings[node_h][node_b] + buildings_to_hospitals[node_b][node_h]
        object_furthest_buildings[node_h]['fromto'] = furthest_fromto


    print('Туда: ')
    min_max = math.inf
    ans = ''
    for node_h in hospitals:
        if (hospitals_to_buildings[node_h][object_furthest_buildings[node_h]['from']] <= min_max):
            min_max = hospitals_to_buildings[node_h][object_furthest_buildings[node_h]['from']] 
            ans = node_h
    print('Ответ: ', ans)
    print('Расстояние до дома с номером ', object_furthest_buildings[ans]['from'], ' равно: ', min_max)

    print('Обратно: ')
    min_max = math.inf
    ans = ''
    for node_h in hospitals:
        if (hospitals_to_buildings[node_h][object_furthest_buildings[node_h]['to']] <= min_max):
            min_max = hospitals_to_buildings[node_h][object_furthest_buildings[node_h]['to']] 
            ans = node_h
    print('Ответ: ', ans)
    print('Расстояние от дома с номером ', object_furthest_buildings[ans]['to'], ' равно: ', min_max)

    print('Туда и обратно: ')
    min_max = math.inf
    ans = ''
    for node_h in hospitals:
        if (hospitals_to_buildings[node_h][object_furthest_buildings[node_h]['fromto']] <= min_max):
            min_max = hospitals_to_buildings[node_h][object_furthest_buildings[node_h]['fromto']] 
            ans = node_h
    print('Ответ: ', ans)
    print('Расстояние до+от дома с номером ', object_furthest_buildings[ans]['fromto'], ' равно: ', min_max)

        
    # ============================= 1.3 =====================================

    print('Задание 3. Для какого объекта инфраструктуры сумма кратчайших расстояний от него до всех домов минимальна.')

    ans = ''
    min_sum = math.inf
    for node_h in hospitals:
        sum = 0
        for node_b in buildings:
            sum = sum + hospitals_to_buildings[node_h][node_b]
        if (sum < min_sum):
            ans = node_h
            min_sum = sum

    print('Ответ: ', ans)
    print('Сумма: ', min_sum)

    # ============================= 1.4 =====================================

    print('Задание 4. Для какого объекта инфраструктуры построенное дерево кратчайших путей имеет минимальный вес.')

    min_weight = math.inf
    ans = ''
    for node_h in hospitals:
        (D, Parent) = hospital_trees[node_h]
        tree_edges = {}
        for node_b in buildings:
            way = graph.getWayInTree(Parent,node_h,node_b)
            for i in range(len(way) - 1):
                tree_edges[way[i]] = way[i+1]
        tree_weight = 0
        for node_1 in tree_edges:
            node_2 = tree_edges[node_1]
            tree_weight = tree_weight + g[node_1][node_2]
        if (tree_weight < min_weight):
            min_weight = tree_weight
            ans = node_h
    
    print('Ответ: ', ans)
    print('Вес дерева: ', min_weight)

    # ============================== Интерфейс =======================================     
            
    while(True):
        print('Просмотреть информацию о больницах? Y/N ')
        if (input() == 'Y'):
            print('Номера N узлов-больниц: ')
            for i in hospitals:
                print(i)
            print('Введите номер узла-больницы: ')
            node_h = str(input())
            print('Ближайший дом: ')
            min_dist = math.inf
            nearest_building = ''
            for node_b in buildings:
                if hospitals_to_buildings[node_h][node_b] < min_dist:
                    nearest_building = node_b
                    min_dist = hospitals_to_buildings[node_h][node_b]
            print(nearest_building)
            print('Расстояние до него: ')
            print(min_dist)
            print('Путь до него: ')
            (D, Parent) = hospital_trees[node_h]
            print(graph.getWayInTree(Parent, node_h, nearest_building))
        else:
            break

        print('Просмотреть информацию о домах? Y/N ')
        if (input() == 'Y'):
            print('Номера M узлов-домов: ')
            for i in buildings:
                print(i)
            print('Введите номер узла-дома: ')
            node_b = str(input())
            print('Ближайшая больница: ')
            min_dist = math.inf
            nearest_hospital = ''
            for node_h in hospitals:
                if buildings_to_hospitals[node_b][node_h] < min_dist:
                    nearest_hospital = node_h
                    min_dist = buildings_to_hospitals[node_b][node_h]
            print(nearest_hospital)
            print('Расстояние до неё: ')
            print(min_dist)
            print('Путь до неё: ')
            (D, Parent) = building_trees[node_b]
            print(graph.getWayInTree(Parent, node_b, nearest_hospital))
        else:
            break




    # ========================= ВИЗУАЛИЗАЦИЯ через networkx ==============================

    # G = nx.Graph()
    # for node in g.keys():
    #     G.add_node(node)
    #     for adj_node in g[node]:
    #         G.add_edge(node,adj_node, weight=g[node][adj_node])

    # nodesi = xmlparser.getNodesCoords()
    # print('Рисуем граф...')
    # nx.draw_networkx(G, pos=nodesi, node_size=0.1, width=0.2, with_labels=False, node_color='black', edge_color='black')
    # fig = plt.gcf()
    # fig.set_size_inches(8, 12, forward=True)
    # file_name = 'Tomsk'+'.png'
    # plt.savefig(file_name, dpi=100)
    # fig.clear() 


    # ============================== через Matplotlib ============================================
    # coords = xmlparser.getNodesCoords()

    # fig = plt.gcf()
    # fig.set_size_inches(24, 24, forward=True)
    # i = 0
    # for node in g:
    #     (node_lat, node_lon) = coords[node]
    #     for adj_node in g[node]:
    #         (adj_node_lat,adj_node_lon) = coords[adj_node]
    #         plt.plot([node_lat,node_lon], [adj_node_lat,adj_node_lon], 'black')
    #     i = i + 1
    #     print(i)
    # fig.savefig('Tomsk.png', dpi=100)
    # plt.show()
    


if __name__ == "__main__":
    main()