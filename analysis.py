import io
import os
from dataclasses import dataclass

import joblib
import numpy as np
import pandas as pd

MODEL_PATH = "model.pkl"
FEATURE_COLUMNS = [
    "precipitation",
    "temperature",
    "pasture_area",
    "livestock_count",
    "livestock_loss",
    "livestock_density",
]
FEATURE_IMPORTANCE = {
    "livestock_density": 48.5,
    "livestock_loss": 15.2,
    "precipitation": 14.1,
    "livestock_count": 10.5,
    "temperature": 7.8,
    "pasture_area": 4.2,
}
RISK_COLORS = {
    "HIGH": ("#DC2626", "#FEF2F2"),
    "MEDIUM": ("#D97706", "#FFFBEB"),
    "LOW": ("#059669", "#ECFDF5"),
}


@dataclass
class Inputs:
    precip: float
    temp: float
    pasture: float
    count: float
    loss: float

    @property
    def density(self) -> float:
        return self.count / self.pasture if self.pasture > 0 else 0.0


@dataclass
class Assessment:
    level: str
    score: int
    prob_high: int
    prob_med: int
    prob_low: int
    from_model: bool

    @property
    def color(self) -> str:
        return RISK_COLORS[self.level][0]

    @property
    def soft_color(self) -> str:
        return RISK_COLORS[self.level][1]


def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    try:
        return joblib.load(MODEL_PATH)
    except Exception:
        return None


def _predict_with_model(model, inputs: Inputs) -> Assessment | None:
    try:
        frame = pd.DataFrame(
            [[inputs.precip, inputs.temp, inputs.pasture, inputs.count, inputs.loss, inputs.density]],
            columns=FEATURE_COLUMNS,
        )
        level = str(model.predict(frame)[0]).upper()
        if level not in RISK_COLORS:
            return None
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(frame)[0]
            high, med, low = int(probs[0] * 100), int(probs[1] * 100), int(probs[2] * 100)
        else:
            high, med, low = {"HIGH": (70, 20, 10), "MEDIUM": (20, 60, 20), "LOW": (10, 20, 70)}[level]
        score = int(np.clip(high + med * 0.5, 0, 100))
        return Assessment(level, score, high, med, low, from_model=True)
    except Exception:
        return None


def _predict_heuristic(inputs: Inputs) -> Assessment:
    density_risk = np.clip((inputs.density - 0.5) / 1.5 * 100, 0, 100)
    precip_risk = np.clip((400 - inputs.precip) / 350 * 100, 0, 100)

    if inputs.temp < 0:
        temp_risk = np.clip(-inputs.temp / 35.0 * 100, 0, 100)
    elif inputs.temp > 25:
        temp_risk = np.clip((inputs.temp - 25) / 20.0 * 100, 0, 100)
    else:
        temp_risk = 0.0

    loss_ratio = inputs.loss / inputs.count * 100 if inputs.count > 0 else 0
    loss_risk = np.clip(loss_ratio / 10.0 * 100, 0, 100)

    total = density_risk * 0.40 + precip_risk * 0.35 + temp_risk * 0.15 + loss_risk * 0.10

    high = int(np.clip(total, 5, 90))
    low = int(np.clip(100 - total, 5, 90))
    med = max(0, 100 - high - low)
    level = "HIGH" if total >= 55 else "MEDIUM" if total >= 35 else "LOW"
    return Assessment(level, int(round(total)), high, med, low, from_model=False)


def assess(inputs: Inputs, model=None) -> Assessment:
    if model is not None:
        result = _predict_with_model(model, inputs)
        if result is not None:
            return result
    return _predict_heuristic(inputs)


def build_insights(inputs: Inputs, t: dict):
    """Return (critical, positive, recommendations) as lists of (icon, label, text)."""
    msg = t["insights"]
    critical, positive, recs = [], [], []

    precip_label = f"{t['kpi_precip']} · {inputs.precip:.1f} {t['unit_mm']}"
    if inputs.precip < 100:
        critical.append(("cloud-rain", precip_label, msg["precip_severe"]))
        recs.append(("droplets", None, msg["rec_precip_severe"]))
    elif inputs.precip < 250:
        critical.append(("cloud-rain", precip_label, msg["precip_low"]))
        recs.append(("refresh", None, msg["rec_precip_low"]))
    else:
        positive.append(("cloud-rain", precip_label, msg["precip_ok"]))

    density_label = f"{t['kpi_density']} · {inputs.density:.2f} {t['unit_density']}"
    if inputs.density > 1.5:
        critical.append(("paw-print", density_label, msg["density_severe"]))
        recs.append(("route", None, msg["rec_density_severe"]))
    elif inputs.density > 0.8:
        critical.append(("paw-print", density_label, msg["density_high"]))
        recs.append(("calendar", None, msg["rec_density_high"]))
    else:
        positive.append(("sprout", density_label, msg["density_ok"]))

    temp_label = f"{t['kpi_temp']} · {inputs.temp:.1f} °C"
    if inputs.temp < -20:
        critical.append(("snowflake", temp_label, msg["temp_cold"]))
        recs.append(("home", None, msg["rec_temp_cold"]))
    elif inputs.temp > 30:
        critical.append(("sun", temp_label, msg["temp_hot"]))
        recs.append(("sun", None, msg["rec_temp_hot"]))
    else:
        positive.append(("thermometer", temp_label, msg["temp_ok"]))

    if inputs.loss > 200:
        loss_label = f"{t['kpi_loss']} · {inputs.loss:.0f} {t['unit_thousand']}"
        critical.append(("triangle-alert", loss_label, msg["loss_high"]))
        recs.append(("syringe", None, msg["rec_loss_high"]))

    if not recs:
        recs.append(("leaf", None, msg["rec_default"]))

    return critical, positive, recs


def build_report_csv(inputs: Inputs, result: Assessment, recs, t: dict) -> bytes:
    labels = t["prob_labels"]
    rows = [
        (t["lbl_precip"], f"{inputs.precip:.1f}"),
        (t["lbl_temp"], f"{inputs.temp:.1f}"),
        (t["lbl_pasture"], f"{inputs.pasture:.1f}"),
        (t["lbl_count"], f"{inputs.count:.1f}"),
        (t["lbl_loss"], f"{inputs.loss:.1f}"),
        (t["kpi_density"], f"{inputs.density:.3f}"),
        (t["risk_level_label"], t["risk_names"][result.level]),
        (t["preview_score"], str(result.score)),
        (f"P({labels[0]}) %", str(result.prob_high)),
        (f"P({labels[1]}) %", str(result.prob_med)),
        (f"P({labels[2]}) %", str(result.prob_low)),
    ]
    rows += [(f"{t['recs_title']} {i}", text) for i, (_, _, text) in enumerate(recs, start=1)]
    buffer = io.StringIO()
    pd.DataFrame(rows, columns=["Parameter", "Value"]).to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8-sig")
