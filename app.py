import streamlit as st
import pandas as pd

# ------------------ Estilo general ------------------
st.set_page_config(page_title="Generador Cypher", layout="centered")

st.title("🧩 Generador Cypher con Filtros Opcionales")
st.markdown("Sube tus archivos y construye la query paso a paso.")

st.markdown("---")

# ------------------ CSV PRINCIPAL ------------------
with st.container():
    st.subheader("📄 1. Subir archivo CSV de relaciones")
    uploaded_file = st.file_uploader("CSV de relaciones", type=["csv"])

# ------------------ CSV DE ATRIBUTOS ------------------
with st.container():
    st.subheader("📄 2. Subir archivo CSV de atributos (opcional)")
    atributos_file = st.file_uploader("CSV de atributos", type=["csv"])

atributos_df = None
atributos_ok = False

if atributos_file is not None:
    atributos_df = pd.read_csv(atributos_file)
    if "nodo" in atributos_df.columns and "atributo" in atributos_df.columns:
        atributos_ok = True
        st.success("CSV de atributos cargado correctamente.")
    else:
        st.error("⚠️ El CSV de atributos debe contener las columnas 'nodo' y 'atributo'")

# ------------------ PROCESAR CSV PRINCIPAL ------------------
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    st.markdown("### 👀 Vista previa del CSV")
    st.dataframe(df, use_container_width=True)

    if not all(col in df.columns for col in ["nodo1", "relacion", "nodo2"]):
        st.error("⚠️ El CSV debe contener las columnas: nodo1, relacion, nodo2")
        st.stop()

    st.markdown("---")

    # ------------------ Nodo 1 ------------------
    st.subheader("🟦 3. Selecciona el Nodo 1")
    nodos1 = sorted(df["nodo1"].unique())
    nodo1_sel = st.selectbox(
        "Nodo origen:",
        options=["(elige uno)"] + nodos1
    )
    if nodo1_sel == "(elige uno)":
        st.stop()
    df_n1 = df[df["nodo1"] == nodo1_sel]

    st.markdown("---")

    # ------------------ Relación ------------------
    st.subheader("🟧 4. Selecciona la relación")
    relaciones = sorted(df_n1["relacion"].unique())
    relacion_sel = st.selectbox(
        "Relación:",
        options=["(elige una)"] + relaciones
    )
    if relacion_sel == "(elige una)":
        st.stop()
    df_rel = df_n1[df_n1["relacion"] == relacion_sel]

    st.markdown("---")

    # ------------------ Nodo 2 ------------------
    st.subheader("🟩 5. Selecciona el Nodo 2")
    nodos2 = sorted(df_rel["nodo2"].unique())
    nodo2_sel = st.selectbox(
        "Nodo destino:",
        options=["(elige uno)"] + nodos2
    )
    if nodo2_sel == "(elige uno)":
        st.stop()

    st.markdown("---")

    # ------------------ Preguntar si quiere filtros ------------------
    usar_filtros = False
    if atributos_ok:
        usar_filtros = (
            st.radio(
                "¿Quieres añadir filtros por atributos?",
                ["No", "Sí"],
                index=0,
                key="usar_filtros_radio"
            ) == "Sí"
        )

    # ------------------ Preparar listas de atributos disponibles ------------------
    filtros_n1, filtros_n2 = [], []
    valores_filtros_n1, valores_filtros_n2 = {}, {}

    atributos_n1, atributos_n2 = [], []
    if atributos_ok and usar_filtros:
        atributos_n1 = atributos_df[atributos_df["nodo"] == nodo1_sel]["atributo"].unique().tolist()
        atributos_n2 = atributos_df[atributos_df["nodo"] == nodo2_sel]["atributo"].unique().tolist()

        st.subheader("🟪 6. Selecciona atributos y sus valores")

        # Nodo 1
        if atributos_n1:
            filtros_n1 = st.multiselect(
                f"Atributos para {nodo1_sel}:",
                atributos_n1,
                key=f"filtros_n1_{nodo1_sel}"
            )
            for att in filtros_n1:
                valores_filtros_n1[att] = st.text_input(
                    f"Valor para {nodo1_sel}.{att}",
                    key=f"{nodo1_sel}_{att}_n1"
                )

        # Nodo 2
        if atributos_n2:
            filtros_n2 = st.multiselect(
                f"Atributos para {nodo2_sel}:",
                atributos_n2,
                key=f"filtros_n2_{nodo2_sel}"
            )
            for att in filtros_n2:
                valores_filtros_n2[att] = st.text_input(
                    f"Valor para {nodo2_sel}.{att}",
                    key=f"{nodo2_sel}_{att}_n2"
                )

    # ------------------ Botón para generar la query ------------------
    if st.button("Generar Query"):

        condiciones = []

        for att, val in valores_filtros_n1.items():
            if val.strip():
                condiciones.append(f"n.{att} = '{val}'")

        for att, val in valores_filtros_n2.items():
            if val.strip():
                condiciones.append(f"m.{att} = '{val}'")

        where_clause = ""
        if condiciones:
            where_clause = "WHERE " + " AND ".join(condiciones)

        query = f"MATCH (n:{nodo1_sel})-[r:{relacion_sel}]-(m:{nodo2_sel})\n"
        if where_clause:
            query += where_clause + "\n"
        query += "RETURN *"

        st.subheader("🧾 7. Query generada")
        query_editable = st.text_area(
            "Puedes editar la query:",
            value=query,
            height=200,
            key="final_query_editor"
        )
        st.code(query_editable, language="cypher")
        st.success("✅ Query lista para copiar y usar.")
