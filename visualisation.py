import xmlparser 
import matplotlib.pyplot as plt
# ============================== Визуализация через Matplotlib ============================================

def drawGraph(G):

    coords = xmlparser.getNodesCoords()

    fig = plt.gcf()
    fig.set_size_inches(24, 24, forward=True)
    i = 0
    for node in G:
        (node_lat, node_lon) = coords[node]
        node_lat = float(node_lat)
        node_lon = float(node_lon)
        for adj_node in G[node]:
            (adj_node_lat,adj_node_lon) = coords[adj_node]
            adj_node_lat = float(adj_node_lat)
            adj_node_lon = float(adj_node_lon)
            plt.plot([node_lat,adj_node_lat], [node_lon,adj_node_lon], 'black')
        i = i + 1
        print(i)
    fig.savefig('Tomsk.png', dpi=100)
    # plt.show()

def drawEdges(edge_list,G,coords):
    print('Рисуем дерево... ')
    fig = plt.gcf()
    fig.set_size_inches(24, 24, forward=True)
    for node in edge_list:
        (node_lat, node_lon) = coords[node]
        node_lat = float(node_lat)
        node_lon = float(node_lon)
        for adj_node in G[node]:
            (adj_node_lat,adj_node_lon) = coords[adj_node]
            adj_node_lat = float(adj_node_lat)
            adj_node_lon = float(adj_node_lon)
            plt.plot([node_lat,adj_node_lat], [node_lon,adj_node_lon], 'red')
    fig.savefig('Tree.png', dpi=100)
    # plt.show()

def drawClusters(nodes,clusters,n,G,coords):
    colors = ['red','blue','green','yellow','pink']
    fig = plt.gcf()
    fig.set_size_inches(24, 24, forward=True)
    for i in range(n):
        for node in clusters[i]:
            (node_lat, node_lon) = coords[node]
            node_lat = float(node_lat)
            node_lon = float(node_lon)
            plt.plot(node_lat,node_lon, color=colors[i], marker='o', markersize=4)
    fig.savefig('pictures/Clusters_'+str(n)+'.png', dpi=100)
    # plt.show()
