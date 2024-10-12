from biblioteka import Biblioteka

def prideti_knyga():
    biblioteka = Biblioteka()
    biblioteka.nuskaityti_knygas()
    pavadinimas = input("Įveskite knygos pavadinimą: ")
    autorius = input("Įveskite knygos autorių: ")
    isleidimo_metai = int(input("Įveskite knygos išleidimo metus: "))
    zanras = input("Įveskite knygos žanrą: ")
    biblioteka.prideti_knyga(pavadinimas, autorius, isleidimo_metai, zanras)
    print("Knyga pridėta sėkmingai.")