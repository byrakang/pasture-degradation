import streamlit as st

from ui.icons import icon

REPO_URL = "https://github.com/byrakang/pasture-degradation"
UNCCD_URL = "https://www.unccd.int"


def html(markup: str) -> None:
    """Render raw HTML; lines are stripped so Markdown never treats indentation as a code block."""
    compact = "\n".join(line.strip() for line in markup.splitlines() if line.strip())
    st.markdown(compact, unsafe_allow_html=True)


def brand(t: dict) -> str:
    return (
        f'<div class="brand"><span class="brand-mark">{icon("sprout", 18)}</span>'
        f'<span class="brand-text">{t["brand"]}</span></div>'
    )


def nav_links(t: dict) -> str:
    links = [
        ("simulator", t["nav_simulator"]),
        ("insights", t["nav_insights"]),
        ("mission", t["nav_mission"]),
        ("dataset", t["nav_dataset"]),
    ]
    items = "".join(f'<a href="#{anchor}">{label}</a>' for anchor, label in links)
    return f'<nav class="nav-links" aria-label="Primary">{items}</nav>'


def hero_copy(t: dict) -> str:
    stats = "".join(
        f'<div><div class="value">{value}</div><div class="label">{label}</div></div>'
        for value, label in t["hero_stats"]
    )
    return f"""
    <section class="hero" aria-labelledby="hero-title">
        <div class="badge fade-up"><span class="badge-icon">{icon("sparkles", 13)}</span>{t["hero_badge"]}</div>
        <h1 id="hero-title" class="hero-title fade-up delay-1">{t["hero_title"]} <span class="accent">{t["hero_title_accent"]}</span></h1>
        <p class="hero-sub fade-up delay-2">{t["hero_sub"]}</p>
        <div class="cta-row fade-up delay-3">
            <a class="btn btn-primary" href="#simulator">{t["cta_primary"]} {icon("arrow-right", 18)}</a>
            <a class="btn btn-ghost" href="#mission">{icon("globe", 18)} {t["cta_secondary"]}</a>
        </div>
        <div class="hero-stats fade-up delay-3">{stats}</div>
    </section>
    """


def hero_preview(t: dict, result) -> str:
    high, med, low = t["prob_labels"]
    probs = [(high, result.prob_high, "#EF4444"), (med, result.prob_med, "#F59E0B"), (low, result.prob_low, "#10B981")]
    rows = "".join(
        f'<div class="prob-row"><span>{label}</span>'
        f'<div class="meter"><div class="meter-fill" style="width:{pct}%;background:{color}"></div></div>'
        f'<span class="pct">{pct}%</span></div>'
        for label, pct, color in probs
    )
    engine = t["engine_model"] if result.from_model else t["engine_heuristic"]
    shield = "shield-check" if result.level == "LOW" else "shield-alert"
    return f"""
    <div class="preview-wrap fade-up delay-2">
        <div class="preview-glow" aria-hidden="true"></div>
        <div class="preview-card" role="status" aria-live="polite">
            <div class="preview-head">
                <span class="live"><span class="live-dot"></span>{t["preview_live"]}</span>
                <span class="chip">{engine}</span>
            </div>
            <div class="risk-row" style="background:{result.soft_color}">
                <div class="risk-icon" style="background:{result.color}">{icon(shield, 24)}</div>
                <div>
                    <div class="eyebrow-sm">{t["risk_level_label"]}</div>
                    <div class="risk-name" style="color:{result.color}">{t["risk_names"][result.level]}</div>
                </div>
                <div class="score"><span class="num">{result.score}</span><span class="den">/100</span>
                <div class="eyebrow-sm">{t["preview_score"]}</div></div>
            </div>
            <div class="meter"><div class="meter-fill" style="width:{result.score}%;background:linear-gradient(90deg,#10B981,#F59E0B,#EF4444)"></div></div>
            <div class="prob-list">{rows}</div>
            <div class="preview-hint">{icon("sliders", 15)} {t["preview_hint"]}</div>
        </div>
    </div>
    """


def section_head(anchor: str, icon_name: str, eyebrow: str, title: str, desc: str) -> str:
    return f"""
    <div id="{anchor}" class="section-head anchor">
        <span class="eyebrow">{icon(icon_name, 14)} {eyebrow}</span>
        <h2>{title}</h2>
        <p>{desc}</p>
    </div>
    """


def _status(level: str) -> str:
    palette = {"ok": ("#047857", "#D1FAE5", "OK"), "warn": ("#B45309", "#FEF3C7", "!"), "bad": ("#B91C1C", "#FEE2E2", "!!")}
    color, bg, label = palette[level]
    return f'<span class="status" style="color:{color};background:{bg}">{label}</span>'


def kpi_grid(t: dict, inputs) -> str:
    precip_state = "bad" if inputs.precip < 100 else "warn" if inputs.precip < 250 else "ok"
    temp_state = "bad" if inputs.temp < -20 or inputs.temp > 30 else "ok"
    density_state = "bad" if inputs.density > 1.5 else "warn" if inputs.density > 0.8 else "ok"
    loss_state = "bad" if inputs.loss > 200 else "ok"
    cards = [
        ("cloud-rain", "", t["kpi_precip"], f"{inputs.precip:.1f}", t["unit_mm"], precip_state),
        ("thermometer", "amber", t["kpi_temp"], f"{inputs.temp:.1f}", "°C", temp_state),
        ("paw-print", "green", t["kpi_density"], f"{inputs.density:.2f}", t["unit_density"], density_state),
        ("trending-down", "red", t["kpi_loss"], f"{inputs.loss:.0f}", t["unit_thousand"], loss_state),
    ]
    items = "".join(
        f"""<div class="card">
        <div class="kpi-top"><span class="icon-pill {tone}">{icon(name)}</span>{_status(state)}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}<span class="kpi-unit">{unit}</span></div>
        </div>"""
        for name, tone, label, value, unit, state in cards
    )
    return f'<div class="grid">{items}</div>'


