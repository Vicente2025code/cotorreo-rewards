// POST /api/login-or-register
// Body: { telefono, nombre?, email?, cumpleanos?, origen? }
//
// Si el miembro existe (por telefono) devuelve sus datos.
// Si no existe, lo crea y devuelve los datos + info que es nuevo.

const { buscarMiembroPorTelefono, crearMiembro, normalizarTelefono, log } = require("./_lib_airtable");
const { sendSessionMessage } = require("./_lib_wati");

function ok(body) {
  return {
    statusCode: 200,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
    body: JSON.stringify(body),
  };
}

function fail(code, msg) {
  return {
    statusCode: code,
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
    body: JSON.stringify({ error: msg }),
  };
}

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") return ok({});
  if (event.httpMethod !== "POST") return fail(405, "Method not allowed");

  let body;
  try { body = JSON.parse(event.body || "{}"); }
  catch { return fail(400, "Body inválido"); }

  const telefono = normalizarTelefono(body.telefono);
  if (!telefono) return fail(400, "Teléfono requerido");

  try {
    let miembro = await buscarMiembroPorTelefono(telefono);
    let nuevo = false;

    if (!miembro) {
      // Crear nuevo
      if (!body.nombre || !body.nombre.trim()) {
        return fail(400, "Nombre requerido para nuevo registro");
      }
      miembro = await crearMiembro({
        telefono,
        nombre: body.nombre,
        email: body.email,
        cumpleanos: body.cumpleanos,
        origen: body.origen || "web",
      });
      nuevo = true;

      // Log evento
      await log("miembro_creado", { telefono, origen: body.origen }, miembro.id);

      // Bienvenida via WATI (session)
      await sendSessionMessage(telefono,
        `¡Bienvenido a Cotorreo Rewards ${body.nombre.split(" ")[0]}! 🎉\n\n` +
        `Ya sos parte del programa. Por cada ₡10.000 en cualquiera de nuestros negocios ` +
        `ganás 1 sello, y con 20 sellos tenés ₡15.000 de crédito.\n\n` +
        `Podés ver tu estado en rewards.grupocotorreo.com`
      );
    }

    // Respuesta
    return ok({
      ok: true,
      nuevo,
      miembro: {
        id: miembro.id,
        id_corto: miembro.fields.id_corto,
        telefono: miembro.fields.telefono,
        nombre: miembro.fields.nombre,
        email: miembro.fields.email || null,
        sellos_actuales: miembro.fields.sellos_actuales || 0,
        sellos_historicos: miembro.fields.sellos_historicos || 0,
        canje_disponible: !!miembro.fields.canje_disponible,
      },
    });
  } catch (e) {
    console.error("login-or-register error:", e);
    return fail(500, e.message);
  }
};
