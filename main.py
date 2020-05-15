import xmlparser
import graph
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import math
import cluster
import csv
import visualisation
import pandas as pd

def main():

    # ============================= Генерация графа ==============================

    # g = graph.getGraphList()

    # ============================ Запись графа в файл ============================

    # with open('graph.csv', 'w') as csv_file:
    #     writer = csv.writer(csv_file, delimiter = ',')
    #     for node in g:
    #         line_csv = []
    #         line_csv.append(node)
    #         for adj_node in g[node]:
    #             line_csv.append(adj_node)
    #             line_csv.append(g[node][adj_node])
    #         writer.writerow(line_csv)       

    # ============================ Чтение графа из файла ==========================

    g = {}
    file_name = 'graph.csv'
    f = open(file_name, 'r')
    for line in f.readlines():
        dates = line.split(',')
        dates[len(dates)-1] = dates[len(dates)-1][:len(dates[len(dates)-1])-1]
        g[dates[0]] = {}
        r = int((len(dates) - 1)/2)
        for i in range(r):
            g[dates[0]][dates[2*i+1]] = float(dates[2*i+2])
    del g['']
    f.close()
    
    # ================================== КРАТЧАЙШИЕ ПУТИ ====================================

    buildings_list = xmlparser.getBuildingsNodes()
    hospitals_list = xmlparser.getHospitalsNodes()
    N = 10
    M = 100
    buildings = []
    hospitals = []
    coords = xmlparser.getNodesCoords()

    for i in range(N):
        hospitals.append(graph.NearestNode(g, coords, hospitals_list[i]))

    while (len(buildings) < M):
        buildings.append(graph.NearestNode(g, coords, random.choice(buildings_list)))

    all_ways_exist = False
    while(not all_ways_exist):

        building_trees = {}
        hospital_trees = {}

        for node in hospitals:
            hospital_trees[node] = graph.Dijkstra(g, node)

        for node in buildings:
            building_trees[node] = graph.Dijkstra(g, node)

        buildings_to_hospitals = {}
        hospitals_to_buildings = {}

        for node_b in buildings:
            buildings_to_hospitals[node_b] = {}
            for node_h in hospitals:
                (D, Parent) = building_trees[node_b]
                buildings_to_hospitals[node_b][node_h] = D[node_h]


        for node_h in hospitals:
            hospitals_to_buildings[node_h] = {}
            for node_b in buildings:
                (D, Parent) = hospital_trees[node_h]
                hospitals_to_buildings[node_h][node_b] = D[node_b]

        isolated_building = ''
        for node_b in buildings:
            for node_h in buildings_to_hospitals[node_b]:
                if (buildings_to_hospitals[node_b][node_h] == math.inf):
                    isolated_building = node_b
                    
        if (isolated_building != ''):
            buildings.remove(isolated_building)
            buildings.append(graph.NearestNode(g, coords, random.choice(buildings_list)))
            continue

        all_ways_exist = True

    # ============================= Запись деревьев в csv ===========================
    
    # for i in range(len(buildings)):
    #     tree = pd.DataFrame(building_trees[buildings[i]])
    #     tree.to_csv('trees/buildings/building_'+str(i)+'.csv')

    # for i in range(len(hospitals)):
    #     tree = pd.DataFrame(hospital_trees[hospitals[i]])
    #     tree.to_csv('trees/hospitals/hospital_'+str(i)+'.csv')


     # ============================= 1.1 =====================================

    print('Задание 1.1')

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

    print('Задание 1.2. Определить, какой из объектов расположен так, что время/расстояние между ним и самым дальним домом минимально')

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
        if (hospitals_to_buildings[node_h][object_furthest_buildings[node_h]['fromto']] + buildings_to_hospitals[object_furthest_buildings[node_h]['fromto']][node_h] <= min_max):
            min_max = hospitals_to_buildings[node_h][object_furthest_buildings[node_h]['fromto']] + buildings_to_hospitals[object_furthest_buildings[node_h]['fromto']][node_h] 
            ans = node_h
    print('Ответ: ', ans)
    print('Расстояние до+от дома с номером ', object_furthest_buildings[ans]['fromto'], ' равно: ', min_max)

        
    # ============================= 1.3 =====================================

    print('Задание 1.3. Для какого объекта инфраструктуры сумма кратчайших расстояний от него до всех домов минимальна.')

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

    print('Задание 1.4. Для какого объекта инфраструктуры построенное дерево кратчайших путей имеет минимальный вес.')

    min_weight = math.inf
    ans = ''

    for node_h in hospitals:
        (D, Parent) = hospital_trees[node_h]
        subtree_edges = graph.getSubtreeEdges(Parent,node_h,buildings)
        subtree_weight = graph.getSubtreeWeight(subtree_edges,g)
        if (subtree_weight < min_weight):
            min_weight = subtree_weight
            ans = node_h
    
    print('Ответ: ', ans)
    print('Вес дерева: ', min_weight)


    # ============================== Интерфейс =======================================     
            
    # while(True):
    #     print('Просмотреть информацию о больницах? Y/N ')
    #     if (input() == 'Y'):
    #         print('Номера N узлов-больниц: ')
    #         for i in hospitals:
    #             print(i)
    #         print('Введите номер узла-больницы: ')
    #         node_h = str(input())
    #         print('Ближайший дом: ')
    #         min_dist = math.inf
    #         nearest_building = ''
    #         for node_b in buildings:
    #             if hospitals_to_buildings[node_h][node_b] < min_dist:
    #                 nearest_building = node_b
    #                 min_dist = hospitals_to_buildings[node_h][node_b]
    #         print(nearest_building)
    #         print('Расстояние до него: ')
    #         print(min_dist)
    #         print('Путь до него: ')
    #         (D, Parent) = hospital_trees[node_h]
    #         print(graph.getWayInTree(Parent, node_h, nearest_building))
    #     else:
    #         break

    #     print('Просмотреть информацию о домах? Y/N ')
    #     if (input() == 'Y'):
    #         print('Номера M узлов-домов: ')
    #         for i in buildings:
    #             print(i)
    #         print('Введите номер узла-дома: ')
    #         node_b = str(input())
    #         print('Ближайшая больница: ')
    #         min_dist = math.inf
    #         nearest_hospital = ''
    #         for node_h in hospitals:
    #             if buildings_to_hospitals[node_b][node_h] < min_dist:
    #                 nearest_hospital = node_h
    #                 min_dist = buildings_to_hospitals[node_b][node_h]
    #         print(nearest_hospital)
    #         print('Расстояние до неё: ')
    #         print(min_dist)
    #         print('Путь до неё: ')
    #         (D, Parent) = building_trees[node_b]
    #         print(graph.getWayInTree(Parent, node_b, nearest_hospital))
    #     else:
    #         break



    # ================================= 2 задание ======================================

    print ('Задание 2')

    hospital = hospitals[0]
    (D,Parent) = hospital_trees[hospital]
    subtree_edges = graph.getSubtreeEdges(Parent,hospital,buildings)
    weight = graph.getSubtreeWeight(subtree_edges,g)
    sum_w = 0
    for node_b in buildings:
        sum_w = sum_w + D[node_b]
    print('Длина дерева:',weight)
    print('Сумма расстояний:',sum_w)


    for n in [2,3,5]:
        print(n,'кластеров: ')
        clusters = cluster.Clustering(buildings,g,n)
        centers = cluster.FindCenters(clusters,g,coords)
        subtree_edges_obj = graph.getSubtreeEdges(Parent,hospital,centers)
        sum_w = 0
        subtree_edges = subtree_edges_obj.copy()
        for i in range(len(clusters)):
            sum_w = sum_w + D[centers[i]]
            (D_cluster,Parent_cluster) = graph.Dijkstra(g,centers[i])
            subtree_edges_cluster = graph.getSubtreeEdges(Parent_cluster,centers[i],clusters[i])
            subtree_edges.update(subtree_edges_cluster)
            for node in clusters[i]:
                sum_w = sum_w + D_cluster[node]
        weight = graph.getSubtreeWeight(subtree_edges,g)
        print('Длина дерева:',weight)
        print('Сумма расстояний:',sum_w)
        visualisation.drawClusters(buildings,clusters,n,g,coords)
        # cluster_info = pd.DataFrame(clusters)
        # cluster_info.to_csv('clusters/cluster_'+str(n)+'.csv')

    
if __name__ == "__main__":
    main()