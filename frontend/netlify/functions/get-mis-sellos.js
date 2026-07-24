// GET /api/get-mis-sellos?telefono=50672882394
// Devuelve el estado actual del miembro + historial reciente.

const { at, buscarMiembroPorTelefono, normalizarTelefono } = require("./_lib_airtable");

function respond(code, body) {
  return {
    statusCode: code,
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
    body: JSON.stringify(body),
  };
}

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") return respond(200, {});

  const telefono = normalizarTelefono(event.queryStringParameters?.telefono);
  if (!telefono) return respond(400, { error: "Teléfono requerido" });

  try {
    const miembro = await buscarMiembroPorTelefono(telefono);
    if (!miembro) return respond(404, { error: "Miembro no encontrado" });

    // Historial ultimas 10 transacciones
    // ARRAYJOIN({miembro}) devuelve el primary field (telefono) del link, no el id
    const transR = await at.get("Transacciones", {
      filterByFormula: `FIND('${telefono}', ARRAYJOIN({miembro}))`,
      sort: [{ field: "fecha_compra", direction: "desc" }],
      maxRecords: 10,
    });
    const transacciones = (transR?.records || []).map(r => ({
      id_corto: r.fields.id_corto,
      fecha: r.fields.fecha_compra,
      monto: r.fields.monto_colones,
      sellos: r.fields.sellos_ganados,
      negocio: r.fields.negocio,
    }));

    // Ultimos 5 canjes
    const canjR = await at.get("Canjes", {
      filterByFormula: `FIND('${telefono}', ARRAYJOIN({miembro}))`,
      sort: [{ field: "id_corto", direction: "desc" }],
      maxRecords: 5,
    });
    const canjes = (canjR?.records || []).map(r => ({
      id_corto: r.fields.id_corto,
      codigo: r.fields.codigo_canje,
      valor: r.fields.valor_credito,
      estado: r.fields.estado,
      fecha_uso: r.fields.fecha_uso || null,
      fecha_expira: r.fields.fecha_expira || null,
      negocio_uso: r.fields.negocio_uso || null,
    }));

    return respond(200, {
      ok: true,
      miembro: {
        id: miembro.id,
        id_corto: miembro.fields.id_corto,
        nombre: miembro.fields.nombre,
        telefono: miembro.fields.telefono,
        sellos_actuales: miembro.fields.sellos_actuales || 0,
        sellos_historicos: miembro.fields.sellos_historicos || 0,
        sellos_canjeados: miembro.fields.sellos_canjeados || 0,
        canje_disponible: !!miembro.fields.canje_disponible,
        cumpleanos: miembro.fields.cumpleanos || null,
      },
      transacciones,
      canjes,
    });
  } catch (e) {
    console.error("get-mis-sellos error:", e);
    return respond(500, { error: e.message });
  }
};
