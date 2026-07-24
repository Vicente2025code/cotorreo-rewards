// GET /api/buscar-miembro?telefono=XXX
// Endpoint del cajero — busca info rapida de un miembro para verificar antes de sumar sellos.
// Header: x-admin-token: <ADMIN_TOKEN>

const { buscarMiembroPorTelefono, normalizarTelefono } = require("./_lib_airtable");

function respond(code, body) {
  return {
    statusCode: code,
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
    body: JSON.stringify(body),
  };
}

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") return respond(200, {});

  const providedToken = event.headers?.["x-admin-token"] || event.headers?.["X-Admin-Token"];
  const expected = process.env.REWARDS_ADMIN_TOKEN || "MAR2103-rewards";
  if (providedToken !== expected) return respond(401, { error: "Unauthorized" });

  const telefono = normalizarTelefono(event.queryStringParameters?.telefono);
  if (!telefono) return respond(400, { error: "Teléfono requerido" });

  try {
    const miembro = await buscarMiembroPorTelefono(telefono);
    if (!miembro) {
      return respond(200, {
        ok: true,
        existe: false,
        telefono,
        mensaje: "Miembro no existe todavía. Se creará al sumar los primeros sellos.",
      });
    }

    return respond(200, {
      ok: true,
      existe: true,
      miembro: {
        id: miembro.id,
        id_corto: miembro.fields.id_corto,
        nombre: miembro.fields.nombre,
        telefono: miembro.fields.telefono,
        sellos_actuales: miembro.fields.sellos_actuales || 0,
        canje_disponible: !!miembro.fields.canje_disponible,
        activo: !!miembro.fields.activo,
      },
    });
  } catch (e) {
    console.error("buscar-miembro error:", e);
    return respond(500, { error: e.message });
  }
};
