# app.py
import os
import random
import hashlib

from flask import Flask, render_template, request, send_from_directory
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection

app = Flask(__name__)

# Uygulama ayağa kalkarken çözümleri bir kez belleğe alalım
ALL_SOLUTIONS = []
def load_solutions():
    global ALL_SOLUTIONS
    path = "solutions3.txt"
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    board = []
    for line in lines + ['']:
        if line.strip() == '':
            if board:
                ALL_SOLUTIONS.append("".join(board))
                board = []
        else:
            board.append(line)
    print(f"[INFO] {len(ALL_SOLUTIONS)} çözümler yüklendi.")

# Her parça için renk tanımları
piece_colors = {
    'A': "#FFD700", 'B': "#FF8C00", 'C': "#FF0000", 'D': "#B22222",
    'E': "#FF69B4", 'F': "#800080", 'G': "#00008B", 'H': "#1E90FF",
    'I': "#ADD8E6", 'J': "#7FFFD4", 'K': "#228B22", 'L': "#ADFF2F",
}

def solution_to_grid(solution_str):
    grid = np.full((5, 11), fill_value='.', dtype='<U1')
    for idx, ch in enumerate(solution_str):
        r = idx // 11
        c = idx % 11
        grid[r, c] = ch
    return grid

# Cache klasöründen PNG servis et
@app.route('/cached/<filename>')
def serve_cached(filename):
    return send_from_directory('cache', filename)

@app.route("/")
def index():
    if not ALL_SOLUTIONS:
        return "<h2>Çözüm bulunamadı.</h2>"

    # “random=1” parametresi varsa rastgele 9 seç, yoksa ilk 9
    if request.args.get("random"):
        if len(ALL_SOLUTIONS) <= 9:
            selected = ALL_SOLUTIONS[:]
        else:
            selected = random.sample(ALL_SOLUTIONS, 9)
    else:
        selected = ALL_SOLUTIONS[:9]

    # Seçilen 9 çözüme ait indeks listesini çıkar (ilk 9 için indices=0..8)
    indices = [ALL_SOLUTIONS.index(sol) for sol in selected]
    # Hash key: indeks listesini "_" ile birleştirip sha256 al
    key_raw = "_".join(map(str, indices))
    key = hashlib.sha256(key_raw.encode('utf-8')).hexdigest()
    cached_filename = f"{key}.png"
    cached_path = os.path.join("cache", cached_filename)

    # Eğer önceden üretilmiş varsa, tekrar üretme
    if not os.path.exists(cached_path):
        # 3×3 ızgara olarak çiz
        rows, cols = 3, 3
        fig, axes = plt.subplots(rows, cols,
                                 figsize=(cols * 3, rows * 2),
                                 dpi=100)
        axes = np.array(axes).reshape(-1)
        for i, ax in enumerate(axes):
            ax.set_xticks([]); ax.set_yticks([])
            ax.set_xlim(-0.5, 10.5); ax.set_ylim(-0.5, 4.5)
            ax.set_aspect('equal'); ax.grid(False)
            if i < len(selected):
                grid = solution_to_grid(selected[i])
                patches, colors = [], []
                for r in range(5):
                    for c in range(11):
                        ch = grid[r, c]
                        if ch != '.':
                            circ = Circle((c, 4 - r), radius=0.45)
                            patches.append(circ)
                            colors.append(piece_colors[ch])
                coll = PatchCollection(patches,
                                       facecolors=colors,
                                       edgecolors='black',
                                       linewidths=0.3)
                ax.add_collection(coll)
            else:
                ax.axis('off')

        # Legend ekle
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

        # PNG’yi cache klasörüne kaydet
        fig.savefig(cached_path, format="png", bbox_inches="tight")
        plt.close(fig)

    # HTML içinde resim için "/cached/<key>.png" yolunu döndür
    img_url = f"/cached/{cached_filename}"
    return render_template("index.html", img_url=img_url)

if __name__ == "__main__":
    # Uygulama başında çözümleri yükle
    load_solutions()
    os.makedirs("cache", exist_ok=True)
    app.run(host="0.0.0.0", port=5001, debug=True)
