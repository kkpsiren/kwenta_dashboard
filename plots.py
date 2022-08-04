import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st

def plot_bar(df,x0='TOTAL_AMOUNT'):
    random_x = df['NAME'].tolist()
    random_y0 = df[x0].tolist()

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=random_x, y=random_y0,opacity=0.5,
                        #mode='lines',
                        name=x0.capitalize().replace('_', ' ')),secondary_y=False)
    # fig.add_trace(go.Scatter(x=random_x, y=random_y1,opacity=0.5,
    #                     mode='lines',
    #                     name=x1.capitalize().replace('_', ' ')),secondary_y=False)
# 
    # fig.update_yaxes(title_text="New Addresses", secondary_y=True)
    # fig.update_yaxes(title_text="Total Addresses", secondary_y=False)
    # fig.update_layout(hovermode="x")
    # fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
# 
    # fig.update_layout(barmode='stack', bargap=0.0,bargroupgap=0.0)
    # fig.update_traces(marker_line_width=0)

    return fig
