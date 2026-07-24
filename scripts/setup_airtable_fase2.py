"""
Fase 2: agregar los campos restantes (links + rollups + formulas dependientes).
Idempotente - solo agrega lo que falta.
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
    req = urllib.request.Request(url, data=data, method=method,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


def get_schema():
    _, r = api("GET", "tables")
    return {t["name"]: t for t in r.get("tables", [])}


def add_field(tid, tname, campo, existentes):
    if campo["name"] in existentes: return
    s, r = api("POST", f"tables/{tid}/fields", campo)
    if s == 200:
        print(f"    + {tname}.{campo['name']}")
    else:
        print(f"    ! FAIL {tname}.{campo['name']}: {json.dumps(r)[:180]}")


schema = get_schema()
miembros_id = schema["Miembros"]["id"]
trans_id = schema["Transacciones"]["id"]
canjes_id = schema["Canjes"]["id"]
eventos_id = schema["EventosLog"]["id"]

print("=== Estado actual de cada tabla ===")
for name in ["Miembros", "Transacciones", "Canjes", "EventosLog"]:
    t = schema[name]
    fnames = [f["name"] for f in t["fields"]]
    print(f"  {name}: {fnames}")

# ================================
# PASO 1: Agregar links (sin prefersSingleRecordLink que causaba error)
# ================================
print("\n=== PASO 1: Links entre tablas ===")
existentes = {f["name"] for f in schema["Transacciones"]["fields"]}
add_field(trans_id, "Transacciones", {
    "name": "miembro", "type": "multipleRecordLinks",
    "options": {"linkedTableId": miembros_id}
}, existentes)

existentes = {f["name"] for f in schema["Canjes"]["fields"]}
add_field(canjes_id, "Canjes", {
    "name": "miembro", "type": "multipleRecordLinks",
    "options": {"linkedTableId": miembros_id}
}, existentes)

existentes = {f["name"] for f in schema["EventosLog"]["fields"]}
add_field(eventos_id, "EventosLog", {
    "name": "miembro", "type": "multipleRecordLinks",
    "options": {"linkedTableId": miembros_id}
}, existentes)

# ================================
# PASO 2: Asegurar que Transacciones tiene id_corto + sellos_ganados
# ================================
print("\n=== PASO 2: Formulas en Transacciones ===")
schema = get_schema()
existentes = {f["name"] for f in schema["Transacciones"]["fields"]}
add_field(trans_id, "Transacciones", {
    "name": "id_corto", "type": "formula",
    "options": {"formula": "'TX-' & DATETIME_FORMAT({fecha_compra}, 'YYYYMMDD') & '-' & RIGHT(RECORD_ID(), 4)"}
}, existentes)
add_field(trans_id, "Transacciones", {
    "name": "sellos_ganados", "type": "formula",
    "options": {"formula": "FLOOR({monto_colones}/10000)"}
}, existentes)

# ================================
# PASO 3: Rollups en Miembros (usar link inverso creado por Airtable)
# ================================
print("\n=== PASO 3: Rollups en Miembros ===")
time.sleep(2)
schema = get_schema()

miembros_tabla = schema["Miembros"]
trans_tabla = schema["Transacciones"]
canjes_tabla = schema["Canjes"]

link_transac_id = None
link_canjes_id = None
for f in miembros_tabla["fields"]:
    if f.get("type") == "multipleRecordLinks":
        opts = f.get("options", {})
        if opts.get("linkedTableId") == trans_id:
            link_transac_id = f["id"]
            print(f"  Link Miembros -> Transacciones: '{f['name']}' (id={f['id']})")
        elif opts.get("linkedTableId") == canjes_id:
            link_canjes_id = f["id"]
            print(f"  Link Miembros -> Canjes: '{f['name']}' (id={f['id']})")

trans_fields = {f["name"]: f["id"] for f in trans_tabla["fields"]}
canjes_fields = {f["name"]: f["id"] for f in canjes_tabla["fields"]}
existentes = {f["name"] for f in miembros_tabla["fields"]}

if link_transac_id and "sellos_ganados" in trans_fields:
    add_field(miembros_id, "Miembros", {
        "name": "sellos_historicos", "type": "rollup",
        "options": {
            "recordLinkFieldId": link_transac_id,
            "fieldIdInLinkedTable": trans_fields["sellos_ganados"],
            "result": {"type": "number", "options": {"precision": 0}},
            "formula": "SUM(values)"
        }
    }, existentes)

if link_canjes_id and "sellos_gastados" in canjes_fields:
    add_field(miembros_id, "Miembros", {
        "name": "sellos_canjeados", "type": "rollup",
        "options": {
            "recordLinkFieldId": link_canjes_id,
            "fieldIdInLinkedTable": canjes_fields["sellos_gastados"],
            "result": {"type": "number", "options": {"precision": 0}},
            "formula": "SUM(IF({estado}='cancelado', 0, values))"
        }
    }, existentes)

# ================================
# PASO 4: Formulas que dependen de rollups
# ================================
print("\n=== PASO 4: Formulas dependientes ===")
time.sleep(1)
schema = get_schema()
existentes = {f["name"] for f in schema["Miembros"]["fields"]}

add_field(miembros_id, "Miembros", {
    "name": "sellos_actuales", "type": "formula",
    "options": {
        "formula": "IF({sellos_historicos}, {sellos_historicos}, 0) - IF({sellos_canjeados}, {sellos_canjeados}, 0)"
    }
}, existentes)

add_field(miembros_id, "Miembros", {
    "name": "canje_disponible", "type": "formula",
    "options": {"formula": "IF({sellos_actuales} >= 20, 1, 0)"}
}, existentes)

# ================================
# REPORTE FINAL
# ================================
print("\n" + "=" * 60)
print("SCHEMA FINAL")
print("=" * 60)
schema = get_schema()
for name in ["Miembros", "Transacciones", "Canjes", "EventosLog"]:
    t = schema[name]
    print(f"\n[{name}] ({len(t['fields'])} campos)")
    for f in t["fields"]:
        print(f"  - {f['name']:22} ({f['type']})")

print(f"\nURL base: https://airtable.com/{BASE_ID}")
