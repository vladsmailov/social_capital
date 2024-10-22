import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network

def graph_define(nodes, edges, titles):
    # G = nx.Graph()  # создаём объект графа
    G = nx.karate_club_graph()

    # определяем список узлов (ID узлов)
    nodes = nodes

    # определяем список рёбер
    # список кортежей, каждый из которых представляет ребро
    # кортеж (id_1, id_2) означает, что узлы id_1 и id_2 соединены ребром
    edges = edges
    # добавляем информацию в объект графа
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # задаем цвета (1 - директор, 2, 3 - завучи)
    color_map = []
    for node in G:
        if node == 2:
            color_map.append('red')
        elif node in (3, 4):
            color_map.append('orange')
        else:
            color_map.append('green')

        # рисуем граф и отображаем его
    nx.draw_circular(G, with_labels=True, font_weight='bold', node_color=color_map, node_size=1000, arrows=True, arrowstyle='<-')
    plt.show()
    net = Network("2000px", "2000px", select_menu=True)  # создаём объект графа

    # добавление узлов
    net.add_nodes(
        nodes,  # node ids
        label=['директор', 'зам.директора', 'заведующий', 'заведующий', 'заведующий', 'программист', 'программист',
               'программист', 'специалист по УМР', 'специалист по УМР', 'методист', 'специалист по УМР', 'программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист','программист',],  # node labels
        # node titles (display on mouse hover)
        title=titles,
        color=['red', 'orange', 'green', 'green', 'green', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue',]
        # node colors (HEX)
    )
    # добавляем тот же список узлов, что и в предыдущем примере
    for edge in edges:
        net.add_edge(edge[0], edge[1])

    # net.toggle_physics(False)
    net.show_buttons(filter_=['physics'])
    net.show('graph5.html', notebook=False)  # save visualization in 'graph.html'
    net.save_graph('graph5.html')