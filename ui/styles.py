GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg: #F8FAFC;
    --surface: #FFFFFF;
    --ink: #0F172A;
    --muted: #475569;
    --subtle: #64748B;
    --line: #E2E8F0;
    --brand: #0284C7;
    --brand-strong: #0369A1;
    --brand-soft: #E0F2FE;
    --accent: #10B981;
    --radius: 18px;
    --shadow: 0 1px 2px rgba(15, 23, 42, .04), 0 10px 30px -14px rgba(15, 23, 42, .14);
    --glow: 0 0 0 1px rgba(2, 132, 199, .22), 0 22px 44px -18px rgba(2, 132, 199, .38);
}

html { scroll-behavior: smooth; }

.stApp {
    font-family: 'Inter', sans-serif;
    color: var(--ink);
    background:
        radial-gradient(1100px 520px at 0% -8%, rgba(14, 165, 233, .16), transparent 60%),
        radial-gradient(900px 480px at 100% -4%, rgba(16, 185, 129, .13), transparent 60%),
        var(--bg);
}

header[data-testid="stHeader"], [data-testid="stDecoration"], [data-testid="stToolbar"],
[data-testid="stHeaderActionElements"] { display: none !important; }

[data-testid="stMainBlockContainer"], .block-container {
    max-width: 1200px;
    padding: 1rem 1.25rem 0 !important;
}

.stMarkdown, .stMarkdown p, button, input, label { font-family: 'Inter', sans-serif !important; }

.anchor { scroll-margin-top: 104px; }

@keyframes fadeUp { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: none; } }
@keyframes pulse { 0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, .55); } 50% { box-shadow: 0 0 0 7px rgba(16, 185, 129, 0); } }
@keyframes badgeGlow { 0%, 100% { box-shadow: 0 0 0 1px rgba(2,132,199,.25), 0 0 18px -2px rgba(2,132,199,.35); } 50% { box-shadow: 0 0 0 1px rgba(16,185,129,.35), 0 0 26px 0 rgba(16,185,129,.4); } }
@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
.fade-up { animation: fadeUp .8s cubic-bezier(.22, 1, .36, 1) both; }
.delay-1 { animation-delay: .08s; } .delay-2 { animation-delay: .16s; } .delay-3 { animation-delay: .24s; }

/* ---------- Floating glass navigation ---------- */
/* Streamlit wraps keyed containers in a height-bound div, so stickiness must live on that wrapper. */
div:has(> .st-key-glass_nav) { position: sticky; top: 12px; z-index: 1000; }
.st-key-glass_nav [data-testid="stMarkdownContainer"], .st-key-glass_nav .stMarkdown { margin: 0 !important; }
.st-key-glass_nav [data-testid="stMarkdownContainer"] > div { margin: 0 !important; }
.st-key-glass_nav {
    padding: .55rem .7rem .55rem 1rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, .68);
    backdrop-filter: saturate(180%) blur(16px);
    -webkit-backdrop-filter: saturate(180%) blur(16px);
    border: 1px solid rgba(226, 232, 240, .9);
    box-shadow: 0 8px 30px -12px rgba(15, 23, 42, .18);
    margin-bottom: .5rem;
}
.st-key-glass_nav [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: .5rem !important; align-items: center; }
.st-key-glass_nav [data-testid="stColumn"] { min-width: 0 !important; width: auto !important; flex: 0 0 auto !important; }
.st-key-glass_nav [data-testid="stColumn"]:first-child { flex: 1 1 auto !important; }
.st-key-glass_nav [data-testid="stColumn"]:nth-child(2) { flex: 2 1 auto !important; }
.st-key-glass_nav [data-testid="stElementContainer"] { width: auto !important; }

.brand { display: flex; align-items: center; gap: .6rem; font-weight: 800; font-size: 1.05rem; color: var(--ink); letter-spacing: -.01em; white-space: nowrap; }
.brand-mark {
    display: grid; place-items: center; width: 34px; height: 34px; border-radius: 10px; color: #fff;
    background: linear-gradient(135deg, var(--brand), var(--accent));
    box-shadow: 0 6px 16px -6px rgba(2, 132, 199, .6);
}
.nav-links { display: flex; justify-content: center; gap: .25rem; }
.nav-links a {
    color: var(--muted) !important; text-decoration: none !important; font-size: .9rem; font-weight: 500;
    padding: .45rem .8rem; border-radius: 999px; transition: background .2s, color .2s;
}
.nav-links a:hover { background: var(--brand-soft); color: var(--brand-strong) !important; }

