import scipy.integrate as spi
import matplotlib.pyplot as plt
import numpy as np


# S - populacja zdrowa
# I - populacja zarażona
# R - populacja ozdrowiała/umarła
# beta - współczynnik zarażania
# gamma - współczynnik zdrowienia


def SIR_model(y, t, beta, gamma, N):
    S, I, R = y
    dSdt = (-beta / N) * I * S
    dIdt = (beta / N) * I * S - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt


beta = 0.6  # wsp zakazenia
gamma = 0.1  # wsp zdrowienia
N = 100 # ile ludzi
I0 = 13  # ile na poczatku chorych
R0 = 5  # ile na poczarku removed
S0 = N - I0 - R0
t_max = 100 # ile dni
dt = 1 # krok czasowy 1 dzien


y0 = S0, R0, I0  # warunki poczatkowe
t_range = np.arange(0, t_max, dt)
result = spi.odeint(SIR_model, y0, t_range, args=(beta, gamma, N))

plt.plot(t_range, result[:, 0], label='S(t)')  # zdrowi
plt.plot(t_range, result[:, 1], label='I(t)')  # zarażeni
plt.plot(t_range, result[:, 2], label='R(t)')  # removed
plt.legend(loc='best')
plt.xlabel('t(dni)')
plt.ylabel('ilość ludzi')
plt.title('model SIR')
plt.show()
