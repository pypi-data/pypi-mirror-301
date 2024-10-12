def is_sorted(arr):  
    """  
    Fungsi untuk memeriksa apakah list diurutkan secara ascending (menaik).  
    
    :param arr: List yang akan diperiksa.  
    :return: True jika list diurutkan, False jika tidak.  
    """  
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))  

def linear_search(arr, target):  
    """  
    Pencarian linear untuk menemukan semua kemunculan target dalam list.  
    
    :param arr: List elemen yang akan dicari.  
    :param target: Elemen yang dicari.  
    :return: List indeks di mana target ditemukan, atau list kosong jika tidak ditemukan.  
    """  
   
    if not isinstance(arr, list):  
        raise ValueError("Argumen pertama harus berupa list.")  
  
    indices = []  

    for i, elem in enumerate(arr):  
        if elem == target:  
            indices.append(i)  

    return indices  

def binary_search(arr, target):
    """
    Pencarian biner untuk menemukan semua kemunculan target dalam list yang terurut.
    List harus diurutkan secara ascending (menaik).
    
    :param arr: List yang sudah diurutkan untuk pencarian.
    :param target: Elemen yang dicari.
    :return: List indeks di mana target ditemukan, atau list kosong jika tidak ditemukan.
    """
    
    if not isinstance(arr, list):
        raise ValueError("Argumen pertama harus berupa list.")
    
    if not is_sorted(arr):
        raise ValueError("List harus diurutkan secara ascending untuk pencarian biner.")

    indices = []

    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        
        if arr[mid] == target:
            
            left = mid
            while left >= 0 and arr[left] == target:
                left -= 1
            
            
            right = mid
            while right < len(arr) and arr[right] == target:
                right += 1

            
            indices.extend(range(left + 1, right))
            break 
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return indices
