
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="SwimData – Zbieranie danych", layout="wide")

# Inicjalizacja session_state
if "zawodnicy" not in st.session_state:
    st.session_state["zawodnicy"] = []
if "grupy" not in st.session_state:
    st.session_state["grupy"] = {}
if "kolumny_trening" not in st.session_state:
    st.session_state["kolumny_trening"] = []
if "kolumny_test" not in st.session_state:
    st.session_state["kolumny_test"] = []
if "treningi" not in st.session_state:
    st.session_state["treningi"] = []
if "testy" not in st.session_state:
    st.session_state["testy"] = []

# Menu
tabs = st.sidebar.radio("📋 Menu", ["Edycja", "Trening", "Testy", "Dane"])

# Zakładka EDYCJA
if tabs == "Edycja":
    st.header("🛠️ Edycja bazy danych")

    st.subheader("1. Dodaj zawodnika")
    with st.form(key="add_athlete"):
        name = st.text_input("Imię i Nazwisko")
        group = st.text_input("Grupa treningowa")
        submitted = st.form_submit_button("Dodaj zawodnika")
        if submitted and name:
            st.session_state["zawodnicy"].append({"Imię i Nazwisko": name, "Grupa": group})
            if group not in st.session_state["grupy"]:
                st.session_state["grupy"][group] = []
            st.session_state["grupy"][group].append(name)
            st.success(f"Dodano zawodnika {name} do grupy {group}")

    st.subheader("2. Dodaj kolumny do Treningu")
    new_col_train = st.text_input("Nowa kolumna treningowa")
    if st.button("Dodaj kolumnę treningową") and new_col_train:
        st.session_state["kolumny_trening"].append(new_col_train)

    st.subheader("3. Dodaj kolumny do Testów")
    new_col_test = st.text_input("Nowa kolumna testowa")
    if st.button("Dodaj kolumnę testową") and new_col_test:
        st.session_state["kolumny_test"].append(new_col_test)

# Zakładka TRENING
if tabs == "Trening":
    st.header("🏊 Formularz treningowy")
    date = st.date_input("Wybierz datę", value=datetime.today())
    session_time = st.time_input("Godzina treningu", value=datetime.now().time())
    session_type = st.selectbox("Trening", ["woda", "ląd"])
    group_names = list(st.session_state["grupy"].keys())
    selected_group = st.selectbox("Wybierz grupę", group_names)

    if selected_group:
        st.subheader("Formularz")
        data = []
        for name in st.session_state["grupy"][selected_group]:
            row = {"Imię i Nazwisko": name}
            col1, *dynamic_cols = st.columns(1 + len(st.session_state["kolumny_trening"]))
            row["Obecny"] = col1.checkbox("Obecny", key=f"{name}_obecny")
            for i, col_name in enumerate(st.session_state["kolumny_trening"]):
                row[col_name] = dynamic_cols[i].text_input(col_name, key=f"{name}_{col_name}")
            data.append(row)
        if st.button("Zapisz trening"):
            df = pd.DataFrame(data)
            df["Data"] = date.strftime("%Y-%m-%d")
            df["Godzina"] = session_time.strftime("%H:%M")
            df["Rodzaj"] = session_type
            st.session_state["treningi"].append(df)
            st.success("Zapisano trening.")

# Zakładka TESTY
if tabs == "Testy":
    st.header("🧪 Formularz testów")
    test_date = st.date_input("Data testu", value=datetime.today())
    test_name = st.text_input("Nazwa testu")
    group_names = list(st.session_state["grupy"].keys())
    selected_group = st.selectbox("Wybierz grupę", group_names)

    if selected_group:
        st.subheader("Wyniki testu")
        data = []
        for name in st.session_state["grupy"][selected_group]:
            row = {"Imię i Nazwisko": name}
            cols = st.columns(len(st.session_state["kolumny_test"]))
            for i, col_name in enumerate(st.session_state["kolumny_test"]):
                row[col_name] = cols[i].text_input(f"{col_name} – {name}", key=f"{name}_{col_name}")
            data.append(row)
        if st.button("Zapisz test"):
            df = pd.DataFrame(data)
            df["Data"] = test_date.strftime("%Y-%m-%d")
            df["Nazwa testu"] = test_name
            st.session_state["testy"].append(df)
            st.success("Zapisano test.")

# Zakładka DANE
if tabs == "Dane":
    st.header("📊 Eksport danych")
    if st.button("📤 Eksportuj dane treningowe do CSV"):
        if st.session_state["treningi"]:
            df_all = pd.concat(st.session_state["treningi"], ignore_index=True)
            csv = df_all.to_csv(index=False).encode("utf-8")
            st.download_button("Pobierz treningi.csv", csv, "treningi.csv", "text/csv")
        else:
            st.warning("Brak danych treningowych.")

    if st.button("📤 Eksportuj dane testowe do CSV"):
        if st.session_state["testy"]:
            df_all = pd.concat(st.session_state["testy"], ignore_index=True)
            csv = df_all.to_csv(index=False).encode("utf-8")
            st.download_button("Pobierz testy.csv", csv, "testy.csv", "text/csv")
        else:
            st.warning("Brak danych testowych.")