def card_head(icon_name: str, tone: str, title: str, subtitle: str = "") -> str:
    sub = f'<div class="card-sub">{subtitle}</div>' if subtitle else ""
    return (
        f'<div class="card-head"><span class="icon-pill {tone}">{icon(icon_name)}</span>'
        f'<div><div class="card-title">{title}</div>{sub}</div></div>'
    )


def density_readout(t: dict, inputs) -> str:
    return f"""
    <div class="density-card">
        <span class="icon-pill green">{icon("paw-print")}</span>
        <div>
            <div class="eyebrow-sm">{t["derived_density"]}</div>
            <div class="kpi-value">{inputs.density:.2f}<span class="kpi-unit">{t["unit_density"]}</span></div>
        </div>
    </div>
    """


def _items(entries, css: str) -> str:
    out = []
    for icon_name, title, text in entries:
        heading = f'<div class="item-title">{title}</div>' if title else ""
        out.append(
            f'<div class="item {css}">{icon(icon_name, 18)}<div>{heading}<div class="item-text">{text}</div></div></div>'
        )
    return "".join(out)


def summary_card(t: dict, result, critical, positive) -> str:
    tone = {"HIGH": "red", "MEDIUM": "amber", "LOW": "green"}[result.level]
    shield = "shield-check" if result.level == "LOW" else "shield-alert"
    neg = (
        f'<div class="list-label" style="color:#B91C1C">{t["factors_negative"]}</div>{_items(critical, "neg")}'
        if critical
        else ""
    )
    pos = (
        f'<div class="list-label" style="color:#047857">{t["factors_positive"]}</div>{_items(positive, "pos")}'
        if positive
        else ""
    )
    return f"""
    <div class="card">
        {card_head(shield, tone, t["risk_titles"][result.level], t["risk_descs"][result.level])}
        {neg}{pos}
    </div>
    """


def recommendations_card(t: dict, recs) -> str:
    return f"""
    <div>
        {card_head("lightbulb", "violet", f'{t["recs_title"]} ({len(recs)})')}
        {_items(recs, "rec")}
    </div>
    """


def mission_section(t: dict) -> str:
    tones = ["", "green", "amber"]
    cards = "".join(
        f'<div class="card">{card_head(name, tones[i], title)}<p class="body">{desc}</p></div>'
        for i, (name, title, desc) in enumerate(t["mission_cards"])
    )
    people = "".join(
        f'<div class="card">{card_head(name, "violet", title)}<p class="body">{desc}</p></div>'
        for name, title, desc in t["stakeholders"]
    )
    return f"""
    <div class="grid-3">{cards}</div>
    <div class="list-label" style="color:var(--subtle);margin-top:2rem">{t["stakeholders_title"]}</div>
    <div class="grid-3">{people}</div>
    """


def cop_dialog_body(t: dict) -> str:
    items = "".join(
        f'<div class="dialog-item"><span class="icon-pill">{icon(name)}</span>'
        f'<div><div class="card-title">{title}</div><div class="card-sub">{desc}</div></div></div>'
        for name, title, desc in t["mission_cards"]
    )
    return f"""
    <div>
        <div class="card-title" style="font-size:1.2rem">{t["cop_modal_title"]}</div>
        <div class="card-sub">{t["cop_sub"]}</div>
        <div class="dialog-meta">
            <span>{icon("map-pin", 14)} {t["cop_loc"]}</span>
            <span>{icon("calendar", 14)} {t["cop_date"]}</span>
        </div>
        <p class="body" style="color:var(--muted);font-size:.92rem;line-height:1.6">{t["mission_desc"]}</p>
        {items}
    </div>
    """


def footer(t: dict) -> str:
    return f"""
    <footer class="site-footer">
        <div class="footer-grid">
            <div>
                {brand(t).replace('class="brand-text"', 'class="brand-text-footer"')}
                <p class="footer-desc">{t["footer_desc"]}</p>
                <span class="footer-badge">{icon("leaf", 14)} {t["hero_badge"]}</span>
            </div>
            <div class="footer-col">
                <h3>{t["footer_platform"]}</h3>
                <a href="#simulator">{icon("sliders", 15)} {t["nav_simulator"]}</a>
                <a href="#insights">{icon("bar-chart", 15)} {t["nav_insights"]}</a>
                <a href="#mission">{icon("target", 15)} {t["nav_mission"]}</a>
                <a href="#dataset">{icon("database", 15)} {t["nav_dataset"]}</a>
            </div>
            <div class="footer-col">
                <h3>{t["footer_resources"]}</h3>
                <a href="{UNCCD_URL}" target="_blank" rel="noopener noreferrer">{icon("globe", 15)} UNCCD {icon("external", 12)}</a>
                <a href="{REPO_URL}" target="_blank" rel="noopener noreferrer">{icon("github", 15)} {t["footer_repo"]} {icon("external", 12)}</a>
            </div>
            <div class="footer-col">
                <h3>{t["footer_event"]}</h3>
                <span>{icon("landmark", 15)} UNCCD COP-17</span>
                <span>{icon("map-pin", 15)} {t["cop_loc"]}</span>
                <span>{icon("calendar", 15)} {t["cop_date"]}</span>
            </div>
        </div>
        <div class="footer-bottom">
            <span>© 2026 {t["brand"]}. {t["footer_rights"]}</span>
            <a href="#top">{t["footer_top"]} {icon("arrow-up", 14)}</a>
        </div>
    </footer>
    """
