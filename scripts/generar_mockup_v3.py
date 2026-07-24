"""Genera mockup V3 de Cotorreo Rewards — paleta amarillo/morado/turquesa."""
import json

with open(r'C:\Users\VICENT~1\AppData\Local\Temp\claude\C--Users-vicente-benitez2\9638ccb6-fcd5-4b92-b05b-dd6c7ef1c6e2\scratchpad\assets-mockup.json', encoding='utf-8') as f:
    a = json.load(f)

F = a['fotos']
L = a['logos']

CSS = """
:root {
  /* Paleta principal — trio balanceado */
  --violet-deep: #3b0764;
  --violet: #6b21a8;
  --violet-vivid: #7c3aed;
  --amber: #f59e0b;
  --amber-soft: #fde68a;
  --amber-deep: #b45309;
  --teal: #0d9488;
  --teal-soft: #99f6e4;
  --teal-vivid: #14b8a6;

  /* Neutros calidos (con tinte violeta muy sutil) */
  --cream: #faf7f4;
  --cream-warm: #f4efe8;
  --sand: #e6dfd5;
  --stone: #8f8577;
  --ink: #1e1435;
  --ink-soft: #5a4d70;
  --line: #d9d0c1;
}
@media (prefers-color-scheme: dark) {
  :root {
    --cream: #14101a;
    --cream-warm: #1a1524;
    --sand: #24202e;
    --stone: #6b6672;
    --ink: #f4efe8;
    --ink-soft: #b8b0c4;
    --line: #2a2536;
  }
}
:root[data-theme="light"] { --cream:#faf7f4; --cream-warm:#f4efe8; --sand:#e6dfd5; --stone:#8f8577; --ink:#1e1435; --ink-soft:#5a4d70; --line:#d9d0c1; }
:root[data-theme="dark"] { --cream:#14101a; --cream-warm:#1a1524; --sand:#24202e; --stone:#6b6672; --ink:#f4efe8; --ink-soft:#b8b0c4; --line:#2a2536; }

* { box-sizing: border-box; }
body {
  margin: 0; background: var(--cream); color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif;
  font-size: 15px; line-height: 1.5; -webkit-font-smoothing: antialiased;
}
.device { max-width: 420px; margin: 0 auto; background: var(--cream); min-height: 100vh; position: relative; box-shadow: 0 0 60px rgba(0,0,0,0.06); }

/* ============ TOP NAV ============ */
.top-nav {
  position: sticky; top: 0; z-index: 40; padding: 14px 20px 12px;
  background: color-mix(in srgb, var(--cream) 92%, transparent);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--line);
  display: flex; align-items: center; justify-content: space-between;
}
.brand-block { display: flex; align-items: center; gap: 10px; }
.grupo-mark {
  width: 40px; height: 40px; border-radius: 12px;
  background: linear-gradient(135deg, var(--violet) 0%, var(--violet-deep) 100%);
  display: grid; place-items: center;
  box-shadow: 0 2px 8px -2px rgba(107, 33, 168, 0.4);
}
.grupo-mark img { width: 26px; height: 26px; filter: brightness(0) invert(1); }
.brand-text { line-height: 1; font-size: 11px; letter-spacing: 0.16em; text-transform: uppercase; color: var(--stone); }
.brand-text b {
  display: block; font-family: Georgia, serif; font-size: 18px;
  letter-spacing: -0.01em; color: var(--ink); text-transform: none;
  font-weight: 400; margin-top: 3px;
}
.avatar {
  width: 40px; height: 40px; border-radius: 50%;
  background: var(--teal); color: white;
  display: grid; place-items: center;
  font-family: Georgia, serif; font-size: 17px;
  box-shadow: 0 2px 8px -2px rgba(13, 148, 136, 0.4);
}

/* ============ HERO ============ */
.hero {
  position: relative; margin: 16px 20px 0; padding: 24px 22px 26px;
  border-radius: 20px; overflow: hidden; color: white;
  background:
    linear-gradient(135deg, var(--violet-deep) 0%, var(--violet) 60%, var(--violet-vivid) 100%);
  box-shadow: 0 12px 32px -12px rgba(59, 7, 100, 0.5);
}
.hero::before {
  content: ''; position: absolute; inset: 0;
  background-image: url("__HERO__");
  background-size: cover; background-position: center;
  opacity: 0.12; mix-blend-mode: overlay;
}
.hero::after {
  content: ''; position: absolute;
  top: -60px; right: -60px;
  width: 200px; height: 200px; border-radius: 50%;
  background: var(--teal-vivid); opacity: 0.15;
  filter: blur(40px);
}
.hero-content { position: relative; z-index: 1; }
.greeting { font-size: 13px; opacity: 0.85; display: flex; align-items: center; gap: 6px; }
.greeting b { font-weight: 500; }
.card-numbers { display: flex; align-items: baseline; gap: 6px; margin-top: 14px; }
.big-n { font-family: Georgia, serif; font-size: 68px; line-height: 0.9; letter-spacing: -0.04em; }
.of-n { font-size: 15px; opacity: 0.75; margin-left: 4px; }
.sellos-bar { display: grid; grid-template-columns: repeat(20, 1fr); gap: 3px; margin-top: 16px; }
.sello-dot { height: 8px; border-radius: 4px; background: rgba(255,255,255,0.2); }
.sello-dot.on { background: var(--teal-vivid); box-shadow: 0 0 8px -2px var(--teal-vivid); }
.card-meta {
  display: flex; justify-content: space-between; align-items: center;
  margin-top: 14px; font-size: 12px; opacity: 0.85;
}
.card-meta .id {
  font-family: "SF Mono", "Cascadia Code", monospace;
  letter-spacing: 0.05em;
  padding: 3px 8px; background: rgba(255,255,255,0.1);
  border-radius: 6px; font-size: 11px;
}

/* ============ SECCION TITULO ============ */
.section-title {
  padding: 28px 20px 12px;
  display: flex; justify-content: space-between; align-items: baseline;
}
.section-title h2 {
  font-family: Georgia, serif; font-weight: 400; margin: 0;
  font-size: 21px; letter-spacing: -0.01em;
}
.section-title .link {
  font-size: 11px; text-transform: uppercase;
  letter-spacing: 0.14em; color: var(--violet);
  text-decoration: none; font-weight: 600;
}

/* ============ NEGOCIOS GRID ============ */
.negocios {
  padding: 0 20px; display: grid;
  grid-template-columns: repeat(3, 1fr); gap: 10px;
}
.negocio-card {
  aspect-ratio: 1; background: var(--cream-warm);
  border: 1px solid var(--line); border-radius: 14px;
  display: grid; place-items: center; padding: 12px;
  cursor: pointer; transition: all 0.2s;
}
.negocio-card:hover {
  border-color: var(--teal);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px -6px rgba(13, 148, 136, 0.25);
}
.negocio-card img { max-width: 88%; max-height: 88%; object-fit: contain; }

/* ============ MENU CAROUSEL ============ */
.menu-scroll {
  display: flex; gap: 12px; padding: 4px 20px 12px;
  overflow-x: auto; scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch; scrollbar-width: none;
}
.menu-scroll::-webkit-scrollbar { display: none; }
.menu-card {
  flex: 0 0 210px; scroll-snap-align: start;
  background: var(--cream-warm); border-radius: 16px;
  overflow: hidden; border: 1px solid var(--line);
  box-shadow: 0 4px 14px -4px rgba(30, 20, 53, 0.12);
  transition: all 0.2s; cursor: pointer;
}
.menu-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px -8px rgba(30, 20, 53, 0.2); }
.menu-card .img { aspect-ratio: 4/3; background-size: cover; background-position: center; }
.menu-card .body { padding: 12px 14px; }
.menu-card h3 { font-family: Georgia, serif; font-weight: 400; margin: 0; font-size: 15px; }
.menu-card .meta { display: flex; justify-content: space-between; align-items: baseline; margin-top: 6px; font-size: 11px; color: var(--ink-soft); }
.menu-card .meta .p {
  color: var(--violet); font-family: Georgia, serif;
  font-size: 15px; font-weight: 500;
}
.menu-card .tag {
  display: inline-block; margin-top: 4px;
  padding: 2px 8px; background: var(--teal-soft); color: var(--teal);
  font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em;
  font-weight: 600; border-radius: 999px;
}

/* ============ CANJE DESTACADO (amarillo) ============ */
.canje-card {
  margin: 4px 20px 20px; padding: 22px;
  background:
    radial-gradient(circle at top right, rgba(180, 83, 9, 0.12), transparent 60%),
    linear-gradient(135deg, #fef3c7 0%, #fbbf24 100%);
  border-radius: 20px; position: relative; overflow: hidden;
  box-shadow: 0 8px 28px -8px rgba(245, 158, 11, 0.45);
}
.canje-card::before {
  content: ''; position: absolute;
  top: -30px; right: -30px;
  width: 140px; height: 140px; border-radius: 50%;
  background: rgba(180, 83, 9, 0.08);
}
.canje-card .content { position: relative; z-index: 1; }
.canje-card .lbl {
  font-size: 10px; text-transform: uppercase;
  letter-spacing: 0.16em; color: #78350f;
  font-weight: 700;
}
.canje-card .amt {
  font-family: Georgia, serif; font-size: 40px;
  letter-spacing: -0.03em; color: #451a03;
  line-height: 1; margin-top: 8px;
}
.canje-card p {
  margin: 10px 0 16px; font-size: 13px; color: #78350f;
  max-width: 260px; line-height: 1.45;
}
.canje-card button {
  background: #1e1435; color: white;
  border: none; border-radius: 999px; padding: 12px 24px;
  font-size: 13px; font-weight: 600;
  letter-spacing: 0.02em; cursor: pointer;
  font-family: inherit;
  box-shadow: 0 4px 12px -2px rgba(30, 20, 53, 0.3);
}

/* ============ ACTIVITY ============ */
.activity { padding: 0 20px 12px; }
.activity-item {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 0; border-bottom: 1px solid var(--line);
}
.activity-item:last-child { border-bottom: none; }
.activity-item .ico {
  width: 42px; height: 42px; border-radius: 12px;
  display: grid; place-items: center; font-size: 20px;
  background: var(--sand);
}
.activity-item.plaza .ico { background: #fce7f3; }
.activity-item.padel .ico { background: var(--teal-soft); }
.activity-item.taqueria .ico { background: var(--amber-soft); }
.activity-item .body { flex: 1; min-width: 0; }
.activity-item .body h4 { margin: 0; font-size: 14px; font-weight: 500; }
.activity-item .body .sub { font-size: 12px; color: var(--stone); margin-top: 2px; }
.activity-item .amt {
  font-family: Georgia, serif;
  color: var(--teal); font-weight: 600; font-size: 16px;
}

/* ============ BOTTOM NAV ============ */
.bottom-nav {
  position: sticky; bottom: 0; background: var(--cream);
  border-top: 1px solid var(--line);
  display: grid; grid-template-columns: repeat(4, 1fr);
  padding: 8px 0 max(8px, env(safe-area-inset-bottom));
  z-index: 30;
}
.nav-item {
  display: grid; place-items: center; gap: 2px; padding: 8px 0;
  cursor: pointer; color: var(--stone);
  font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em;
  transition: color 0.15s;
}
.nav-item.active { color: var(--violet); }
.nav-item.active svg path { fill: var(--violet); }
.nav-item svg { width: 22px; height: 22px; fill: currentColor; }

/* ============ INTRO ============ */
.intro {
  max-width: 900px; margin: 40px auto 20px;
  padding: 20px; text-align: center;
}
.intro .label {
  color: var(--stone); font-size: 11px;
  text-transform: uppercase; letter-spacing: 0.16em;
}
.intro h1 {
  font-family: Georgia, serif; font-weight: 400;
  font-size: 34px; margin: 8px 0 6px; letter-spacing: -0.02em;
}
.intro h1 em { font-style: italic; color: var(--violet); }
.intro .palette-strip {
  display: inline-flex; gap: 8px; margin: 14px 0 8px;
  padding: 8px 14px; background: var(--cream-warm);
  border: 1px solid var(--line); border-radius: 999px;
}
.intro .swatch {
  width: 20px; height: 20px; border-radius: 50%;
  border: 2px solid var(--cream-warm);
  box-shadow: 0 1px 3px rgba(0,0,0,0.15);
}
.intro p { color: var(--ink-soft); max-width: 620px; margin: 10px auto 0; }
"""

