import pandas as pd
import numpy as np
import plotly_express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def total_sunburst(data):
    fig = go.Figure(go.Sunburst(
        ids=data['ids'],
        parents=data['parents'],
        labels=data['labels'],
        values=data['value']
    ))
    fig.update_layout(
        title_text=data['title'],
        # Other layout customizations can be added here
    )
    fig.show()

def sankey(node_data, link_data):
    fig = go.Figure(go.Sankey(
        arrangement='snap',
        node=dict(
            label=node_data["label"],
            color=node_data["color"],
            pad=10,
            align="right",
        ),
        link=dict(
            arrowlen=15,
            source=link_data["source"],
            target=link_data["target"],
            value=link_data["value"],
            color=link_data["color"]
        )
    ))
    fig.show()

