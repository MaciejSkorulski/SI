
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="SwimData – Zbieranie danych", layout="wide")

# Inicjalizacja sesji
if "zawodnicy" not in st.session_state:
    st.session_state["zawodnicy"] = {"1": []}
if "grupa_id" not in st.session_state:
    st.session_state["grupa_id"] = 1
if "dane_treningowe" not in st.session_state:
    st.session_state["dane_treningowe"] = []

# Menu boczne
zakladka = st.sidebar.radio("Wybierz zakładkę:", ["Edycja", "Trening", "Dane"])

# ---------------------------------
# EDYCJA
# ---------------------------------
if zakladka == "Edycja":
    st.header("🛠️ Edycja grupy treningowej")
    grupa_id = str(st.session_state["grupa_id"])
    st.write(f"Aktualna grupa: {grupa_id}")

    with st.form("dodaj_zawodnika"):
        imie_nazwisko = st.text_input("Imię i Nazwisko zawodnika")
        dodaj = st.form_submit_button("Dodaj zawodnika")
        if dodaj and imie_nazwisko.strip():
            st.session_state["zawodnicy"][grupa_id].append(imie_nazwisko.strip())

    st.write("### Lista zawodników:")
    do_usuniecia = st.multiselect("Zaznacz zawodników do usunięcia", st.session_state["zawodnicy"][grupa_id])
    if st.button("Usuń zaznaczonych"):
        st.session_state["zawodnicy"][grupa_id] = [
            z for z in st.session_state["zawodnicy"][grupa_id] if z not in do_usuniecia
        ]

# ---------------------------------
# TRENING
# ---------------------------------
elif zakladka == "Trening":
    st.header("🏊 Formularz treningowy")
    data = st.date_input("Wybierz dzień", datetime.now().date())
    pora = st.selectbox("Pora treningu", ["Rano", "Popołudniu", "Wieczorem"])
    typ = st.radio("Typ treningu:", ["Ląd", "Woda"])
    grupa_id = st.selectbox("Wybierz grupę", list(st.session_state["zawodnicy"].keys()))

    st.subheader("Formularz obecności")
    obecnosci = []
    for zawodnik in st.session_state["zawodnicy"][grupa_id]:
        obecny = st.checkbox(f"{zawodnik}", key=f"{zawodnik}_{data}_{pora}")
        obecnosci.append({"Imię i Nazwisko": zawodnik, "Obecny": obecny})

    if st.button("Zapisz trening"):
        for entry in obecnosci:
            st.session_state["dane_treningowe"].append({
                "Data": data.strftime("%Y-%m-%d"),
                "Pora": pora,
                "Typ": typ,
                "Grupa": grupa_id,
                "Imię i Nazwisko": entry["Imię i Nazwisko"],
                "Obecny": entry["Obecny"]
            })
        st.success("✅ Zapisano dane treningowe.")

# ---------------------------------
# DANE
# ---------------------------------
elif zakladka == "Dane":
    st.header("📁 Zapisane dane treningowe")
    df = pd.DataFrame(st.session_state["dane_treningowe"])
    if not df.empty:
        st.dataframe(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Pobierz CSV", data=csv, file_name="trening.csv", mime="text/csv")
    else:
        st.info("Brak danych do wyświetlenia.")
