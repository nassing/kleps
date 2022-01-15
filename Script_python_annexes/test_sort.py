import random
#import pytest

#Définition de la fonction QuickSort

def DoubleQuickSort(refList, otherList): #QuickSort classique
    QuickSort0(refList,otherList,0,len(refList)-1)

def QuickSortPartition (refList,otherList, start, end):
    pivot = refList [start]
    low = start + 1
    high = end
    while True:
        while low <= high and refList [high] >= pivot:
            high = high - 1
        while low <= high and refList[low]<= pivot:
            low=low+ 1
        if low <= high:
            refList[low], refList [high] = refList [high], refList[low]
            otherList [low], otherList[high] = otherList [high], otherList [low]
        else:
            break    
    refList[start], refList [high]= refList [high], refList [start]
    otherList [start], otherList [high] = otherList [high], otherList[start]
    return high

def QuickSort0(refList,otherList, start, end):
    if start >= end:
        return
    p = QuickSortPartition ( refList,otherList, start, end)
    QuickSort0(refList, otherList, start, p-1)
    QuickSort0 (refList,otherList, p+1, end)


#Création de la fonction vérifiant que le tri est correct
def test_sort():
    all_correct = True
    for k in range(100):#On vérifie que l'alglo fonctionne sur 100 listes aléatoires
        list = []
        for u in range(10000):
            list.append(random.randrange(0,1000)+(0.01*random.randrange(0,100)))
        id_list = [i for i in range(len(list))]
        list2 = list.copy()
        list2.sort()
        DoubleQuickSort(list, id_list)
        if not list == list2:
            all_correct = False
    assert all_correct