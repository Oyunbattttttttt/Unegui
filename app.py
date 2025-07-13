from flask import Flask, render_template
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio

app = Flask(__name__)

@app.route("/")
def index():
    # 📂 Load Excel data
    file_path = 'excel_chart_web/2025.xlsx'

    df = pd.read_excel(file_path)

    # ✅ Normalize date to strip time
    df['date_clean'] = pd.to_datetime(df['date_clean'], errors='coerce').dt.date

    # 🧹 Drop rows with missing values
    df = df.dropna(subset=['price', 'date_clean'])

    # ✅ Convert to million tögrөгs
    df['price'] = df['price'] / 1000000

    # 📅 Group by date
    daily = df.groupby('date_clean').agg({
    'price': 'median',
    'id': 'count'  # count of ads
    }).rename(columns={'id': 'count'}).reset_index()

    # 📈 Rolling averages
    daily['7-day'] = daily['price'].rolling(7).mean()
    daily['30-day'] = daily['price'].rolling(30).mean()


    # 📊 Create chart with subplots
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Scatter plot of daily prices
    fig.add_trace(go.Scatter(
        x=daily['date_clean'], y=daily['price'],
        mode='markers',
        name='Тухайн өдөр',
        marker=dict(color='gray', size=6)
    ))

    # 7-day moving average
    fig.add_trace(go.Scatter(
        x=daily['date_clean'], y=daily['7-day'],
        mode='lines', name='Сүүлийн 7 хоног',
        line=dict(color='black', width=2)
    ))

    # 30-day moving average (dotted)
    fig.add_trace(go.Scatter(
        x=daily['date_clean'], y=daily['30-day'],
        mode='lines', name='Сүүлийн 30 хоног',
        line=dict(color='black', width=2, dash='dot')
    ))

    # Bar chart for count of listings
    fig.add_trace(go.Bar(
        x=daily['date_clean'], y=daily['count'],
        name='Зарын тоо',
        marker=dict(color='lightgray'),
        opacity=0.6
    ), secondary_y=True)

    # 🖋️ Layout settings
    fig.update_layout(
        title="🚗 Машины үнэ (медиан сая.₮)",
        template="simple_white",
        hovermode="x unified",
        legend=dict(orientation="h", y=-0.3),
        height=600
    )

    fig.update_yaxes(title_text="сая төгрөг", secondary_y=False)
    fig.update_yaxes(title_text="Зарын тоо", secondary_y=True)

    # 🔄 Convert to HTML
    chart_html = pio.to_html(fig, full_html=False)

    return render_template("index.html", chart=chart_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

