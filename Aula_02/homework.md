---
authors:
- Filipe Fernandes
date: '15-Agosto-2013'
title: Dever de casa 00
...

1) Equação de onda
==================

Usando a equação $y = A \cos(\omega t - kz + \phi)$ produza 5 gráficos:

* $x = 0$, onda fixa num ponto no espaço;
* $t = 0$, uma "fotografia de uma onda".  Faça essa onda coincidir com a anterior;
* Escolha um dos gráficos acima e varie a sua fase para: 90$^\circ$, 180$^\circ$, e 270$^\circ$.


$y = A \cos(\omega t - kx + \phi)$

$T = \frac{1}{f} = \frac{2\pi}{\omega} \rightarrow \left[\text{s} \right] $

$\text{L ou } \lambda = \frac{2\pi}{k} \rightarrow \left[ \text{m} \right]$


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python .numberLines}
import matplotlib.pyplot as plt

def adjust_spines(ax, spines):
    """http://matplotlib.org/examples/pylab_examples/spine_placement_demo.html"""
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 10))
            spine.set_smart_bounds(True)
        else:
            spine.set_color('none')

    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        ax.yaxis.set_ticks([])
    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        ax.xaxis.set_ticks([])

twopi = 2 * np.pi

n = 2  # Duas ondas.
A = 2  # Amplitude = 2 metros.
w = twopi / 10  # T = 10 segundos.
k = twopi / 200  # lambda = 200 metros.
phi = np.deg2rad(180)  # Fase [rad]
t = np.arange(0, 10 * n, 0.01)  # Vetor tempo [s]
x = np.arange(0, 200 * n)  # Vetor espaço [m]

y1 = A * np.cos(w * t - k * 0 + phi)  # Um ponto do oceano.
y2 = A * np.cos(w * 0 - k * x + phi)  # Uma "foto" de um instante.

fig, (ax0, ax1) = plt.subplots(nrows=2, sharey=True, figsize=(6, 4))
fig.tight_layout()
ax0.set_ylim([-2.1, 2.1])

ax0.plot(t, y1, linewidth='2', color='#CC9900')
ax0.axhline(color='grey')
adjust_spines(ax0, ['left','bottom'])

ax1.plot(x, y2, linewidth='2', color='#99CC33')
ax1.axhline(color='grey')
adjust_spines(ax1, ['left','bottom'])

_ = plt.figtext(0, 0.5, 'Amplitude [m]', ha='right', va='center', rotation=90)
_ = plt.figtext(1.01, 0.5, u'Período [s]', color='#CC9900')
_ = plt.figtext(1.01, 0.05, u'Distância [m]', color='#99CC33')
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


![Solução](./time_space_wave.pdf)


[nbviewer.](http://nbviewer.ipython.org/urls/raw.github.com/o
cefpaf/waves_and_tides/master/Aula_02/time_space_wave.ipynb)
