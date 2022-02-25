from csv import reader


def import_csv_layout(path):
    terrain_map = []
    path = './levels/0/level_0..tmx'
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map
