class flight():
    def __init__(self, name, age):
        self.jina=name
        self.miaka=age


class a(flight()):
    def b(self):
        return self.jina
    

obj=a
print(obj)