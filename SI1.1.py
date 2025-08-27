
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ------------------------------------------
# KONFIGURACJA STRONY
# ------------------------------------------
st.set_page_config(page_title="Aplikacja do zbierania danych", layout="wide")
st.title("📊 Aplikacja do zbierania danych – Performance")

# Ścieżki do plików
FOLDER_OBECNOSC = "dane/obecnosc"
FOLDER_TESTY = "dane/testy"
os.makedirs(FOLDER_OBECNOSC, exist_ok=True)
os.makedirs(FOLDER_TESTY, exist_ok=True)

# ------------------------------------------
# ZAKŁADKA: Edycja
# ------------------------------------------
with st.sidebar:
    zakladka = st.radio("Wybierz zakładkę:", ["Edycja", "Trening", "Testy", "Dane"])

if zakladka == "Edycja":
    st.header("🛠️ Edycja danych")
    sub_tab = st.radio("Co chcesz edytować?", ["Lista obecności", "Testy"])

    if sub_tab == "Lista obecności":
        st.subheader("📋 Edycja listy zawodników")
        uploaded = st.file_uploader("Wgraj plik CSV z listą obecności", type="csv")
        if uploaded:
            df = pd.read_csv(uploaded)
            edited = st.data_editor(df, num_rows="dynamic")
            if st.button("💾 Zapisz listę"):
                file_path = f"{FOLDER_OBECNOSC}/lista_obecnosci.csv"
                edited.to_csv(file_path, index=False)
                st.success(f"Zapisano do {file_path}")

    elif sub_tab == "Testy":
        st.subheader("📄 Definicja testów")
        nazwa_testu = st.text_input("Nazwa testu")
        liczba_kolumn = st.number_input("Liczba kolumn z wynikami", min_value=1, step=1)
        if liczba_kolumn:
            kolumny = [st.text_input(f"Nazwa kolumny {i+1}") for i in range(int(liczba_kolumn))]
        if st.button("✅ Zapisz test"):
            if nazwa_testu and all(kolumny):
                test_file = pd.DataFrame(columns=["Imię i Nazwisko"] + kolumny)
                test_file.to_csv(f"{FOLDER_TESTY}/{nazwa_testu}.csv", index=False)
                st.success("Test zapisany.")

# ------------------------------------------
# ZAKŁADKA: Trening
# ------------------------------------------
elif zakladka == "Trening":
    st.header("🏊 Rejestracja treningu")
    data = st.date_input("Data treningu", value=datetime.now())
    godzina = st.time_input("Godzina treningu")
    rodzaj = st.selectbox("Rodzaj treningu", ["Woda", "Ląd"])
    uploaded = st.file_uploader("Wgraj listę zawodników (CSV)", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        for col in df.columns:
            if "obecnosc" in col:
                df.drop(columns=col, inplace=True)
        nazwa_kolumny = f"obecnosc.{data}"
        df[nazwa_kolumny] = st.multiselect("Zaznacz obecnych zawodników", df["Imię i Nazwisko"])
        if st.button("📥 Zapisz obecność"):
            save_path = f"{FOLDER_OBECNOSC}/obecnosc_{data}_{godzina.strftime('%H%M')}.csv"
            df.to_csv(save_path, index=False)
            st.success(f"Dane zapisane do {save_path}")

# ------------------------------------------
# ZAKŁADKA: Testy
# ------------------------------------------
elif zakladka == "Testy":
    st.header("📈 Rejestracja wyników testów")
    data = st.date_input("Data testu", value=datetime.now())
    testy = os.listdir(FOLDER_TESTY)
    wybor_testu = st.selectbox("Wybierz test", testy)
    grupa = st.file_uploader("Wgraj grupę zawodników", type="csv")
    if grupa and wybor_testu:
        df_grupa = pd.read_csv(grupa)
        df_test = pd.read_csv(f"{FOLDER_TESTY}/{wybor_testu}")
        for kol in df_test.columns[1:]:
            df_grupa[kol] = st.text_input(f"Wyniki dla {kol}", placeholder="Wpisz ręcznie lub użyj importu")
        if st.button("💾 Zapisz wyniki testu"):
            df_grupa.to_csv(f"{FOLDER_TESTY}/wyniki_{wybor_testu}_{data}.csv", index=False)
            st.success("Wyniki zapisane.")

# ------------------------------------------
# ZAKŁADKA: Dane
# ------------------------------------------
elif zakladka == "Dane":
    st.header("📂 Przegląd i pobieranie danych")
    typ = st.radio("Rodzaj danych", ["Obecność", "Testy"])
    folder = FOLDER_OBECNOSC if typ == "Obecność" else FOLDER_TESTY
    pliki = os.listdir(folder)
    plik = st.selectbox("Wybierz plik", pliki)
    if st.button("⬇️ Pobierz plik"):
        with open(os.path.join(folder, plik), "rb") as f:
            st.download_button(label="Pobierz", data=f, file_name=plik)