CSS = CSS.replace("__HERO__", F['hero_local'])

def img(u): return f'<img src="{u}" />'
def bg(u): return f'style="background-image:url({u})"'

html = f"""<title>Cotorreo Rewards V3 · amarillo · morado · turquesa</title>
<style>{CSS}</style>

<div class="intro">
  <div class="label">Cotorreo Rewards · Rediseño V3</div>
  <h1>Menos verde, más <em>identidad</em>.</h1>
  <div class="palette-strip">
    <span class="swatch" style="background:#6b21a8" title="Morado"></span>
    <span class="swatch" style="background:#f59e0b" title="Amarillo"></span>
    <span class="swatch" style="background:#0d9488" title="Turquesa"></span>
  </div>
  <p>Trio balanceado: morado para el hero (premium), amarillo para canjes (llama a la acción), turquesa como accent fresco. El verde queda solo donde vive naturalmente — el logo. Después pasás las fotos del menú y las intercambio.</p>
</div>

<div class="device">
  <div class="top-nav">
    <div class="brand-block">
      <div class="grupo-mark"><img src="{L['grupo_vertical_blanco']}" /></div>
      <div class="brand-text">Grupo Cotorreo<b>Rewards</b></div>
    </div>
    <div class="avatar">V</div>
  </div>

  <div class="hero">
    <div class="hero-content">
      <div class="greeting">¡Hola <b>Vicente</b> 👋</div>
      <div class="card-numbers"><span class="big-n">12</span><span class="of-n">/ 20 sellos</span></div>
      <div class="sellos-bar" id="sellos-bar"></div>
      <div class="card-meta">
        <span>Faltan 8 para tu canje</span>
        <span class="id">RW-8394F</span>
      </div>
    </div>
  </div>

  <div class="section-title"><h2>Nuestros negocios</h2><a class="link" href="#">Ver todos</a></div>
  <div class="negocios">
    <div class="negocio-card">{img(L['cotorreo_plaza'])}</div>
    <div class="negocio-card">{img(L['cotorreo_taqueria'])}</div>
    <div class="negocio-card">{img(L['alpadel'])}</div>
    <div class="negocio-card">{img(L['bebros'])}</div>
    <div class="negocio-card">{img(L['pits'])}</div>
    <div class="negocio-card">{img(L['nube'])}</div>
  </div>

  <div class="section-title"><h2>Explorá el menú</h2><a class="link" href="#">Ver todo</a></div>
  <div class="menu-scroll">
    <div class="menu-card">
      <div class="img" {bg(F['plato_1'])}></div>
      <div class="body">
        <h3>Tacos al Pastor</h3>
        <div class="meta"><span>Plaza · Cocina</span><span class="p">₡4.900</span></div>
        <div class="tag">Lunes 2x1</div>
      </div>
    </div>
    <div class="menu-card">
      <div class="img" {bg(F['plato_2'])}></div>
      <div class="body">
        <h3>Quesabirrias</h3>
        <div class="meta"><span>Taquería</span><span class="p">₡5.000</span></div>
        <div class="tag">Miércoles 2x1</div>
      </div>
    </div>
    <div class="menu-card">
      <div class="img" {bg(F['bebida'])}></div>
      <div class="body">
        <h3>Bubble Tea Choco</h3>
        <div class="meta"><span>Bebidas</span><span class="p">₡3.500</span></div>
      </div>
    </div>
    <div class="menu-card">
      <div class="img" {bg(F['alpadel'])}></div>
      <div class="body">
        <h3>Cancha de Pádel</h3>
        <div class="meta"><span>Alpadel</span><span class="p">₡6.000/h</span></div>
      </div>
    </div>
  </div>

  <div class="section-title"><h2>Tu progreso</h2></div>
  <div class="canje-card">
    <div class="content">
      <span class="lbl">Próximo canje</span>
      <div class="amt">₡15.000</div>
      <p>Completá 8 sellos más para desbloquear tu crédito canjeable en cualquier negocio del grupo.</p>
      <button>Ver detalle</button>
    </div>
  </div>

  <div class="section-title"><h2>Última actividad</h2><a class="link" href="#">Historial</a></div>
  <div class="activity">
    <div class="activity-item plaza">
      <div class="ico">🌮</div>
      <div class="body"><h4>Plaza Cotorreo</h4><div class="sub">Hoy · ₡25.000</div></div>
      <div class="amt">+2</div>
    </div>
    <div class="activity-item padel">
      <div class="ico">🎾</div>
      <div class="body"><h4>Alpadel</h4><div class="sub">Ayer · ₡12.000</div></div>
      <div class="amt">+1</div>
    </div>
    <div class="activity-item taqueria">
      <div class="ico">🍹</div>
      <div class="body"><h4>Cotorreo Taquería</h4><div class="sub">Sáb · ₡18.000</div></div>
      <div class="amt">+1</div>
    </div>
  </div>

  <div class="bottom-nav">
    <div class="nav-item active"><svg viewBox="0 0 24 24"><path d="M12 2L2 9v13h6v-7h8v7h6V9L12 2z"/></svg>Inicio</div>
    <div class="nav-item"><svg viewBox="0 0 24 24"><path d="M8.1 13.34l2.83-2.83L3.91 3.5c-1.56 1.56-1.56 4.09 0 5.66l4.19 4.18zm6.78-1.81c1.53.71 3.68.21 5.27-1.38 1.91-1.91 2.28-4.65.81-6.12-1.46-1.46-4.20-1.10-6.12.81-1.59 1.59-2.09 3.74-1.38 5.27L3.7 19.87l1.41 1.41L12 14.41l6.88 6.88 1.41-1.41L13.41 13l1.47-1.47z"/></svg>Menú</div>
    <div class="nav-item"><svg viewBox="0 0 24 24"><path d="M20 6h-2.18c.11-.31.18-.65.18-1 0-1.66-1.34-3-3-3-1.05 0-1.96.54-2.5 1.35l-.5.67-.5-.68C10.96 2.54 10.05 2 9 2 7.34 2 6 3.34 6 5c0 .35.07.69.18 1H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-5-2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM9 4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm11 15H4v-2h16v2zm0-5H4V8h5.08L7 10.83 8.62 12 11 8.76l1-1.36 1 1.36L15.38 12 17 10.83 14.92 8H20v6z"/></svg>Canjear</div>
    <div class="nav-item"><svg viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>Cuenta</div>
  </div>
</div>

<script>
  const bar = document.getElementById('sellos-bar');
  for (let i = 0; i < 20; i++) {{
    const d = document.createElement('div');
    d.className = 'sello-dot' + (i < 12 ? ' on' : '');
    bar.appendChild(d);
  }}
</script>
"""

path = r'C:\Users\VICENT~1\AppData\Local\Temp\claude\C--Users-vicente-benitez2\9638ccb6-fcd5-4b92-b05b-dd6c7ef1c6e2\scratchpad\rewards-v3.html'
with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'V3 generado: {len(html)//1024}KB en {path}')
