import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import layout
from bokeh.models import Slider, Div, ColumnDataSource
import scipy.integrate as spi

def SIR_model(y, t, beta, gamma, N):
    S, I, R = y
    dSdt = (-beta / N) * I * S
    dIdt = (beta / N) * I * S - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

beta = 0.2
gamma = 0.6
N = 1000
I0 = 100
R0 = 1
S0 = N - I0 - R0
t_max = 100
dt = 1

y0 = S0, R0, I0
t_range = np.arange(0, t_max, dt)
result = spi.odeint(SIR_model, y0, t_range, args=(beta, gamma, N))
sus = result[:, 0]
infected = result[:, 1]
removed = result[:, 2]

source = ColumnDataSource(data=dict(t=t_range, sus=sus, infected=infected, removed=removed))

fig = figure(title='SIR model', x_axis_label='t(dni)', y_axis_label='ilość ludzi', width=800, height=400)
fig.line('t', 'sus', source=source, legend_label='S(t)', line_width=2, line_color='blue')
fig.line('t', 'infected', source=source, legend_label='I(t)', line_width=2, line_color='red')
fig.line('t', 'removed', source=source, legend_label='R(t)', line_width=2, line_color='green')

s1 = Slider(title='beta', value=0.5, start=0.01, end=1, step=0.01)
s2 = Slider(title='gamma', value=0.5, start=0.01, end=1, step=0.01)
s3 = Slider(title='Initial I', value=I0, start=0, end=N, step=1)

div = Div(text="<h1>Model SIR</h1>")

def update(attr, old, new):
    beta = s1.value
    gamma = s2.value
    I0 = s3.value
    S0 = N - I0 - R0
    y0 = S0, I0, R0

    t_range = np.arange(0, t_max, dt)
    result = spi.odeint(SIR_model, y0, t_range, args=(beta, gamma, N))
    sus = result[:, 0]
    infected = result[:, 1]
    removed = result[:, 2]

    source.data = dict(t=t_range, sus=sus, infected=infected, removed=removed)

s1.on_change('value', update)
s2.on_change('value', update)
s3.on_change('value', update)


curdoc().add_root(layout([[div], [fig], [s1, s2, s3]])) # jak macierz

# bokeh serve projekt09/projekt09.py