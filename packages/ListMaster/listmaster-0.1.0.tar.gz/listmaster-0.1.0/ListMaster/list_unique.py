def unique_elements(input_list):
    """
    Mengembalikan list hanya dengan elemen-elemen unik (tanpa duplikat).

    Args:
        input_list (list): List yang berisi elemen-elemen.

    Returns:
        list: List dengan elemen-elemen unik.
    """
    try:
        return list(set(input_list))
    except TypeError:
        print("Input harus berupa list yang berisi elemen-elemen yang bisa di-hash (seperti angka atau string).")
        return []


def sum_unique(input_list):
    """
    Mengembalikan jumlah dari semua elemen unik dalam list.

    Args:
        input_list (list): List yang berisi elemen-elemen.

    Returns:
        int/float: Jumlah dari elemen-elemen unik dalam list.
    """
    try:
        return sum(set(input_list))
    except TypeError:
        print("Input harus berupa list yang berisi elemen-elemen yang dapat dijumlahkan.")
        return 0


def unique_and_sort(input_list):
    """
    Mengembalikan elemen unik yang sudah diurutkan secara ascending.

    Args:
        input_list (list): List yang berisi elemen-elemen.

    Returns:
        list: List elemen unik yang diurutkan.
    """
    try:
        return sorted(set(input_list))
    except TypeError:
        print("Input harus berupa list yang berisi elemen-elemen yang bisa diurutkan.")
        return []


def get_duplicates(input_list):
    """
    Mengembalikan elemen-elemen yang duplikat dalam list (tidak unik).

    Args:
        input_list (list): List yang berisi elemen-elemen.

    Returns:
        list: List elemen-elemen yang duplikat.
    """
    try:
        seen = set()
        duplicates = set()
        for item in input_list:
            if item in seen:
                duplicates.add(item)
            else:
                seen.add(item)
        return list(duplicates)
    except TypeError:
        print("Input harus berupa list yang berisi elemen-elemen yang bisa di-hash (seperti angka atau string).")
        return []