// Helper cliente Airtable para Cotorreo Rewards.
// Requiere env vars: AIRTABLE_TOKEN + AIRTABLE_REWARDS_BASE_ID
//
// 4 tablas: Miembros | Transacciones | Canjes | EventosLog

const AIRTABLE_BASE_URL = "https://api.airtable.com/v0";

function cfg() {
  const token = process.env.AIRTABLE_TOKEN;
  const baseId = process.env.AIRTABLE_REWARDS_BASE_ID;
  if (!token || !baseId) throw new Error("Faltan AIRTABLE_TOKEN o AIRTABLE_REWARDS_BASE_ID");
  return { token, baseId };
}

async function airtableRequest(method, path, body) {
  const { token, baseId } = cfg();
  const url = `${AIRTABLE_BASE_URL}/${baseId}/${path}`;
  const opts = {
    method,
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  };
  if (body) opts.body = JSON.stringify(body);
  const r = await fetch(url, opts);
  const text = await r.text();
  if (!r.ok) {
    throw new Error(`Airtable ${method} ${path} status=${r.status}: ${text.slice(0, 200)}`);
  }
  return text ? JSON.parse(text) : null;
}

const at = {
  get: (table, params) => {
    const qs = new URLSearchParams();
    Object.entries(params || {}).forEach(([k, v]) => {
      if (v !== undefined && v !== null) qs.append(k, v);
    });
    return airtableRequest("GET", `${encodeURIComponent(table)}?${qs.toString()}`);
  },
  post: (table, body) => airtableRequest("POST", encodeURIComponent(table), body),
  patch: (table, id, fields) =>
    airtableRequest("PATCH", `${encodeURIComponent(table)}/${id}`, { fields }),
  delete: (table, id) => airtableRequest("DELETE", `${encodeURIComponent(table)}/${id}`),
};

// ============================================
// Helpers dominio Rewards
// ============================================

/**
 * Normaliza telefono a formato "50672882394" (solo digitos, 11 caracteres si CR).
 */
function normalizarTelefono(tel) {
  const d = String(tel || "").replace(/\D/g, "");
  if (!d) return "";
  // Si empieza con 8 digitos, asumir CR y prefijar 506
  if (d.length === 8) return "506" + d;
  return d;
}

/**
 * Busca miembro por telefono. Devuelve null si no existe.
 */
async function buscarMiembroPorTelefono(telefono) {
  const clean = normalizarTelefono(telefono);
  if (!clean) return null;
  const r = await at.get("Miembros", {
    filterByFormula: `{telefono}='${clean}'`,
    maxRecords: 1,
  });
  const records = r?.records || [];
  return records[0] || null;
}

/**
 * Crea un miembro nuevo.
 */
async function crearMiembro({ telefono, nombre, email, cumpleanos, origen }) {
  const clean = normalizarTelefono(telefono);
  if (!clean) throw new Error("Telefono invalido");
  const fields = {
    telefono: clean,
    nombre: (nombre || "").trim(),
    origen_registro: origen || "web",
    activo: true,
  };
  if (email) fields.email = email.trim().toLowerCase();
  if (cumpleanos) fields.cumpleanos = cumpleanos;
  const r = await at.post("Miembros", { fields, typecast: true });
  return r;
}

/**
 * Registra una transaccion (compra) para un miembro.
 * Devuelve el registro creado (incluye sellos_ganados calculado).
 */
async function registrarTransaccion({ miembroId, monto, negocio, cajero, metodoRegistro, notas, fechaCompra }) {
  const fields = {
    miembro: [miembroId],
    monto_colones: Number(monto),
    negocio: negocio || "plaza_cotorreo",
    metodo_registro: metodoRegistro || "manual_telefono",
    fecha_compra: fechaCompra || new Date().toISOString().slice(0, 10),
  };
  if (cajero) fields.cajero = cajero;
  if (notas) fields.notas = notas;
  const r = await at.post("Transacciones", { fields, typecast: true });
  return r;
}

/**
 * Trae al miembro recargando sus rollups (necesario despues de crear transaccion).
 * Los rollups en Airtable se recalculan async — pequeno delay ayuda.
 */
async function recargarMiembro(miembroId) {
  return await airtableRequest("GET", `Miembros/${miembroId}`);
}

/**
 * Genera un codigo de canje de 6 digitos unico.
 */
async function generarCodigoCanjeUnico() {
  for (let i = 0; i < 5; i++) {
    const code = String(Math.floor(100000 + Math.random() * 900000));
    const r = await at.get("Canjes", {
      filterByFormula: `{codigo_canje}='${code}'`,
      maxRecords: 1,
    });
    if (!(r?.records?.length)) return code;
  }
  throw new Error("No se pudo generar codigo unico despues de 5 intentos");
}

/**
 * Registra un evento en EventosLog.
 */
async function log(tipo, payload, miembroId) {
  try {
    const fields = { tipo_evento: tipo, payload_json: JSON.stringify(payload || {}) };
    if (miembroId) fields.miembro = [miembroId];
    await at.post("EventosLog", { fields, typecast: true });
  } catch (e) {
    console.log("EventosLog error:", e.message);
  }
}

module.exports = {
  at,
  normalizarTelefono,
  buscarMiembroPorTelefono,
  crearMiembro,
  registrarTransaccion,
  recargarMiembro,
  generarCodigoCanjeUnico,
  log,
};
