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
import numpy as np;
import time
import copy;

# Se abre y lee el archivo (entrada).
input = open("./libros_entrada7.txt");
content = input.readlines();

"""
se asocian los indices de esta forma:
0 <- nombre del libro.
1 <- numero de páginas del libro.
content[2].split()[1]
"""

# funciones auxiliares
# O(n^3)
def floyd_warshall(ad, n):

    # calcula el minimo entre 2 valores, incluyendo infinito ("i") - O(1)

    def minimum(a, b):
        if a == "i" and b == "i":
            return "i";
        elif a == "i":
            return b;
        elif b == "i":
            return a;
        else:
            return min(a,b);

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

    def dij(d, k):
        if k == 0:
            return ad;
        elif k >= 0:
            for i in range(0, n):
                for j in range(0, n):
                    if i == k-1 or j == k-1:
                        continue;
                    if i == j:
                        continue;
                    a = d[i][j];
                    b = sum(d[i][k-1],d[k-1][j]);
                    mini = minimum(a,b);
                    if mini != "i":
                        if mini <= 1440:
                            d[i][j] = mini;
        else:
            raise Exception("Error!, k debe ser mayor o igual a 0");
        return d;
        
    D = dij(ad, 0);

    # Iteración para hallar la matriz de pesos máximos y trayectoria - O(n^3)

    for k in range(1,n):
        dij(D, k)

    return D;

def translate(W, sol):
    """
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

def optimal_sol(W, sol, c, maximum, best, prevsol):
    """
    devuelve el rango de libros que se asignará a cada escritor en la 
    solución optima.
    ej: [3, 4, 6]
    significa:
    autor 1 -> lib 1 - lib 3
    autor 2 -> lib 4 - lib 5
    autor 3 -> lib 6
    """
    sols = translate(W, sol);
    best = max(sols);
    print("c",c,"n",n,"best",best,"max",maximum,"sol",sol,"sols",sols,"prevsol",prevsol)
    if c==n:
        return sol;
    if best < maximum:
        maximum = best;
        prevsol = sol.copy();        
        c = 0;
    for i in range(0,n):
        if sols[i] == best:
            print("sol[i]",sol[i],"sol[i-1]",sol[i-1],"w:",sols[i]);
            c += 1;
            if i == 0 and sol[i] == 0:
                return sol;
            if i == n-1:
                return prevsol;
            if (sol[i] - sol[i-1]) == 1:
                return sol;
            sol[i] = sol[i] - 1;
            # print("best",best,"max",maximum)
            return optimal_sol(W, sol, c, maximum, best, prevsol);

def opt_sol_dyn(A, n, i, best, bSol, sol):
    # print("i",i,"n-1",n-1,"sol", sol)
    if len(sol) != n or len(bSol) != n:
        raise Exception("Error!, la longitud del beneficio no coincide con el número de escritores");
    if i == n-1:
        # print("bsol",bSol,"best",best)
        return (bSol, best);
    if i == 0:
        if sol[i] == 0:
            return opt_sol_dyn(A, n, i+1, best, bSol, sol);
        else:
            sol[i] = sol[i] - 1;
            val = max(translate(A, sol));
            if best > val:
                return opt_sol_dyn(A, n, i, val, copy.deepcopy(sol), sol);
            return opt_sol_dyn(A, n, i, best, bSol, sol);
    else:
        if sol[i]-1 == sol[i-1]:
            return opt_sol_dyn(A, n, i+1, best, bSol, sol);
        else:
            sol[i] = sol[i] - 1;
            val = max(translate(A, sol));
            if best > val:
                return opt_sol_dyn(A, n, i, val, copy.deepcopy(sol), sol);
            return opt_sol_dyn(A, n, i, best, bSol, sol);

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
    # Se crea matriz de pesos (cantidad de paginas acumuladas)
    sums = np.zeros((m,m));
    c = 0;
    for i in range(0,m):
        c = 0;
        for j in range(i,m):
            c += pages[j];
            sums[i][j] = c;
    print("sums");
    print(sums);

    # Se halla la mejor solución (optima) para los lectores.
    bM = [];
    for i in range(n,m):
        bM.append(i);

    a = copy.deepcopy(bM);
    (sol, maxTime) = opt_sol_dyn(sums, n, 0, max(translate(sums, bM)), bM, a);

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
        if (sol[i] - sol[i-1]) != 1:
            output.write(f"lib{sol[i-1]+2} - lib{sol[i]+1}\n");
        else:
            output.write(f"lib{sol[i]+1}\n");
    if (sol[n-1] - sol[n-2]) != 1:
        output.write(f"lib{sol[n-2]+2} - lib{m}\n");
    else:
        output.write(f"lib{sol[n-1]+1}");
output.close();
