
import streamlit as st
import datetime

# Inicjalizacja sesji
if "grupy" not in st.session_state:
    st.session_state["grupy"] = {}  # {"1": ["Jan Kowalski", "Anna Nowak"]}
if "kolumny_obecnosc" not in st.session_state:
    st.session_state["kolumny_obecnosc"] = []

# MENU
menu = st.sidebar.radio("📋 Menu", ["Edycja", "Trening", "Testy", "Dane"])

if menu == "Edycja":
    st.title("🛠️ Edycja danych")

    with st.form("nowa_grupa"):
        st.subheader("➕ Stwórz nową grupę")
        nazwa_grupy = st.text_input("Nazwa grupy")
        zawodnicy = st.text_area("Lista zawodników (jeden na linię)").split("\n")
        submitted = st.form_submit_button("Dodaj grupę")
        if submitted and nazwa_grupy and zawodnicy:
            st.session_state["grupy"][nazwa_grupy] = [z.strip() for z in zawodnicy if z.strip()]
            st.success(f"Dodano grupę: {nazwa_grupy}")

    st.subheader("🧑‍🤝‍🧑 Istniejące grupy")
    for grupa, zawodnicy in st.session_state["grupy"].items():
        with st.expander(f"Grupa: {grupa}"):
            for i, zawodnik in enumerate(zawodnicy):
                col1, col2 = st.columns([4,1])
                col1.write(zawodnik)
                if col2.button("Usuń", key=f"{grupa}_{i}"):
                    st.session_state["grupy"][grupa].remove(zawodnik)
                    st.experimental_rerun()

    st.subheader("➕ Dodaj kolumnę do listy obecności")
    nowa_kolumna = st.text_input("Nazwa nowej kolumny")
    if st.button("Dodaj kolumnę"):
        if nowa_kolumna and nowa_kolumna not in st.session_state["kolumny_obecnosc"]:
            st.session_state["kolumny_obecnosc"].append(nowa_kolumna)
            st.success(f"Dodano kolumnę: {nowa_kolumna}")

elif menu == "Trening":
    st.title("🏊 Formularz treningowy")
    dzien = st.date_input("Wybierz datę", datetime.date.today())
    godzina = st.time_input("Godzina treningu", datetime.datetime.now().time())
    rodzaj = st.selectbox("Trening", ["woda", "ląd"])
    grupa = st.selectbox("Wybierz grupę", list(st.session_state["grupy"].keys()) or [""])

    if grupa in st.session_state["grupy"]:
        zawodnicy = st.session_state["grupy"][grupa]
        kolumny = st.session_state["kolumny_obecnosc"]
        st.subheader("📋 Formularz")
        dane = {}
        for zawodnik in zawodnicy:
            row = {}
            col = st.columns(2 + len(kolumny))
            row["Obecny"] = col[0].checkbox("Obecny", key=f"{grupa}_{zawodnik}_ob")
            col[1].write(zawodnik)
            for i, kol in enumerate(kolumny):
                row[kol] = col[i+2].text_input(kol, key=f"{grupa}_{zawodnik}_{kol}")
            dane[zawodnik] = row

        if st.button("Zapisz trening"):
            st.success("✅ Zapisano dane treningowe (tymczasowo w pamięci)")

elif menu == "Testy":
    st.title("🧪 Formularz testów")
    dzien = st.date_input("Data testu", datetime.date.today())
    nazwa = st.text_input("Nazwa testu")
    grupa = st.selectbox("Wybierz grupę", list(st.session_state["grupy"].keys()) or [""])

    if grupa in st.session_state["grupy"]:
        zawodnicy = st.session_state["grupy"][grupa]
        kolumny = st.session_state["kolumny_obecnosc"]
        st.subheader("📋 Wyniki testu")
        dane = {}
        for zawodnik in zawodnicy:
            row = {}
            col = st.columns(1 + len(kolumny))
            col[0].write(zawodnik)
            for i, kol in enumerate(kolumny):
                row[kol] = col[i+1].text_input(kol, key=f"{grupa}_{zawodnik}_t_{kol}")
            dane[zawodnik] = row

        if st.button("Zapisz test"):
            st.success("✅ Zapisano dane testowe (tymczasowo w pamięci)")

elif menu == "Dane":
    st.title("📊 Zakładka danych")
    st.write("Dane nie są jeszcze zapisywane trwale. Później dodamy eksport CSV lub zapis na serwerze.")
