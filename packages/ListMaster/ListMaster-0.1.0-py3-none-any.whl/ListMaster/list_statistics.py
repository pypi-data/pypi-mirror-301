def rata_rata(target_list):
    """Menghitung rata-rata dari elemen numerik dalam list."""
    if not all(isinstance(i, (int, float)) for i in target_list):
        raise ValueError("List harus berisi angka.")
    
    if len(target_list) == 0:  # Cek apakah list kosong
        return 0  # Kembalikan 0 jika list kosong
    
    total = sum(target_list)
    count = len(target_list)
    return total / count

def median(target_list):
    """Menghitung median dari elemen numerik dalam list."""
    if not all(isinstance(i, (int, float)) for i in target_list):
        raise ValueError("List harus berisi angka.")
    
    sorted_list = sorted(target_list)
    n = len(sorted_list)
    
    if n == 0:  # Cek apakah list kosong
        return 0  # Kembalikan 0 jika tidak ada elemen
    
    mid = n // 2
    if n % 2 == 0:
        return (sorted_list[mid - 1] + sorted_list[mid]) / 2
    else:
        return sorted_list[mid]

def min_max(target_list):
    """Mengembalikan nilai minimum dan maksimum dari elemen numerik dalam list."""
    if len(target_list) == 0:
        raise ValueError("List tidak boleh kosong.")
    
    if not all(isinstance(i, (int, float)) for i in target_list):
        raise ValueError("List harus berisi angka.")
    
    minimum = min(target_list)
    maksimum = max(target_list)
    return minimum, maksimum

def modus(target_list):
    """Menghitung modus dari elemen dalam list."""
    if len(target_list) == 0:
        raise ValueError("List tidak boleh kosong.")
    
    frekuensi = {}
    for elemen in target_list:
        frekuensi[elemen] = frekuensi.get(elemen, 0) + 1
        
    max_freq = max(frekuensi.values())
    modus_list = [k for k, v in frekuensi.items() if v == max_freq]
    
    if len(modus_list) < len(frekuensi):
        return modus_list
    else:
        return "Tidak ada modus (semua elemen muncul dengan frekuensi yang sama)."