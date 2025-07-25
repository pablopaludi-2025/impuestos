import pandas as pd

# Leer archivos
cobros_df = pd.read_excel("2025-07-Cobros Realizados.xlsx")
facturas_df = pd.read_excel("2025-07-Facturas Realizadas.xlsx")

# Normalizar CUIT y nombre
cobros_df['CUIT'] = cobros_df['CUIT'].astype(str).str.strip()
facturas_df['CUIT'] = facturas_df['CUIT'].astype(str).str.strip()
cobros_df['Nombre'] = cobros_df['Nombre'].astype(str).str.upper().str.strip()
facturas_df['Nombre'] = facturas_df['Nombre'].astype(str).str.upper().str.strip()

# Asegurar tipo fecha
cobros_df['Fecha'] = pd.to_datetime(cobros_df['Fecha'], errors='coerce')
facturas_df['Fecha'] = pd.to_datetime(facturas_df['Fecha'], errors='coerce')

# Asegurar campo Detalle en cobros
if 'Detalle' not in cobros_df.columns:
    cobros_df['Detalle'] = ''
else:
    cobros_df['Detalle'] = cobros_df['Detalle'].astype(str).fillna('')

# Crear campo Detalle Formateado para cobros de forma segura
def format_detalle_cobro(row):
    fecha_str = row['Fecha'].strftime('%Y-%m-%d') if pd.notnull(row['Fecha']) else '(sin fecha)'
    detalle = str(row['Detalle']).strip()
    importe_str = f"${row['Importe']:.2f}" if pd.notnull(row['Importe']) else "$0.00"
    return f"{fecha_str}  {importe_str}  {detalle}"

cobros_df['Detalle Formateado'] = cobros_df.apply(format_detalle_cobro, axis=1)

# Agrupar detalles de cobros
detalle_cobros = cobros_df.groupby('CUIT')['Detalle Formateado'].apply(
    lambda detalles: '[' + ' | '.join(detalles) + ']'
).reset_index().rename(columns={'Detalle Formateado': 'Detalle Cobro'})

# Agrupar totales
cobros_total = cobros_df.groupby('CUIT', as_index=False).agg({'Nombre': 'first', 'Importe': 'sum'})
cobros_total.rename(columns={'Importe': 'Cobrado'}, inplace=True)
facturas_total = facturas_df.groupby('CUIT', as_index=False).agg({'Nombre': 'first', 'Importe': 'sum'})
facturas_total.rename(columns={'Importe': 'Facturado'}, inplace=True)

# Asegurar campo Nro y crear Detalle Factura con fecha
if 'Nro' not in facturas_df.columns:
    facturas_df['Nro'] = '(sin número)'
else:
    facturas_df['Nro'] = facturas_df['Nro'].astype(str).fillna('(sin número)')

def format_detalle_factura(row):
    fecha_str = row['Fecha'].strftime('%Y-%m-%d') if pd.notnull(row['Fecha']) else '(sin fecha)'
    importe_str = f"${row['Importe']:.2f}" if pd.notnull(row['Importe']) else "$0.00"
    return f"N°{row['Nro']}  {fecha_str}  {importe_str}"

facturas_df['Detalle Factura'] = facturas_df.apply(format_detalle_factura, axis=1)

detalle_facturas = facturas_df.groupby('CUIT')['Detalle Factura'].apply(
    lambda detalles: '[' + ' | '.join(detalles) + ']'
).reset_index().rename(columns={'Detalle Factura': 'Detalle Facturas'})

# Combinar todo
resumen = pd.merge(cobros_total, facturas_total, on='CUIT', how='outer', suffixes=('_Cobro', '_Factura')).fillna(0)
resumen = pd.merge(resumen, detalle_cobros, on='CUIT', how='left').fillna({'Detalle Cobro': '[]'})
resumen = pd.merge(resumen, detalle_facturas, on='CUIT', how='left').fillna({'Detalle Facturas': '[]'})

# Unificar nombre
resumen['Nombre'] = resumen.apply(lambda row: row['Nombre_Cobro'] or row['Nombre_Factura'], axis=1)

# Calcular diferencia
resumen['Cobrado'] = pd.to_numeric(resumen['Cobrado'], errors='coerce').fillna(0)
resumen['Facturado'] = pd.to_numeric(resumen['Facturado'], errors='coerce').fillna(0)
resumen['Pendiente de Facturar'] = resumen['Cobrado'] - resumen['Facturado']

# Resultado final
resumen_final = resumen[['CUIT', 'Nombre', 'Cobrado', 'Facturado', 'Pendiente de Facturar', 'Detalle Cobro', 'Detalle Facturas']]

# Dividir por situación
pendiente_negativo = resumen_final[resumen_final['Pendiente de Facturar'] < 0]
pendiente_cero = resumen_final[resumen_final['Pendiente de Facturar'] == 0]
pendiente_positivo = resumen_final[resumen_final['Pendiente de Facturar'] > 0]

# Mostrar salida por grupos
def imprimir_grupo(titulo, df):
    print(titulo)
    if df.empty:
        print("Sin datos.\n")
    else:
        print(df.to_csv(index=False))

imprimir_grupo("🟡 Saldo a favor del cliente (Facturado > Cobrado):", pendiente_negativo)
imprimir_grupo("✅ Sin deuda (Cobrado == Facturado):", pendiente_cero)
imprimir_grupo("🔴 Pendiente de facturar (Cobrado > Facturado):", pendiente_positivo)
