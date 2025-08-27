
import streamlit as st
import pandas as pd
import datetime

# Inicjalizacja sesji
if "zawodnicy" not in st.session_state:
    st.session_state.zawodnicy = []
if "kolumny_trening" not in st.session_state:
    st.session_state.kolumny_trening = ["Obecność"]
if "testy" not in st.session_state:
    st.session_state.testy = {}
if "grupy" not in st.session_state:
    st.session_state.grupy = {}

st.sidebar.title("Menu")
menu = st.sidebar.radio("Wybierz zakładkę:", ["Edycja", "Trening", "Testy", "Dane"])

def edycja():
    st.header("Edycja danych")

    with st.expander("1. Edytuj listę zawodników"):
        new_name = st.text_input("Dodaj zawodnika")
        if st.button("Dodaj zawodnika"):
            if new_name and new_name not in st.session_state.zawodnicy:
                st.session_state.zawodnicy.append(new_name)
        st.write("Lista zawodników:", st.session_state.zawodnicy)

    with st.expander("2. Edytuj kolumny treningowe"):
        new_col = st.text_input("Dodaj kolumnę treningową")
        if st.button("Dodaj kolumnę treningową"):
            if new_col and new_col not in st.session_state.kolumny_trening:
                st.session_state.kolumny_trening.append(new_col)
        st.write("Kolumny treningowe:", st.session_state.kolumny_trening)

    with st.expander("3. Zarządzaj testami (nazwy + kolumny)"):
        test_name = st.text_input("Nazwa testu")
        if st.button("Dodaj nowy test"):
            if test_name and test_name not in st.session_state.testy:
                st.session_state.testy[test_name] = []

        selected_test = st.selectbox("Wybierz test", list(st.session_state.testy.keys()))
        if selected_test:
            new_test_col = st.text_input("Dodaj kolumnę do testu")
            if st.button("Dodaj kolumnę testową"):
                if new_test_col and new_test_col not in st.session_state.testy[selected_test]:
                    st.session_state.testy[selected_test].append(new_test_col)
            st.write(f"Kolumny testowe ({selected_test}):", st.session_state.testy[selected_test])

    with st.expander("4. Zarządzaj grupami"):
        group_name = st.text_input("Nazwa nowej grupy")
        if st.button("Stwórz grupę"):
            if group_name and group_name not in st.session_state.grupy:
                st.session_state.grupy[group_name] = []
        selected_group = st.selectbox("Wybierz grupę", list(st.session_state.grupy.keys()))
        if selected_group:
            member = st.selectbox("Dodaj zawodnika do grupy", st.session_state.zawodnicy)
            if st.button("Dodaj do grupy"):
                if member not in st.session_state.grupy[selected_group]:
                    st.session_state.grupy[selected_group].append(member)
            if st.button("Usuń z grupy"):
                if member in st.session_state.grupy[selected_group]:
                    st.session_state.grupy[selected_group].remove(member)
            st.write(f"Członkowie grupy {selected_group}:", st.session_state.grupy[selected_group])

def trening():
    st.header("Trening")

    date = st.date_input("Wybierz dzień", value=datetime.date.today())
    typ = st.radio("Typ treningu:", ["Ląd", "Woda"])
    pora_dnia = st.selectbox("Pora treningu:", ["Rano", "Popołudniu", "Wieczorem"])
    grupa = st.selectbox("Wybierz grupę", list(st.session_state.grupy.keys()))
    if grupa:
        zawodnicy = st.session_state.grupy[grupa]
        kolumny = ["Imię i Nazwisko"] + st.session_state.kolumny_trening
        data = []
        for zawodnik in zawodnicy:
            wiersz = [zawodnik] + [""] * len(st.session_state.kolumny_trening)
            data.append(wiersz)
        df = pd.DataFrame(data, columns=kolumny)
        edited_df = st.data_editor(df, num_rows="dynamic")
        if st.button("Zapisz trening"):
            file_name = f"trening_{date}_{pora_dnia}.csv"
            edited_df.to_csv(file_name, index=False)
            st.success(f"Zapisano do pliku {file_name}")

def testy():
    st.header("Testy")

    date = st.date_input("Wybierz dzień testu", value=datetime.date.today())
    selected_test = st.selectbox("Wybierz test", list(st.session_state.testy.keys()))
    grupa = st.selectbox("Wybierz grupę", list(st.session_state.grupy.keys()))
    if grupa and selected_test:
        zawodnicy = st.session_state.grupy[grupa]
        kolumny = ["Imię i Nazwisko"] + st.session_state.testy[selected_test]
        data = []
        for zawodnik in zawodnicy:
            wiersz = [zawodnik] + [""] * len(st.session_state.testy[selected_test])
            data.append(wiersz)
        df = pd.DataFrame(data, columns=kolumny)
        edited_df = st.data_editor(df, num_rows="dynamic")
        if st.button("Zapisz testy"):
            file_name = f"testy_{selected_test}_{date}.csv"
            edited_df.to_csv(file_name, index=False)
            st.success(f"Zapisano do pliku {file_name}")

def dane():
    st.header("Dane")
    st.info("Tutaj w przyszłości pojawi się możliwość filtrowania i pobierania danych.")

if menu == "Edycja":
    edycja()
elif menu == "Trening":
    trening()
elif menu == "Testy":
    testy()
elif menu == "Dane":
    dane()
