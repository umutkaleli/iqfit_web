# app.py
import io
import random
import base64

from flask import Flask, render_template, request
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection

app = Flask(__name__)

def read_solutions(file_path):
    solutions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    board = []
    for line in lines + ['']:
        if line.strip() == '':
            if board:
                solutions.append(''.join(board))
                board = []
        else:
            board.append(line)
    return solutions

def solution_to_grid(solution_str):
    grid = np.full((5, 11), fill_value='.', dtype='<U1')
    for idx, ch in enumerate(solution_str):
        r = idx // 11
        c = idx % 11
        grid[r, c] = ch
    return grid

piece_colors = {
    'A': "#FFD700", 'B': "#FF8C00", 'C': "#FF0000", 'D': "#B22222",
    'E': "#FF69B4", 'F': "#800080", 'G': "#00008B", 'H': "#1E90FF",
    'I': "#ADD8E6", 'J': "#7FFFD4", 'K': "#228B22", 'L': "#ADFF2F",
}

@app.route("/")
def index():
    # Burada dosya adını "solutions3.txt" olarak değiştirdik:
    all_sols = read_solutions("solutions3.txt")
    if not all_sols:
        return "<h2>Çözüm bulunamadı.</h2>"

    # Eğer query param “random” varsa rastgele 9 seç, yoksa ilk 9’u al
    if request.args.get("random"):
        if len(all_sols) <= 9:
            selected = all_sols[:]
        else:
            selected = random.sample(all_sols, 9)
    else:
        selected = all_sols[:9]

    num = len(selected)  # genellikle 9
    rows, cols = 3, 3

    # Burada figsize’i büyüttük: sütun başına 3 inch, satır başına 2 inch
    fig, axes = plt.subplots(rows, cols,
                             figsize=(cols * 3, rows * 2),
                             dpi=100)

    axes = np.array(axes).reshape(-1)

    for i, ax in enumerate(axes):
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlim(-0.5, 10.5); ax.set_ylim(-0.5, 4.5)
        ax.set_aspect('equal'); ax.grid(False)
        if i < num:
            grid = solution_to_grid(selected[i])
            patches, colors = [], []
            for r in range(5):
                for c in range(11):
                    ch = grid[r, c]
                    if ch != '.':
                        circ = Circle((c, 4 - r), radius=0.45)
                        patches.append(circ)
                        colors.append(piece_colors[ch])
            coll = PatchCollection(patches, facecolors=colors, edgecolors='black', linewidths=0.3)
            ax.add_collection(coll)
        else:
            ax.axis('off')

    legend_patches = [
        plt.Line2D([0], [0], marker='o', color='w',
                   markerfacecolor=piece_colors[chr(ord('A') + i)],
                   markersize=6, label=chr(ord('A') + i))
        for i in range(12)
    ]
    fig.legend(handles=legend_patches,
               loc='upper center',
               ncol=6,
               bbox_to_anchor=(0.5, -0.02))

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.1)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return render_template("index.html", img_data=img)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
