import streamlit as st
import pandas as pd
import datetime
import requests
from supabase import create_client
from imagenes import LOGO_BASE64


# Configuración de la página apta para pantallas de celular y PC
st.set_page_config(page_title="Avícola Procampo Pro", page_icon="🐔", layout="centered")

# Usamos HTML para pintar el logo perfectamente centrado y estirado
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="{LOGO_BASE64}" style="width: 100%; max-width: 600px; border-radius: 10px;">
    </div>
    """,
    unsafe_allow_html=True
)


url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

url_supabase = st.secrets["SUPABASE_URL"]
key_supabase = st.secrets["SUPABASE_KEY"]

st.title("CONTROL CENTRALIZADO")

# Menú lateral interactivo
menu = st.sidebar.selectbox("Seleccione un Módulo", ["Registrar Producción", "Registrar Gastos", "Dashboard Financiero"])

def porcentaje_produccion_x_dia (total_huevos_x_dia, total_aves):
        if total_aves <= 0:
            return 0.0
        
        porcentaje = (total_huevos_x_dia/total_aves) * 100
        return round(porcentaje, 2)
    
# --- MÓDULO 1: REGISTRAR PRODUCCIÓN ---
if menu == "Registrar Producción":
    st.header("DATOS DIARIOS")
    
    with st.form("form_cloud_prod", clear_on_submit=True):
        fecha = st.date_input("Fecha", datetime.date.today())
        aves = st.number_input("Aves Totales Activas", min_value=1, value=768)
        mortalidad = st.number_input("Aves Muertas Hoy", min_value=0, value=0)
        
        st.subheader("Clasificación de Huevos (Unidades)")
        col1, col2 = st.columns(2)
        with col1:
            h_c = st.number_input("Huevo Tipo C", min_value=0, value=0)
            h_b = st.number_input("Huevo Tipo B", min_value=0, value=0)
            h_a = st.number_input("Huevo Tipo A", min_value=0, value=0)
            h_aa = st.number_input("Huevo Tipo AA", min_value=0, value=0)
            h_aaa = st.number_input("Huevo Tipo AAA", min_value=0, value=0)
            h_yumbo = st.number_input("Huevo Yumbo", min_value=0, value=0)
            h_roto = st.number_input("Huevo Roto", min_value=0, value=0)
            
        #with col2:
            #precio = st.number_input("Precio base de venta por unidad ($ COP)", min_value=0, value=450)
        
        boton_enviar = st.form_submit_button("CARGAR")
        
        if boton_enviar:
            total_huevos_x_dia = h_c + h_b + h_a + h_aa + h_aaa + h_yumbo + h_roto
            total_aves = aves
            porcentaje_dia = porcentaje_produccion_x_dia(total_huevos_x_dia, total_aves)
            st.metric(label="Porcentaje de Producción", value=f"{porcentaje_dia}%")
            
            # Diccionario con los datos que espera la tabla de Supabase
            datos_insertar = {
                "fecha": str(fecha),
                "aves_totales": aves,
                "mortalidad": mortalidad,
                "huevo_c": h_c,
                "huevo_b": h_b,
                "huevo_a": h_a,
                "huevo_aa": h_aa,
                "huevo_aaa": h_aaa,
                "huevo_yumbo": h_yumbo,
                "huevo_roto": h_roto,
                "total_huevos": total_huevos_x_dia,
                "porcentaje_produccion": porcentaje_dia
            }        
        
            # --- ENVÍO DIRECTO SEGURO CON REQUESTS ---
            
            try:
                # Usamos el cliente nativo 'supabase' que ya está configurado en tu app
                respuesta = supabase.table("produccion_diaria").insert(datos_insertar).execute()
            
                # Si llega aquí, todo salió excelente
                st.success("¡Datos de producción guardados exitosamente en Supabase!")
            
            except Exception as e:
                # Si no hay internet o la URL está mal, la app NO se congela en pantalla negra.
                # En su lugar, muestra este aviso rojo controlado:
                st.error("❌ No se pudieron enviar los datos.")
                st.warning(f"Detalle del error (Revisa tu conexión o credenciales): {e}")
           

# --- MÓDULO 2: REGISTRAR GASTOS ---
elif menu == "Registrar Gastos":
    st.header("Registro de Gastos / Costos")
    
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
            st.success("Gasto registrado y sincronizado de forma permanente.")

# --- MÓDULO 3: DASHBOARD FINANCIERO (Tu vista de Inversor) ---
elif menu == "Dashboard Financiero":
    st.header("Inteligencia de Negocios e Históricos")
    
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
