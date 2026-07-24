// Helper WATI para Cotorreo Rewards - envío de mensajes session
// Requiere env var: WATI_TOKEN

const WATI_ENDPOINT = "https://live-mt-server.wati.io";
const TENANT_ID = "1085608";
const CHANNEL_PHONE = "50683436583";

const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
           "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36";

function normalizeNumber(tel) {
  const d = String(tel || "").replace(/\D/g, "");
  if (!d) return "";
  if (d.length === 8) return "506" + d;
  return d;
}

/**
 * Envia mensaje session (texto plano). Requiere ventana 24h abierta.
 */
async function sendSessionMessage(to, message) {
  const token = process.env.WATI_TOKEN;
  if (!token) {
    console.log("WATI_TOKEN faltante, skip envio");
    return { ok: false, error: "no_token" };
  }
  const num = normalizeNumber(to);
  if (!num) return { ok: false, error: "invalid_number" };

  const endpoint = `${WATI_ENDPOINT}/${TENANT_ID}/api/v1/sendSessionMessage/${num}`;
  const payload = new URLSearchParams({
    messageText: String(message || "").trim(),
    channelPhoneNumber: CHANNEL_PHONE,
  });

  try {
    const r = await fetch(endpoint, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": UA,
      },
      body: payload.toString(),
    });
    const text = await r.text();
    return { ok: r.ok, status: r.status, body: text.slice(0, 200) };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

/**
 * Envia template Marketing (funciona fuera de ventana 24h).
 */
async function sendTemplate(to, templateName, params = []) {
  const token = process.env.WATI_TOKEN;
  if (!token) return { ok: false, error: "no_token" };
  const num = normalizeNumber(to);
  if (!num) return { ok: false, error: "invalid_number" };

  const endpoint = `${WATI_ENDPOINT}/${TENANT_ID}/api/v1/sendTemplateMessage?whatsappNumber=${num}`;
  const parameters = params.map((v, i) => ({ name: String(i + 1), value: String(v) }));

  try {
    const r = await fetch(endpoint, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
        "User-Agent": UA,
      },
      body: JSON.stringify({
        template_name: templateName,
        broadcast_name: `rewards_${templateName}_${Date.now()}`,
        parameters,
      }),
    });
    const text = await r.text();
    return { ok: r.ok, status: r.status, body: text.slice(0, 200) };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

module.exports = { sendSessionMessage, sendTemplate, normalizeNumber };