.st-key-lang_switch [data-testid="stButtonGroup"] { gap: 0; }
.st-key-about_btn button {
    border-radius: 999px !important; border: none !important; color: #fff !important; font-weight: 600 !important;
    background: linear-gradient(135deg, var(--brand), var(--brand-strong)) !important;
    box-shadow: 0 8px 20px -8px rgba(2, 132, 199, .7); padding: .35rem 1rem !important; min-height: 2.25rem;
    transition: transform .2s, box-shadow .2s;
}
.st-key-about_btn button:hover { transform: translateY(-1px); box-shadow: 0 12px 26px -8px rgba(2, 132, 199, .8); }

/* ---------- Hero ---------- */
.hero { padding: 3.5rem 0 2rem; }
.badge {
    display: inline-flex; align-items: center; gap: .55rem; padding: .4rem .9rem .4rem .5rem;
    border-radius: 999px; font-size: .82rem; font-weight: 600; color: var(--brand-strong);
    background: rgba(224, 242, 254, .75); animation: badgeGlow 3.5s ease-in-out infinite;
}
.badge-icon { display: grid; place-items: center; width: 22px; height: 22px; border-radius: 999px; background: var(--brand); color: #fff; }
.hero h1.hero-title {
    font-size: clamp(2.3rem, 5.4vw, 4rem) !important; line-height: 1.04 !important; font-weight: 900 !important;
    letter-spacing: -.035em; color: var(--ink) !important; margin: 1.25rem 0 1rem !important; padding: 0 !important;
    text-wrap: balance;
}
.hero-title .accent {
    background: linear-gradient(100deg, var(--brand) 10%, var(--accent) 90%);
    -webkit-background-clip: text; background-clip: text; color: transparent;
}
.hero-sub { font-size: 1.1rem; line-height: 1.65; color: var(--muted); max-width: 36rem; margin: 0 0 1.75rem; text-wrap: pretty; }
.cta-row { display: flex; flex-wrap: wrap; gap: .75rem; }
.btn {
    display: inline-flex; align-items: center; gap: .5rem; padding: .85rem 1.35rem; border-radius: 999px;
    font-weight: 600; font-size: .98rem; text-decoration: none !important; transition: transform .2s, box-shadow .2s, background .2s;
}
.btn-primary { color: #fff !important; background: linear-gradient(135deg, var(--brand), var(--brand-strong)); box-shadow: 0 14px 30px -12px rgba(2, 132, 199, .75); }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 18px 36px -12px rgba(2, 132, 199, .85); }
.btn-primary:hover .lucide { transform: translateX(3px); }
.btn .lucide { transition: transform .2s; }
.btn-ghost { color: var(--ink) !important; background: rgba(255, 255, 255, .8); border: 1px solid var(--line); }
.btn-ghost:hover { background: #fff; transform: translateY(-2px); box-shadow: var(--shadow); }
.hero-stats { display: flex; flex-wrap: wrap; gap: 2rem; margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid var(--line); }
.hero-stats .value { font-size: 1.75rem; font-weight: 800; letter-spacing: -.02em; color: var(--ink); }
.hero-stats .label { font-size: .85rem; color: var(--subtle); }

/* ---------- Hero preview card ---------- */
.preview-wrap { position: relative; padding: 1rem 0; animation: float 7s ease-in-out infinite; }
.preview-glow {
    position: absolute; inset: 8% 6%; border-radius: 32px; filter: blur(48px); opacity: .55;
    background: linear-gradient(135deg, var(--brand), var(--accent));
}
.preview-card {
    position: relative; border-radius: 24px; padding: 1.5rem; background: rgba(255, 255, 255, .86);
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, .9); box-shadow: 0 30px 60px -24px rgba(15, 23, 42, .3);
}
.preview-head { display: flex; align-items: center; justify-content: space-between; gap: .75rem; font-size: .85rem; font-weight: 600; color: var(--muted); }
.live { display: inline-flex; align-items: center; gap: .5rem; }
.live-dot { width: 8px; height: 8px; border-radius: 999px; background: var(--accent); animation: pulse 2s infinite; }
.chip { font-size: .72rem; font-weight: 600; padding: .25rem .6rem; border-radius: 999px; background: #F1F5F9; color: var(--muted); }
.risk-row { display: flex; align-items: center; gap: 1rem; margin: 1.25rem 0 1rem; padding: 1rem; border-radius: 16px; }
.risk-icon { display: grid; place-items: center; width: 48px; height: 48px; border-radius: 14px; color: #fff; flex-shrink: 0; }
.eyebrow-sm { font-size: .72rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--subtle); }
.risk-name { font-size: 1.6rem; font-weight: 900; letter-spacing: -.02em; line-height: 1.1; }
.score { margin-left: auto; text-align: right; }
.score .num { font-size: 2rem; font-weight: 900; letter-spacing: -.03em; color: var(--ink); }
.score .den { font-size: .85rem; color: var(--subtle); }
.meter { height: 8px; border-radius: 999px; background: #EEF2F7; overflow: hidden; }
.meter-fill { height: 100%; border-radius: 999px; transition: width .6s cubic-bezier(.22, 1, .36, 1); }
.prob-list { display: grid; gap: .7rem; margin-top: 1.25rem; }
.prob-row { display: grid; grid-template-columns: 64px 1fr 40px; align-items: center; gap: .75rem; font-size: .85rem; color: var(--muted); }
.prob-row .pct { text-align: right; font-weight: 700; color: var(--ink); font-variant-numeric: tabular-nums; }
.prob-row .meter { height: 6px; }
.preview-hint { display: flex; align-items: center; gap: .5rem; margin-top: 1.25rem; padding-top: 1rem; border-top: 1px dashed var(--line); font-size: .8rem; color: var(--subtle); }

/* ---------- Sections ---------- */
.section-head { margin: 3.5rem 0 1.5rem; max-width: 44rem; }
.eyebrow {
    display: inline-flex; align-items: center; gap: .4rem; font-size: .78rem; font-weight: 700; letter-spacing: .06em;
    text-transform: uppercase; color: var(--brand-strong); background: var(--brand-soft); padding: .35rem .75rem; border-radius: 999px;
}
.section-head h2 {
    font-size: clamp(1.6rem, 3vw, 2.25rem) !important; font-weight: 800 !important; letter-spacing: -.025em;
    color: var(--ink) !important; margin: .9rem 0 .5rem !important; padding: 0 !important; line-height: 1.15 !important;
}
.section-head p { color: var(--muted); font-size: 1rem; line-height: 1.6; margin: 0; }

/* ---------- Cards ---------- */
.card, div[class*="st-key-card_"] {
    background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius);
    box-shadow: var(--shadow); transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease;
}
.card { padding: 1.4rem; height: 100%; }
div[class*="st-key-card_"] { padding: 1.4rem 1.4rem .8rem; }
.card:hover, div[class*="st-key-card_"]:hover { transform: translateY(-3px); box-shadow: var(--glow); border-color: rgba(2, 132, 199, .35); }

.grid { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); }
.grid-3 { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }

.icon-pill { display: inline-grid; place-items: center; width: 42px; height: 42px; border-radius: 12px; color: var(--brand); background: var(--brand-soft); flex-shrink: 0; }
.icon-pill.green { color: #047857; background: #D1FAE5; }
.icon-pill.amber { color: #B45309; background: #FEF3C7; }
.icon-pill.red { color: #B91C1C; background: #FEE2E2; }
.icon-pill.violet { color: #6D28D9; background: #EDE9FE; }

.kpi-top { display: flex; align-items: center; justify-content: space-between; }
.kpi-label { font-size: .85rem; font-weight: 600; color: var(--subtle); margin-top: 1rem; }
.kpi-value { font-size: 1.85rem; font-weight: 800; letter-spacing: -.025em; color: var(--ink); line-height: 1.2; font-variant-numeric: tabular-nums; }
.kpi-unit { font-size: .9rem; font-weight: 600; color: var(--subtle); margin-left: .25rem; }
.status { font-size: .72rem; font-weight: 700; padding: .25rem .55rem; border-radius: 999px; }

.card-head { display: flex; align-items: flex-start; gap: .85rem; margin-bottom: .75rem; }
.card-title { font-size: 1.05rem; font-weight: 700; color: var(--ink); line-height: 1.3; }
.card-sub { font-size: .85rem; color: var(--subtle); margin-top: .15rem; line-height: 1.45; }
.card p.body { font-size: .92rem; color: var(--muted); line-height: 1.6; margin: .6rem 0 0; }

.list-label { font-size: .72rem; font-weight: 800; letter-spacing: .07em; text-transform: uppercase; margin: 1.1rem 0 .6rem; }
.item { display: flex; gap: .75rem; padding: .7rem .8rem; border-radius: 12px; margin-bottom: .5rem; }
.item .lucide { flex-shrink: 0; margin-top: 2px; }
.item-title { font-size: .85rem; font-weight: 700; color: var(--ink); }
.item-text { font-size: .85rem; color: var(--muted); line-height: 1.5; }
.item.neg { background: #FEF2F2; } .item.neg .lucide { color: #DC2626; }
.item.pos { background: #F0FDF4; } .item.pos .lucide { color: #059669; }
.item.rec { background: #F0F9FF; } .item.rec .lucide { color: var(--brand); }

.density-card { display: flex; align-items: center; gap: .9rem; padding: 1rem; border-radius: 14px; background: linear-gradient(135deg, #F0F9FF, #ECFDF5); border: 1px solid #D5EEF9; margin-top: .4rem; }
.density-card .kpi-value { font-size: 1.5rem; }

div[class*="st-key-card_"] [data-testid="stSlider"] label p { font-weight: 600; color: var(--ink); font-size: .9rem; }
.st-key-export_btn button {
    border-radius: 999px !important; font-weight: 600 !important; border: 1px solid var(--line) !important;
    background: var(--ink) !important; color: #fff !important; transition: transform .2s;
}
.st-key-export_btn button:hover { transform: translateY(-1px); background: #1E293B !important; }
[data-testid="stFileUploaderDropzone"] { border-radius: 14px; border: 1.5px dashed #BAE6FD; background: #F8FCFF; }

/* ---------- Dialog ---------- */
div[role="dialog"] { border-radius: 22px !important; }
.dialog-meta { display: flex; flex-wrap: wrap; gap: .5rem; margin: .75rem 0 1.25rem; }
.dialog-meta span { display: inline-flex; align-items: center; gap: .4rem; font-size: .82rem; font-weight: 600; color: var(--muted); background: #F1F5F9; padding: .35rem .7rem; border-radius: 999px; }
.dialog-item { display: flex; gap: .85rem; padding: .9rem; border-radius: 14px; border: 1px solid var(--line); margin-bottom: .6rem; }

/* ---------- Footer ---------- */
.site-footer { margin: 5rem -1.25rem 0; padding: 3.5rem 1.25rem 1.5rem; background: #0B1220; color: #CBD5E1; border-radius: 28px 28px 0 0; }
.footer-grid { display: grid; gap: 2.5rem; grid-template-columns: 1.6fr repeat(3, 1fr); }
.site-footer .brand { color: #fff; }
.footer-desc { font-size: .9rem; line-height: 1.65; color: #94A3B8; margin: 1rem 0 1.25rem; max-width: 22rem; }
.footer-col h3 { font-size: .78rem !important; font-weight: 700 !important; letter-spacing: .08em; text-transform: uppercase; color: #fff !important; margin: 0 0 1rem !important; padding: 0 !important; }
.footer-col a, .footer-col span { display: flex; align-items: center; gap: .5rem; color: #94A3B8 !important; text-decoration: none !important; font-size: .9rem; padding: .3rem 0; transition: color .2s; }
.footer-col a:hover { color: #fff !important; }
.footer-badge { display: inline-flex; align-items: center; gap: .45rem; font-size: .78rem; font-weight: 600; color: #6EE7B7; background: rgba(16, 185, 129, .12); border: 1px solid rgba(16, 185, 129, .25); padding: .35rem .75rem; border-radius: 999px; }
.footer-bottom { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 1rem; margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid rgba(148, 163, 184, .18); font-size: .82rem; color: #64748B; }
.footer-bottom a { color: #94A3B8 !important; text-decoration: none !important; display: inline-flex; align-items: center; gap: .35rem; }
.footer-bottom a:hover { color: #fff !important; }

/* ---------- Responsive ---------- */
@media (max-width: 900px) {
    .st-key-glass_nav [data-testid="stColumn"]:nth-child(2) { display: none !important; }
    .footer-grid { grid-template-columns: 1fr 1fr; }
    .footer-grid > :first-child { grid-column: 1 / -1; }
    .hero { padding: 2.25rem 0 1rem; }
}
@media (max-width: 640px) {
    .st-key-glass_nav { border-radius: 20px; padding: .5rem .6rem .5rem .8rem; }
    .brand-text { display: none; }
    .hero-stats { gap: 1.25rem; }
    .btn { flex: 1 1 auto; justify-content: center; }
    .section-head { margin-top: 2.5rem; }
    .footer-grid { grid-template-columns: 1fr; }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation: none !important; transition: none !important; }
    html { scroll-behavior: auto; }
}
</style>
"""
