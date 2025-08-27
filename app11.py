
import streamlit as st
import pandas as pd
from datetime import date

# Inicjalizacja sesji
if "athletes" not in st.session_state:
    st.session_state.athletes = []
if "training_columns" not in st.session_state:
    st.session_state.training_columns = ["Obecność"]
if "test_columns" not in st.session_state:
    st.session_state.test_columns = ["Obecność"]

st.set_page_config(page_title="SwimData", layout="wide")

st.title("SwimData 2025")

menu = st.sidebar.radio("Menu", ["Edycja", "Trening", "Testy", "Dane"])

if menu == "Edycja":
    st.header("Edycja listy zawodników i kolumn")

    with st.expander("Lista zawodników"):
        new_name = st.text_input("Dodaj zawodnika", "")
        if st.button("Dodaj zawodnika") and new_name:
            st.session_state.athletes.append(new_name)
        st.write("Zawodnicy:", st.session_state.athletes)
        remove_name = st.selectbox("Usuń zawodnika", [""] + st.session_state.athletes)
        if st.button("Usuń wybranego zawodnika") and remove_name:
            st.session_state.athletes.remove(remove_name)

    with st.expander("Kolumny dla Treningu"):
        new_col_train = st.text_input("Nowa kolumna treningowa", key="train_col")
        if st.button("Dodaj kolumnę treningową") and new_col_train:
            st.session_state.training_columns.append(new_col_train)
        st.write("Kolumny trening:", st.session_state.training_columns)

    with st.expander("Kolumny dla Testów"):
        new_col_test = st.text_input("Nowa kolumna testowa", key="test_col")
        if st.button("Dodaj kolumnę testową") and new_col_test:
            st.session_state.test_columns.append(new_col_test)
        st.write("Kolumny testy:", st.session_state.test_columns)

elif menu == "Trening":
    st.header("Trening")

    selected_date = st.date_input("Data treningu", date.today())
    pora_dnia = st.selectbox("Pora dnia", ["Rano", "Popołudniu", "Wieczorem"])

    st.subheader("Lista obecności i dane treningowe")

    if st.session_state.athletes:
        df = pd.DataFrame({ "Imię i Nazwisko": st.session_state.athletes })
        for col in st.session_state.training_columns:
            df[col] = ""

        edited = st.data_editor(df, num_rows="dynamic", key="training_editor")

        if st.button("Zapisz dane treningowe"):
            file_path = f"trening_{selected_date}_{pora_dnia}.csv"
            edited.to_csv(file_path, index=False)
            st.success(f"Dane zapisane do pliku: {file_path}")
    else:
        st.warning("Brak zawodników. Dodaj ich w zakładce Edycja.")

elif menu == "Testy":
    st.header("Testy")

    selected_date = st.date_input("Data testu", date.today())
    selected_test = st.text_input("Nazwa testu")

    st.subheader("Wyniki testów")

    if st.session_state.athletes:
        df = pd.DataFrame({ "Imię i Nazwisko": st.session_state.athletes })
        for col in st.session_state.test_columns:
            df[col] = ""

        edited = st.data_editor(df, num_rows="dynamic", key="test_editor")

        if st.button("Zapisz dane testowe"):
            file_path = f"test_{selected_date}_{selected_test}.csv"
            edited.to_csv(file_path, index=False)
            st.success(f"Dane zapisane do pliku: {file_path}")
    else:
        st.warning("Brak zawodników. Dodaj ich w zakładce Edycja.")

elif menu == "Dane":
    st.header("Dane")

    st.write("Pliki CSV z danymi treningów i testów będą zapisywane lokalnie po kliknięciu przycisku 'Zapisz'.")
