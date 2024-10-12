def filter_genap(list_angka):
    """
    Memfilter angka genap dari list.

    Args:
        list_angka (list): List yang berisi angka.

    Returns:
        list: List yang berisi angka genap.
    """
    list_genap = []
    try:
        for angka in list_angka:
            if angka % 2 == 0:
                list_genap.append(angka)
    except TypeError:
        print("Input harus berupa list yang berisi angka.")
    return list_genap


def filter_lebih_dari(list_angka, nilai):
    """
    Memfilter angka yang lebih besar dari nilai tertentu.

    Args:
        list_angka (list): List yang berisi angka.
        nilai: Nilai batas untuk filter.

    Returns:
        list: List yang berisi angka lebih besar dari nilai.
    """
    list_hasil = []
    try:
        for angka in list_angka:
            if angka > nilai:
                list_hasil.append(angka)
    except TypeError:
        print("Input harus berupa list yang berisi angka.")
    return list_hasil


def filter_habis_dibagi(list_angka, pembagi):
    """
    Memfilter angka yang habis dibagi oleh pembagi tertentu.

    Args:
        list_angka (list): List yang berisi angka.
        pembagi: Angka yang digunakan sebagai pembagi.

    Returns:
        list: List yang berisi angka yang habis dibagi oleh pembagi.
    """
    list_hasil = []
    try:
        for angka in list_angka:
            if angka % pembagi == 0:
                list_hasil.append(angka)
    except TypeError:
        print("Input harus berupa list yang berisi angka.")
    return list_hasil


def filter_mengandung(list_string, substring):
    """
    Memfilter string yang mengandung substring tertentu.

    Args:
        list_string (list): List yang berisi string.
        substring (str): Substring yang dicari dalam string.

    Returns:
        list: List yang berisi string yang mengandung substring.
    """
    list_hasil = []
    try:
        for string in list_string:
            if substring in string:
                list_hasil.append(string)
    except TypeError:
        print("Input harus berupa list yang berisi string.")
    return list_hasil

