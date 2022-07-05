"""
Objetivo: asignar los procedimientos
a la sala de tal forma que no hayan
cruces en los horarios seleccionados y se maximice
el tiempo que la sala se encuentre en
funcionamiento en el día.
"""

# Se abre y lee el archivo (entrada).
input = open("./sala_operaciones_entrada4.txt");
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
    return ["{hrsT}:{minT}".format(hrsT=paddingElementsLeft("0",2,ht), 
                                  minT=paddingElementsLeft("0",2,mt)), ht*60+mt];

def timeDiff(d1, d2):
    """
    formato de tiempo permitido: 00:00
    """
    h1 = int(d1[0:2]);
    m1 = int(d1[3:5]);
    h2 = int(d2[0:2]);
    m2 = int(d2[3:5]);
    if m1 > m2:
        h2 -= 1;    
        m2 += 60;
        ht = abs(h2-h1);
        mt = abs(m2-m1);
        if (ht*60+mt) > 1440:
            raise Exception("Error!, el resultado es mayor que 24hrs");
        return ["{hrsT}:{minT}".format(hrsT=paddingElementsLeft("0",2,ht), 
                                    minT=paddingElementsLeft("0",2,mt)), ht*60+mt];
    if m2 > m1:
        h1 -= 1;
        m1 += 60;
        ht = abs(h2-h1);
        mt = abs(m2-m1);
        if (ht*60+mt) > 1440:
            raise Exception("Error!, el resultado es mayor que 24hrs");
        return ["{hrsT}:{minT}".format(hrsT=paddingElementsLeft("0",2,ht), 
                                    minT=paddingElementsLeft("0",2,mt)), ht*60+mt];
    else:
        ht = abs(h2-h1);
        mt = abs(m2-m1);
        if (ht*60+mt) > 1440:
            raise Exception("Error!, el resultado es mayor que 24hrs");
        return ["{hrsT}:{minT}".format(hrsT=paddingElementsLeft("0",2,ht), 
                                    minT=paddingElementsLeft("0",2,mt)), ht*60+mt];

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
    
def timeInMin(t):
    """
    formato de tiempo permitido: 00:00
    """
    h = int(t[0:2]);
    m = int(t[3:5]);
    return h*60 + m;

# print(paddingElementsLeft("0",7,"232"));
# print(timeSum("10:45", "12:35")); # 23:20
# print(timeDiff("10:45", "23:20")); #12:35
# print(timeDiff("10:00", "23:00")); #13:00
# print(isGtTime("10:48", "10:47"));

# Se inicializan variables 
n = int(content[0].split()[0])
c = 0;
res = [];

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
# se selecciona cuál hora de inicio se acerca más a las 0:00
minProc = content[1].split();

for i in range(2, n+1):
    proc = content[i].split();
    if isGtTime(minProc[1], proc[1]):
        minProc = proc;

# Se hace la secuencia de procedimientos
c += 1;
res.append(minProc);
totalT = timeDiff(res[c-1][2],res[c-1][1])[0];

for i in range(1, n+1):
    # print("i:",i)
    proc = content[i].split();
    totalMin = timeInMin(totalT);
    if (totalMin) >= 1440:
        break;
    if proc[0] == res[c-1][0]:
        continue;
    print("newVal:", totalMin+timeDiff(proc[2],proc[1])[1], "totalTime:",totalMin,"timeDiff:", timeDiff(proc[2],proc[1])[1],"proc:",proc,"res:",res[c-1], "limit:", (totalMin+timeDiff(proc[2],proc[1])[1] <= 1440))
    if (isGtTime(proc[1],res[c-1][2]) or (res[c-1][2] == proc[1])) and (totalMin+timeDiff(proc[2],proc[1])[1] <= 1440):
        print("totalTimera:",totalT);
        print("result:",timeSum(totalT,timeDiff(proc[1],res[c-1][2])[0]), "timeDiff:", timeDiff(proc[1],res[c-1][2])[0], "proc:", proc[1], "res:", res[c-1][2]);
        totalT = timeSum(totalT,timeDiff(proc[2],proc[1])[0])[0];
        print("totalTimerb:",totalT);
        print("newTotalT:",totalT)
        c += 1;
        res.append(proc);
        totalMin = timeInMin(totalT);
        # print("2-totalMin:",totalMin, "another:",timeDiff(res[c-1][2],proc[1])[1]);

input.close();

# Se genera la salida en formato .txt
output = open("./sala_operaciones_salida.txt", "w");
output.write(f"{c} -- procedimientos\n");
output.write("{time} -- tiempo de uso\n".format(
    time=totalT));
for i in range(0,c):
    output.write(f"{res[i][0]}\n");
output.close();