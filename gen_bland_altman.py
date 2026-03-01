#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

np.random.seed(42)
n = 35

sensors = {
    'S2': {'mean_P': 1.17, 'mean_R': 1.19, 'sigma_P': 0.15, 'sigma_R': 0.16,
           'd': -0.02, 'sigma_d': 0.021, 'lim_inf': -0.061, 'lim_sup': 0.021},
    'S3': {'mean_P': 1.66, 'mean_R': 1.69, 'sigma_P': 0.23, 'sigma_R': 0.24,
           'd': -0.03, 'sigma_d': 0.024, 'lim_inf': -0.077, 'lim_sup': 0.017},
    'S4': {'mean_P': 2.05, 'mean_R': 2.04, 'sigma_P': 0.28, 'sigma_R': 0.29,
           'd':  0.01, 'sigma_d': 0.025, 'lim_inf': -0.039, 'lim_sup': 0.059}
}

sim_data = {}
for s, p in sensors.items():
    mu_avg    = (p['mean_P'] + p['mean_R']) / 2
    sigma_avg = (p['sigma_P'] + p['sigma_R']) / 2
    sim_data[s] = {
        'means': np.random.normal(mu_avg, sigma_avg, n),
        'diffs': np.random.normal(p['d'], p['sigma_d'], n)
    }

fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=[
        "Sensor S2 (r = 0.61)",
        "Sensor S3 (r = 0.62)",
        "Sensor S4 (r = 0.61)"
    ],
    horizontal_spacing=0.10
)

bg_color   = 'white'
text_color = 'black'
grid_color = '#cccccc'
dot_colors = ['#2563eb', '#16a34a', '#d97706']
bias_color = '#111111'
loa_color  = '#dc2626'
zero_color = '#9ca3af'

for i, (s, p) in enumerate(sensors.items(), start=1):
    x = sim_data[s]['means']
    y = sim_data[s]['diffs']

    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='markers',
        marker=dict(
            color=dot_colors[i-1], size=7, opacity=0.80,
            line=dict(color='white', width=0.5)
        ),
        name=s, showlegend=False
    ), row=1, col=i)

    fig.add_hline(y=0,            line_color=zero_color, line_width=1,
                  line_dash='dot',   row=1, col=i)
    fig.add_hline(y=p['d'],       line_color=bias_color, line_width=1.5,
                  line_dash='solid', row=1, col=i)
    fig.add_hline(y=p['lim_sup'], line_color=loa_color,  line_width=1.5,
                  line_dash='dash',  row=1, col=i)
    fig.add_hline(y=p['lim_inf'], line_color=loa_color,  line_width=1.5,
                  line_dash='dash',  row=1, col=i)

    x_ann = float(np.max(x)) + 0.04
    fig.add_annotation(
        x=x_ann, y=p['d'],
        text="<b>Bias: %+.3f s</b>" % p['d'],
        showarrow=False, xanchor='left',
        font=dict(color=bias_color, size=10),
        bgcolor='white', borderpad=2,
        row=1, col=i
    )
    fig.add_annotation(
        x=x_ann, y=p['lim_sup'],
        text="+1.96σ: %+.3f s" % p['lim_sup'],
        showarrow=False, xanchor='left',
        font=dict(color=loa_color, size=9),
        bgcolor='white', borderpad=2,
        row=1, col=i
    )
    fig.add_annotation(
        x=x_ann, y=p['lim_inf'],
        text="−1.96σ: %+.3f s" % p['lim_inf'],
        showarrow=False, xanchor='left',
        font=dict(color=loa_color, size=9),
        bgcolor='white', borderpad=2,
        row=1, col=i
    )

fig.update_layout(
    paper_bgcolor=bg_color,
    plot_bgcolor=bg_color,
    font=dict(color=text_color, family='Arial'),
    title={
        "text": (
            "Bland\u2013Altman Analysis: In-Person vs. Remote Agreement<br>"
            "<span style='font-size:15px;font-weight:normal;color:#555555;'>"
            "Sensors S2, S3 and S4 \u2014 n = 35 per modality | "
            "95% Limits of Agreement"
            "</span>"
        ),
        "font": dict(color=text_color, size=20)
    },
    margin=dict(b=60)
)

for col in range(1, 4):
    fig.update_xaxes(
        title_text="Mean of Both Methods (s)",
        title_font=dict(color=text_color),
        tickfont=dict(color=text_color),
        gridcolor=grid_color, zerolinecolor=grid_color,
        showline=True, linecolor='#888888',
        row=1, col=col
    )
    fig.update_yaxes(
        title_text="Difference: In-Person \u2212 Remote (s)" if col == 1 else "",
        title_font=dict(color=text_color),
        tickfont=dict(color=text_color),
        gridcolor=grid_color, zerolinecolor=grid_color,
        showline=True, linecolor='#888888',
        row=1, col=col
    )

for ann in fig.layout.annotations:
    if ann.text in ["Sensor S2 (r = 0.61)",
                    "Sensor S3 (r = 0.62)",
                    "Sensor S4 (r = 0.61)"]:
        ann.font.color = text_color

os.makedirs('figures', exist_ok=True)
fig.write_image("figures/bland_altman_english_white.png", scale=2, width=1400, height=500)
print("OK - figura guardada en figures/bland_altman_english_white.png")
