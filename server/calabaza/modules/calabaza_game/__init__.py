

class expresion():
    OK = 0

    def tick(self, calabaza):
        calabaza.body.get('energy').dec(0.0001)

    def get(self):
        return self.OK


class energy():
    energy = 100.0

    def get(self):
        return self.energy

    def set(self, val):
        self.energy = val
        return self.energy

    def dec(self, val):
        self.energy -= val
        if energy < 0.0:
            self.energy == 0.0


class alpha_status():
    alpha = 0.0

    def tick(self, calabaza):
        energy_prop = calabaza.body.get('energy')
        energy = energy_prop.get()
        if energy < 10.0 and self.alpha <= 0.0:
            self.alpha = 100.0
            energy_prop.set(30.0)


class health():
    molecular = 100.0

    def tick(self, calabaza):
        alpha = calabaza.body.get('alpha_status').get()

        if alpha > 0.0:
            self.molecular += 0.001


class calabaza():
    body = []

    def __init__(self):
        self.body['energy'] = energy
        self.body['alpha_status'] = alpha_status
        self.body['expresion'] = expresion

    def tick(self):
        for mod in self.body:
            self.body[mod].tick(self)


class calabaza_game():
    calabaza = None

    def __init__(self):
        self.calabaza = calabaza

    def tick(self):
        self.calabaza.tick()
