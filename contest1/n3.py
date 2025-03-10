class Taxi(object):
    def __init__(self, id, pos, time, length, speed):
        self.id = id
        self.pos = pos
        self.time = time
        self.length = length
        self.speed = speed

    def update(self, pos, time):
        self.pos = pos
        self.time = time

    def check(self, pos, time, order_time):
        rel_pos = (pos + self.length - self.pos) % self.length
        if (rel_pos + 1) / self.speed <= time - self.time:
            max_dist = self.length - 1
        else:
            max_dist = rel_pos
        return max_dist / self.speed <= order_time


n, l, s = [int(i) for i in input().split()]
taxi_db = dict()
for i in range(n):
    inp = input().split()
    if inp[0] == "TAXI":
        time, id, pos = [int(i) for i in inp[1:]]
        if id in taxi_db:
            taxi_db[id].update(pos, time)
        else:
            taxi_db[id] = Taxi(id, pos, time, l, s)
    else:
        time, id, pos, order_time = [int(i) for i in inp[1:]]
        amount = 0
        can_go = []
        for taxi in taxi_db.values():
            if taxi.check(pos, time, order_time):
                can_go.append(taxi.id)
                amount += 1
            if amount == 5:
                break
        if amount == 0:
            print(-1)
        else:
            print(*can_go)
