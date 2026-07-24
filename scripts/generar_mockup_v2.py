"""Genera el mockup V2 pro de Cotorreo Rewards con fotos y logos reales."""
import json

with open(r'C:\Users\VICENT~1\AppData\Local\Temp\claude\C--Users-vicente-benitez2\9638ccb6-fcd5-4b92-b05b-dd6c7ef1c6e2\scratchpad\assets-mockup.json', encoding='utf-8') as f:
    a = json.load(f)

F = a['fotos']
L = a['logos']

CSS = """
:root {
  --green: #059669; --green-dark: #047857; --green-deep: #064e3b;
  --cream: #faf7f0; --cream-warm: #f5efe0; --sand: #e8e2d5;
  --stone: #a8a196; --ink: #0f1d18; --ink-soft: #4a5c55;
  --line: #ded7c5; --amber: #d97706;
}
@media (prefers-color-scheme: dark) {
  :root { --cream:#0f1210; --cream-warm:#16191a; --sand:#1f2422; --stone:#6b6960; --ink:#f5efe0; --ink-soft:#b8b09f; --line:#2a2f2b; }
}
:root[data-theme="light"] { --cream:#faf7f0; --cream-warm:#f5efe0; --sand:#e8e2d5; --stone:#a8a196; --ink:#0f1d18; --ink-soft:#4a5c55; --line:#ded7c5; }
:root[data-theme="dark"] { --cream:#0f1210; --cream-warm:#16191a; --sand:#1f2422; --stone:#6b6960; --ink:#f5efe0; --ink-soft:#b8b09f; --line:#2a2f2b; }

* { box-sizing: border-box; }
body { margin: 0; background: var(--cream); color: var(--ink); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif; font-size: 15px; line-height: 1.5; -webkit-font-smoothing: antialiased; }
.device { max-width: 420px; margin: 0 auto; background: var(--cream); min-height: 100vh; position: relative; box-shadow: 0 0 60px rgba(0,0,0,0.05); }

.top-nav { position: sticky; top: 0; z-index: 40; padding: 14px 20px 12px; background: color-mix(in srgb, var(--cream) 92%, transparent); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-bottom: 1px solid var(--line); display: flex; align-items: center; justify-content: space-between; }
.brand-block { display: flex; align-items: center; gap: 10px; }
.grupo-mark { width: 40px; height: 40px; border-radius: 50%; background: var(--green); display: grid; place-items: center; }
.grupo-mark img { width: 26px; height: 26px; }
.brand-text { line-height: 1; font-size: 11px; letter-spacing: 0.16em; text-transform: uppercase; color: var(--stone); }
.brand-text b { display: block; font-family: Georgia, serif; font-size: 18px; letter-spacing: -0.01em; color: var(--ink); text-transform: none; font-weight: 400; margin-top: 3px; }
.avatar { width: 38px; height: 38px; border-radius: 50%; background: var(--sand); display: grid; place-items: center; font-family: Georgia, serif; font-size: 16px; color: var(--green-deep); }

.hero { position: relative; padding: 22px 20px 28px; background: linear-gradient(135deg, var(--green-deep) 0%, var(--green) 55%, var(--green-dark) 100%); color: white; overflow: hidden; }
.hero::before { content: ''; position: absolute; inset: 0; background-image: url("__HERO__"); background-size: cover; background-position: center; opacity: 0.18; mix-blend-mode: overlay; }
.hero-content { position: relative; z-index: 1; }
.greeting { font-size: 13px; opacity: 0.85; }
.greeting b { font-weight: 500; }
.card-numbers { display: flex; align-items: baseline; gap: 6px; margin-top: 14px; }
.big-n { font-family: Georgia, serif; font-size: 72px; line-height: 0.9; letter-spacing: -0.04em; }
.of-n { font-size: 15px; opacity: 0.75; margin-left: 4px; }
.sellos-bar { display: grid; grid-template-columns: repeat(20, 1fr); gap: 3px; margin-top: 16px; }
.sello-dot { height: 8px; border-radius: 4px; background: rgba(255,255,255,0.2); }
.sello-dot.on { background: white; }
.card-meta { display: flex; justify-content: space-between; align-items: center; margin-top: 14px; font-size: 12px; opacity: 0.8; }
.card-meta .id { font-family: "SF Mono", monospace; letter-spacing: 0.05em; }

.section-title { padding: 30px 20px 12px; display: flex; justify-content: space-between; align-items: baseline; }
.section-title h2 { font-family: Georgia, serif; font-weight: 400; margin: 0; font-size: 21px; letter-spacing: -0.01em; }
.section-title .link { font-size: 11px; text-transform: uppercase; letter-spacing: 0.14em; color: var(--stone); text-decoration: none; }

.negocios { padding: 0 20px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.negocio-card { aspect-ratio: 1; background: var(--cream-warm); border: 1px solid var(--line); border-radius: 12px; display: grid; place-items: center; padding: 12px; cursor: pointer; transition: all 0.2s; }
.negocio-card:hover { border-color: var(--green); transform: translateY(-2px); box-shadow: 0 6px 16px -6px rgba(5,150,105,0.2); }
.negocio-card img { max-width: 88%; max-height: 88%; object-fit: contain; }

.menu-scroll { display: flex; gap: 12px; padding: 4px 20px 12px; overflow-x: auto; scroll-snap-type: x mandatory; -webkit-overflow-scrolling: touch; scrollbar-width: none; }
.menu-scroll::-webkit-scrollbar { display: none; }
.menu-card { flex: 0 0 200px; scroll-snap-align: start; background: var(--cream-warm); border-radius: 14px; overflow: hidden; box-shadow: 0 4px 14px -4px rgba(15,29,24,0.12); border: 1px solid var(--line); }
.menu-card .img { aspect-ratio: 4/3; background-size: cover; background-position: center; }
.menu-card .body { padding: 12px 14px; }
.menu-card h3 { font-family: Georgia, serif; font-weight: 400; margin: 0; font-size: 15px; }
.menu-card .meta { display: flex; justify-content: space-between; align-items: baseline; margin-top: 5px; font-size: 11px; color: var(--ink-soft); }
.menu-card .meta .p { color: var(--ink); font-family: Georgia, serif; font-size: 14px; }

.canje-card { margin: 4px 20px 20px; padding: 20px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 16px; position: relative; overflow: hidden; box-shadow: 0 4px 20px -6px rgba(217,119,6,0.35); }
.canje-card::before { content: '🎁'; position: absolute; top: -12px; right: -12px; font-size: 110px; opacity: 0.15; transform: rotate(-15deg); }
.canje-card .lbl { font-size: 11px; text-transform: uppercase; letter-spacing: 0.14em; color: #92400e; font-weight: 600; }
.canje-card .amt { font-family: Georgia, serif; font-size: 34px; letter-spacing: -0.02em; color: #78350f; line-height: 1; margin-top: 6px; }
.canje-card p { margin: 8px 0 0; font-size: 13px; color: #78350f; max-width: 260px; }

.activity { padding: 0 20px 12px; }
.activity-item { display: flex; align-items: center; gap: 12px; padding: 12px 0; border-bottom: 1px solid var(--line); }
.activity-item:last-child { border-bottom: none; }
.activity-item .ico { width: 40px; height: 40px; border-radius: 50%; background: var(--sand); display: grid; place-items: center; font-size: 18px; }
.activity-item .body { flex: 1; min-width: 0; }
.activity-item .body h4 { margin: 0; font-size: 14px; font-weight: 500; }
.activity-item .body .sub { font-size: 12px; color: var(--stone); margin-top: 2px; }
.activity-item .amt { font-family: Georgia, serif; color: var(--green); font-weight: 500; }

.bottom-nav { position: sticky; bottom: 0; background: var(--cream); border-top: 1px solid var(--line); display: grid; grid-template-columns: repeat(4, 1fr); padding: 8px 0 max(8px, env(safe-area-inset-bottom)); z-index: 30; }
.nav-item { display: grid; place-items: center; gap: 2px; padding: 8px 0; cursor: pointer; color: var(--stone); font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em; }
.nav-item.active { color: var(--green); }
.nav-item svg { width: 22px; height: 22px; fill: currentColor; }

.intro { max-width: 900px; margin: 40px auto 20px; padding: 20px; text-align: center; }
.intro .label { color: var(--stone); font-size: 11px; text-transform: uppercase; letter-spacing: 0.16em; }
.intro h1 { font-family: Georgia, serif; font-weight: 400; font-size: 32px; margin: 8px 0 6px; letter-spacing: -0.02em; }
.intro p { color: var(--ink-soft); max-width: 620px; margin: 0 auto; }
""".replace("__HERO__", F['hero_local'])

