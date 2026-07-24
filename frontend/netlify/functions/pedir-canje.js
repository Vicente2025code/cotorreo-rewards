// POST /api/pedir-canje
// El cliente pide canjear 20 sellos por ₡15.000 de crédito.
//
// Body: { telefono }
// Response: { codigo_canje, valor, fecha_expira }

const { at, buscarMiembroPorTelefono, generarCodigoCanjeUnico, normalizarTelefono, log } = require("./_lib_airtable");
const { sendSessionMessage } = require("./_lib_wati");

const SELLOS_POR_CANJE = 20;
const VALOR_CANJE_COLONES = 15000;
const DIAS_EXPIRA = 30;

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

  let body;
  try { body = JSON.parse(event.body || "{}"); }
  catch { return respond(400, { error: "Body inválido" }); }

  const telefono = normalizarTelefono(body.telefono);
  if (!telefono) return respond(400, { error: "Teléfono requerido" });

  try {
    const miembro = await buscarMiembroPorTelefono(telefono);
    if (!miembro) return respond(404, { error: "Miembro no encontrado" });

    const sellos = Number(miembro.fields.sellos_actuales || 0);
    if (sellos < SELLOS_POR_CANJE) {
      return respond(400, {
        error: `No tenés suficientes sellos. Tenés ${sellos}, necesitás ${SELLOS_POR_CANJE}.`,
        sellos_actuales: sellos,
        faltan: SELLOS_POR_CANJE - sellos,
      });
    }

    // Generar código único
    const codigo = await generarCodigoCanjeUnico();

    // Fecha expira = hoy + 30 días
    const expira = new Date();
    expira.setDate(expira.getDate() + DIAS_EXPIRA);
    const fechaExpira = expira.toISOString().slice(0, 10);

    // Crear registro canje
    const canje = await at.post("Canjes", {
      fields: {
        miembro: [miembro.id],
        codigo_canje: codigo,
        valor_credito: VALOR_CANJE_COLONES,
        sellos_gastados: SELLOS_POR_CANJE,
        estado: "pendiente",
        fecha_expira: fechaExpira,
        fecha_solicitud: new Date().toISOString(),
      },
      typecast: true,
    });

    // Log evento
    await log("canje_solicitado", { codigo, valor: VALOR_CANJE_COLONES, expira: fechaExpira }, miembro.id);

    // Notificar cliente
    const nombre = (miembro.fields.nombre || "").split(" ")[0] || "amigo";
    await sendSessionMessage(telefono,
      `🎁 ${nombre}, tu código de canje es:\n\n` +
      `*${codigo}*\n\n` +
      `Vale ₡${VALOR_CANJE_COLONES.toLocaleString("es-CR")} en cualquier negocio de Grupo Cotorreo.\n` +
      `Válido hasta ${fechaExpira}.\n\n` +
      `Mostrá este código al cajero al momento de pagar. ¡Disfrutalo!`
    );

    return respond(200, {
      ok: true,
      codigo_canje: codigo,
      valor: VALOR_CANJE_COLONES,
      sellos_gastados: SELLOS_POR_CANJE,
      fecha_expira: fechaExpira,
      canje_id: canje.id,
    });
  } catch (e) {
    console.error("pedir-canje error:", e);
    await log("error", { fn: "pedir-canje", msg: e.message, body });
    return respond(500, { error: e.message });
  }
};
