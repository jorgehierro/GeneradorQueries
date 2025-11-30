import streamlit as st
import pandas as pd

st.title("Generador de Queries Cypher")

uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("### Vista previa del CSV cargado:")
    st.dataframe(df)

    expected_columns = ["nodo1", "relacion", "nodo2"]
    if not all(col in df.columns for col in expected_columns):
        st.error("El CSV debe contener las columnas: nodo1, relacion, nodo2")
    else:
        # -----------------------------------------------------
        # 1️⃣ Selección de Nodo 1
        # -----------------------------------------------------
        st.subheader("1️⃣ Selecciona el Nodo 1")

        nodos1_unicos = sorted(df["nodo1"].unique())
        nodo1_sel = st.selectbox(
            "Elige un nodo de origen:",
            options=["(elige uno)"] + nodos1_unicos,
            index=0
        )

        if nodo1_sel != "(elige uno)":
            df_filtrado_nodo1 = df[df["nodo1"] == nodo1_sel]

            # -----------------------------------------------------
            # 2️⃣ Selección de relación
            # -----------------------------------------------------
            st.subheader("2️⃣ Selecciona la relación")

            relaciones = sorted(df_filtrado_nodo1["relacion"].unique())
            relacion_sel = st.selectbox(
                "Relaciones posibles:",
                options=["(elige una)"] + relaciones,
                index=0
            )

            if relacion_sel != "(elige una)":
                df_filtrado_rel = df_filtrado_nodo1[df_filtrado_nodo1["relacion"] == relacion_sel]

                # -----------------------------------------------------
                # 3️⃣ Selección de Nodo 2
                # -----------------------------------------------------
                st.subheader("3️⃣ Selecciona el Nodo 2")

                nodos2 = sorted(df_filtrado_rel["nodo2"].unique())
                nodo2_sel = st.selectbox(
                    "Nodos destino posibles:",
                    options=["(elige uno)"] + nodos2,
                    index=0
                )

                # -----------------------------------------------------
                # 4️⃣ Generación de la Query
                # -----------------------------------------------------
                if nodo2_sel != "(elige uno)":
                    st.subheader("4️⃣ Query generada")

                    query = f"""
MATCH (n:{nodo1_sel})-[r:{relacion_sel}]-(m:{nodo2_sel})
RETURN *
                    """.strip()

                    st.code(query, language="cypher")
