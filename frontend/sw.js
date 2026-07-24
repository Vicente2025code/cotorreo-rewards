// Service Worker minimo para Cotorreo Rewards PWA
// Estrategia: network-first para HTML y API, cache-first para assets estáticos.

const CACHE_NAME = "cotorreo-rewards-v1";
const STATIC_ASSETS = [
  "/",
  "/index.html",
  "/manifest.json",
  "/assets/icon-192.png",
  "/assets/icon-512.png",
  "/assets/apple-touch-icon.png",
  "/assets/logo-horizontal.svg",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  // API: siempre red, sin cache
  if (url.pathname.startsWith("/api/")) {
    return;
  }

  // Assets estáticos (icons, logos): cache-first
  if (url.pathname.startsWith("/assets/") || url.pathname === "/manifest.json") {
    event.respondWith(
      caches.match(event.request).then((cached) => cached || fetch(event.request))
    );
    return;
  }

  // HTML: network-first con fallback a cache
  event.respondWith(
    fetch(event.request)
      .then((resp) => {
        // Guardar en cache la respuesta exitosa
        if (resp.ok) {
          const clone = resp.clone();
          caches.open(CACHE_NAME).then((c) => c.put(event.request, clone));
        }
        return resp;
      })
      .catch(() => caches.match(event.request))
  );
});
