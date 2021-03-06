from calabaza.modules.calabaza_game.calabaza import calabaza
from calabaza.modules.calabaza_game.weather import weather


class calabaza_game():
    calabaza = None

    def __init__(self):
        self.weather = weather(2759794)
        self.calabaza = calabaza()

    def tick(self):
        self.weather.tick()
        self.calabaza.add_external('weather', self.weather.get())
        self.calabaza.tick()

    def get(self):
        get_data = {}
        for mod in self.calabaza.body:
            get_data[mod] = self.calabaza.body[mod].get()
        get_data['weather'] = self.weather.get()
        return get_data

    def mod(self, name):
        return self.calabaza.body.get(name)
