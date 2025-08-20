class Address:
    def __init__(self, index, city, street, building, flat):
        self.index = index
        self.city = city
        self.street = street
        self.building = building
        self.flat = flat
    def __str__(self):
        return f"{self.index} {self.city}, {self.street}, {self.building}, {self.flat}"