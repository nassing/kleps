import time
import random

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

#Mesure du temps nécessaire à l'éxécution d'un tri sur une liste de nb_values valeurs, allant de 0 à max_value
def testQuickSort(nb_values,max_value):
    import time
    id = [ i for i in range(nb_values)]#le contenue de cette liste n'influe pas vraiment la vitesse du tri
    test_list = []
    for u in range(nb_values):
        test_list.append(random.randrange(0,max_value)+(0.01*random.randrange(0,100)))
    start = time.time()
    DoubleQuickSort(test_list, id)
    end = time.time()
    time = (end - start)
    return time

#calcul du temps moyen sur 30 éxécution nécessaire à l'éxécution du tri pour un nombre de valeur contenue dans size, allant de 0 à 1000
#renvoie une liste de couple (nombre de valeur, temps moyen)
def rangeTimeQuickstort():
    size = [100, 1000, 10000, 100000, 1000000]
    results = []
    for i in size:
        average_time = 0
        for u in range(10):
            average_time += testQuickSort(i,1000)
        average_time = average_time/10
        results.append((i, average_time))
    return results

print(rangeTimeQuickstort())