import math

import networkx as nx


class GridTools:
    """
    Tools to handling grid and map plan
    """

    # datamap format as bit activation for one position
    MOVE_NORTH_BLOCKED = 1
    MOVE_SOUTH_BLOCKED = 2
    MOVE_EAST_BLOCKED = 4
    MOVE_WEST_BLOCKED = 8

    @staticmethod
    # thanks to
    # https://www.analytics-link.com/post/2018/08/21/calculating-the-compass-direction-between-two-points-in-python
    # but with origin in upper left
    def direction_grid_neighbor(pos1, pos2, dist_type='manhattan'):
        """
        Return the direction of a neighbor from a position

        :param pos1: Initial position
        :param pos2: neighbor position
        :param dist_type: type of distance (manhattan, get N, S, E or W, euclidian, get all directions)
        :return: the direction according to the distance type. None if pos1=pos2
        """
        # next to but different position
        result = None
        delta_x = pos1[0] - pos2[0]
        delta_y = pos1[1] - pos2[1]
        degrees_temp = math.atan2(delta_x, delta_y) / math.pi * 180
        if degrees_temp < 0:
            degrees_final = 360 + degrees_temp
        else:
            degrees_final = degrees_temp
        compass_lookup = round(degrees_final / 45)
        if dist_type == 'manhattan':
            compass_brackets = ["N", None, "W", None, "S", None, "E", None, "N"]
            distance = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
            if distance == 1:
                result = compass_brackets[compass_lookup]
        if dist_type == 'euclidian':
            compass_brackets = ["N", "NW", "W", "SW", "S", "SE", "E", "NE", "N"]
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    if x != 0 or y != 0:
                        if pos1[0] + x == pos2[0] and pos1[1] + y == pos2[1]:
                            result = compass_brackets[compass_lookup]
        return result

    @staticmethod
    def is_connected_neighbor(data_map, from_pos, to_pos):
        """
        Return if positions are directly connected according to a datamap

        :param data_map: The datamap. See create_graph() for format
        :param from_pos: initial position
        :param to_pos: final position
        :return: True if there is a link between from_pos and to_pos
        """
        direction = GridTools.direction_grid_neighbor(from_pos, to_pos)
        result = GridTools.is_connected_by_direction(data_map, from_pos, direction)
        return result

    @staticmethod
    def is_connected_by_direction(data_map, from_pos, direction):
        """
        Calculate if we can go from a position to a direction

        :param data_map: The data map. See create_graph() for format
        :param from_pos: initial position
        :param direction: direction to go
        :return: True if the direction is not blocked in this position
        """
        result = False
        if direction == 'S' and not data_map[from_pos[1]][from_pos[0]] & GridTools.MOVE_SOUTH_BLOCKED:
            result = True
        if direction == 'N' and not data_map[from_pos[1]][from_pos[0]] & GridTools.MOVE_NORTH_BLOCKED:
            result = True
        if direction == 'E' and not data_map[from_pos[1]][from_pos[0]] & GridTools.MOVE_EAST_BLOCKED:
            result = True
        if direction == 'W' and not data_map[from_pos[1]][from_pos[0]] & GridTools.MOVE_WEST_BLOCKED:
            result = True
        return result

    @staticmethod
    def create_graph(data_map):
        """
        Create a directional graph from a data_map.

        Format for each square :
        bit 1 : North blocked, bit 2 : South blocked, bit 3 : East blocked, bit 4 : West blocked

        :param data_map: 2D array with the format described (bitwise) for each square
        :return: a networkx.DiGraph instance
        """
        graph = nx.DiGraph()
        map_size = (len(data_map[0]), len(data_map))
        for x in range(map_size[0]):
            for y in range(map_size[1]):
                graph.add_node((x, y))
        for node1 in graph.nodes:
            for node2 in graph.nodes:
                if GridTools.is_connected_neighbor(data_map, node1, node2):
                    graph.add_edge(node1, node2)
        return graph

    @staticmethod
    def adapt_path_from_selected(graph, origin, path, selected):
        """
        Adapt an existing path with a new position, if possible.

        :param graph: The graph used to adapt the path
        :param origin: the origin position
        :param path: path to adapt. Must be a valid path
        :param selected: the selected position to add or not into the path
        :return: the new path, adapted or not.
        """
        list_pos = [origin] + path + [selected]
        result = path
        if selected in path:
            result = path[:path.index(selected)]
        else:
            if nx.classes.function.is_path(graph, list_pos):
                result = list_pos[1:]
        return result
