"""
charts.py
Functions to take in a DataFrame as argument and return Altair charts
for usage in the Streamlit dashboard.
"""

import altair as alt
import pandas as pd


# Custom color scale for 'judgement_favour' using user-provided colors.
JUDGEMENT_DOMAINS = ["Plaintiff", "Defendant", "Undisclosed"]
# Using provided colors for key categories and neutral grey for Undisclosed.
JUDGEMENT_RANGES = ["#007f8c", "#12516a", "#707070"]

ruling_color_scale = alt.Scale(
    domain=JUDGEMENT_DOMAINS,
    range=JUDGEMENT_RANGES
)


def get_overall_ruling_bias_chart(data: pd.DataFrame):
    """Donut chart showing favour (Plaintiff vs Defendant vs Undisclosed)."""
    data = data.copy()
    data["judgement_favour"] = data["judgement_favour"].fillna("Undisclosed")
    counts = data["judgement_favour"].value_counts().reset_index()
    counts.columns = ["judgement_favour", "count"]

    chart = (
        alt.Chart(counts)
        .mark_arc(innerRadius=50)
        .encode(
            theta=alt.Theta(field="count", type="quantitative"),
            color=alt.Color(
                field="judgement_favour",
                type="nominal",
                title="Ruling Favour",
                scale=ruling_color_scale,
            ),
            tooltip=["judgement_favour", "count"],
        )
        .properties(width=250, height=250, title="Overall Ruling Bias")
    )

    return chart


def get_judge_ruling_bias_chart(data: pd.DataFrame, judge_name: str = ""):
    """Donut chart showing an individual judge's ruling bias."""
    if data.empty:
        return (
            alt.Chart(pd.DataFrame({"message": ["No hearings available for this judge."]}))
            .mark_text(align="center", fontSize=13, color="gray")
            .encode(text="message:N")
            .properties(height=80)
        )

    data = data.copy()
    data["judgement_favour"] = data["judgement_favour"].fillna("Undisclosed")
    counts = data["judgement_favour"].value_counts().reset_index()
    counts.columns = ["judgement_favour", "count"]

    title = f"Ruling Bias for {judge_name}" if judge_name else "Judge Ruling Bias"

    chart = (
        alt.Chart(counts)
        .mark_arc(innerRadius=50)
        .encode(
            theta=alt.Theta(field="count", type="quantitative"),
            color=alt.Color(
                field="judgement_favour",
                type="nominal",
                title="Ruling Favour",
                scale=ruling_color_scale,
            ),
            tooltip=["judgement_favour", "count"],
        )
        .properties(width=250, height=250, title=title)
    )

    return chart


def get_recent_hearings_table(data: pd.DataFrame):
    recent = data.sort_values(by="hearing_date", ascending=False).head(5)
    table = recent[
        ["hearing_date", "court_name",
         "hearing_title", "judgement_favour", "hearing_url", "hearing_citation"]
    ].rename(
        columns={
            "hearing_citation": "Citation",
            "hearing_date": "Date",
            "court_name": "Court",
            "hearing_title": "Case Title",
            "judgement_favour": "Ruling Favour",
            "hearing_url": "Source URL",
        }
    )

    # REMOVED custom styling to use Streamlit's default DataFrame appearance.
    return table


def get_rulings_by_court_chart(data: pd.DataFrame):
    """Stacked bar chart showing ruling by court."""
    data = data.copy()
    data["judgement_favour"] = data["judgement_favour"].fillna("Undisclosed")
    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            y=alt.Y("court_name:N", title="Court"),
            x=alt.X("count():Q", title="Number of Hearings"),
            color=alt.Color(
                "judgement_favour:N",
                title="Ruling Favour",
                scale=ruling_color_scale,
            ),
            tooltip=["court_name", "count()"],
        )
        .properties(title="Recent Rulings across Different Courts")
    )
    return chart


def get_rulings_by_title(data: pd.DataFrame):
    """Composite bar chart showing the disparity in rulings by title."""
    data = data.copy()
    data["title_name"] = data["title_name"].fillna("Unknown")
    data["judgement_favour"] = data["judgement_favour"].fillna("Undisclosed")

    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("count():Q", title="Number of Hearings"),
            y=alt.Y("title_name:N", sort="-x", title="Judge Title"),
            color=alt.Color(
                "judgement_favour:N",
                title="Ruling Favour",
                scale=ruling_color_scale,
            ),
            tooltip=[
                alt.Tooltip("title_name:N", title="Title"),
                alt.Tooltip("judgement_favour:N", title="Ruling Favour"),
                alt.Tooltip("count():Q", title="Number of Hearings"),
            ],
        )
        .properties(title="Rulings by Judicial Title", width=500, height=300)
    )

    return chart


def get_anomalies_visualisation(data: pd.DataFrame):
    """Visualisation showing frequency of anomalies per court over time."""
    anomalies = data[
        data["hearing_anomaly"].fillna("").apply(lambda x: x.strip().lower() not in ["none found"])
    ].copy()

    if anomalies.empty:
        return (
            alt.Chart(pd.DataFrame({"message": ["No significant anomalies detected."]}))
            .mark_text(align="center", fontSize=13, color="gray")
            .encode(text="message:N")
            .properties(height=80)
        )

    anomalies["hearing_date"] = pd.to_datetime(anomalies["hearing_date"], errors="coerce")
    anomalies["month"] = anomalies["hearing_date"].dt.to_period("M").astype(str)

    counts = anomalies.groupby(["court_name", "month"]).size().reset_index(name="count")

    chart = (
        alt.Chart(counts)
        .mark_rect()
        .encode(
            x=alt.X("month:N", title="Month", sort="ascending"),
            y=alt.Y("court_name:N", title="Court"),
            color=alt.Color("count:Q", title=
                            "No. of Anomalies", scale=alt.Scale(scheme="orangered")),
            tooltip=[
                alt.Tooltip("court_name:N", title="Court"),
                alt.Tooltip("month:N", title="Month"),
                alt.Tooltip("count:Q", title="Anomalies"),
            ],
        )
        .properties(title="Court Anomalies Over Time", width=300, height=250)
    )

    return chart