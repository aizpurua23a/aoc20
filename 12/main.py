from numpy import cos, sin, radians, array, float64, int64


def get_playbook(filename):
    with open(filename, 'r') as file:
        return [(instruction[0], int(instruction[1:])) for instruction in file.read().splitlines()]


class Ship:
    def __init__(self, initial_pos, initial_bearing):
        self.x = initial_pos[0]
        self.y = initial_pos[1]
        self.current_bearing = initial_bearing  # One of E S W N

    def __repr__(self):
        return "Currently at ({}, {}), heading {}. Manhattan distance is: {}".format(self.x, self.y,
                                                                                     self.current_bearing,
                                                                                     self.manhattan_distance())

    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)

    def sail(self, playbook):
        for bearing, amount in playbook:
            if bearing in ('L', 'R'):
                self.steer(bearing, amount)

            if bearing in ('N', 'E', 'S', 'W'):
                self.move_cardinal(bearing, amount)

            if bearing == 'F':
                self.move_cardinal(self.current_bearing, amount)

    def steer(self, towards, amount):
        cardinal_points = ('N', 'E', 'S', 'W')
        increment = amount//90
        index = cardinal_points.index(self.current_bearing)
        if towards == 'R':
            self.current_bearing = cardinal_points[index - len(cardinal_points) + increment]
        if towards == 'L':
            self.current_bearing = cardinal_points[index - increment]

    def move_cardinal(self, bearing, distance):
        if bearing == 'N':
            self.y = self.y + distance
        if bearing == 'S':
            self.y = self.y - distance
        if bearing == 'E':
            self.x = self.x + distance
        if bearing == 'W':
            self.x = self.x - distance


class WaypointShip:
    def __init__(self, initial_pos, initial_vector):
        self.pos = array(initial_pos.copy())
        self.dpos = array(initial_vector.copy())

    def __repr__(self):
        return "Currently at {}, waypoint relative pos: {}. MD from 0,0: {}".format(self.pos, self.dpos, self.manhattan_distance())

    def manhattan_distance(self):
        return sum(abs(coord) for coord in self.pos)

    def sail(self, playbook):
        for bearing, amount in playbook:
            if bearing in ('L', 'R'):
                self.rotate_waypoint(bearing, amount)
            if bearing in ('N', 'E', 'S', 'W'):
                self.move_wayopint(bearing, amount)
            if bearing == 'F':
                self.go_forward(amount)

    def rotate_waypoint(self, towards, amount):
        if towards == 'R':
            amount *= -1
        c, s = cos(radians(float64(amount))), sin(radians(float64(amount)))
        rotation_matrix = array(((c, -s), (s, c)))
        result = rotation_matrix.dot(self.dpos)
        self.dpos = array([int(round(element))for element in result])

    def move_wayopint(self, bearing, distance):
        increment = array([0, 0])
        if bearing == 'N':
            increment = (0, distance)
        if bearing == 'S':
            increment = (0, -distance)
        if bearing == 'E':
            increment = (distance, 0)
        if bearing == 'W':
            increment = (-distance, 0)
        self.dpos += increment

    def go_forward(self, amount):
        self.pos += self.dpos * amount


if __name__ == '__main__':
    playbook = get_playbook('input.txt')
    s = Ship((0, 0), 'E')
    s.sail(playbook)
    print(s)

    ws = WaypointShip([0, 0], [10, 1])
    ws.sail(playbook)
    print(ws)



