import streamlit as st
import pandas as pd

st.title("Generador de Queries OpenCypher con selección de nodos")

uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("### Vista previa del CSV cargado")
    st.dataframe(df)

    expected_columns = ["nodo1", "relacion", "nodo2"]
    if not all(col in df.columns for col in expected_columns):
        st.error("El CSV debe contener las columnas: nodo1, relacion, nodo2")
    else:
        # Obtener nodos únicos
        nodos_unicos = sorted(set(df["nodo1"]).union(set(df["nodo2"])))
        
        st.write("### Selecciona los nodos que quieres incluir:")
        nodos_seleccionados = st.multiselect(
            "Nodos disponibles:",
            options=nodos_unicos
        )

        if nodos_seleccionados:
            # Filtrar filas si nodo1 O nodo2 está incluido
            df_filtrado = df[
                df["nodo1"].isin(nodos_seleccionados) |
                df["nodo2"].isin(nodos_seleccionados)
            ]

            st.write("### Filas usadas para generar las queries:")
            st.dataframe(df_filtrado)

            queries = [
                f"MATCH (n:{row['nodo1']})-[r:{row['relacion']} ]-(m:{row['nodo2']})\nRETURN *"
                for _, row in df_filtrado.iterrows()
            ]

            all_queries_text = "\n\n".join(queries)

            st.write("### Queries generadas:")
            st.text_area(
                label="Copia las queries:",
                value=all_queries_text,
                height=300
            )
        else:
            st.info("Selecciona al menos un nodo para generar las queries.")
