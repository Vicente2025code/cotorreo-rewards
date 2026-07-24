"""
Setup automatico + idempotente del schema Airtable para Cotorreo Rewards.
Puede correrse multiple veces: solo crea lo que falta.
"""
import os, json, time, urllib.request, urllib.error


def _get_token():
    fallback = r"C:\Users\vicente benitez2\.airtable_token"
    if os.path.exists(fallback):
        with open(fallback, "r", encoding="utf-8") as f:
            return f.read().strip()
    return os.environ.get("AIRTABLE_TOKEN", "")


TOKEN = _get_token()
BASE_ID = "appikgN0kBCRVOIC1"
API = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}"


def api(method, path, body=None):
    url = f"{API}/{path}"
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


def get_schema():
    s, r = api("GET", "tables")
    if s != 200:
        raise Exception(f"getSchema failed: {r}")
    return {t["name"]: t for t in r.get("tables", [])}


def crear_o_obtener_tabla(nombre, description, fields_iniciales, schema):
    if nombre in schema:
        t = schema[nombre]
        print(f"  [{nombre}] YA EXISTE (id={t['id']}, {len(t.get('fields', []))} campos)")
        return t["id"]
    s, r = api("POST", "tables", {
        "name": nombre, "description": description, "fields": fields_iniciales
    })
    if s == 200:
        print(f"  [{nombre}] CREADA (id={r['id']}, {len(r['fields'])} campos)")
        return r["id"]
    print(f"  [{nombre}] FAIL: {json.dumps(r)[:150]}")
    return None


def agregar_campo(tabla_id, tabla_nombre, campo, existentes):
    if campo["name"] in existentes:
        return existentes[campo["name"]]
    s, r = api("POST", f"tables/{tabla_id}/fields", campo)
    if s == 200:
        print(f"    + {tabla_nombre}.{campo['name']}")
        return r.get("id")
    print(f"    ! FAIL {tabla_nombre}.{campo['name']}: {json.dumps(r)[:150]}")
    return None


def field_names(tabla):
    return {f["name"]: f["id"] for f in tabla.get("fields", [])}


# ================================
# FASE 1: Crear tablas con campos base (SIN createdTime, SIN links, SIN formulas)
# ================================
print("=" * 60); print("FASE 1: Crear tablas con campos basicos"); print("=" * 60)

schema = get_schema()

miembros_id = crear_o_obtener_tabla("Miembros", "Clientes inscritos en Cotorreo Rewards", [
    {"name": "telefono", "type": "singleLineText"},
    {"name": "nombre", "type": "singleLineText"},
    {"name": "email", "type": "email"},
], schema)

transacciones_id = crear_o_obtener_tabla("Transacciones", "Cada compra que genera sellos", [
    {"name": "fecha_compra", "type": "date", "options": {"dateFormat": {"name": "iso"}}},
    {"name": "monto_colones", "type": "number", "options": {"precision": 0}},
], schema)

canjes_id = crear_o_obtener_tabla("Canjes", "Cada canje pedido/hecho por un miembro", [
    {"name": "codigo_canje", "type": "singleLineText"},
    {"name": "valor_credito", "type": "number", "options": {"precision": 0}},
], schema)

eventos_id = crear_o_obtener_tabla("EventosLog", "Auditoria de eventos del sistema", [
    {"name": "payload_json", "type": "multilineText"},
], schema)

# ================================
# FASE 2: Agregar campos regulares a cada tabla (recargar schema)
# ================================
print("\n" + "=" * 60); print("FASE 2: Campos regulares"); print("=" * 60)
schema = get_schema()

# --- Miembros ---
existentes = field_names(schema["Miembros"])
print("\n[Miembros] campos regulares:")
agregar_campo(miembros_id, "Miembros", {"name": "cumpleanos", "type": "date", "options": {"dateFormat": {"name": "iso"}}}, existentes)
agregar_campo(miembros_id, "Miembros", {"name": "fecha_registro", "type": "createdTime", "options": {"result": {"type": "dateTime", "options": {"dateFormat": {"name": "iso"}, "timeFormat": {"name": "24hour"}, "timeZone": "America/Costa_Rica"}}}}, existentes)
agregar_campo(miembros_id, "Miembros", {"name": "origen_registro", "type": "singleSelect", "options": {"choices": [
    {"name": "web"}, {"name": "cajero"}, {"name": "migracion_loopy"}, {"name": "bot_whatsapp"}]}}, existentes)
