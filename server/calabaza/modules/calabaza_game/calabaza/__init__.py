

class expresion():
    OK = 0

    def tick(self, calabaza):
        calabaza.body.get('energy').dec(0.0001)

    def get(self):
        return self.OK


class energy():
    energy = 100.0

    def set(self, val):
        self.energy = val
        return self.energy

    def dec(self, val):
        self.energy -= val
        if self.energy < 0.0:
            self.energy == 0.0

    def get(self):
        return self.energy

    def tick(self, calabaza):
        return


class alpha_status():
    alpha = 0.0

    def tick(self, calabaza):
        energy_prop = calabaza.body.get('energy')
        energy = energy_prop.get()
        if energy < 10.0 and self.alpha <= 0.0:
            self.alpha = 100.0
            energy_prop.set(30.0)

    def get(self):
        return self.alpha


class health():
    molecular = 100.0

    def tick(self, calabaza):
        alpha = calabaza.body.get('alpha_status').get()

        if alpha > 0.0:
            self.molecular += 0.001

    def get(self):
        return self.molecular


class calabaza():
    body = {}

    def __init__(self, weather):
        self.body['weather'] = weather
        self.body['energy'] = energy()
        self.body['alpha_status'] = alpha_status()
        self.body['expresion'] = expresion()
        self.body['health'] = health()

    def tick(self):
        for mod in self.body:
            self.body[mod].tick(self)
