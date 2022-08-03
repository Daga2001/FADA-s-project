"""
Objetivo: Su trabajo consiste en determinar como repartir
los libros entre los escritores de forma que
el tiempo que se demoren realizando las copias
sea el mínimo teniendo en cuenta que el tiempo
que se demoran en realizar las copias depende
del escritor que tenga mas paginas asignadas.
Hacer la copia de una pagina tiene una duracion de un dia.

NOTA: un escritor le puede
corresponder los libros que estan entre l0 y l3 a
otro escritor desde l4 y l6 y así sucesivamente.
"""

# se importa libreria math
from os import system
import numpy as np;
import math;
import copy
import time;

# Se abre y lee el archivo (entrada).
input = open("./libros_entrada8.txt");
content = input.readlines();

"""
se asocian los indices de esta forma:
0 <- nombre del libro.
1 <- numero de páginas del libro.
content[2].split()[1]
"""

# funciones auxiliares
def translate(W, sol):
    """
    O(n)
    devuelve el arreglo de pesos asociados a los indices del arreglo solución
    ejemplo:
    entrada: [1, 4, 5]
    salida: [275.0, 335.0, 350.0]
    Esto significa que para un total de 6 libros (considerando que el máximo indice es 5):
    el autor 1 toma 2 libros que tienen 275 páginas,
    el autor 2 toma 3 libros que tienen 335 páginas y 
    el autor 3 toma 1 libros que tiene 350 páginas.
    """
    sols = [];
    sols.append(W[0][sol[0]]);
    for i in range(1, n):
        c = abs(sol[i-1] - sol[i]) - 1;
        sols.append(W[sol[i]-c][sol[i]]);
    return sols;

def posibilities(W, sol, pos, n, m):
    """
    entradas:
    W -> matriz de sumas.
    sol -> vector con indices de la solución inicial.
    se asume que por defecto es un vector de la forma:
    [i_m-n,i_m-n+1,i_n-m+2,...,i_m-1];
    pos -> array con las posibles distribuciones de los autores
    que nos sirven como subproblemas para solucionar el problema global.
    n -> número de escritores.
    m -> número de libros.

    devuelve el rango de libros que se asignará a cada escritor en la 
    solución optima.
    ej: [3, 4, 6]
    significa:
    autor 1 -> lib 1 - lib 3
    autor 2 -> lib 4 - lib 5
    autor 3 -> lib 6
    """
    def isGrowing(vec, a, b):
        # print("grows",vec)
        for i in range(a,b):
            # print("grows","i",vec[i],vec);
            if vec[i] != vec[i+1]-1:
                return False;
        return True;
    
    sol[0] -= n;
    iSol = copy.deepcopy(sol);

    # O((m-n!))
    for t in range(0, math.factorial(m-n+2)):
        # print("t",t)
        for u in range(sol[n],sol[n+1]):
            # print("4.1.sol",sol)
            sol[n] = u;
            pos.append([copy.deepcopy(sol), max(translate(W, sol))]);

        # print("4.sol",sol)
        sol[n-1] = sol[n-1]+1;
        # print("5.sol",sol)
        sol[n] = sol[n-1]+1;

        if sol[n-1]+1 == sol[n] and sol[n+1]-1 == sol[n]:
            for k in range(n-1,-1,-1):
                # print("k",k);

                # se puede continuar?
                if k == 0:
                    # print("n",n,"m",m,"m-(n+2)",m-(n+2),"sol[0]",sol[0])
                    if sol[k] >= iSol[0] + n:
                        # do nothing - stop!
                        pos.append([copy.deepcopy(sol), max(translate(W, sol))]);
                        return pos;
                    # hay una secuencia creciente después del primer elemento?
                    if isGrowing(sol,k+1,n):
                        # los ultimos dos digitos son distantes en 1?
                        if sol[n+1]-1 == sol[n]:
                            pos.append([copy.deepcopy(sol), max(translate(W, sol))]);
                            # print("theSol",sol)
                            for c in range(k, n+1):
                                if c == k:
                                    sol[c] = sol[c] + 1;
                                else:
                                    sol[c] = sol[c-1] + 1;
                            # print("2- theSol",sol)
                            if sol[k] >= iSol[0] + n:
                                # do nothing - stop!
                                pos.append([copy.deepcopy(sol), max(translate(W, sol))]);
                                return pos;
                            break;
                        else:
                            pos.append([copy.deepcopy(sol), max(translate(W, sol))]);
                            break;
                    else:
                        pos.append([copy.deepcopy(sol), max(translate(W, sol))]);
                        break;

                if isGrowing(sol,k+1,n) and sol[n+1]-1 == sol[n]:
                    if k-1 == 0:
                        continue;
                    pos.append([copy.deepcopy(sol), max(translate(W, sol))]);
                    sol[k-1] = sol[k-1]+1;
                    # print("2.sol",sol)
                    sol[k] = sol[k-1]+1;
                    # print("3.sol",sol)
                    sol[k+1] = sol[k]+1;
                    # print("7.sol",sol)

