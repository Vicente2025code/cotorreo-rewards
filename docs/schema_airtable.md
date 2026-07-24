# Schema Airtable — Cotorreo Rewards

Base: **Cotorreo Rewards** (nueva) o reutilizamos alguna existente. Recomendado crearla nueva para aislar.

## Tabla 1: `Miembros`

Un registro por cliente inscrito en Rewards.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_corto` | Formula | ID legible tipo `RW-{RECORD_ID last 5}` |
| `telefono` | Single line text | WhatsApp normalizado (`50672882394` sin +) — LLAVE ÚNICA |
| `nombre` | Single line text | Nombre del cliente |
| `email` | Email | Opcional, para wallet passes Apple/Google |
| `cumpleanos` | Date | Para sello regalo el día del cumple |
| `fecha_registro` | Created time | Fecha de inscripción al programa |
| `origen_registro` | Single select | `web`, `cajero`, `migracion_loopy`, `bot_whatsapp` |
| `sellos_actuales` | Rollup | Suma sellos activos (no canjeados) desde tabla `Transacciones` |
| `sellos_historicos` | Rollup | Total sellos ganados en toda la historia |
| `canjes_hechos` | Rollup | Total canjes completados |
| `credito_disponible` | Rollup | Suma créditos otorgados no usados |
| `credito_usado` | Rollup | Créditos ya redimidos |
| `wallet_pass_id` | Single line text | ID único del wallet pass (Apple/Google) |
| `activo` | Checkbox | true por default. false si opt-out |
| `notas_admin` | Long text | Notas manuales para casos especiales |

## Tabla 2: `Transacciones`

Un registro por cada compra que gana sellos.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_corto` | Formula | `TX-{fecha_YYYYMMDD}-{RECORD_ID last 4}` |
| `miembro` | Link → Miembros | Cliente que hizo la compra |
| `fecha_compra` | Date | Cuándo se registró la compra |
| `monto_colones` | Number | Monto de la compra en ₡ |
| `sellos_ganados` | Formula | `FLOOR(monto_colones / 10000)` — 1 sello por cada 10k |
| `negocio` | Single select | `plaza_cotorreo`, `cotorreo_taqueria`, `alpadel`, `bebros`, `otro_1`, `otro_2` |
| `cajero` | Single line text | Nombre del que registró (Mariela, Lili, etc.) |
| `metodo_registro` | Single select | `qr_scan`, `manual_telefono`, `import_csv` |
| `notas` | Long text | Opcional |

## Tabla 3: `Canjes`

Un registro por cada canje pedido/hecho.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_corto` | Formula | `CJ-{RECORD_ID last 5}` |
| `miembro` | Link → Miembros | Cliente que canjea |
| `codigo_canje` | Single line text | Código único 6 dígitos que muestra el cliente |
| `fecha_solicitud` | Created time | Cuándo el cliente pidió el canje |
| `fecha_uso` | Date | Cuándo el cajero validó (null si no usado) |
| `valor_credito` | Number | Valor del canje en ₡ (por default 15000) |
| `sellos_gastados` | Number | Cuántos sellos consumió (por default 20) |
| `estado` | Single select | `pendiente`, `usado`, `expirado`, `cancelado` |
| `negocio_uso` | Single select | Donde se redimió (mismo enum que Transacciones) |
| `cajero_valido` | Single line text | Quién validó el código |
| `fecha_expira` | Date | Códigos expiran a los 30 días |

## Tabla 4: `EventosLog`

Auditoría de todo lo que pasa.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_corto` | Autonumber | ID |
| `fecha` | Created time | Cuándo |
| `tipo_evento` | Single select | `miembro_creado`, `sellos_sumados`, `canje_solicitado`, `canje_validado`, `canje_expirado`, `notif_wati_enviada`, `error`, `otro` |
| `miembro` | Link → Miembros | Miembro afectado (opcional) |
| `payload_json` | Long text | JSON con detalles del evento |

## Views útiles

### En `Miembros`:
- **Todos activos**: `activo = true`
- **Con 20+ sellos** (canje disponible): `sellos_actuales >= 20`
- **Cumples del mes**: filtro por mes actual
- **Migración Loopy**: `origen_registro = 'migracion_loopy'`

### En `Canjes`:
- **Pendientes**: `estado = 'pendiente'`
- **Por expirar** (últimos 5 días): filtro por fecha_expira
- **Últimos usados**: sort por fecha_uso DESC

## Setup inicial

1. Crear base **Cotorreo Rewards** en Airtable
2. Crear las 4 tablas con los campos de arriba
3. Configurar las views
4. Guardar API key + base_id como env vars:
   - `AIRTABLE_TOKEN`
   - `AIRTABLE_REWARDS_BASE_ID`
