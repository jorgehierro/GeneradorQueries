import streamlit as st
import pandas as pd

# ------------------ Estilo general ------------------
st.set_page_config(page_title="Generador Cypher", layout="centered")

st.title("🧩 Generador de Queries Cypher con Atributos")
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

# Cargar atributos si existe
atributos_df = None
atributos_ok = False

if atributos_file is not None:
    atributos_df = pd.read_csv(atributos_file)

    # validar columnas
    if "nodo" in atributos_df.columns and "atributo" in atributos_df.columns:
        atributos_ok = True
        st.success("CSV de atributos cargado correctamente.")
    else:
        st.error("⚠️ El CSV de atributos debe contener las columnas 'nodo' y 'atributo'")

# Procesar CSV principal
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.markdown("### 👀 Vista previa del CSV de relaciones")
    st.dataframe(df, use_container_width=True)

    expected_columns = ["nodo1", "relacion", "nodo2"]
    if not all(col in df.columns for col in expected_columns):
        st.error("⚠️ El CSV debe contener las columnas: nodo1, relacion, nodo2")

    else:

        st.markdown("---")

        # ------------------ Nodo 1 ------------------
        with st.container():
            st.subheader("🟦 3. Selecciona el Nodo 1")
            nodos1_unicos = sorted(df["nodo1"].unique())
            nodo1_sel = st.selectbox(
                "Nodo de origen:",
                options=["(elige uno)"] + nodos1_unicos,
                index=0,
                key="nodo1_select"
            )

        # Continuar si se selecciona Nodo1
        if nodo1_sel != "(elige uno)":

            df_filtrado_nodo1 = df[df["nodo1"] == nodo1_sel]

            st.markdown("---")

            # ------------------ Relación ------------------
            with st.container():
                st.subheader("🟧 4. Selecciona la relación")

                relaciones = sorted(df_filtrado_nodo1["relacion"].unique())
                relacion_sel = st.selectbox(
                    "Relaciones disponibles:",
                    options=["(elige una)"] + relaciones,
                    index=0,
                    key="relacion_select"
                )

            if relacion_sel != "(elige una)":

                df_filtrado_rel = df_filtrado_nodo1[df_filtrado_nodo1["relacion"] == relacion_sel]

                st.markdown("---")

                # ------------------ Nodo 2 ------------------
                with st.container():
                    st.subheader("🟩 5. Selecciona el Nodo 2")

                    nodos2 = sorted(df_filtrado_rel["nodo2"].unique())
                    nodo2_sel = st.selectbox(
                        "Nodo destino:",
                        options=["(elige uno)"] + nodos2,
                        index=0,
                        key="nodo2_select"
                    )

                if nodo2_sel != "(elige uno)":

                    st.markdown("---")

                    # ------------------ Filtros de atributos ------------------
                    with st.container():
                        st.subheader("🟪 6. Añadir filtros opcionales")

                        filtros_nodo1 = []
                        filtros_nodo2 = []

                        if atributos_ok:

                            # Atributos de nodo1
                            atributos_n1 = atributos_df[atributos_df["nodo"] == nodo1_sel]["atributo"].unique().tolist()
                            if atributos_n1:
                                filtros_nodo1 = st.multiselect(
                                    f"Atributos disponibles para {nodo1_sel}:",
                                    atributos_n1,
                                    key=f"attr_{nodo1_sel}_n1"
                                )

                            # Atributos de nodo2
                            atributos_n2 = atributos_df[atributos_df["nodo"] == nodo2_sel]["atributo"].unique().tolist()
                            if atributos_n2:
                                filtros_nodo2 = st.multiselect(
                                    f"Atributos disponibles para {nodo2_sel}:",
                                    atributos_n2,
                                    key=f"attr_{nodo2_sel}_n2"
                                )
                        else:
                            st.info("Sube un CSV de atributos para habilitar filtros automáticos.")

                    # ------------------ Construcción filtros ------------------
                    def construir_filtros(lista):
                        if not lista:
                            return ""
                        pares = [f"{attr}: VALOR" for attr in lista]
                        return "{ " + ", ".join(pares) + " }"

                    filtro_n1 = construir_filtros(filtros_nodo1)
                    filtro_n2 = construir_filtros(filtros_nodo2)

                    # ------------------ Generación de Query ------------------
                    st.markdown("---")
                    with st.container():
                        st.subheader("🧾 7. Query generada (editable)")

                        query_base = (
                            f"MATCH (n:{nodo1_sel} {filtro_n1 if filtro_n1 else ''})"
                            f"-[r:{relacion_sel}]-"
                            f"(m:{nodo2_sel} {filtro_n2 if filtro_n2 else ''})\n"
                            f"RETURN *"
                        )

                        query_editable = st.text_area(
                            "Puedes editar la query manualmente:",
                            value=query_base,
                            height=180,
                            key="query_edit"
                        )

                        st.code(query_editable, language="cypher")
                        st.success("✅ Query lista para copiar y usar.")
