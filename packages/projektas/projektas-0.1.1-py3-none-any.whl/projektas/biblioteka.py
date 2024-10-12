import pickle
from datetime import datetime, timedelta
from Knygos import Knyga

class Biblioteka:
    def __init__(self):
        self.knygos = []
        self.paimtos_knygos = {}

    def prideti_knyga(self, pavadinimas, autorius, isleidimo_metai, zanras):
        nauja_knyga = Knyga(pavadinimas, autorius, isleidimo_metai, zanras)
        self.knygos.append(nauja_knyga)
        self.issaugoti_knygas()

    def isimti_knyga(self, pavadinimas):
        for knyga in self.knygos:
            if knyga.pavadinimas == pavadinimas:
                self.knygos.remove(knyga)
                self.issaugoti_knygas()
                return
        print("Knyga nerasta.")

    def paimti_knyga(self, pavadinimas, skaitytojas):
        for knyga in self.knygos:
            if knyga.pavadinimas == pavadinimas and not knyga.paimta:
                knyga.paimta = True
                knyga.grazinimo_data = datetime.date.today() + datetime.timedelta(days=14)
                self.paimtos_knygos[skaitytojas] = knyga
                self.issaugoti_knygas()
                return
        print("Knyga nepaimta.")

    def grazinti_knyga(self, pavadinimas, skaitytojas):
        if skaitytojas in self.paimtos_knygos:
            knyga = self.paimtos_knygos[skaitytojas]
            if knyga.pavadinimas == pavadinimas:
                knyga.paimta = False
                del self.paimtos_knygos[skaitytojas]
                self.issaugoti_knygas()
                return
        print("Knyga nepraimta.")
        
    def perziureti_visas(self):
        for knyga in self.knygos:
            print(knyga)

    def perziureti_veluojancias(self):
        for skaitytojas, knyga in self.paimtos_knygos.items():
            if knyga.grazinimo_data < datetime.date.today():
                print(f"Knyga '{knyga.pavadinimas}' by {knyga.autorius} is overdue for {skaitytojas}.")

    def issaugoti_knygas(self):
        with open("knygos.pkl", "wb") as f:
            pickle.dump(self.knygos, f)

    def nuskaityti_knygas(self):
        try:
            with open("knygos.pkl", "rb") as f:
                self.knygos = pickle.load(f)
        except FileNotFoundError:
            pass