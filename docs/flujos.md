# Flujos operativos — Cotorreo Rewards

## Flujo 1: Registro de nuevo cliente

**Opción A: Cajero registra en el momento**
```
Cliente pide pagar en Plaza Cotorreo
    ↓
Cajero: "¿Sos parte de Cotorreo Rewards?"
    ↓
Cliente: "No"
    ↓
Cajero abre cajero.html en tablet/celular
    ↓
Pone teléfono + nombre → click "Crear miembro"
    ↓
Netlify function: crea registro en Miembros
    ↓
Genera wallet pass (Apple/Google)
    ↓
Envía WATI: "¡Bienvenido a Cotorreo Rewards Juan! Tenés 0 sellos"
    ↓
Mensaje incluye link para agregar tarjeta al wallet
    ↓
Cliente agrega tarjeta al celular
    ↓
Cajero suma sellos por la compra actual
```

**Opción B: Cliente se auto-registra**
```
Cliente ve poster en Plaza con QR "Únete a Rewards"
    ↓
Escanea → rewards.grupocotorreo.com
    ↓
Formulario: teléfono + nombre + email + cumpleaños
    ↓
Recibe WATI con wallet pass
    ↓
En próxima compra, muestra QR al cajero
```

## Flujo 2: Sumar sellos por compra

```
Cliente paga en cualquier negocio
    ↓
Cliente muestra QR de su wallet (tiene su teléfono codificado)
    ↓
Cajero escanea con app cajero.html en su celular
    O
Cajero escribe teléfono manual
    ↓
Cajero pone monto de la compra (ej: ₡25000)
    ↓
Cajero selecciona negocio (auto-preseteado según sede)
    ↓
Click "Sumar sellos"
    ↓
Netlify: calcula sellos = FLOOR(25000/10000) = 2 sellos
    ↓
Crea registro en Transacciones
    ↓
Actualiza sellos_actuales del miembro
    ↓
Si sellos_actuales llega a 20 → dispara notificación WATI
    ↓
Actualiza wallet pass del cliente (aparece con sellos nuevos)
```

## Flujo 3: Canje

```
Cliente completa 20 sellos
    ↓
Bot WATI le manda: "¡Ganaste canje de ₡15.000! Pedilo escribiendo /canje"
    ↓
Cliente escribe "/canje" al bot
    ↓
Bot llama a función pedir-canje
    ↓
Genera código único de 6 dígitos (ej: 384501)
    ↓
Crea registro en Canjes (estado=pendiente, expira 30 días)
    ↓
Descuenta 20 sellos del miembro
    ↓
Bot manda: "Tu código es 384501. Mostralo al cajero. Vale ₡15.000"
    ↓
Cliente va a cualquier negocio
    ↓
Cajero abre app cajero.html → pestaña "Validar canje"
    ↓
Pone código 384501 + monto de la cuenta
    ↓
Sistema valida: código existe, no usado, no expirado
    ↓
Marca canje como usado
    ↓
Cliente paga (₡monto_total - ₡15.000)
```

## Flujo 4: Notificaciones automáticas

**Trigger: sellos_actuales >= 20**
- Enviar 1 sola vez cuando cruza el umbral
- Bot WATI: "¡Ganaste canje de ₡15.000!"

**Trigger: cumpleaños**
- Diario 9 AM CR, cron en n8n
- Busca miembros con cumpleaños hoy
- Suma sello regalo + WATI: "Feliz cumple! Te regalamos 1 sello"

**Trigger: canje por expirar (últimos 3 días)**
- Diario 10 AM CR
- WATI: "Tu canje 384501 vence en X días. Vení a usarlo"

**Trigger: sin actividad 60 días**
- Semanal (opcional)
- WATI: "Te extrañamos! Aún tenés X sellos esperando"

## Flujo 5: Migración desde Loopy

```
Vicente/Mariela exporta desde Loopy: CSV con {telefono, nombre, sellos_actuales}
    ↓
Script Python: scripts/importar_loopy.py
    ↓
Por cada línea:
    - Crear miembro en Airtable (origen_registro='migracion_loopy')
    - Crear transacción especial (metodo_registro='import_csv', sellos_ganados=X)
    ↓
Al terminar, mandar comunicado masivo por WATI:
    "Nuevo Cotorreo Rewards! Tus sellos ya migraron. Ver aquí: rewards.grupocotorreo.com/mi-cuenta?t={telefono}"
    ↓
Cliente entra → ve sus sellos migrados → agrega wallet pass
```

## Roles / permisos

- **Cliente**: ver sus sellos, pedir canje, actualizar datos personales
- **Cajero**: sumar sellos, validar canjes, buscar cliente por teléfono
- **Admin (Mariela/Vicente)**: todo lo anterior + editar miembros, ver reportes, corregir errores manualmente

## Endpoints Netlify Functions (planificados)

| Endpoint | Método | Descripción | Auth |
|---|---|---|---|
| `/api/login-or-register` | POST | Crear o loguear miembro por teléfono | OTP WATI |
| `/api/get-mis-sellos` | GET | Ver sellos del miembro actual | JWT |
| `/api/sumar-sellos` | POST | Cajero suma sellos por compra | ADMIN_TOKEN |
| `/api/buscar-miembro` | GET | Buscar por teléfono (cajero) | ADMIN_TOKEN |
| `/api/pedir-canje` | POST | Cliente pide canje | JWT |
| `/api/validar-canje` | POST | Cajero valida código | ADMIN_TOKEN |
| `/api/get-canjes` | GET | Historial canjes del miembro | JWT |
| `/api/generar-wallet-pass` | GET | Genera Apple/Google wallet pass | JWT |
| `/api/webhook-notif` | POST | Trigger interno de notificaciones WATI | INTERNAL_TOKEN |
| `/api/admin-reporte` | GET | Métricas para Mariela | ADMIN_TOKEN |
