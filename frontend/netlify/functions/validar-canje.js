// POST /api/validar-canje
// Cajero valida el codigo de 6 digitos que muestra el cliente.
//
// Body: { codigo, negocio, cajero }
// Header: x-admin-token: <ADMIN_TOKEN>
//
// Response: { ok, canje, mensaje }

const { at, log } = require("./_lib_airtable");
const { sendSessionMessage } = require("./_lib_wati");

function respond(code, body) {
  return {
    statusCode: code,
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
    body: JSON.stringify(body),
  };
}

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") return respond(200, {});
  if (event.httpMethod !== "POST") return respond(405, { error: "Method not allowed" });

  // Auth admin
  const providedToken = event.headers?.["x-admin-token"] || event.headers?.["X-Admin-Token"];
  const expected = process.env.REWARDS_ADMIN_TOKEN || "MAR2103-rewards";
  if (providedToken !== expected) return respond(401, { error: "Unauthorized" });

  let body;
  try { body = JSON.parse(event.body || "{}"); }
  catch { return respond(400, { error: "Body inválido" }); }

  const codigo = String(body.codigo || "").trim();
  const negocio = body.negocio;
  const cajero = body.cajero || "";

  if (!/^\d{6}$/.test(codigo)) return respond(400, { error: "Código debe ser 6 dígitos" });
  if (!negocio) return respond(400, { error: "Negocio requerido" });

  const NEGOCIOS_VALIDOS = ["plaza_cotorreo", "cotorreo_taqueria", "alpadel", "bebros", "otro_1", "otro_2"];
  if (!NEGOCIOS_VALIDOS.includes(negocio)) {
    return respond(400, { error: `Negocio inválido. Válidos: ${NEGOCIOS_VALIDOS.join(", ")}` });
  }

  try {
    // Buscar canje por codigo
    const r = await at.get("Canjes", {
      filterByFormula: `{codigo_canje}='${codigo}'`,
      maxRecords: 1,
    });
    const canje = (r?.records || [])[0];
    if (!canje) return respond(404, { error: "Código no existe" });

    const estado = canje.fields.estado;
    if (estado === "usado") {
      return respond(400, {
        error: `Código ya usado el ${canje.fields.fecha_uso} en ${canje.fields.negocio_uso}`,
        canje: { id: canje.id, estado, fecha_uso: canje.fields.fecha_uso }
      });
    }
    if (estado === "cancelado") {
      return respond(400, { error: "Código cancelado" });
    }
    if (estado === "expirado") {
      return respond(400, { error: `Código expiró el ${canje.fields.fecha_expira}` });
    }

    // Chequear expiración por fecha (por si el estado no se actualizó)
    const hoy = new Date().toISOString().slice(0, 10);
    if (canje.fields.fecha_expira && canje.fields.fecha_expira < hoy) {
      await at.patch("Canjes", canje.id, { estado: "expirado" });
      return respond(400, { error: `Código expiró el ${canje.fields.fecha_expira}` });
    }

    // Marcar como usado
    await at.patch("Canjes", canje.id, {
      estado: "usado",
      fecha_uso: hoy,
      negocio_uso: negocio,
      cajero_valido: cajero,
    });

    // Log
    const miembroId = (canje.fields.miembro || [])[0];
    await log("canje_validado", { codigo, valor: canje.fields.valor_credito, negocio, cajero }, miembroId);

    // Notificar cliente que canje se uso
    if (miembroId) {
      const miembroR = await at.get("Miembros", {
        filterByFormula: `RECORD_ID()='${miembroId}'`, maxRecords: 1,
      });
      const miembro = (miembroR?.records || [])[0];
      if (miembro?.fields?.telefono) {
        const nombre = (miembro.fields.nombre || "").split(" ")[0] || "amigo";
        await sendSessionMessage(miembro.fields.telefono,
          `¡Listo ${nombre}! Tu canje de ₡${canje.fields.valor_credito.toLocaleString("es-CR")} ` +
          `fue aplicado en ${negocio.replace(/_/g, " ")}. 🎉\n\n` +
          `Seguí sumando sellos para ganar más beneficios.`
        );
      }
    }

    return respond(200, {
      ok: true,
      mensaje: "Código validado. Aplicá el descuento al cliente.",
      canje: {
        id: canje.id,
        id_corto: canje.fields.id_corto,
        valor: canje.fields.valor_credito,
        fecha_uso: hoy,
        negocio_uso: negocio,
      },
    });
  } catch (e) {
    console.error("validar-canje error:", e);
    await log("error", { fn: "validar-canje", msg: e.message, body });
    return respond(500, { error: e.message });
  }
};
