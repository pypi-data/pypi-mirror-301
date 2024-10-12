from biblioteka import Biblioteka

def isimti_knyga():
    biblioteka = Biblioteka()
    biblioteka.nuskaityti_knygas()
    pavadinimas = input("Įveskite knygos pavadinimą: ")
    biblioteka.isimti_knyga(pavadinimas)
    print("Knyga išimta sėkmingai")