agregar_campo(miembros_id, "Miembros", {"name": "wallet_pass_id", "type": "singleLineText"}, existentes)
agregar_campo(miembros_id, "Miembros", {"name": "activo", "type": "checkbox", "options": {"icon": "check", "color": "greenBright"}}, existentes)
agregar_campo(miembros_id, "Miembros", {"name": "notas_admin", "type": "multilineText"}, existentes)

# --- Transacciones ---
existentes = field_names(schema["Transacciones"])
print("\n[Transacciones] campos regulares:")
agregar_campo(transacciones_id, "Transacciones", {"name": "negocio", "type": "singleSelect", "options": {"choices": [
    {"name": "plaza_cotorreo"}, {"name": "cotorreo_taqueria"}, {"name": "alpadel"},
    {"name": "bebros"}, {"name": "otro_1"}, {"name": "otro_2"}]}}, existentes)
agregar_campo(transacciones_id, "Transacciones", {"name": "cajero", "type": "singleLineText"}, existentes)
agregar_campo(transacciones_id, "Transacciones", {"name": "metodo_registro", "type": "singleSelect", "options": {"choices": [
    {"name": "qr_scan"}, {"name": "manual_telefono"}, {"name": "import_csv"}]}}, existentes)
agregar_campo(transacciones_id, "Transacciones", {"name": "notas", "type": "multilineText"}, existentes)

# --- Canjes ---
existentes = field_names(schema["Canjes"])
print("\n[Canjes] campos regulares:")
agregar_campo(canjes_id, "Canjes", {"name": "fecha_solicitud", "type": "createdTime", "options": {"result": {"type": "dateTime", "options": {"dateFormat": {"name": "iso"}, "timeFormat": {"name": "24hour"}, "timeZone": "America/Costa_Rica"}}}}, existentes)
agregar_campo(canjes_id, "Canjes", {"name": "fecha_uso", "type": "date", "options": {"dateFormat": {"name": "iso"}}}, existentes)
agregar_campo(canjes_id, "Canjes", {"name": "sellos_gastados", "type": "number", "options": {"precision": 0}}, existentes)
agregar_campo(canjes_id, "Canjes", {"name": "estado", "type": "singleSelect", "options": {"choices": [
    {"name": "pendiente"}, {"name": "usado"}, {"name": "expirado"}, {"name": "cancelado"}]}}, existentes)
agregar_campo(canjes_id, "Canjes", {"name": "negocio_uso", "type": "singleSelect", "options": {"choices": [
    {"name": "plaza_cotorreo"}, {"name": "cotorreo_taqueria"}, {"name": "alpadel"},
    {"name": "bebros"}, {"name": "otro_1"}, {"name": "otro_2"}]}}, existentes)
agregar_campo(canjes_id, "Canjes", {"name": "cajero_valido", "type": "singleLineText"}, existentes)
agregar_campo(canjes_id, "Canjes", {"name": "fecha_expira", "type": "date", "options": {"dateFormat": {"name": "iso"}}}, existentes)

# --- EventosLog ---
existentes = field_names(schema["EventosLog"])
print("\n[EventosLog] campos regulares:")
agregar_campo(eventos_id, "EventosLog", {"name": "fecha", "type": "createdTime", "options": {"result": {"type": "dateTime", "options": {"dateFormat": {"name": "iso"}, "timeFormat": {"name": "24hour"}, "timeZone": "America/Costa_Rica"}}}}, existentes)
agregar_campo(eventos_id, "EventosLog", {"name": "tipo_evento", "type": "singleSelect", "options": {"choices": [
    {"name": "miembro_creado"}, {"name": "sellos_sumados"},
    {"name": "canje_solicitado"}, {"name": "canje_validado"},
    {"name": "canje_expirado"}, {"name": "notif_wati_enviada"},
    {"name": "error"}, {"name": "otro"}]}}, existentes)

# ================================
# FASE 3: LINKS entre tablas
# ================================
print("\n" + "=" * 60); print("FASE 3: Links entre tablas"); print("=" * 60)
schema = get_schema()

existentes = field_names(schema["Transacciones"])
agregar_campo(transacciones_id, "Transacciones", {
    "name": "miembro", "type": "multipleRecordLinks",
    "options": {"linkedTableId": miembros_id, "prefersSingleRecordLink": True}
}, existentes)

existentes = field_names(schema["Canjes"])
agregar_campo(canjes_id, "Canjes", {
    "name": "miembro", "type": "multipleRecordLinks",
    "options": {"linkedTableId": miembros_id, "prefersSingleRecordLink": True}
}, existentes)

