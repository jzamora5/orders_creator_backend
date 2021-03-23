from datetime import datetime
from flask import request

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def getNestedValue(arr, i, keys=[]):
    datesKeys = ["created_at", "updated_at"]

    if not keys:
        return arr[i]

    obj = arr[i]
    for key in keys:
        obj = obj[key]
        if key in datesKeys:
            break

        if not obj:
            return arr[i]

    return obj


def mergeSort(arr, keys=[]):
    if len(arr) > 1:

        mid = len(arr)//2

        L = arr[:mid]

        R = arr[mid:]

        mergeSort(L, keys)

        mergeSort(R, keys)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if getNestedValue(L, i, keys) < getNestedValue(R, j, keys):
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


def sortResponse(request, arr):
    sort = request.args.get("sort", None)

    if not sort:
        return

    reverse = 0

    if sort[0] == '-':
        reverse = 1
        sort = sort[1:]

    keys = sort.split(',')

    mergeSort(arr, keys)

    if reverse:
        arr.reverse()
