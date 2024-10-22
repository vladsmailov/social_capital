#!/usr/bin/env python
# coding: utf-8

# In[35]:


import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()  # создаём объект графа

# определяем список узлов (ID узлов)
nodes = [1, 2, 3, 4, 5, 6, 7]

# определяем список рёбер
# список кортежей, каждый из которых представляет ребро
# кортеж (id_1, id_2) означает, что узлы id_1 и id_2 соединены ребром
edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 5), (6, 4), (2, 6), (4, 7)]

# добавляем информацию в объект графа
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# задаем цвета (1 - директор, 2, 3 - завучи)
color_map = []
for node in G:
    if node == 1:
        color_map.append('red')
    elif node in (2, 3):
        color_map.append('orange')
    else:
        color_map.append('green')

    # рисуем граф и отображаем его
nx.draw(G, with_labels=True, font_weight='bold', node_color=color_map, node_size=2000)
plt.show()

# In[43]:


import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()  # создаём объект графа

# определяем список узлов (ID узлов)
nodes = [1, 2, 3, 4, 5, 6, 7]

# определяем список рёбер
# список кортежей, каждый из которых представляет ребро
# кортеж (id_1, id_2) означает, что узлы id_1 и id_2 соединены ребром
edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 5), (6, 4), (2, 6), (4, 7)]

# добавляем информацию в объект графа
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# задаем цвета (1 - директор, 2, 3 - завучи)
color_map = []
for node in G:
    if node == 1:
        color_map.append('red')
    elif node in (2, 3):
        color_map.append('orange')
    else:
        color_map.append('green')

    # рисуем граф и отображаем его
fig, ax = plt.subplots(figsize=(10, 10))
pos = nx.spring_layout(G, k=0.5, iterations=50)
nx.draw_networkx(G, pos=pos, with_labels=True, font_weight='bold', node_color=color_map, node_size=2000, ax=ax)

# Делаем граф интерактивным
cid = fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, G, pos, ax))
plt.show()


# Функция обработки клика мыши
def on_click(event, G, pos, ax):
    if event.inaxes == ax:
        for node, coords in pos.items():
            if ((event.xdata - coords[0]) ** 2 + (event.ydata - coords[1]) ** 2) < 0.1 ** 2:
                pos[node] = [event.xdata, event.ydata]
                nx.draw_networkx(G, pos=pos, with_labels=True, font_weight='bold', node_color=color_map, node_size=2000,
                                 ax=ax)
                plt.draw()
                break


# In[44]:


import matplotlib.pyplot as plt
from pyvis.network import Network

# Создаём объект графа
g = Network(height='100%', width='100%', bgcolor='#222222', font_color='white')

# определяем список узлов (ID узлов)
nodes = [1, 2, 3, 4, 5, 6, 7]

# определяем список рёбер
# список кортежей, каждый из которых представляет ребро
# кортеж (id_1, id_2) означает, что узлы id_1 и id_2 соединены ребром
edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 5), (6, 4), (2, 6), (4, 7)]

# добавляем информацию в объект графа
for node in nodes:
    g.add_node(node)

for edge in edges:
    g.add_edge(edge[0], edge[1])

# задаем цвета (1 - директор, 2, 3 - завучи)
for node in nodes:
    if node == 1:
        g.get_node(node)['color'] = 'red'
    elif node in (2, 3):
        g.get_node(node)['color'] = 'orange'
    else:
        g.get_node(node)['color'] = 'green'

# Делаем граф интерактивным
g.show_buttons(filter_=['physics'])
g.save_graph('graph.html')

# In[ ]:




