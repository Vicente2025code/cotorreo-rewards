// POST /api/sumar-sellos
// Endpoint del cajero. Registra compra + suma sellos + notifica si llega a 20.
//
// Body: { telefono, monto, negocio, cajero?, metodo?, notas? }
// Header: x-admin-token: <ADMIN_TOKEN>
//
// Response: { miembro, transaccion, sellos_ganados, sellos_actuales, canje_disponible, era_umbral }

const {
  buscarMiembroPorTelefono, crearMiembro, registrarTransaccion,
  recargarMiembro, normalizarTelefono, log
} = require("./_lib_airtable");
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

  const telefono = normalizarTelefono(body.telefono);
  const monto = Number(body.monto);
  const negocio = body.negocio;
  const cajero = body.cajero || "";

  if (!telefono) return respond(400, { error: "Teléfono requerido" });
  if (!Number.isFinite(monto) || monto <= 0) return respond(400, { error: "Monto inválido" });
  if (!negocio) return respond(400, { error: "Negocio requerido" });

  const NEGOCIOS_VALIDOS = ["plaza_cotorreo", "cotorreo_taqueria", "alpadel", "bebros", "otro_1", "otro_2"];
  if (!NEGOCIOS_VALIDOS.includes(negocio)) {
    return respond(400, { error: `Negocio inválido. Válidos: ${NEGOCIOS_VALIDOS.join(", ")}` });
  }

  try {
    // 1. Buscar o crear miembro (con nombre "Cliente" si no está registrado — cajero completa después)
    let miembro = await buscarMiembroPorTelefono(telefono);
    let creado = false;
    if (!miembro) {
      miembro = await crearMiembro({
        telefono,
        nombre: body.nombre || "Cliente",
        origen: "cajero",
      });
      creado = true;
      await log("miembro_creado", { telefono, via: "cajero_sumar_sellos", cajero }, miembro.id);
    }

    // Snapshot sellos antes
    const sellosAntes = Number(miembro.fields.sellos_actuales || 0);

    // 2. Crear la transacción
    const tx = await registrarTransaccion({
      miembroId: miembro.id,
      monto,
      negocio,
      cajero,
      metodoRegistro: body.metodo || "manual_telefono",
      notas: body.notas,
    });
    const sellosGanados = Number(tx.fields.sellos_ganados || 0);

    // 3. Recargar miembro para tomar el rollup actualizado
    // (Los rollups en Airtable pueden tardar 1-2s en recalcular)
    await new Promise(r => setTimeout(r, 1500));
    const miembroActualizado = await recargarMiembro(miembro.id);
    const sellosDespues = Number(miembroActualizado.fields.sellos_actuales || 0);
    const canjeDisponible = !!miembroActualizado.fields.canje_disponible;

    // Detectar si cruzó el umbral de 20 (antes < 20, ahora >= 20)
    const eraUmbral = sellosAntes < 20 && sellosDespues >= 20;

    // 4. Log evento
    await log("sellos_sumados", {
      telefono, monto, sellosGanados, sellosDespues, negocio, cajero, eraUmbral
    }, miembro.id);

    // 5. Notificar por WATI
    const nombre = (miembroActualizado.fields.nombre || "").split(" ")[0] || "amigo";
    if (creado) {
      // Mensaje bienvenida + primeros sellos
      await sendSessionMessage(telefono,
        `¡Bienvenido a Cotorreo Rewards ${nombre}! 🎉\n\n` +
        `Acabás de ganar tus primeros *${sellosGanados} sellos* por tu compra de ₡${monto.toLocaleString("es-CR")}.\n\n` +
        `Con 20 sellos ganás ₡15.000 de crédito. ¡Seguí acumulando!`
      );
    } else if (eraUmbral) {
      // ¡Canje ganado!
      await sendSessionMessage(telefono,
        `🎉 ¡${nombre}, ganaste un canje de ₡15.000!\n\n` +
        `Ya llegaste a 20 sellos. Para canjearlo, escribí *canje* al bot y te doy el código.\n\n` +
        `Válido en cualquier negocio de Grupo Cotorreo.`
      );
    } else if (sellosGanados > 0) {
      // Sumaste sellos pero no umbral
      await sendSessionMessage(telefono,
        `¡Sumaste *${sellosGanados} sellos* ${nombre}! 🎯\n\n` +
        `Tenés ${sellosDespues} de 20. ${20 - sellosDespues} más y ganás ₡15.000 de crédito.`
      );
    }

    return respond(200, {
      ok: true,
      miembro: {
        id: miembroActualizado.id,
        id_corto: miembroActualizado.fields.id_corto,
        nombre: miembroActualizado.fields.nombre,
        telefono: miembroActualizado.fields.telefono,
      },
      transaccion: {
        id: tx.id,
        id_corto: tx.fields.id_corto,
      },
      sellos_ganados: sellosGanados,
      sellos_actuales: sellosDespues,
      canje_disponible: canjeDisponible,
      era_umbral: eraUmbral,
      miembro_creado: creado,
    });
  } catch (e) {
    console.error("sumar-sellos error:", e);
    await log("error", { fn: "sumar-sellos", msg: e.message, body });
    return respond(500, { error: e.message });
  }
};
