import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import random

# "solutions.txt" dosyasından çözümleri oku
def read_solutions(file_path):
    solutions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    board = []
    for line in lines + ['']:  # Son satırı da işlemek için boş satır ekle
        if line.strip() == '':
            if board:
                solutions.append(''.join(board))
                board = []
        else:
            board.append(line)
    return solutions

# Çözüm stringini 5×11 boyutunda bir grid (karakter matrisi) haline getir
def solution_to_grid(solution_str):
    grid = np.full((5, 11), fill_value='.', dtype='<U1')
    for idx, ch in enumerate(solution_str):
        row = idx // 11
        col = idx % 11
        grid[row, col] = ch
    return grid

# Her parçayı (A–L) resimdeki renk kodlarına uygun şekilde tanımlıyoruz:
piece_colors = {
    'A': "#FFD700",  # Parça #1 (sarı)
    'B': "#FF8C00",  # Parça #2 (turuncu)
    'C': "#FF0000",  # Parça #3 (kırmızı)
    'D': "#B22222",  # Parça #4 (koyu kırmızı)
    'E': "#FF69B4",  # Parça #5 (pembe)
    'F': "#800080",  # Parça #6 (mor)
    'G': "#00008B",  # Parça #7 (lacivert)
    'H': "#1E90FF",  # Parça #8 (açık mavi)
    'I': "#ADD8E6",  # Parça #9 (bebe mavisi/aydın mavi)
    'J': "#7FFFD4",  # Parça #10 (teal/akvamarin)
    'K': "#228B22",  # Parça #11 (yeşil)
    'L': "#ADFF2F",  # Parça #12 (lime yeşili)
}

# Çözümleri oku
solutions = read_solutions('solutions.txt')

if len(solutions) == 0:
    print("Uyarı: 'solutions.txt' içinde hiç çözüm bulunamadı veya dosya boş.")
    exit(1)

# Rastgele 100 çözüm seç (eğer toplam < 100 ise tümünü seç)
count_to_show = 100
if len(solutions) < count_to_show:
    selected_solutions = solutions[:]  # tüm çözümler
else:
    selected_solutions = random.sample(solutions, count_to_show)

num_to_show = len(selected_solutions)

# Kaç satır × sütun grid gerekli, kabaca kare yakın bir düzen kuralım
grid_cols = 10
grid_rows = (num_to_show + grid_cols - 1) // grid_cols  # tam bölen yoksa bir satır daha

fig, axes = plt.subplots(grid_rows, grid_cols, figsize=(grid_cols * 2, grid_rows * 1.5), dpi=100)
axes = axes.flatten()  # 1D liste olarak erişmek için

for idx, ax in enumerate(axes):
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_aspect('equal')
    ax.grid(False)

    if idx < num_to_show:
        sol = selected_solutions[idx]
        grid = solution_to_grid(sol)
        patches = []
        colors = []
        # 5×11 grid içinde her hücre için daire yarat
        for r in range(5):
            for c in range(11):
                ch = grid[r, c]
                if ch != '.':
                    circ = Circle((c, 4 - r), radius=0.45)  # y eksenini ters çevir
                    patches.append(circ)
                    colors.append(piece_colors[ch])
        collection = PatchCollection(patches, facecolors=colors, edgecolors='black', linewidths=0.3)
        ax.add_collection(collection)

    else:
        # Gösterime dahil olmayan eksik hücreler için boş bırak
        ax.axis('off')

# Sadece alt kenarda legend olarak parça renklerini ekleyelim
legend_patches = [
    plt.Line2D([0], [0], marker='o', color='w',
               markerfacecolor=piece_colors[chr(ord('A') + i)],
               markersize=6, label=chr(ord('A') + i))
    for i in range(12)
]
fig.legend(handles=legend_patches, loc='upper center', ncol=6, bbox_to_anchor=(0.5, -0.02))

plt.tight_layout()
plt.subplots_adjust(bottom=0.05)  # legend için biraz boşluk ayarları
plt.show()
