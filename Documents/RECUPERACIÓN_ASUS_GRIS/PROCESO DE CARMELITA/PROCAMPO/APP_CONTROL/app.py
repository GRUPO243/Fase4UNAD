import streamlit as st
import pandas as pd
import datetime
import httpx
from supabase import create_client, Client


# 1. Conexión Segura a la Base de Datos en la Nube (Supabase)
# Lee de forma automática las credenciales guardadas en .streamlit/secrets.toml
url_supabase = st.secrets["SUPABASE_URL"]
key_supabase = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url_supabase, key_supabase)

client_options = {"http_client": httpx.Client(http2=False)}
supabase: Client = create_client(url_supabase, key_supabase, options=client_options)

# Configuración de la página apta para pantallas de celular y PC
st.set_page_config(page_title="Avícola Procampo Pro", page_icon="🐔", layout="centered")

st.title("🐔 Avícola Procampo - Control Centralizado")

# Menú lateral interactivo
menu = st.sidebar.selectbox("Seleccione un Módulo", ["Registrar Producción", "Registrar Gastos", "Dashboard Financiero"])

# --- MÓDULO 1: REGISTRAR PRODUCCIÓN ---
if menu == "Registrar Producción":
    st.header("📝 Entrada de Datos de Producción")
    
    with st.form("form_cloud_prod", clear_on_submit=True):
        fecha = st.date_input("Fecha", datetime.date.today())
        aves = st.number_input("Aves Totales Activas", min_value=1, value=768)
        mortalidad = st.number_input("Aves Muertas Hoy", min_value=0, value=0)
        
        st.subheader("Clasificación de Huevos (Unidades)")
        col1, col2 = st.columns(2)
        with col1:
            h_aaa = st.number_input("Cantidad AAA", min_value=0, value=0)
            h_aa = st.number_input("Cantidad AA", min_value=0, value=0)
        with col2:
            precio = st.number_input("Precio base de venta por unidad ($ COP)", min_value=0, value=450)
        
        boton_enviar = st.form_submit_button("Sincronizar con la Nube")
        
        if boton_enviar:
            # Diccionario con los datos que espera la tabla de Supabase
            datos_insertar = {
                "fecha": str(fecha),
                "aves_totales": aves,
                "mortalidad": mortalidad,
                "huevo_aaa": h_aaa,
                "huevo_aa": h_aa,
                "precio_referencia": precio
            }
            # Inserta la fila en la tabla de internet inmediatamente
            respuesta = supabase.table("produccion_diaria").insert(datos_insertar).execute()
            st.success("🚀 Datos guardados exitosamente en la base de datos global.")

# --- MÓDULO 2: REGISTRAR GASTOS ---
elif menu == "Registrar Gastos":
    st.header("💸 Registro de Gastos / Costos")
    
    with st.form("form_cloud_gastos", clear_on_submit=True):
        fecha_gasto = st.date_input("Fecha del Gasto", datetime.date.today())
        categoria = st.selectbox("Categoría", ["Alimento (Purina)", "Vacunas/Medicina", "Servicios Públicos", "Empaques", "Mantenimiento", "Otros"])
        monto = st.number_input("Monto total ($ COP)", min_value=0, step=1000)
        descripcion = st.text_input("Descripción / Detalle")
        
        boton_gasto = st.form_submit_button("Sincronizar Gasto")
        
        if boton_gasto:
            datos_gasto = {
                "fecha": str(fecha_gasto),
                "categoria": categoria,
                "monto": monto,
                "descripcion": descripcion
            }
            # Inserta el gasto en la segunda tabla de internet
            respuesta = supabase.table("gastos_operativos").insert(datos_gasto).execute()
            st.success("💰 Gasto registrado y sincronizado de forma permanente.")

# --- MÓDULO 3: DASHBOARD FINANCIERO (Tu vista de Inversor) ---
elif menu == "Dashboard Financiero":
    st.header("📊 Inteligencia de Negocios e Históricos")
    
    # Descargar datos en vivo desde la nube para procesarlos con Python
    res_prod = supabase.table("produccion_diaria").select("*").execute()
    res_gastos = supabase.table("gastos_operativos").select("*").execute()
    
    df_prod = pd.DataFrame(res_prod.data)
    df_gastos = pd.DataFrame(res_gastos.data)
    
    # Calcular Ingresos Totales de los datos de la nube
    if not df_prod.empty:
        total_huevos = df_prod["huevo_aaa"] + df_prod["huevo_aa"]
        df_prod["ingreso_calculado"] = total_huevos * df_prod["precio_referencia"]
        total_ingresos = df_prod["ingreso_calculado"].sum()
    else:
        total_ingresos = 0
        
    # Calcular Egresos Totales
    total_egresos = df_gastos["monto"].sum() if not df_gastos.empty else 0
    utilidad_neta = total_ingresos - total_egresos
    
    # Mostrar tarjetas con métricas financieras
    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos Totales", f"${total_ingresos:,.0f} COP")
    col2.metric("Egresos Totales", f"${total_egresos:,.0f} COP")
    col3.metric("Utilidad Neta", f"${utilidad_neta:,.0f} COP")
    
    st.markdown("---")
    st.subheader("Distribución de Utilidades (Pacto 75% / 25%)")
    
    pago_anyela = max(0, utilidad_neta * 0.75)
    pago_inversor = max(0, utilidad_neta * 0.25)
    
    c_inv, c_gest = st.columns(2)
    c_inv.markdown(f"**Tu 25% (Inversor):**\n### ${pago_inversor:,.0f} COP")
    c_gest.markdown(f"**75% Anyela (Gestora):**\n### ${pago_anyela:,.0f} COP")