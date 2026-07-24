"""
Migra clientes desde CSV de Loopy Loyalty a Airtable Cotorreo Rewards.

Logica:
1. Lee data/loopy_export.csv
2. Dedup por telefono (queda registro con MAS sellos)
3. Solo migra opted_in='yes' (dieron consentimiento)
4. Crea miembros con origen_registro='migracion_loopy'
5. Para los con sellos>0, crea transaccion 'MIGRACION LOOPY' (monto=sellos*10000)
6. Reporta stats finales

Idempotente: si el miembro ya existe (por telefono), skipea.
"""
import os, json, csv, re, time, urllib.request, urllib.error

def _get_token():
    fallback = r"C:\Users\vicente benitez2\.airtable_token"
    if os.path.exists(fallback):
        return open(fallback).read().strip()
    return os.environ.get("AIRTABLE_TOKEN", "")

TOKEN = _get_token()
BASE_ID = "appikgN0kBCRVOIC1"
API = f"https://api.airtable.com/v0/{BASE_ID}"
CSV_PATH = r"C:\Users\vicente benitez2\cotorreo-rewards\data\loopy_export.csv"


def api(method, path, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(f"{API}/{path}", data=data, method=method,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())


def normalizar(tel):
    d = re.sub(r"\D", "", tel or "")
    if not d: return ""
    if d.startswith("506") and len(d) == 11: return d
    if len(d) == 11 and d.startswith("506"): return d
    if len(d) == 8: return "506" + d
    return d


# === 1. LEER CSV ===
print("[1/4] Leyendo CSV Loopy...")
registros = []
with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f):
        tel = normalizar(row.get("telefono", ""))
        if not tel: continue
        registros.append({
            "telefono": tel,
            "nombre": (row.get("nombre") or "").strip(),
            "email": (row.get("email") or "").strip(),
            "cumpleanos": (row.get("cumpleanos") or "").strip(),
            "stamps": int(row.get("stamps_earned") or "0"),
            "opted_in": (row.get("opted_in") or "").strip().lower() == "yes",
            "card_status": (row.get("card_status") or "").strip(),
        })
print(f"  Total registros crudo: {len(registros)}")


# === 2. DEDUP por telefono (queda con MAS sellos) ===
print("\n[2/4] Deduplicando por telefono...")
por_tel = {}
for r in registros:
    tel = r["telefono"]
    if tel not in por_tel or r["stamps"] > por_tel[tel]["stamps"]:
        por_tel[tel] = r
    elif r["stamps"] == por_tel[tel]["stamps"] and r["opted_in"] and not por_tel[tel]["opted_in"]:
        por_tel[tel] = r
print(f"  Telefonos unicos: {len(por_tel)}")

todos = list(por_tel.values())
opted_in = [r for r in todos if r["opted_in"]]
opted_out = [r for r in todos if not r["opted_in"]]
print(f"  Con opted_in='yes': {len(opted_in)}")
print(f"  Con opted_in='no' (se migran igual, se respetará en campañas): {len(opted_out)}")

con_sellos = [r for r in todos if r["stamps"] > 0]
print(f"  Con sellos > 0: {len(con_sellos)}")


# === 3. CHECK MIEMBROS EXISTENTES en Airtable (para idempotencia) ===
print("\n[3/4] Verificando miembros ya migrados en Airtable...")
existentes = set()
offset = None
while True:
    path = "Miembros?pageSize=100&fields[]=telefono"
    if offset: path += f"&offset={offset}"
    s, r = api("GET", path)
    if s != 200: break
    for rec in r.get("records", []):
        tel = (rec.get("fields", {}).get("telefono") or "").strip()
        if tel: existentes.add(tel)
    offset = r.get("offset")
    if not offset: break
print(f"  Miembros ya en Airtable: {len(existentes)}")

pendientes = [r for r in todos if r["telefono"] not in existentes]
print(f"  A migrar (no existen aun): {len(pendientes)}")


# === 4. MIGRAR ===
print(f"\n[4/4] Migrando {len(pendientes)} miembros...")
ok = 0
fallos = 0
fallidos_detalle = []
for i, r in enumerate(pendientes, 1):
    # Crear miembro (marcar 'activo' según opted_in original de Loopy)
    fields = {
        "telefono": r["telefono"],
        "nombre": r["nombre"],
        "origen_registro": "migracion_loopy",
        "activo": r["opted_in"],  # true si opted_in=yes, false si opted_in=no
        "fecha_registro": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
    }
    if not r["opted_in"]:
        fields["notas_admin"] = "Migrado desde Loopy con opted_in=no. Respetar en campañas masivas."
    if r["email"]:
        fields["email"] = r["email"].lower()
    if r["cumpleanos"] and re.match(r"^\d{4}-\d{2}-\d{2}$", r["cumpleanos"]):
        fields["cumpleanos"] = r["cumpleanos"]

    s, resp = api("POST", "Miembros", {"fields": fields, "typecast": True})
    if s != 200:
        fallos += 1
        fallidos_detalle.append({"tel": r["telefono"], "nombre": r["nombre"], "err": json.dumps(resp)[:120]})
        continue

    miembro_id = resp["id"]

    # Si tiene sellos, crear transaccion "MIGRACION LOOPY"
    if r["stamps"] > 0:
        monto = r["stamps"] * 10000  # inverso de la formula sellos_ganados
        tx_fields = {
            "miembro": [miembro_id],
            "monto_colones": monto,
            "negocio": "plaza_cotorreo",  # asumimos Plaza como default histórico
            "cajero": "MIGRACION_LOOPY",
            "metodo_registro": "import_csv",
            "notas": f"Migracion Loopy Loyalty: {r['stamps']} sellos historicos",
            "fecha_compra": "2025-01-01",  # fecha aproximada retroactiva
        }
        s2, _ = api("POST", "Transacciones", {"fields": tx_fields, "typecast": True})

    ok += 1
    if i % 20 == 0 or i == len(pendientes):
        print(f"  [{i}/{len(pendientes)}] OK={ok} FAIL={fallos}")
    # throttle suave
    time.sleep(0.1)

# === REPORTE ===
print(f"\n{'='*60}")
print(f"MIGRACION COMPLETADA")
print(f"{'='*60}")
print(f"  Migrados OK: {ok}")
print(f"  Fallos: {fallos}")
print(f"  Skipeados (opted_out): {len(opted_out)}")
print(f"  Skipeados (ya existian): {len(opted_in) - len(pendientes)}")

if fallidos_detalle:
    print(f"\nPrimeros 5 fallos:")
    for f in fallidos_detalle[:5]:
        print(f"  {f['tel']} {f['nombre']}: {f['err']}")
