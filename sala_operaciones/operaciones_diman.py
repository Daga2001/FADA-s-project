"""
Objetivo: asignar los procedimientos
a la sala de tal forma que no hayan
cruces en los horarios seleccionados y se maximice
el tiempo que la sala se encuentre en
funcionamiento en el día.
"""

# Se abre y lee el archivo (entrada).
from importlib.resources import contents
import numpy as np
import math

input = open("./sala_operaciones_entrada6.txt");
content = input.readlines();

"""
se asocian los indices de esta forma:
0 <- nombre del procedimiento.
1 <- hora de inicio del procedimiento.
2 <- hora de finalización del procedimiento.
content[2].split()[1]
"""

# funciones auxiliares
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

def isGtTime(d1, d2):
    """
    formato de tiempo permitido: 00:00
    """
    h1 = int(d1[0:2]);
    m1 = int(d1[3:5]);
    h2 = int(d2[0:2]);
    m2 = int(d2[3:5]);
    if h1 > h2:
        return True;
    elif h1 == h2: 
        if m1 > m2:
            return True;
        else:
            return False;
    return False;

def isGtOrEqualTime(t1, t2):
    return isGtTime(t1,t2) or t1 == t2;
    
def radix_sort_time(A, n):
    # A[2].split()[1]
    sorted = [];
    for i in range(0,2):
        for j in range(1,n):
            A[j].split()[i+1]
    return sorted;

def adjacency(A, n):
    ad = np.zeros((n,n));
    for i in range(0,n):
        for j in range(i+1,n):
            # print("A", A[i].split()[2], A[j].split()[1]);
            if isGtOrEqualTime(A[j].split()[1], A[i].split()[2]):
                # print("sum:", timeSum( timeDiff(A[i].split()[1],A[i].split()[2]), 
                # timeDiff(A[j].split()[1],A[j].split()[2])), "t1:", timeDiff(A[i].split()[1],A[i].split()[2]) ,"t2", timeDiff(A[j].split()[1],A[j].split()[2]) )
                ad[i][j] = m[j];
    return ad;

def weightSol(sol):
    w = 0;
    for i in range(0, len(sol)):
        w += m[sol[i]];
    return w;

def increasesByOne(sol):
    for i in range(1, len(sol)):
        if sol[i] - sol[i-1] != 1:
            return False;
    return True;

def doHasNeighbors(A, n, p):
    if p >= n-1:
        return False;
    for i in range(p+1, n):
        if A[p][i] != 0:
            return True;
    return False;

def max_path(A, n, pi, sol, w):
    l = len(sol)
    if l == n:
        return sol;
    maxW = m[pi];
    for i in range(l-1, -1, -1):
        p = sol[i-1];
        pf = sol[i];
        for j in range(n-1, p, -1):
            print("sol[i-1]",p,"j",j,"maxW",maxW);
            if pf == n-1 or A[p][j] == 0:
                print("pass")
                continue;
            # if not doHasNeighbors(A, n, j):
            #     print("passed")

            #     continue;
            newSol = sol[0:pf];
            newW = weightSol(newSol);
            print("newW",newW,"newSol",newSol);
            if w < w-m[p]+m[j]:
                w = w-m[p]+m[j];
            

    return sol;

# for i in range(0, 1460, 10):
#     print("i:",i,"minToHrs(i):",minToHrs(i));
# print(paddingElementsLeft("0",7,"232"));
# print(timeSum("10:45", "12:35")); # 23:20
# print(timeSum("22:40", "00:40")); # 23:20
# print(timeDiff("04:40","17:30")); #12:35
# print(timeDiff("10:00", "23:00")); #13:00
# print(timeDiff("00:00", "22:40")); #22:40
# print(isGtTime("10:48", "10:47"));
# print(isGtOrEqualTime("17:30", "17:30"));

# Se inicializan variables 
n = int(content[0].split()[0])

# Cuerpo del algoritmo solución.
# Se ordenan los procedimientos siguiendo idea del radix-sort
# sorted_content = radix_sort_time(content, n);
# print("sorted:",sorted_content);

# obtenemos la matriz del tiempo requerido para cada procedimiento (en minutos)
m = [];
for i in range(1,n+1):
    m.append(hrsToMin( timeDiff(content[i].split()[1], content[i].split()[2]) ));
print("m:", m);

# obtenemos una matriz para indicar los tiempos máximos alcanzables para cada procedimiento.
p = [0]*n;
ac = m[n-1];
for i in range(n-2, -1, -1):
    ac += m[i];
    if ac < 1440:
        p[i] = ac;
    else:
        p[i] = hrsToMin(timeDiff(content[i+1].split()[1], "24:00"));
print("p:",p);

# Obtenemos la matriz de vecindad de los procedimientos
content = content[1:len(content)]
M = adjacency(content,n);
print(M);

# Obtenemos la primera solución voraz
px = 0;
s0 = [px];
for i in range(1, n):
    if M[px][i] == 0:
        continue;
    s0.append(i);
    px = i;
print("s0:", s0, "w0:", weightSol(s0));

res = max_path(M, n, 0, s0, weightSol(s0));
print(res)
# print("neighbors",doHasNeighbors(M, n, 7));

input.close();

# Se genera la salida en formato .txt
# output = open("./sala_operaciones_salida.txt", "w");
# output.write(f"{c} -- procedimientos\n");
# output.write("{time} -- tiempo de uso\n".format(
#     time=totalT));
# for i in range(0,c):
#     output.write(f"{res[i][0]}\n");
# output.close();