
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="SwimData – Zbieranie danych", layout="wide")

# ---------------------------
# Nawigacja – zakładki
# ---------------------------
tabs = st.sidebar.radio("📋 Menu", ["Edycja", "Trening", "Testy", "Dane"])

# ---------------------------
# EDYCJA
# ---------------------------
if tabs == "Edycja":
    st.header("🛠️ Edycja baz danych")

    st.subheader("1. Lista obecności – konfiguracja")
    st.write("Tu w przyszłości będzie możliwość dodawania kolumn i edycji nazw.")
    st.info("📌 Dane będą ładowane/zapisywane z/do pliku CSV (np. zawodnicy.csv)")

    st.subheader("2. Grupy zawodników")
    st.write("Tworzenie i edycja grup na podstawie listy zawodników.")

    st.subheader("3. Testy")
    st.write("Definiowanie testów: nazwa testu, liczba i nazwy kolumn.")
    st.caption("➡️ Wszystko będzie zapisywane do pliku `testy.csv`")

# ---------------------------
# TRENING
# ---------------------------
elif tabs == "Trening":
    st.header("🏊 Rejestr treningu")

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_date = st.date_input("Data treningu", value=datetime.today())
    with col2:
        training_type = st.selectbox("Rodzaj treningu", ["Woda", "Ląd"])
    with col3:
        training_time = st.time_input("Godzina treningu")

    st.subheader("Grupa i obecność")
    st.write("Po wybraniu grupy zostanie załadowana lista zawodników.")

# ---------------------------
# TESTY
# ---------------------------
elif tabs == "Testy":
    st.header("🧪 Rejestr testów")

    col1, col2 = st.columns(2)
    with col1:
        selected_date = st.date_input("Data testu", value=datetime.today(), key="test_date")
    with col2:
        test_name = st.selectbox("Wybierz test", ["Grip", "CMJ", "Skok startowy", "Inny test"])

    st.subheader("Grupa i formularz testu")
    st.write("Po wybraniu grupy załadują się kolumny zdefiniowane wcześniej.")

# ---------------------------
# DANE
# ---------------------------
elif tabs == "Dane":
    st.header("📂 Pobieranie danych")
    st.write("Tutaj będzie możliwość filtrowania i pobierania danych z treningów i testów.")
    st.info("✅ Dane będą zapisywane w formacie CSV, z kolumnami zgodnymi z definicją (Imię i Nazwisko jako pierwsza).")
