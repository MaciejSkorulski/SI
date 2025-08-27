
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="SwimData – Zbieranie danych", layout="wide")

# ----------------------
# Nawigacja – zakładki
# ----------------------
tabs = st.sidebar.radio("📋 Menu", ["Edycja", "Trening", "Testy", "Dane"])

# Inicjalizacja sesji
if "zawodnicy" not in st.session_state:
    st.session_state["zawodnicy"] = {"1": ["Zawodnik 1", "Zawodnik 2", "Zawodnik 3", "Zawodnik 4"]}
if "trening_data" not in st.session_state:
    st.session_state["trening_data"] = []

# ----------------------
# Zakładka: TRENING
# ----------------------
if tabs == "Trening":
    st.header("🏊‍♂️ Formularz treningowy")
    data_treningu = st.date_input("Wybierz dzień", value=date.today())
    typ_treningu = st.radio("Typ treningu:", ["Ląd", "Woda"])
    pora_dnia = st.selectbox("Pora dnia treningu:", ["Rano", "Popołudniu", "Wieczorem"])
    grupy = list(st.session_state["zawodnicy"].keys())
    grupa = st.selectbox("Wybierz grupę", grupy)

    st.subheader("Formularz")
    wyniki = []
    for zawodnik in st.session_state["zawodnicy"][grupa]:
        obecny = st.checkbox(f"{zawodnik}", key=f"tr_{zawodnik}")
        wyniki.append({"Imię i Nazwisko": zawodnik, f"obecnosc.{data_treningu}": "1" if obecny else "0"})

    if st.button("Zapisz trening"):
        df = pd.DataFrame(wyniki)
        st.session_state["trening_data"].append(df)
        st.success("✅ Trening zapisany!")