existentes = field_names(schema["EventosLog"])
agregar_campo(eventos_id, "EventosLog", {
    "name": "miembro", "type": "multipleRecordLinks",
    "options": {"linkedTableId": miembros_id, "prefersSingleRecordLink": True}
}, existentes)

# ================================
# FASE 4: FORMULAS
# ================================
print("\n" + "=" * 60); print("FASE 4: Formulas"); print("=" * 60)
schema = get_schema()

existentes = field_names(schema["Miembros"])
agregar_campo(miembros_id, "Miembros", {
    "name": "id_corto", "type": "formula",
    "options": {"formula": "'RW-' & RIGHT(RECORD_ID(), 5)"}
}, existentes)

existentes = field_names(schema["Transacciones"])
agregar_campo(transacciones_id, "Transacciones", {
    "name": "id_corto", "type": "formula",
    "options": {"formula": "'TX-' & DATETIME_FORMAT({fecha_compra}, 'YYYYMMDD') & '-' & RIGHT(RECORD_ID(), 4)"}
}, existentes)

agregar_campo(transacciones_id, "Transacciones", {
    "name": "sellos_ganados", "type": "formula",
    "options": {"formula": "FLOOR({monto_colones}/10000)"}
}, existentes)

existentes = field_names(schema["Canjes"])
agregar_campo(canjes_id, "Canjes", {
    "name": "id_corto", "type": "formula",
    "options": {"formula": "'CJ-' & RIGHT(RECORD_ID(), 5)"}
}, existentes)

# ================================
# FASE 5: ROLLUPS en Miembros
# ================================
print("\n" + "=" * 60); print("FASE 5: Rollups en Miembros"); print("=" * 60)
time.sleep(2)
schema = get_schema()

miembros_tabla = schema["Miembros"]
trans_tabla = schema["Transacciones"]
canjes_tabla = schema["Canjes"]

# Encontrar link inverso auto-generado en Miembros
link_transac_id = None
link_canjes_id = None
for f in miembros_tabla.get("fields", []):
    if f.get("type") == "multipleRecordLinks":
        opts = f.get("options", {})
        if opts.get("linkedTableId") == transacciones_id:
            link_transac_id = f["id"]
            print(f"  Link inverso Transacciones: {f['name']} (id={f['id']})")
        elif opts.get("linkedTableId") == canjes_id:
            link_canjes_id = f["id"]
            print(f"  Link inverso Canjes: {f['name']} (id={f['id']})")

trans_fields = field_names(trans_tabla)
canjes_fields = field_names(canjes_tabla)

existentes = field_names(miembros_tabla)

if link_transac_id and "sellos_ganados" in trans_fields:
    agregar_campo(miembros_id, "Miembros", {
        "name": "sellos_historicos", "type": "rollup",
        "options": {
            "recordLinkFieldId": link_transac_id,
            "fieldIdInLinkedTable": trans_fields["sellos_ganados"],
            "result": {"type": "number", "options": {"precision": 0}},
            "formula": "SUM(values)"
        }
    }, existentes)

if link_canjes_id and "sellos_gastados" in canjes_fields:
    agregar_campo(miembros_id, "Miembros", {
        "name": "sellos_canjeados", "type": "rollup",
        "options": {
            "recordLinkFieldId": link_canjes_id,
            "fieldIdInLinkedTable": canjes_fields["sellos_gastados"],
            "result": {"type": "number", "options": {"precision": 0}},
            "formula": "SUM(IF({estado}='cancelado', 0, values))"
        }
    }, existentes)

# Ahora sí, formulas que dependen de los rollups
time.sleep(1)
schema = get_schema()
existentes = field_names(schema["Miembros"])
agregar_campo(miembros_id, "Miembros", {
    "name": "sellos_actuales", "type": "formula",
    "options": {
        "formula": "IF({sellos_historicos}, {sellos_historicos}, 0) - IF({sellos_canjeados}, {sellos_canjeados}, 0)"
    }
}, existentes)

agregar_campo(miembros_id, "Miembros", {
    "name": "canje_disponible", "type": "formula",
    "options": {"formula": "IF({sellos_actuales} >= 20, 1, 0)"}
}, existentes)

print("\n" + "=" * 60); print("SETUP COMPLETO"); print("=" * 60)
final_schema = get_schema()
for name in ["Miembros", "Transacciones", "Canjes", "EventosLog"]:
    if name in final_schema:
        t = final_schema[name]
        print(f"  {name:15} id={t['id']}  campos={len(t['fields'])}")

print(f"\nAbrir base: https://airtable.com/{BASE_ID}")
