from datetime import datetime
from flask import request

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def getNestedValue(arr, i, keys=None):
    dates_keys = ["created_at", "updated_at"]

    if not keys:
        return arr[i]

    obj = arr[i]
    for key in keys:
        obj = obj[key]
        if key in dates_keys:
            break

        if not obj:
            return arr[i]

    return obj


def mergeSort(arr, keys=None):
    if len(arr) > 1:

        mid = len(arr)//2

        left = arr[:mid]

        right = arr[mid:]

        mergeSort(left, keys)

        mergeSort(right, keys)

        i = j = k = 0

        while i < len(left) and j < len(right):
            if getNestedValue(left, i, keys) < getNestedValue(right, j, keys):
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1


def sort_response(request, arr):
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
