
def lin_search (arr, x):
    for i in range (len(arr)):
        if arr[i] == x:
            return i
    return -1    

result = lin_search(arr = [10, 20, 80, 30, 60, 50, 110, 100, 130, 170], x=130)

if(result == -1):
    print("Element not found")
else:
    print("Element found at index: ", result)