def dynamic_sol(W, n, m):
    """
    W -> matriz de sumas.
    n -> número de escritores.
    m -> número de libros.
    """
    totalW = W[0][m-1];
    partialW = 0;
    writers = n;
    first_sol = [];
    # toma la solución inicial - O(n)
    for i in range(0,n-1):
        if i == 0:
            for j in range(0,m):
                partialW += pages[j];
                totalW -= pages[j];
                prom = totalW/(writers-1);
                # print("partial",partialW,"totalW",totalW,"prom",prom,"writers",writers)
                # print("firts_sol",first_sol);
                if partialW > prom:
                    partialW = 0;
                    writers -= 1;
                    if j == m-1:
                        j -= 1;
                    first_sol.append(j);
                    break;
        else:
            for j in range(first_sol[i-1]+1,m):
                partialW += pages[j];
                totalW -= pages[j];
                prom = totalW/(writers-1);
                # print("partial",partialW,"totalW",totalW,"prom",prom,"writers",writers)
                # print("firts_sol",first_sol);
                if partialW > prom:
                    partialW = 0;
                    writers -= 1;
                    if j == m-1:
                        j -= 1;
                    first_sol.append(j);
                    break;
    first_sol.append(m-1);
    
    pos = [];
    print("1- firts_sol",first_sol);

    posibilities(W, copy.deepcopy(first_sol), pos, n-2, m);
    
    L = len(pos);
    # print(pos)
    # print("posibilities",L)

    bestSol = pos[0][0];
    bestW = pos[0][1];
    for i in range(1,L):
        iSol = pos[i][0];
        w = pos[i][1];
        if w < bestW:
            bestSol = iSol;
            bestW = w;
    

    return bestSol;

# Se inicializan variables 
# Número de escritores.
n = int(content[0].split()[0])
# Número de libros.
m = int(content[0].split()[1]);

# Número de libros real
nBooks = len(content) - 1;

start = time.time();

# Cuerpo del algoritmo solución.
if not n > m and not n < 1 and m == nBooks:
    # Se crea vector de paginas para usarlo en la creación de la matriz de sumas
    pages = [];
    for i in range(1,m+1):
        pages.append(int(content[i].split()[1]));
    # Se crea matriz de sumas
    sums = np.zeros((m,m));
    c = 0;
    for i in range(0,m):
        c = 0;
        for j in range(i,m):
            c += pages[j];
            sums[i][j] = c;

    # print("pages:",pages)
    print("sums:")
    print(sums);

    # Se halla la mejor solución (optima) para los lectores.
    sol = dynamic_sol(sums, n, m);
    maxTime = max(translate(sums, sol));

    print("sol:")
    print(sol);
    print("pags")
    print(maxTime);
else:
    raise Exception("Error! invalid input values:",(n,m));

end = time.time();

print(" --- execution time: {t} --- ".format(t = end-start));

input.close();

# Se genera la salida en formato .txt
output = open("./libros_salida.txt", "w");
output.write(f"{maxTime} -- dias requeridos\n");
if sol[0] > 0:
    output.write(f"lib{1} - lib{sol[0]+1}\n");
else:
    output.write(f"lib{sol[0]+1}\n");
if n > 1:
    for i in range(1,n-1):
        # print("i",i)
        if (sol[i] - sol[i-1]) != 1:
            output.write(f"lib{sol[i-1]+2} - lib{sol[i]+1}\n");
        else:
            output.write(f"lib{sol[i]+1}\n");
    if (sol[n-1] - sol[n-2]) != 1:
        output.write(f"lib{sol[n-2]+2} - lib{m}\n");
    else:
        output.write(f"lib{sol[n-1]+1}");
output.close();