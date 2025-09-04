from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio
import os

app = Flask(__name__)

@app.route("/")
def index():
    file_path = 'excel_chart_web/2025.xlsx'
    df = pd.read_excel(file_path)

    titles = sorted(df['title'].dropna().unique())
    years = sorted(df['Үйлдвэрлэсэн он:'].dropna().astype(int).unique())

    title_filter = request.args.get("title", default=None)
    year_filter = request.args.get("year", default=None)  # ✅ changed param name

    df['date_clean'] = pd.to_datetime(df['date_clean'], errors='coerce').dt.date
    df = df.dropna(subset=['price', 'date_clean'])

    if title_filter:
        df = df[df['title'].str.contains(title_filter, case=False, na=False)]
    if year_filter:
        try:
            year_int = int(year_filter)
            df = df[df['Үйлдвэрлэсэн он:'] == year_int]
        except ValueError:
            pass

    df['price'] = df['price'] / 1_000_000

    daily = df.groupby('date_clean').agg({
        'price': 'median',
        'id': 'count'
    }).rename(columns={'id': 'count'}).reset_index()

    daily['7-day'] = daily['price'].rolling(7).mean()
    daily['30-day'] = daily['price'].rolling(30).mean()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=daily['date_clean'], y=daily['price'],
        mode='markers', name='Тухайн өдөр',
        marker=dict(color='gray', size=6)
    ))
    fig.add_trace(go.Scatter(
        x=daily['date_clean'], y=daily['7-day'],
        mode='lines', name='Сүүлийн 7 хоног',
        line=dict(color='black', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=daily['date_clean'], y=daily['30-day'],
        mode='lines', name='Сүүлийн 30 хоног',
        line=dict(color='black', width=2, dash='dot')
    ))
    fig.add_trace(go.Bar(
        x=daily['date_clean'], y=daily['count'],
        name='Зарын тоо',
        marker=dict(color='lightgray'),
        opacity=0.6
    ), secondary_y=True)

    fig.update_layout(
        title="🚗 Машины үнэ (медиан сая.₮)",
        template="simple_white",
        hovermode="x unified",
        legend=dict(orientation="h", y=-0.3),
        height=600
    )
    fig.update_yaxes(title_text="сая төгрөг", secondary_y=False)
    fig.update_yaxes(title_text="Зарын тоо", secondary_y=True)

    chart_html = pio.to_html(fig, full_html=False)

    html_out = render_template(
        "index_v2.html",
        chart=chart_html,
        titles=titles,
        years=years,
        current_title=title_filter,
        current_year=year_filter
    )

    # ✨ Save rendered HTML into docs/index.html
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html_out)

    return html_out   # still serves dynamically in Flask
