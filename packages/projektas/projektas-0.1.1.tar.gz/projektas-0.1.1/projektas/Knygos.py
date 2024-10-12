
class Knyga:
    def __init__(self, pavadinimas, autorius, isleidimo_metai, zanras):
        self.pavadinimas = pavadinimas
        self.autorius = autorius
        self.isleidimo_metai = isleidimo_metai
        self.zanras = zanras
        self.paimta = False
        self.grazinimo_data = None

    def __str__(self):
        return f"Pavadinimas: {self.pavadinimas}, Autorius: {self.autorius}, Išleidimo metai: {self.isleidimo_metai}, Žanras: {self.zanras}"