import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import matplotlib.animation as animation
import math

# dominio coloreado
def domain_coloring(w):
    mag = np.abs(w)
    arg = np.angle(w)

    H = (arg + np.pi) / (2*np.pi)
    V = 1 / (1 + np.exp(-0.3 * np.log1p(mag)))
    S = np.ones_like(H)

    hsv = np.stack([H, S, V], axis=-1)
    rgb = hsv_to_rgb(hsv)
    rgb[~np.isfinite(rgb)] = 0
    return rgb

# animación
def make_animation(f, S, xlim, ylim, filename, frames=30):
    Nx, Ny = 400, 400
    x = np.linspace(*xlim, Nx)
    y = np.linspace(*ylim, Ny)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    img_f = domain_coloring(f(Z))

    fig, axes = plt.subplots(1, 2, figsize=(10,5))

    def update(N):
        for ax in axes:
            ax.clear()

        # izquierda
        axes[0].imshow(img_f, extent=[*xlim, *ylim], origin='lower', aspect='auto')
        axes[0].set_title("f(z)")
        axes[0].set_xticks(np.linspace(*xlim, 5))
        axes[0].set_yticks(np.linspace(*ylim, 5))

        # derecha
        W = S(Z, N+1)
        img_S = domain_coloring(W)

        axes[1].imshow(img_S, extent=[*xlim, *ylim], origin='lower', aspect='auto')
        axes[1].set_title(f"S_N(z), N={N+1}")
        axes[1].set_xticks(np.linspace(*xlim, 5))
        axes[1].set_yticks(np.linspace(*ylim, 5))

    plt.tight_layout()
    ani = animation.FuncAnimation(fig, update, frames=frames, interval=200)
    ani.save(filename, writer="pillow")
    print(f"Guardado: {filename}")