from numpy import random


def quick_sort(list):
    return quick_sort_helper(list, 0, len(list) - 1)


def quick_sort_helper(list, first, last):
    if first < last:
        print('First and Last are {} and {}'.format(first, last))

        pivot = get_pivot(list, first, last)
        # pivot = list[first]
        partitionIndex = partition(list, pivot, first, last)

        print('\n')

        quick_sort_helper(list, first, partitionIndex - 1)
        quick_sort_helper(list, partitionIndex + 1, last)
    # else:
    #     print('Cannot quick sort partition since first and last are {} and {}'.format(first, last))
    #     print('\n')


def get_pivot(list, low, hi):
    length = hi - low + 1
    if length % 2 == 0:
        mid = low + int(length / 2) - 1
    else:
        mid = low + int((length + 1) / 2) - 1

    # print('{} => {}, {} => {}, {} => {}'.format(low, list[low], mid, list[mid], hi, list[hi]))
    pivots = [list[low], list[mid], list[hi]]
    pivots.sort()

    median = pivots[1]
    return median


def partition(list, pivot, first, last):
    leftPointer = first
    rightPointer = last

    print('Pivot is {}'.format(pivot))

    print(list)

    while leftPointer <= rightPointer:
        print('Left pointer {} => {}, Right pointer {} => {}'.format(leftPointer, list[leftPointer], rightPointer,
                                                                     list[rightPointer]))
        if list[leftPointer] <= pivot:
            leftPointer += 1
        elif list[rightPointer] >= pivot:
            rightPointer -= 1
        else:
            print('Swap left {} <=> {} right'.format(list[leftPointer], list[rightPointer]))

            temp = list[leftPointer]
            list[leftPointer] = list[rightPointer]
            list[rightPointer] = temp

            print(list)

            leftPointer += 1
            rightPointer -= 1

    pivotIndex = list.index(pivot)
    partitionIndex = rightPointer

    print('Pivot index {} and partition index {}'.format(pivotIndex, partitionIndex))

    if pivotIndex != partitionIndex:
        print('\nSwap pivot {} <=> {} partition '.format(list[pivotIndex], list[partitionIndex]))

        temp = list[pivotIndex]
        list[pivotIndex] = list[partitionIndex]
        list[partitionIndex] = temp

        print(list)

    return partitionIndex


def generate_random_list(size = 10):
    # return [96, 21, 91, 22, 82, 55, 66, 58, 47, 34]
    return [51, 29, 6, 54, 93, 42, 47, 10, 79, 77]
    # return list(random.randint(1, 100, size))


if __name__ == '__main__':
    list = generate_random_list()
    quick_sort(list)
    print(list)