import streamlit as st
import pandas as pd

st.title("Generador de Queries OpenCypher desde CSV")

uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("### Vista previa del CSV cargado")
    st.dataframe(df)

    expected_columns = ["nodo1", "relacion", "nodo2"]
    if not all(col in df.columns for col in expected_columns):
        st.error("El CSV debe contener las columnas: nodo1, relacion, nodo2")
    else:
        st.write("### Queries generadas:")

        queries = []
        for _, row in df.iterrows():
            nodo1 = row["nodo1"]
            relacion = row["relacion"]
            nodo2 = row["nodo2"]

            query = f"MATCH (n:{nodo1})-[r:{relacion}]-(m:{nodo2})\nRETURN *"
            queries.append(query)

        all_queries_text = "\n\n".join(queries)

        # Mostrar cuadro de texto para copiar
        st.text_area(
            label="Copia tus queries aquí:",
            value=all_queries_text,
            height=400
        )
