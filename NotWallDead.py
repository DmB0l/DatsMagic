import math


def wall_checking(transports, mapSize, maxAccel):
    undo_wall_dist = 1000  # Константа, можно менять

    command_to_transports = []
    ind = 0
    for transport in transports:
        transport_x = transport['x']
        transport_y = transport['y']

        map_size_x = mapSize['x']
        map_size_y = mapSize['y']

        # Проверки на углы
        if transport_x <= undo_wall_dist and transport_y <= undo_wall_dist:
            if transport['velocity']['x'] < 0 or transport['velocity']['y'] < 0:
                command_to_transports.append({'wall_danger': True, 'x': maxAccel, 'y': maxAccel})

        elif transport_x >= map_size_x - undo_wall_dist and transport_y <= undo_wall_dist:
            if transport['velocity']['x'] > 0 or transport['velocity']['y'] < 0:
                command_to_transports.append({'wall_danger': True, 'x': -maxAccel, 'y': maxAccel})

        elif transport_x <= undo_wall_dist and transport_y >= map_size_y - undo_wall_dist:
            if transport['velocity']['x'] < 0 or transport['velocity']['y'] > 0:
                command_to_transports.append({'wall_danger': True, 'x': maxAccel, 'y': -maxAccel})

        elif transport_x >= map_size_x - undo_wall_dist and transport_y >= map_size_y - undo_wall_dist:
            if transport['velocity']['x'] > 0 or transport['velocity']['y'] > 0:
                command_to_transports.append({'wall_danger': True, 'x': -maxAccel, 'y': -maxAccel})


        # Проверка на стороны
        elif transport_x <= undo_wall_dist:
            if transport['velocity']['x'] < 0:
                command_to_transports.append({'wall_danger': True, 'x': maxAccel, 'y': 0})

        elif transport_x >= map_size_x - undo_wall_dist:
            if transport['velocity']['x'] > 0:
                command_to_transports.append({'wall_danger': True, 'x': -maxAccel, 'y': 0})

        elif transport_y <= undo_wall_dist:
            if transport['velocity']['y'] < 0:
                command_to_transports.append({'wall_danger': True, 'x': 0, 'y': maxAccel})

        elif transport_y >= map_size_y - undo_wall_dist:
            if transport['velocity']['y'] > 0:
                command_to_transports.append({'wall_danger': True, 'x': 0, 'y': -maxAccel})

        else:
            command_to_transports.append({'wall_danger': False, 'x': 0, 'y': 0})

        ind += 1

    return command_to_transports
