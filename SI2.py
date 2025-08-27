
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="SwimData2025", layout="wide")

# Sesja - dane tymczasowe
if "zawodnicy" not in st.session_state:
    st.session_state.zawodnicy = []
if "kolumny" not in st.session_state:
    st.session_state.kolumny = ["Imię i Nazwisko"]
if "grupy" not in st.session_state:
    st.session_state.grupy = {}
if "dane_trening" not in st.session_state:
    st.session_state.dane_trening = []
if "dane_testy" not in st.session_state:
    st.session_state.dane_testy = []

# Zakładki
tab1, tab2, tab3, tab4 = st.tabs(["Edycja", "Trening", "Testy", "Dane"])

with tab1:
    st.header("Edycja listy zawodników i grup")

    # Dodaj zawodnika
    with st.form("dodaj_zawodnika"):
        imie_nazwisko = st.text_input("Imię i Nazwisko")
        grupa = st.text_input("Grupa (np. A, B, Juniorzy)")
        submitted = st.form_submit_button("Dodaj zawodnika")
        if submitted and imie_nazwisko:
            st.session_state.zawodnicy.append(imie_nazwisko)
            if grupa:
                st.session_state.grupy.setdefault(grupa, []).append(imie_nazwisko)
            st.success(f"Dodano: {imie_nazwisko}")

    # Dodaj kolumnę
    with st.form("dodaj_kolumne"):
        nowa_kolumna = st.text_input("Nazwa nowej kolumny")
        sub_col = st.form_submit_button("Dodaj kolumnę")
        if sub_col and nowa_kolumna:
            if nowa_kolumna not in st.session_state.kolumny:
                st.session_state.kolumny.append(nowa_kolumna)
                st.success(f"Dodano kolumnę: {nowa_kolumna}")

    # Lista zawodników
    st.subheader("Lista zawodników")
    df = pd.DataFrame(st.session_state.zawodnicy, columns=["Imię i Nazwisko"])
    st.dataframe(df, use_container_width=True)

    # Lista grup
    st.subheader("Grupy treningowe")
    for grupa, lista in st.session_state.grupy.items():
        st.markdown(f"**{grupa}**")
        st.write(lista)

with tab2:
    st.header("Trening")
    data_treningu = st.date_input("Wybierz datę", datetime.date.today())
    pora = st.selectbox("Trening", ["woda", "ląd"])
    godzina = st.time_input("Godzina treningu")
    grupa_wybrana = st.selectbox("Wybierz grupę", list(st.session_state.grupy.keys()) if st.session_state.grupy else [])

    if grupa_wybrana:
        zawodnicy = st.session_state.grupy[grupa_wybrana]
        st.subheader("Formularz treningowy")
        wpisy = []
        for zawodnik in zawodnicy:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                obecny = st.checkbox("Obecny", key=f"ob_{zawodnik}")
            with col2:
                typ = st.selectbox("Typ (A/B)", ["A", "B"], key=f"typ_{zawodnik}")
            with col3:
                grip = st.text_input("Grip test", key=f"grip_{zawodnik}")
            with col4:
                uwagi = st.text_input("Uwagi", key=f"uwagi_{zawodnik}")
            wpisy.append({
                "Imię i Nazwisko": zawodnik,
                "Data": str(data_treningu),
                "Godzina": str(godzina),
                "Rodzaj": pora,
                "Obecny": obecny,
                "Typ": typ,
                "Grip test": grip,
                "Uwagi": uwagi
            })
        if st.button("Zapisz trening"):
            st.session_state.dane_trening.extend(wpisy)
            df_zapis = pd.DataFrame(wpisy)
            filename = f"/mnt/data/trening_{data_treningu}.csv"
            df_zapis.to_csv(filename, index=False)
            st.success(f"Zapisano dane treningowe do pliku: {filename}")

with tab3:
    st.header("Testy")
    data_testu = st.date_input("Data testu", datetime.date.today(), key="data_testu")
    test_nazwa = st.text_input("Nazwa testu", key="nazwa_testu")
    grupa_testowa = st.selectbox("Wybierz grupę", list(st.session_state.grupy.keys()) if st.session_state.grupy else [], key="grupa_testowa")

    if grupa_testowa:
        zawodnicy = st.session_state.grupy[grupa_testowa]
        st.subheader("Wyniki testu")
        wpisy_test = []
        for zawodnik in zawodnicy:
            col1, col2 = st.columns(2)
            with col1:
                wynik = st.text_input("Wynik", key=f"wynik_{zawodnik}")
            with col2:
                uwaga = st.text_input("Uwagi", key=f"uwaga_test_{zawodnik}")
            wpisy_test.append({
                "Imię i Nazwisko": zawodnik,
                "Data": str(data_testu),
                "Test": test_nazwa,
                "Wynik": wynik,
                "Uwagi": uwaga
            })
        if st.button("Zapisz test"):
            st.session_state.dane_testy.extend(wpisy_test)
            df_test = pd.DataFrame(wpisy_test)
            filename = f"/mnt/data/test_{test_nazwa}_{data_testu}.csv"
            df_test.to_csv(filename, index=False)
            st.success(f"Zapisano dane testowe do pliku: {filename}")

with tab4:
    st.header("Pobierz dane")

    if st.session_state.dane_trening:
        st.subheader("Dane z treningów")
        df_tr = pd.DataFrame(st.session_state.dane_trening)
        st.dataframe(df_tr)
        st.download_button("Pobierz dane treningowe CSV", df_tr.to_csv(index=False), file_name="trening_dane.csv")

    if st.session_state.dane_testy:
        st.subheader("Dane z testów")
        df_ts = pd.DataFrame(st.session_state.dane_testy)
        st.dataframe(df_ts)
        st.download_button("Pobierz dane testowe CSV", df_ts.to_csv(index=False), file_name="testy_dane.csv")
