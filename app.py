import pandas as pd
import streamlit as st
import random

# Configurazione grafica per smartphone
st.set_page_config(page_title="Il Mio Guardaroba", page_icon="👔", layout="centered")

st.title("👔 Il Mio Guardaroba Intelligente")
st.write("Scegli le condizioni di oggi e lascia che l'app crei l'abbinamento perfetto.")

# Caricamento diretto dal link di OneDrive che abbiamo configurato
@st.cache_data(ttl=10)
def carica_guardaroba():
    link_onedrive = "https://live.com"
    try:
    # Inganna OneDrive fingendosi un browser umano (Chrome)
    import urllib.request
    req = urllib.request.Request(link_onedrive, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
    df = pd.read_excel(response.read())
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Errore nel collegamento a OneDrive: {e}")
        return None

df = carica_guardaroba()

if df is not None:
    st.header("🎛️ Filtri del Giorno")
    
    col1, col2 = st.columns(2)
    with col1:
        stagione = st.selectbox("☀️ Stagione", ["PRIMAVERA AUTUNNO", "INVERNO", "ESTATE"])
    with col2:
        formalita = st.selectbox("🤵 Formalità", [1, 2, 3, 4], format_func=lambda x: {
            1: "1 - Formale", 2: "2 - Business", 3: "3 - Smart Casual", 4: "4 - Sportivo"
        }[x])

    if st.button("🚀 GENERATORE OUTFIT DI OGGI", use_container_width=True):
        
        def estrai_capo(colonna, filtra_sf=True):
            if filtra_sf:
                mask = (
                    ((df["STAGIONALITA'"] == stagione) | (df["STAGIONALITA'"].isna())) &
                    ((df["FORMALITA'"] == formalita) | (df["FORMALITA'"].isna())) &
                    (df[colonna].notna()) & (df[colonna].astype(str).str.strip() != "")
                )
            else:
                mask = (df[colonna].notna()) & (df[colonna].astype(str).str.strip() != "")
                
            opzioni = df[mask][colonna].dropna().unique().tolist()
            return random.choice(opzioni) if opzioni else "Nessuna opzione disponibile"

        scarpa = estrai_capo("CALZATURA")
        pantalone = estrai_capo("PANTALONE")
        capo1 = estrai_capo("1° CAPO")
        camicia = estrai_capo("CAMICIA")
        maglione = estrai_capo("MAGLIONE")
        capospalla = estrai_capo("CAPO SPALLA")
        orologio = estrai_capo("OROLOGIO", filtra_sf=False)
        auto = estrai_capo("AUTO", filtra_sf=False)

        st.success("✨ Ecco il tuo look consigliato!")
        st.markdown(f"### 🚗 Garage & Accessori")
        st.info(f"**Auto:** {auto}\n\n**Orologio:** {orologio}")
        st.markdown(f"### 👕 Abbigliamento")
        st.warning(
            f"👟 **Calzatura:** {scarpa}\n\n"
            f"👖 **Pantalone:** {pantalone}\n\n"
            f"👕 **Base Layer:** {capo1 if capo1 != 'Nessuna opzione disponibile' else 'Vedi camicia'}\n\n"
            f"👔 **Camicia:** {camicia if camicia != 'Nessuna opzione disponibile' else 'Nessuna'}\n\n"
            f"🧶 **Maglieria:** {maglione if maglione != 'Nessuna opzione disponibile' else 'Nessuno'}\n\n"
            f"🧥 **Capospalla:** {capospalla}"
        )
