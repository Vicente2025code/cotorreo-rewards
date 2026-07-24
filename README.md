# Cotorreo Rewards

Sistema propio de programa de lealtad para Grupo Cotorreo — reemplaza Loopy Loyalty.

## Alcance

- **6 negocios**: Plaza Cotorreo, Cotorreo Taquería (Plaza Encuentro), Alpadel, Bebros, y 2 más
- **Regla**: ₡10.000 gastados = 1 sello · 20 sellos = ₡15.000 crédito
- **Idioma**: Español CR (voseo)
- **URL cliente**: rewards.grupocotorreo.com
- **Base**: Airtable + Netlify Functions + WATI bot integración

## Stack

- **Frontend**: HTML + React vía CDN (mismo patrón que mundial.grupocotorreo.com)
- **Backend**: Netlify Functions (Node.js)
- **DB**: Airtable
- **Notificaciones**: WATI bot existente
- **Wallet**: Apple Wallet (PassKit) + Google Wallet
- **Deploy**: Netlify

## Plan de desarrollo

### Fase 1 — Núcleo (esta semana)
- [x] Estructura carpetas
- [ ] Schema Airtable + doc
- [ ] Netlify functions base
- [ ] Frontend cliente básico (ver sellos)
- [ ] Frontend cajero (sumar sellos)

### Fase 2 — Canjes
- [ ] Flujo de canje (cliente pide → código único → cajero valida)
- [ ] Historial de canjes

### Fase 3 — Notificaciones automáticas
- [ ] Integración con bot WATI existente
- [ ] Notificación al llegar a 20 sellos
- [ ] Recordatorios de canjes disponibles
- [ ] Notificación cumpleaños con sello regalo

### Fase 4 — Wallet passes
- [ ] Apple Wallet (PassKit)
- [ ] Google Wallet
- [ ] Auto-update al ganar/canjear sellos

### Fase 5 — Migración Loopy
- [ ] Export CSV desde Loopy
- [ ] Importar clientes existentes (100-300)
- [ ] Comunicación a clientes del cambio

### Fase 6 — Deploy prod
- [ ] Netlify config
- [ ] Domain rewards.grupocotorreo.com
- [ ] Testing con equipo

## Ahorro esperado

- Loopy Loyalty actual: $50-150 USD/mes = ~$1,200/año
- Nuevo sistema: $0/mes extra (Airtable + Netlify free tier alcanza)
- **Ahorro anual**: ~$1,200 USD 💰

## Estructura del repo

```
cotorreo-rewards/
├── frontend/
│   ├── index.html              # App cliente (ver sellos)
│   ├── cajero.html             # App cajero (sumar sellos, validar canjes)
│   ├── admin.html              # Panel Mariela (opcional)
│   ├── assets/                 # Logos, imágenes
│   └── netlify/
│       └── functions/          # Backend API
│           ├── login-or-register.js
│           ├── sumar-sellos.js
│           ├── get-mis-sellos.js
│           ├── pedir-canje.js
│           ├── validar-canje.js
│           ├── _lib_airtable.js
│           └── _lib_wati.js
├── docs/
│   ├── schema_airtable.md      # Estructura de tablas
│   └── flujos.md               # Diagramas de flujos
├── scripts/                    # Scripts one-off (migración Loopy, etc)
└── data/                       # Data local (CSVs)
```
