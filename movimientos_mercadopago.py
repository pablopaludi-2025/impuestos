import mercadopago

ACCESS_TOKEN = "APP_USR-XXXX"
sdk = mercadopago.SDK(ACCESS_TOKEN)

result = sdk.payment().search({
    "status": "approved",
    "sort": "date_created",
    "criteria": "desc"
})

print("📊 Últimos pagos recibidos:")

for p in result["response"]["results"][:5]:
    payment_id = p["id"]
    detalle = sdk.payment().get(payment_id)["response"]

    monto = detalle.get("transaction_amount")
    fecha = detalle.get("date_created")
    estado = detalle.get("status")
    descripcion = detalle.get("description", "-")

    payer = detalle.get("payer", {})
    nombre = f"{payer.get('first_name', '')} {payer.get('last_name', '')}".strip()
    email = payer.get("email", "-")
    identificacion = payer.get("identification", {})
    tipo_doc = identificacion.get("type", "-")
    numero_doc = identificacion.get("number", "-")

    # Detectar si es débito automático
    subscription_id = detalle.get("subscription_id")
    es_debito_automatico = "✅ DÉBITO AUTOMÁTICO" if subscription_id else "—"

    print(f"\n🧾 Pago ID: {payment_id}")
    print(f"💵 Monto: {monto}")
    print(f"📅 Fecha: {fecha}")
    print(f"🔖 Estado: {estado}")
    print(f"📝 Descripción: {descripcion}")
    print(f"👤 Pagador: {nombre} | Email: {email}")
    print(f"🆔 {tipo_doc}: {numero_doc}")
    print(f"🔁 Tipo de cobro: {es_debito_automatico}")
