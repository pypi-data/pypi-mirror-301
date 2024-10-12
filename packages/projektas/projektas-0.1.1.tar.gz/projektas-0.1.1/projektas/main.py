import streamlit as st
from Prideti_knyga import prideti_knyga
from biblioteka import Biblioteka
from Isimti_knyga import isimti_knyga
from Knygos import Knyga


def main():
    st.title("Biblioteka")
    st.header("Prisijungti")

    username = st.text_input("Įveskite naudotojo vardą:")
    password = st.text_input("Įveskite slaptažodį:", type="password")

    if st.button("Prisijungti"):
        if username == "bibliotekininkas" and password == "slaptazodis":
            st.header("Bibliotekininkas")
            biblioteka = Biblioteka()
            biblioteka.nuskaityti_knygas()

            options = ["Pridėti knygą", "Išimti knygą", "Peržiūrėti visas knygas", "Peržiūrėti visas vėluojančias knygas", "Išeiti"]
            choice = st.selectbox("Pasirinkite funkciją:", options)

            if choice == "Pridėti knygą":
                prideti_knyga()
            elif choice == "Išimti knygą":
                isimti_knyga()
            elif choice == "Peržiūrėti visas knygas":
                biblioteka.perziureti_visas()
            elif choice == "Peržiūrėti visas vėluojančias knygas":
                biblioteka.perziureti_veluojancias()
            elif choice == "Išeiti":
                st.write("Sėkmingai išėjote iš sistema.")
        elif username == "skaitytojas" and password == "slaptazodis":
            st.header("Skaitytojas")
            biblioteka = Biblioteka()
            biblioteka.nuskaityti_knygas()

            options = ["Paimti knygą", "Gražinti knygą", "Peržiūrėti visas knygas", "Peržiūrėti visas vėluojančias knygas", "Išeiti"]
            choice = st.selectbox("Pasirinkite funkciją:", options)

            if choice == "Paimti knygą":
                pavadinimas = st.text_input("Įveskite knygos pavadinimą:")
                skaitytojas = st.text_input("Įveskite skaitytojo kortelės numerį:")
                biblioteka.paimti_knyga(pavadinimas, skaitytojas)
            elif choice == "Gražinti knygą":
                pavadinimas = st.text_input("Įveskite knygos pavadinimą:")
                skaitytojas = st.text_input("Įveskite skaitytojo kortelės numerį:")
                biblioteka.grazinti_knyga(pavadinimas, skaitytojas)
            elif choice == "Peržiūrėti visas knygas":
                biblioteka.perziureti_visas()
            elif choice == "Peržiūrėti visas vėluojančias knygas":
                biblioteka.perziureti_veluojancias()
            elif choice == "Išeiti":
                st.write("Sėkmingai išėjote iš sistema.")
        else:
            st.write("Neteisingas naudotojo vardas arba slaptažodis.")

if __name__ == "__main__":
    main()