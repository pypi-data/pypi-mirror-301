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


def merge_sort(arr, reverse=False):
    """
    Mengurutkan array menggunakan algoritma Merge Sort. Algoritma ini menggunakan pendekatan 
    "divide and conquer" dengan membagi list menjadi dua bagian, mengurutkan setiap bagian secara 
    rekursif, lalu menggabungkannya kembali.

    Args:
        arr (list): List yang akan diurutkan.
        reverse (bool): Jika True, mengurutkan dalam urutan descending (menurun). 
                        Jika False, mengurutkan dalam urutan ascending (menaik).
    """
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L, reverse=reverse)
        merge_sort(R, reverse=reverse)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if (L[i] < R[j] and not reverse) or (L[i] > R[j] and reverse):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr


def quick_sort(arr, reverse=False):
    """
    Mengurutkan array menggunakan algoritma Quick Sort. Quick Sort memilih elemen yang disebut "pivot", 
    kemudian mempartisi list sehingga elemen-elemen yang lebih kecil dari pivot ada di kiri, dan yang
    lebih besar ada di kanan. Algoritma ini kemudian diterapkan secara rekursif pada setiap bagian.

    Args:
        arr (list): List yang akan diurutkan.
        reverse (bool): Jika True, mengurutkan dalam urutan descending (menurun). 
                        Jika False, mengurutkan dalam urutan ascending (menaik).
    """
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        if reverse:
            left = [x for x in arr if x > pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x < pivot]
        else:
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]
        return quick_sort(left, reverse) + middle + quick_sort(right, reverse)

# Timsort (bawaan Python)
def tim_sort(arr, reverse=False):
    arr.sort(reverse=reverse)
    return arr