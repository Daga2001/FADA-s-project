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
import math;

# Se abre y lee el archivo (entrada).
input = open("./libros_entrada2.txt");
content = input.readlines();

"""
se asocian los indices de esta forma:
0 <- nombre del libro.
1 <- numero de páginas del libro.
content[2].split()[1]
"""

# funciones auxiliares
def merge(A, p, q, r):
    n_1 = q - p + 1;
    n_2 = r - q;
    L = [None]*n_1;
    R = [None]*n_2;
    for i in range(0, n_1):
        L[i] = A[p + i - 1];
    for j in range(0, n_2):
        R[j] = A[q + j];
    # L[n_1-1] = 999999999999999999;
    # R[n_2-1] = 999999999999999999;
    i = 0;
    j = 0;
    for k in range(p, r):
        if L[i] <= R[j]:
            A[k] = L[i];
            i += 1;
        else:
            A[k] = R[j];
            j = j + 1;

def merge_sort(A, p, r):
    if p < r:
        q = math.floor((p + r)/2);
        merge_sort(A, p , q);
        merge_sort(A, q + 1 , r);
        merge(A, p, q, r);
        
# test = [1,3,2,6,1,4];
# print("merge_sort:",merge_sort(test, 0, 6))
# print("test:", test)

# Se inicializan variables 
n = int(content[0].split()[0])
m = int(content[0].split()[1]);
pagT = 0;

# Valida correctitud en las entradas
# for i in range(1, n+1):
#     proc = content[i].split();
#     hi = int(proc[1][0:2]);
#     mi = int(proc[1][3:5]);
#     hf = int(proc[2][0:2]);
#     mf = int(proc[2][3:5]);
#     if (hi > 24 or hf > 24) or (timeDiff(proc[2],proc[1])[1] == 0):
#         raise Exception("Error! valores de entrada invalidos o incoherentes, revisar entrada."); 

# Cuerpo del algoritmo solución.
# Se halla la sumatoria de todas las páginas de los libros.
for i in range(1, m+1):
    pagT += int(content[i].split()[1]);

# Se distribuyen las páginas por el número de escritores.
promBooks = round(pagT/n);
cPag = 0;
timeMax = 0;
auPag = [];
totalAuPag = [];

for j in range(0,n):
    auPag.append(content[1].split());
    cPag = int(content[1].split()[1]);
    del content[1];
    k = 1;
    m -=1;
    print("j:",j,"n:",n, "m:",m)
    print("1content:",content);
    i = 1;
    while(i < m+1):
        print("i:",i,"m:",m)
        print("i-content:",content, "m:", m);
        book = content[i].split();
        pag = int(book[1]);
        print("i-book:",book,"cPag:",cPag,"pag:",pag,"totalAugPag:",totalAuPag,"auPag:",auPag);
        print("1cPag:",cPag,"pag:",pag,"supNPag:",promBooks)
        cPag += pag;
        k += 1;
        del content[i];
        m -= 1;
        i -= 1;
        if cPag >= promBooks:
            print("---cPag:",cPag,"supNPag:",promBooks)
            auPag.append(book);
            break;
        print("f-i:",i,"f-m:",m)
        print("f-cPag:",cPag,"pag:",pag,"totalAugPag:",totalAuPag,"auPag:",auPag);
        print("f-content:",content, "m:", m);
        i += 1;
    #xD
    print("------- f2-cPag:",cPag)
    if cPag > timeMax:
        timeMax = cPag;
    cPag = 0;
    totalAuPag.append(auPag);
    print("totalAuPag1:",totalAuPag)
    print("pag:",pag,"totalAugPag:",totalAuPag,"auPag:",auPag);
    auPag = [];
    print("au4:",auPag)

print("totalAuPag:",totalAuPag);

input.close();

# Se genera la salida en formato .txt
output = open("./libros_salida.txt", "w");
output.write(f"{timeMax} -- dias requeridos\n");
for i in range(0,n):
    output.write(f"{totalAuPag[i]}\n");
output.close();