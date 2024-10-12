def bubble_sort(arr, reverse=False):
    """
    Mengurutkan array menggunakan algoritma Bubble Sort. Algoritma ini membandingkan 
    elemen-elemen berdekatan dan menukarnya jika mereka dalam urutan yang salah. 
    Proses ini diulangi sampai daftar terurut.

    Args:
        arr (list): List yang akan diurutkan.
        reverse (bool): Jika True, mengurutkan dalam urutan descending (menurun). 
                        Jika False, mengurutkan dalam urutan ascending (menaik).    
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if (arr[j] > arr[j+1] and not reverse) or (arr[j] < arr[j+1] and reverse):
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def selection_sort(arr, reverse=False):
    """
    Mengurutkan array menggunakan algoritma Selection Sort. Algoritma ini menemukan
    elemen terkecil (atau terbesar) di list yang tidak terurut, kemudian menukarnya
    dengan elemen pada posisi awal yang belum terurut. Proses ini diulangi untuk setiap posisi.

    Args:
        arr (list): List yang akan diurutkan.
        reverse (bool): Jika True, mengurutkan dalam urutan descending (menurun). 
                        Jika False, mengurutkan dalam urutan ascending (menaik).    
    """
    n = len(arr)
    for i in range(n):
        idx = i
        for j in range(i+1, n):
            if (arr[j] < arr[idx] and not reverse) or (arr[j] > arr[idx] and reverse):
                idx = j
        arr[i], arr[idx] = arr[idx], arr[i]
    return arr


def insertion_sort(arr, reverse=False):
    """
    Mengurutkan array menggunakan algoritma Insertion Sort. Algoritma ini bekerja dengan membagi
    array menjadi bagian terurut dan tidak terurut. Setiap elemen dari bagian yang tidak terurut 
    dipilih dan dimasukkan pada posisi yang benar di bagian terurut.

    Args:
        arr (list): List yang akan diurutkan.
        reverse (bool): Jika True, mengurutkan dalam urutan descending (menurun). 
                        Jika False, mengurutkan dalam urutan ascending (menaik).    
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and ((key < arr[j] and not reverse) or (key > arr[j] and reverse)):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# Timsort (bawaan Python)
def tim_sort(arr, reverse=False):
    arr.sort(reverse=reverse)
    return arr