def img(u): return f'<img src="{u}" />'
def bg(u): return f'style="background-image:url({u})"'

html = f"""<title>Cotorreo Rewards V2</title>
<style>{CSS}</style>

<div class="intro">
  <div class="label">Cotorreo Rewards · Rediseño V2</div>
  <h1>Rewards + Menú, todo en uno.</h1>
  <p>Con tus fotos reales del local, logos oficiales de los 6 negocios y menú integrado. Cliente ve sus sellos, explora los negocios y descubre el menú desde la misma app. Decime qué ajustar.</p>
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
        <span>Faltan 8 sellos para tu próximo canje</span>
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
      <div class="body"><h3>Tacos al Pastor</h3><div class="meta"><span>Plaza · Cocina</span><span class="p">₡4.900</span></div></div>
    </div>
    <div class="menu-card">
      <div class="img" {bg(F['plato_2'])}></div>
      <div class="body"><h3>Quesabirrias</h3><div class="meta"><span>Taquería</span><span class="p">₡5.000</span></div></div>
    </div>
    <div class="menu-card">
      <div class="img" {bg(F['bebida'])}></div>
      <div class="body"><h3>Bubble Tea Choco</h3><div class="meta"><span>Bebidas</span><span class="p">₡3.500</span></div></div>
    </div>
    <div class="menu-card">
      <div class="img" {bg(F['alpadel'])}></div>
      <div class="body"><h3>Cancha de Pádel</h3><div class="meta"><span>Alpadel</span><span class="p">₡6.000/h</span></div></div>
    </div>
  </div>

  <div class="section-title"><h2>Tu progreso</h2></div>
  <div class="canje-card">
    <span class="lbl">Próximo canje</span>
    <div class="amt">₡15.000</div>
    <p>Completá 8 sellos más para desbloquear tu crédito canjeable en cualquier negocio del grupo.</p>
  </div>

  <div class="section-title"><h2>Última actividad</h2><a class="link" href="#">Historial</a></div>
  <div class="activity">
    <div class="activity-item">
      <div class="ico">🌮</div>
      <div class="body"><h4>Plaza Cotorreo</h4><div class="sub">Hoy · ₡25.000</div></div>
      <div class="amt">+2</div>
    </div>
    <div class="activity-item">
      <div class="ico">🎾</div>
      <div class="body"><h4>Alpadel</h4><div class="sub">Ayer · ₡12.000</div></div>
      <div class="amt">+1</div>
    </div>
    <div class="activity-item">
      <div class="ico">🍹</div>
      <div class="body"><h4>Cotorreo Taquería</h4><div class="sub">Sáb · ₡18.000</div></div>
      <div class="amt">+1</div>
    </div>
  </div>

  <div class="bottom-nav">
    <div class="nav-item active"><svg viewBox="0 0 24 24"><path d="M12 2L2 9v13h6v-7h8v7h6V9L12 2z"/></svg>Inicio</div>
    <div class="nav-item"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/></svg>Menú</div>
    <div class="nav-item"><svg viewBox="0 0 24 24"><path d="M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z"/></svg>Canjear</div>
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

path = r'C:\Users\VICENT~1\AppData\Local\Temp\claude\C--Users-vicente-benitez2\9638ccb6-fcd5-4b92-b05b-dd6c7ef1c6e2\scratchpad\rewards-v2.html'
with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Generado: {len(html)//1024}KB')
print(f'Path: {path}')
