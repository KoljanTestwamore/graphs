import xmlparser
import random
import math
import heapq
from geopy.distance import geodesic


# def getGraphList():
#     print('Строим граф...')
#     streets = xmlparser.getRoads()
#     graph_list = {}
#     coords = xmlparser.getNodesCoords()
#     for street in streets:

#         # проверка на одностороннее движение
#         oneway = False
#         if 'oneway' in street.keys():
#             if (street['oneway'] == 'yes') or (street['oneway'] == 'true') or (street['oneway'] == '1'):
#                 oneway = True
#         if 'junction' in street.keys():
#             if (street['junction'] == 'roundabout'):
#                 oneway = True
#         if (street['highway'] == 'motorway') or (street['highway'] == 'motorway_link'):
#             oneway = True

#         # пустой список смежности
#         refs = street['refs']
#         for node in refs:
#             if (not node in graph_list.keys()):
#                 graph_list[node] = []

#         # ребра
#         for i in range(len(refs)):
#             if (i < len(refs) - 1):
#                 node1_coords = coords[refs[i]]
#                 node2_coords = coords[refs[i + 1]]
#                 distance = geodesic(node1_coords, node2_coords).m
#                 graph_list[refs[i]].append((refs[i+1],distance))
#                 if (not oneway):
#                     graph_list[refs[i+1]].append((refs[i],1))

#     # веса вершин
#     weights = {}
#     for v in graph_list.keys():
#         weights[v] = random.random() + 1

#     print('Граф построен')
#     return (graph_list, weights)

def getGraphList():
    print('Строим граф...')
    streets = xmlparser.getRoads()
    graph_list = {}
    coords = xmlparser.getNodesCoords()
    for street in streets:

        # проверка на одностороннее движение
        oneway = False
        if 'oneway' in street.keys():
            if (street['oneway'] == 'yes') or (street['oneway'] == 'true') or (street['oneway'] == '1'):
                oneway = True
        if 'junction' in street.keys():
            if (street['junction'] == 'roundabout'):
                oneway = True
        if (street['highway'] == 'motorway') or (street['highway'] == 'motorway_link'):
            oneway = True

        # пустой список смежности
        refs = street['refs']
        for node in refs:
            if (not node in graph_list.keys()):
                graph_list[node] = {}

        # ребра
        for i in range(len(refs)):
            if (i < len(refs) - 1):
                node1_coords = coords[refs[i]]
                node2_coords = coords[refs[i + 1]]
                distance = geodesic(node1_coords, node2_coords).m * (random.random() + 1)
                graph_list[refs[i]][refs[i+1]] = distance 
                if (not oneway):
                    graph_list[refs[i+1]][refs[i]] = distance

    print('Граф построен')
    return graph_list


# def NearestNode(G,coords,obj):
#     print('Ищем вершину, ближайшую к: ', obj, '...')
    
#     obj_coords = coords[obj]
#     min_dist = math.inf

#     for node in G:
#         node_coords = coords[node]
#         distance = geodesic(node_coords, obj_coords).m
#         if (distance < min_dist):
#             min_dist = distance
#             result = node
#     return result

def NearestNode(G,coords,obj):
    # print('Ищем вершину, ближайшую к: ', obj, '...')
    
    (obj_lat, obj_lon) = coords[obj]
    obj_lat = float(obj_lat)
    obj_lon = float(obj_lon)
    min_dist = math.inf

    for node in G:
        (lat,lon) = coords[node]
        lat = float(lat)
        lon = float(lon)
        distance = (lat-obj_lat)**2 + (lon-obj_lon)**2
        if (distance < min_dist):
            min_dist = distance
            result = node
    return result

def NearestNode2(G,coords,obj_lat,obj_lon):
    min_dist = math.inf

    for node in G:
        (lat,lon) = coords[node]
        lat = float(lat)
        lon = float(lon)
        distance = (lat-obj_lat)**2 + (lon-obj_lon)**2
        if (distance < min_dist):
            min_dist = distance
            result = node
    return result

def Dijkstra(G, start_node):
    # print('Строим дерево кратчайших путей из вершины: ', start_node, '...')
    D = {}
    Parent = {}

    for node in G:
        D[node] = math.inf
        Parent[node] = node
    D[start_node] = 0

    q = []
    heapq.heappush(q,(0, start_node))


    while (len(q) > 0):

        node_info = heapq.heappop(q)
        (dist,curr_node) = node_info
        if (dist > D[curr_node]):
            continue

        for child_node in G[curr_node]:
            distance = G[curr_node][child_node]
            if (D[child_node] > D[curr_node] + distance):
                D[child_node] = D[curr_node] + distance
                Parent[child_node] = curr_node
                heapq.heappush(q,(D[child_node],child_node))

    # print('Дерево построено')
    return (D,Parent)

def getWayInTree(Parent, start_node, end_node):
    way = []
    way.insert(0, end_node)
    curr_node = end_node

    while (curr_node != start_node):
        curr_node = Parent[curr_node]
        way.insert(0, curr_node)

    return way


def getSubtreeEdges(Parent, start_node, end_nodes):

    subtree_edges = {}
    for end_node in end_nodes:
        way = getWayInTree(Parent,start_node,end_node)
        for i in range(len(way) - 1):
            subtree_edges[way[i]] = way[i+1]

    return subtree_edges

def getSubtreeWeight(subtree_edges, G):

    subtree_weight = 0

    for node_1 in subtree_edges:
        node_2 = subtree_edges[node_1]
        subtree_weight = subtree_weight + G[node_1][node_2]
        
    return subtree_weight





