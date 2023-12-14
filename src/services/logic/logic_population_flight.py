import pandas as pd
import plotly.graph_objects as go


def create_plot(popular_flights):
    df = pd.DataFrame(popular_flights, columns=['Departure Airport', 'Arrival Airport', 'Tickets Sold'])

    df = df.sort_values(by='Tickets Sold', ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df['Tickets Sold'],
        x=df['Departure Airport'] + ' to ' + df['Arrival Airport'],
        orientation='v',
        marker=dict(color='#636efa'),
        hovertemplate='Tickets Sold=%{y}<br>Route=%{x}<extra></extra>',
        textposition='auto',
    ))

    fig.update_layout(
        title='Top 10 Popular Flights',
        xaxis_title='Route',
        yaxis_title='Tickets Sold',
    )

    fig.update_traces(
        type='bar',
        hoverinfo='text',
        hovertext='Tickets Sold=%{y}<br>Route=%{x}',
        marker=dict(color='#636efa'),
    )
    return fig
