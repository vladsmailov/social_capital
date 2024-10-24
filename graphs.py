
from pyvis.network import Network


def graph_define(nodes_indexes, edges, titles, nodes_sizes, lables):
    color_map = []
    nodes = []

    for index in nodes_indexes:
        nodes.append(index-1)
    for node in nodes:
        if node == 14:
            color_map.append('red')
        elif node in (1, 2, 8, 12, 25, 32):
            color_map.append('orange')
        elif node in (3, 4, 13, 43):
            color_map.append('pink')
        elif node in (5, 11, 16, 23, 33, 39, 42):
            color_map.append('blue')
        elif node in (6, 15, 29, 37):
            color_map.append('silver')
        elif node in (7, 9, 24, 30):
            color_map.append('grey')
        elif node in (10, 19):
            color_map.append('yellow')
        elif node in (17, 20, 26, 35):
            color_map.append('brown')
        elif node in (21, 27, 28, 34, 41):
            color_map.append('purple')
        else:
            color_map.append('green')

    net = Network("1000px", "100%", directed=True, cdn_resources="remote", filter_menu=True, neighborhood_highlight=True, bgcolor="#b0b0b0")

    net.add_nodes(
        nodes=nodes,
        label=lables,
        size=[size[1] for size in nodes_sizes.items()],
        title=titles,
        color=color_map
    )
    for edge in edges:
        net.add_edge(edge[0]-1, edge[1]-1)
    net.show_buttons(filter_=['nodes', 'edges', 'physics'])
    net.force_atlas_2based()
    net.toggle_physics(False)
    net.show('graph5.html', notebook=False)
    net.save_graph('graph5.html')
    net.write_html('grath.html')