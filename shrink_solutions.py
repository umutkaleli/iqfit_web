import os
import random

def read_solutions(file_path):
    """
    solutions.txt içindeki tüm çözümleri liste halinde döner.
    Her çözüm 5 satır × 11 sütun + ardından bir boş satır (ayırıcı) içerir.
    """
    solutions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        current = []
        for line in f:
            if line.strip() == "":
                if current:
                    solutions.append("".join(current))
                    current = []
            else:
                current.append(line)
        if current:
            solutions.append("".join(current))
    return solutions

def write_solutions(solutions, output_path):
    """
    Verilen çözümleri (string listesi) output_path dosyasına yazar.
    Her çözümün sonuna bir boş satır koyar.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for sol in solutions:
            f.write(sol)
            f.write("\n")

if __name__ == "__main__":
    inp = "solutions.txt"
    outp = "solutions_shrunk.txt"
    max_bytes = 40 * 1024 * 1024  # 40 MB

    orig_size = os.path.getsize(inp)
    print(f"Orijinal solutions.txt boyutu: {orig_size / (1024*1024):.2f} MB")

    all_sols = read_solutions(inp)
    total = len(all_sols)
    print(f"Toplam çözüm sayısı: {total}")

    if orig_size <= max_bytes:
        print("Dosya zaten 40 MB’ın altında. Küçültmeye gerek yok.")
        write_solutions(all_sols, outp)
        print(f"Dosya kopyalandı: {outp}")
    else:
        avg_sol_size = orig_size / total
        keep_count = int(max_bytes / avg_sol_size)
        keep_count = max(1, keep_count - 5)  # Bir miktar daha azaltarak güvenli tutar
        print(f"Tahmini olarak her çözüm ~{avg_sol_size/1024:.1f} KB.")
        print(f"40 MB sınırı için yaklaşık {keep_count} çözüm saklanacak.")

        if keep_count >= total:
            selected = all_sols[:]
        else:
            selected = random.sample(all_sols, keep_count)

        write_solutions(selected, outp)

        new_size = os.path.getsize(outp)
        print(f"Yeni dosya ({outp}) boyutu: {new_size / (1024*1024):.2f} MB")
        if new_size > max_bytes:
            print("UYARI: Hâlâ 40 MB üstünde. Daha az çözüm seçmeyi deneyin.")
        else:
            print(f"Başarı: '{outp}' dosyası artık 40 MB altında.")
