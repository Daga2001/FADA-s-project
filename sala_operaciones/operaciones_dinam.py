"""
Objetivo: asignar los procedimientos
a la sala de tal forma que no hayan
cruces en los horarios seleccionados y se maximice
el tiempo que la sala se encuentre en
funcionamiento en el día.
"""

# Se abre y lee el archivo (entrada).
import numpy as np;
import math;
import time;
import copy;

input = open("./sala_operaciones_entrada10.txt");
content = input.readlines();

"""
se asocian los indices de esta forma:
0 <- nombre del procedimiento.
1 <- hora de inicio del procedimiento.
2 <- hora de finalización del procedimiento.
content[2].split()[1]
"""

# funciones auxiliares
def merge(nam, tim, arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m
 
    # create temp arrays, L1 -> names, L2 -> times (final or initial)
    L = [0] * (n1)
    R = [0] * (n2)
    L1 = [0] * (n1)
    R1 = [0] * (n2)
    L2 = [0] * (n1)
    R2 = [0] * (n2)
 
    # Copy data to temp arrays L[] and R[]
    for i in range(0, n1):
        L[i] = arr[l + i]
        L1[i] = nam[l + i]
        L2[i] = tim[l + i]
 
    for j in range(0, n2):
        R[j] = arr[m + 1 + j]
        R1[j] = nam[m + 1 + j]
        R2[j] = tim[m + 1 + j]
 
    # Merge the temp arrays back into arr[l..r]
    i = 0     # Initial index of first subarray
    j = 0     # Initial index of second subarray
    k = l     # Initial index of merged subarray

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            nam[k] = L1[i]
            tim[k] = L2[i]
            arr[k] = L[i]
            i += 1
        else:
            nam[k] = R1[j]
            tim[k] = R2[j]
            arr[k] = R[j]
            j += 1
        k += 1
 
    # Copy the remaining elements of L[], if there
    # are any
    while i < n1:
        nam[k] = L1[i]
        tim[k] = L2[i]
        arr[k] = L[i]
        i += 1
        k += 1
 
    # Copy the remaining elements of R[], if there
    # are any
    while j < n2:
        nam[k] = R1[j]
        tim[k] = R2[j]
        arr[k] = R[j]
        j += 1
        k += 1
 
# l is for left index and r is right index of the
# sub-array of arr to be sorted
 
def mergeSort(nam, tim, arr, l, r):
    if l < r:
 
        # Same as (l+r)//2, but avoids overflow for
        # large l and h
        m = l+(r-l)//2
 
        # Sort first and second halves
        mergeSort(nam, tim, arr, l, m)
        mergeSort(nam, tim, arr, m+1, r)
        merge(nam, tim, arr, l, m, r)

# O(nlgn)
def sort_time(A, n):
    """
    ti -> arreglo con tiempos iniciales;
    tf -> arreglo con tiempos finales;
    n -> número de procedimientos;
    """
    # Hallamos el arreglo de los nombres de los procedimientos - O(n)
    names = [];
    for i in range(1, n+1):
        names.append(A[i].split()[0]);

    # Hallamos el arreglo de los tiempos iniciales (en minutos) - O(n)
    ti = [];
    for i in range(1, n+1):
        ti.append(hrsToMin(A[i].split()[1]));

    # Hallamos el arreglo de los tiempos finales (en minutos) - O(n)
    tf = [];
    for i in range(1, n+1):
        tf.append(hrsToMin(A[i].split()[2]));
    
    # Se ordenan los tiempos iniciales de menor a mayor - O(nlgn)
    # merge-sort tiene complejidad O(nlgn).
    mergeSort(names, tf, ti, 0, n-1);

    # Se convierten en horas de nuevo los valores de los procedimientos - O(n)
    for i in range(0, n):
        ti[i] = minToHrs(ti[i]);

    for i in range(0, n):
        tf[i] = minToHrs(tf[i]);

    # Se crea el arreglo final ordenado - O(n)
    sorted = [];
    for i in range(0, n):
        proc = names[i];
        t1 = ti[i];
        t2 = tf[i];
        sorted.append([proc,t1,t2]);

    return sorted;

def paddingElementsLeft(e, n, val):
    """
    convierte al valor en uno de longitud n añadiendo elementos definidos:
    val <- valor (str/numeric)
    e <- elementos (str)
    n <- número de elementos (int); 
    """
    res = "";
    val = str(val);
    k = len(val);
    if k >= n:
        return val;
    for i in range(0,abs(k-n)):
        res += e;
    res += val;
    return res;

def minToHrs(m):
    if m > 1440:
        raise Exception("Error!, el resultado es mayor que 24hrs");
    hrs = math.trunc(m/60);
    min = (m - (hrs * 60));
    return "{hours}:{minutes}".format(hours = paddingElementsLeft("0",2,hrs), 
                                      minutes = paddingElementsLeft("0",2,min));

def hrsToMin(t):
    """
    formato de tiempo permitido: 00:00
    """
    h = int(t[0:2]);
    m = int(t[3:5]);
    res = h*60 + m;
    if res > 1440:
        raise Exception("Error!, el resultado es mayor que 24hrs");
    return res;

def timeSum(t1, t2):
    """
    formato de tiempo permitido: hh:mm
    """
    t1 = hrsToMin(t1);
    t2 = hrsToMin(t2);
    res = abs(t1 + t2);
    return minToHrs(res);

def timeDiff(t1, t2):
    """
    formato de tiempo permitido: hh:mm
    """
    t1 = hrsToMin(t1);
    t2 = hrsToMin(t2);
    res = abs(t1 - t2);
    return minToHrs(res);

def adjacency(A, n, m):
    ad = [];
    pi = [];
    c = 0;
    for i in range(0,n):
        piX = [];
        adX = [];
        for j in range(0,n):
            if i == j:
                c += 1;
                adX.append(0);
                piX.append(None);
                continue;
            t1 = A[j][1];
            t2 = A[i][2];
            if hrsToMin(t1) >= hrsToMin(t2):
                adX.append(m[j]);
                piX.append(i);
            else:
                # "i"
                c += 1;
                adX.append("i");
                piX.append(None);
        ad.append(adX);
        pi.append(piX);
    # si es una matriz de 0s y is
    if c == n*n:
        return (None,None);
    return (ad,pi);

def printM(matrix):
    for i in range(0,n):
        print(matrix[i])

# O(n^3)
def floyd_warshall(ad, tr, n):

    # calcula el minimo entre 2 valores, incluyendo infinito ("i") - O(1)

    def maximum(a, b):
        if a == "i" and b == "i":
            return "i";
        elif a == "i":
            return a;
        elif b == "i":
            return b;
        else:
            return max(a,b);

    # Suma 2 valores, incluyendo al infinito como posible valor - O(1)
    
    def sum(a, b):
        if a == "i" and b == "i":
            return "i";
        elif a == "i":
            return a;
        elif b == "i":
            return b;
        else:
            return a + b;

    # Iteración sobre la matriz de pesos y trayectorias - O(n^2)

    def dij(d, pi, k):
        if k == 0:
            return (ad,tr);
        elif k >= 0:
            for i in range(0, n):
                for j in range(0, n):
                    if i == k-1 or j == k-1:
                        continue;
                    if i == j:
                        continue;
                    a = d[i][j];
                    b = sum(d[i][k-1],d[k-1][j]);
                    maxi = maximum(a,b);
                    if maxi != "i":
                        if maxi <= 1440:
                            d[i][j] = maxi;
                            pi[i][j] = k-1;
        else:
            raise Exception("Error!, k debe ser mayor o igual a 0");
        return d;
        
    (D,T) = dij(ad, tr, 0);

    # Iteración para hallar la matriz de pesos máximos y trayectoria - O(n^3)

    for k in range(1,n):
        dij(D, T, k)

    return (D,T);

# O(n!)
def allPosibilitiesFor(A, n, m, k, p, ai, pos, posA, posAp, wn, wnA):
    """
    entradas:
    A -> matriz de pesos
    pos -> matriz de posibilidades totales
    posA -> matriz de posibilidades acumuladoras
    posAp -> matriz de posibilidades acumuladoras anterior.
    n -> número de procedimientos
    m -> vector de pesos de cada procedimiento
    k -> iterador para recorridos.
    p -> número del procedimiento
    pi -> indice de un procedimiento superior
    wn -> peso acumulado de la solución
    ai -> iterador para pesos y caminos anteriores
    salida:
    devuelve todos los posibles caminos para un vertice.
    """
    if k == p:
        posAp[ai] = copy.deepcopy(posA);
        wnA[ai] = copy.deepcopy(wn[0]);
        for i in range(p+1,n):
            if A[p][i] != "i" and A[p][i] != 0:
                newAp = copy.deepcopy(posAp[ai])
                newAp.append(i)
                posAp[ai+1] = newAp;
                newWnA = copy.deepcopy(wnA[ai] + A[p][i]);
                wnA[ai+1] = copy.deepcopy(newWnA);
                allPosibilitiesFor(A, n, m, i, p, ai+1, pos, posA, posAp, wn, wnA);
                posA = copy.deepcopy(posAp[ai]);
                wn[0] = copy.deepcopy(wnA[ai]);
                wn[0] = wn[0] + A[p][i]
                posA.append(i);
                pos.append([posA,wn[0]])
    else: 
        for i in range(k,n):
            if A[k][i] != "i" and A[k][i] != 0:
                newAp = copy.deepcopy(posAp[ai])
                newAp.append(i)
                posAp[ai+1] = newAp;
                newWnA = copy.deepcopy(wnA[ai] + A[k][i]);
                wnA[ai+1] = copy.deepcopy(newWnA);
                allPosibilitiesFor(A, n, m, i, p, ai+1, pos, posA, posAp, wn, wnA); 
                posA = copy.deepcopy(posAp[ai]);
                wn[0] = copy.deepcopy(wnA[ai]);
                wn[0] = wn[0] + A[p][i]
                posA.append(i);
                pos.append([posA,wn[0]])

# O(n!)
def max_path(p):
    k = p;
    pos = [];
    posA = [p];
    posAp = [];
    wnA = [];
    ai = 0;
    for i in range(0,n):
        posAp.append(0);
        wnA.append(0);
    wn = [m[p]];
    allPosibilitiesFor(M, n, m, k, p, ai, pos, posA, posAp, wn, wnA);
    
    print("p",p,"n",n,"posibilities",len(pos))

    # Hallamos el máximo valor posible.
    L = len(pos)
    sol = [];
    if L > 0:
        sol = pos[0];
        for i in range(1,L):
            if pos[i][1] > sol[1]:
                sol = pos[i];
    return sol;

# Se inicializan variables 
n = int(content[0].split()[0])

start = time.time();

# Cuerpo del algoritmo solución.

# Se ordenan los procedimientos de mayor a menor según su tiempo de inicio.
proc = sort_time(content, n);

# obtenemos el vector del tiempo requerido para cada procedimiento (en minutos)
maxP = 0;
maxW = 0;
m = [];
for i in range(0,n):
    wp = hrsToMin( timeDiff(proc[i][1], proc[i][2]) );
    if maxW < wp:
        maxP = i;
        maxW = wp;
    m.append(wp);

# se halla un vector que representa el máximo valor alcanzable desde un procedimiento.
mPos = [];
mW = 0;
for i in range(0,n):
    mW += m[i];
    if mW < 1440:
        mPos.append(mW);
    else:
        mPos.append(abs(hrsToMin(proc[i][1])-1440));

# Obtenemos la matriz de pesos de los procedimientos
(M,T) = adjacency(proc,n,m);

if M != None:
    
    # Hallamos la solución cuyo beneficio es el optimo para el problema.
    bSol = max_path(0);
    best = bSol[1];
    for i in range(1,n):
        sol = max_path(i);
        if sol[1] > best:
            bSol = sol;
            best = sol[1]; 
        if best > mPos[i]:
            break;
        
    print("sol",bSol);
    c = len(sol[0]);
    totalT = best;
    sol = sol[0];

    if maxW > totalT:
        c = 1;
        totalT = maxW;
        sol = [maxP];

else:
    c = 1;
    totalT = maxW
    sol = [maxP];

end = time.time();

print("--- execution time: {t} ---".format(t=end-start));

input.close();

# Se genera la salida en formato .txt
output = open("./sala_operaciones_salida.txt", "w");
output.write(f"{c} -- procedimientos\n");
output.write("{time} -- tiempo de uso\n".format(
    time=minToHrs(totalT)));
for i in range(0,c):
    output.write(f"{proc[sol[i]][0]}\n");
output.close();