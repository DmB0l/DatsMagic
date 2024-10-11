import math


def wall_checking(transports, mapSize):
    undo_wall_dist = 30  # Константа, можно менять

    command_to_transports = []
    for transport in transports:
        transport_x = transport['x']
        transport_y = transport['y']

        map_size_x = mapSize['x']
        map_size_y = mapSize['y']

        # Проверки на углы
        if transport_x <= undo_wall_dist and transport_y <= undo_wall_dist:
            if transport['velocity']['x'] < 0 or transport['velocity']['y'] < 0:
                command_to_transports.append({'wall_danger': True, 'x': 10, 'y': 10})

        elif transport_x >= map_size_x - undo_wall_dist and transport_y <= undo_wall_dist:
            if transport['velocity']['x'] > 0 or transport['velocity']['y'] < 0:
                command_to_transports.append({'wall_danger': True, 'x': -10, 'y': 10})

        elif transport_x <= undo_wall_dist and transport_y >= map_size_y - undo_wall_dist:
            if transport['velocity']['x'] < 0 or transport['velocity']['y'] > 0:
                command_to_transports.append({'wall_danger': True, 'x': 10, 'y': -10})

        elif transport_x >= map_size_x - undo_wall_dist and transport_y >= map_size_y - undo_wall_dist:
            if transport['velocity']['x'] > 0 or transport['velocity']['y'] > 0:
                command_to_transports.append({'wall_danger': True, 'x': -10, 'y': -10})


        # Проверка на стороны
        elif transport_x <= undo_wall_dist:
            if transport['velocity']['x'] < 0:
                command_to_transports.append({'wall_danger': True, 'x': 10, 'y': 0})

        elif transport_x >= map_size_x - undo_wall_dist:
            if transport['velocity']['x'] > 0:
                command_to_transports.append({'wall_danger': True, 'x': -10, 'y': 0})

        elif transport_y <= undo_wall_dist:
            if transport['velocity']['y'] < 0:
                command_to_transports.append({'wall_danger': True, 'x': 0, 'y': 10})

        elif transport_y >= map_size_y - undo_wall_dist:
            if transport['velocity']['y'] > 0:
                command_to_transports.append({'wall_danger': True, 'x': 0, 'y': -10})

        else:
            command_to_transports.append({'wall_danger': False, 'x': 0, 'y': 0})

    return command_to_transports
