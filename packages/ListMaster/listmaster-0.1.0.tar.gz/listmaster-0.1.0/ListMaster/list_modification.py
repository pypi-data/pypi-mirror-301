def gabungkan_list(*lists):
    """
    Menggabungkan sejumlah list menjadi satu list besar.

    Parameter:
    *lists: List
        Satu atau lebih list yang ingin digabungkan menjadi satu list besar.
    
    Returns:
    List
        List baru yang berisi semua elemen dari list-list yang diberikan.
    
    Raises:
    TypeError
        Jika salah satu parameter bukan list.
    """
    hasil = []
    try:
        for lst in lists:
            if not isinstance(lst, list):
                raise TypeError(f"Semua argumen harus berupa list, tetapi ditemukan {type(lst).__name__}")
            hasil.extend(lst)
    except TypeError as e:
        print(f"Terjadi kesalahan: {e}")
        return []
    
    return hasil

def gabungkan_tanpa_duplikat(*lists):
    """
    Menggabungkan sejumlah list menjadi satu list besar tanpa elemen duplikat.

    Parameter:
    *lists: List
        Satu atau lebih list yang ingin digabungkan menjadi satu list besar.
    
    Returns:
    List
        List baru yang berisi semua elemen dari list-list yang diberikan tanpa elemen duplikat.

    Raises:
    TypeError
        Jika salah satu parameter bukan list.
    """
    hasil = []
    try:
        for lst in lists:
            if not isinstance(lst, list):
                raise TypeError(f"Semua argumen harus berupa list, tetapi ditemukan {type(lst).__name__}")
            hasil.extend(lst)
    except TypeError as e:
        print(f"Terjadi kesalahan: {e}")
        return []

    return list(set(hasil))  # Menghapus duplikat dengan mengubah ke set lalu kembali ke list

def gabungkan_list_unik(*lists):
    """
    Menggabungkan sejumlah list menjadi satu list besar dan memastikan setiap elemen hanya muncul sekali.

    Parameter:
    *lists: List
        Satu atau lebih list yang ingin digabungkan menjadi satu list besar.
    
    Returns:
    List
        List baru yang berisi semua elemen dari list-list yang diberikan tanpa elemen duplikat, 
        dan urutan pertama kali elemen muncul tetap dipertahankan.

    Raises:
    TypeError
        Jika salah satu parameter bukan list.

    """
    hasil = []
    try:
        for lst in lists:
            if not isinstance(lst, list):
                raise TypeError(f"Semua argumen harus berupa list, tetapi ditemukan {type(lst).__name__}")
            for elemen in lst:
                if elemen not in hasil:  # Memastikan elemen hanya muncul sekali
                    hasil.append(elemen)
    except TypeError as e:
        print(f"Terjadi kesalahan: {e}")
        return []

    return hasil 