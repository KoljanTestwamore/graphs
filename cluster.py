import xmlparser
import graph
import numpy as np
import math
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from matplotlib import pyplot as plt

# def Clustering(elems,G,n):
#     print('Разбиваем вершины на ', n, 'кластеров ...')

#     clusters = []
#     elems_trees = {}
#     for elem in elems:
#         clusters.append([elem])
#         elems_trees[elem] = graph.Dijkstra(G,elem)

#     while(len(clusters) > n):
#         dist = np.zeros((len(clusters),len(clusters))) 
#         for i in range(len(clusters)):
#             for j in range(i+1,len(clusters)):
#                 max_d = 0
#                 for elem_1 in clusters[i]:
#                     (D,Parent) = elems_trees[elem_1]
#                     for elem_2 in clusters[j]:
#                         d = D[elem_2]
#                         if (d > max_d):
#                             dist[i][j] = d
#                             dist[j][i] = d

#         min_d = math.inf
#         curr_i = 0
#         curr_j = 0
#         for i in range(len(clusters)):
#             for j in range(len(clusters)):
#                 if(i == j):
#                     continue
#                 if (dist[i][j] < min_d):
#                     min_d = dist[i][j]
#                     curr_i = i
#                     curr_j = j

#         new_cluster = clusters[curr_i] + clusters[curr_j]
#         clusters.pop(curr_i)
#         clusters.pop(curr_j-1)
#         clusters.append(new_cluster)

#     return clusters

def DistanceMatrix(elems,G,n):

    elems_trees = {}
    for elem in elems:
        elems_trees[elem] = graph.Dijkstra(G,elem)

    dist = []
    for i in range(len(elems)):
        (D,Parent) = elems_trees[elems[i]]
        for j in range(i+1,len(elems)):
            dist.append(D[elems[j]])                      

    return dist



def Clustering(elems,G,n):

    dist = DistanceMatrix(elems,G,n)
    clusters = []
    Z = linkage(dist, 'complete')
    flat_cluster = fcluster(Z,n,criterion='maxclust')

    for i in range(max(flat_cluster)):
        clusters.append([])

    for i in range(len(elems)):
        clusters[flat_cluster[i] - 1].append(elems[i])

    fig = plt.figure(figsize=(25, 10))
    dn = dendrogram(Z)
    plt.show()

    return clusters




def FindCenters(clusters,G,coords):

    centers = []

    for cluster in clusters:
        center_lat = 0
        center_lon = 0
        for elem in cluster:
            (lat,lon) = coords[elem]
            lat = float(lat)
            lon = float(lon)
            center_lat = center_lat + lat
            center_lon = center_lon + lon
        center_lat = center_lat / len(cluster)
        center_lon = center_lon / len(cluster)
        center_node = graph.NearestNode2(G,coords,center_lat,center_lon)
        centers.append(center_node)

    return centers








