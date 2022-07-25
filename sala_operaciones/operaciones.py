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


input = open("./sala_operaciones_entrada3.txt");
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

def timeSum(d1, d2):
    """
    formato de tiempo permitido: 00:00
    """
    h1 = int(d1[0:2]);
    m1 = int(d1[3:5]);
    h2 = int(d2[0:2]);
    m2 = int(d2[3:5]);
    ht = abs(h2+h1);
    mt = abs(m2+m1);
    if mt >= 60:
        mt -= 60;
        ht += 1;
    if (ht*60+mt) > 1440:
        raise Exception("Error!, el resultado es mayor que 24hrs");
    return "{hrsT}:{minT}".format(hrsT=paddingElementsLeft("0",2,ht), 
                                  minT=paddingElementsLeft("0",2,mt));

def timeDiff(d1, d2):
    """
    formato de tiempo permitido: 00:00
    """
    if d1 == "00:00":
        return d2;
    if d2 == "00:00":
        return d1;
    h1 = int(d1[0:2]);
    m1 = int(d1[3:5]);
    h2 = int(d2[0:2]);
    m2 = int(d2[3:5]);
    if h1 == h2:
        ht = abs(h2-h1);
        mt = abs(m2-m1);
        return "{hrsT}:{minT}".format(hrsT=paddingElementsLeft("0",2,ht), 
                                    minT=paddingElementsLeft("0",2,mt));
    if m1 > m2:
        h2 -= 1;    
        m2 += 60;
        ht = abs(h2-h1);
        mt = abs(m2-m1);
        if (ht*60+mt) > 1440:
            raise Exception("Error!, el resultado es mayor que 24hrs");
        return "{hrsT}:{minT}".format(hrsT=paddingElementsLeft("0",2,ht), 
                                    minT=paddingElementsLeft("0",2,mt));
    if m2 > m1:
        h1 -= 1;
        m1 += 60;
        ht = abs(h2-h1);
        mt = abs(m2-m1);
        if (ht*60+mt) > 1440:
            raise Exception("Error!, el resultado es mayor que 24hrs");
        return "{hrsT}:{minT}".format(hrsT=paddingElementsLeft("0",2,ht), 
                                    minT=paddingElementsLeft("0",2,mt));
    else:
        ht = abs(h2-h1);
        mt = abs(m2-m1);
        if (ht*60+mt) > 1440:
            raise Exception("Error!, el resultado es mayor que 24hrs");
        return "{hrsT}:{minT}".format(hrsT=paddingElementsLeft("0",2,ht), 
                                    minT=paddingElementsLeft("0",2,mt));

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
    
def timeInMin(t):
    """
    formato de tiempo permitido: 00:00
    """
    h = int(t[0:2]);
    m = int(t[3:5]);
    return h*60 + m;

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

def max_path(A, n, pi, j, b):
    print("pi",pi,"j",j,"A",A[pi][j])
    if pi == n-1 or j == n-1:
        return b;
    elif A[pi][j] == 0:
        print("r", pi, j+1,"A",A[pi][j+1])
        return max_path(A, pi, j+1, n, b);
    else:
        print("m[pi]",m[pi],"b",b)
        return max(max_path(A, pi, j+1, n, b),max_path(A, pi, pi+1, n, b + m[j]));

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
    m.append(timeInMin( timeDiff(content[i].split()[1], content[i].split()[2]) ));
print("m:", m);

# Obtenemos la matriz de vecindad de los procedimientos
content = content[1:len(content)]
M = adjacency(content,n);
print(M);

res = max_path(M, n, 0, 1, m[0]);
print(res)

input.close();

# Se genera la salida en formato .txt
# output = open("./sala_operaciones_salida.txt", "w");
# output.write(f"{c} -- procedimientos\n");
# output.write("{time} -- tiempo de uso\n".format(
#     time=totalT));
# for i in range(0,c):
#     output.write(f"{res[i][0]}\n");
# output.close();