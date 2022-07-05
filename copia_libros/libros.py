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
input = open("./libros_entrada1.txt");
content = input.readlines();

"""
se asocian los indices de esta forma:
0 <- nombre del libro.
1 <- numero de páginas del libro.
content[2].split()[1]
"""

# funciones auxiliares

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
supNPag = math.ceil(pagT/n)
infNPag = math.floor(pagT/n);
cPag = 0;
auPag = [];
totalAuPag = [];
print("t:",totalAuPag,"au:",auPag)

for j in range(0,n):
    auPag.append(content[1].split());
    cPag = int(content[1].split()[1]);
    del content[1];
    k = 1;
    m -=1;
    print("j:",j,"n:",n, "m:",m)
    print("1content:",content);
    if m > 2:
        for i in range(1, m+1):
            if i == m+1:
                break;
            print("i:",i,"m:",m)
            print("i-content:",content, "m:", m);
            book = content[i].split();
            pag = int(book[1]);
            lastAuPag = int(auPag[k-1][1]);
            print("lastAuPag:",lastAuPag);
            print("i-book:",book,"cPag:",cPag,"pag:",pag,"totalAugPag:",totalAuPag,"auPag:",auPag);
            if j == n-1:
                print("1cPag:",cPag,"pag:",pag,"supNPag:",supNPag)
                if cPag >= supNPag:
                    print("---cPag:",cPag,"supNPag:",supNPag)
                    break;
                elif cPag+pag <= supNPag:
                    cPag += pag;
                    k += 1;
                    auPag.append(book);
                    del content[i];
                    m -= 1;
                    i -= 1;
                elif cPag+pag-lastAuPag <= supNPag:
                    cPag += pag-lastAuPag;
                    print("send back the book");
                    print("contenta:",content,"auPag[k-1]:",auPag[k-1])
                    content[m-1] = f"{content[m-1]}\n"
                    content.append(f"{auPag[k-1][0]} {auPag[k-1][1]}");
                    print("contentb:",content)
                    del auPag[k-1];
                    k -= 1;
                    auPag.append(book);
                    k += 1;
                    del content[i];
            else:
                print("2cPag:",cPag,"pag:",pag,"supNPag:",supNPag)
                if cPag >= infNPag:
                    print("---cPag:",cPag,"infNPag:",infNPag)
                    break;
                elif cPag+pag <= infNPag:
                    cPag += pag;
                    k += 1;
                    auPag.append(book);
                    del content[i];
                    m -= 1;
                    i -= 1;
                elif cPag+pag-lastAuPag <= infNPag:
                    cPag += pag-lastAuPag;
                    print("send back the book");
                    print("contenta:",content,"auPag[k-1]:",auPag[k-1])
                    content[m-1] = f"{content[m-1]}\n"
                    content.append(f"{auPag[k-1][0]} {auPag[k-1][1]}");
                    print("contentb:",content)
                    del auPag[k-1];
                    k -= 1;
                    auPag.append(book);
                    k += 1;
                    del content[i];
            print("f-cPag:",cPag,"pag:",pag,"totalAugPag:",totalAuPag,"auPag:",auPag);
            print("f-content:",content, "m:", m);
        #xD
        print("------- f2-cPag:",cPag)
        cPag = 0;
        totalAuPag.append(auPag);
        print("totalAuPag1:",totalAuPag)
        print("pag:",pag,"totalAugPag:",totalAuPag,"auPag:",auPag);
        auPag = [];
        print("au4:",auPag)
    else:
        print("abscontent:",content[2].split());
        auPag.append(content[1].split())
        auPag.append(content[2].split())
        totalAuPag.append(auPag);


print("totalAuPag:",totalAuPag);

input.close();

# Se genera la salida en formato .txt
output = open("./libros_salida.txt", "w");
output.write(f"{supNPag} -- dias requeridos\n");
for i in range(0,n):
    output.write(f"{totalAuPag[i]}\n");
output.close();