import streamlit as st
import pandas as pd

# ------------------ Estilo general ------------------
st.set_page_config(page_title="Generador Cypher", layout="centered")

st.title("🧩 Generador de Queries Cypher")
st.markdown("Sube tu archivo y selecciona paso a paso los elementos para construir la query.")

st.markdown("---")

# ------------------ Carga del archivo ------------------
with st.container():
    st.subheader("📄 1. Subir archivo CSV")
    uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.markdown("### 👀 Vista previa del CSV")
    st.dataframe(df, use_container_width=True)

    expected_columns = ["nodo1", "relacion", "nodo2"]
    if not all(col in df.columns for col in expected_columns):
        st.error("⚠️ El CSV debe contener las columnas: nodo1, relacion, nodo2")
    else:

        st.markdown("---")

        # ------------------ Nodo 1 ------------------
        with st.container():
            st.subheader("🟦 2. Selecciona el Nodo 1")

            nodos1_unicos = sorted(df["nodo1"].unique())
            nodo1_sel = st.selectbox(
                "Nodo de origen:",
                options=["(elige uno)"] + nodos1_unicos,
                index=0
            )

        if nodo1_sel != "(elige uno)":

            df_filtrado_nodo1 = df[df["nodo1"] == nodo1_sel]

            st.markdown("---")

            # ------------------ Relación ------------------
            with st.container():
                st.subheader("🟧 3. Selecciona la relación")

                relaciones = sorted(df_filtrado_nodo1["relacion"].unique())
                relacion_sel = st.selectbox(
                    "Relaciones disponibles:",
                    options=["(elige una)"] + relaciones,
                    index=0
                )

            if relacion_sel != "(elige una)":

                df_filtrado_rel = df_filtrado_nodo1[df_filtrado_nodo1["relacion"] == relacion_sel]

                st.markdown("---")

                # ------------------ Nodo 2 ------------------
                with st.container():
                    st.subheader("🟩 4. Selecciona el Nodo 2")

                    nodos2 = sorted(df_filtrado_rel["nodo2"].unique())
                    nodo2_sel = st.selectbox(
                        "Nodo destino:",
                        options=["(elige uno)"] + nodos2,
                        index=0
                    )

                if nodo2_sel != "(elige uno)":

                    st.markdown("---")

                    # ------------------ Query final ------------------
                    with st.container():
                        st.subheader("🧾 5. Query generada")

                        query = f"""
MATCH (n:{nodo1_sel})-[r:{relacion_sel}]-(m:{nodo2_sel})
RETURN *
                        """.strip()

                        st.code(query, language="cypher")
                        st.success("✅ Query generada correctamente. Puedes copiarla desde el cuadro superior.")
