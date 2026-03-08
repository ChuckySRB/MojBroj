from math import factorial
eq=""
znak=["/","*","+","-"]
Kombinacije=["A","ABo","ABoCo","ABCoo","ABCDooo","ABCoDoo","ABoCDoo","ABoCoDo","ABCDEoooo","ABCDoEooo","ABCoDEooo","ABoCDEooo",\
             "ABCDooEoo","ABCoDoEoo","ABoCDoEoo","ABCooDEoo","ABoCoDEoo","ABCDoooEo","ABCoDooEo","ABoCDooEo","ABCooDoEo","ABoCoDoEo",\
             "ABCDEFooooo","ABCDEoFoooo","ABCDoEFoooo","ABCoDEFoooo","ABoCDEFoooo","ABCDEooFooo","ABCDoEoFooo","ABCoDEoFooo","ABoCDEoFooo",\
             "ABCDooEFooo","ABCoDoEFooo","ABoCDoEFooo","ABCooDEFooo","ABCooDEFooo","ABoCoDEFooo","ABCDEoooFoo","ABCDoEooFoo","ABCoDEooFoo",\
             "ABoCDEooFoo","ABCDooEoFoo","ABCoDoEoFoo","ABoCDoEoFoo","ABCooDEoFoo","ABoCoDEoFoo","ABCDoooEFoo","ABCoDooEFoo","ABoCDooEFoo",\
             "ABCooDoEFoo","ABoCoDoEFoo","ABCDEooooFo","ABCDoEoooFo","ABCoDEoooFo","ABoCDEoooFo",\
             "ABCDooEooFo","ABCoDoEooFo","ABoCDoEooFo","ABCooDEooFo","ABoCoDEooFo","ABCDoooEoFo","ABCoDooEoFo","ABoCDooEoFo","ABCooDoEoFo","ABoCoDoEoFo"]
D={}
N=[]
o=[]
#[9,3,6,5,15,25] 873.
#Brojevi = [5,3,3,7,10,25]
#broj=912.
#Brojevi = [9,3,8,9,20,25]
#broj=992.
Brojevi = [9,3,8,9,20,25]
broj=992.
# ------ Globalne promenljive ------- #

def result():
    global eq,D,N,o,znak
    l=0
    S=[]
    for i in eq:
        if i=="o":
            x = znak[o[l]]
            l+=1
            op2 = S.pop()
            op1 = S.pop()
            if x == "/":
                if op2 == 0:
                    S.append(-1)
                    break
                rez = op1 / op2
            elif x == "*":
                rez = op2 * op1
            elif x == "+":
                rez = op2 + op1
            elif x == "-":
                rez = op1 - op2
            S.append(rez)
        else:
            S.append(D[i])
    rez=S.pop()
    return rez
def provera(a, i, c):
    if a[i]==c:
        a[i]=0
        if i==c-1:
            return
        else:
            a[i+1]+=1
            provera(a,i+1,c)
    else:
        return
def provera2(N,i,R):
    R[i]+=1
    if R[i]==6:
        R[i]=0
        N[i]=(N[i]+1)%6
        if i+1==len(N):
            return
        else:
            provera2(N,i+1,R)
    elif (N[i]+1)%6 in N:
        N[i]=(N[i]+1)%6
        provera2(N,i,R)
    else:
        N[i]=(N[i] + 1) % 6
    return

def RESI():
    global eq,D,o,N,znak
    Z=[]
    p=0
    for i in eq:
        if i == "o":
            Z.append(znak[o[p]])
            p+=1
        else:
            Z.append(D[i])
    print (Z)
    return

# ------------------------------------------


for i in Kombinacije:
    N = [0, 1, 2, 3, 4, 5]
    R = [0,0,0,0,0,0]
    o = [0, 0, 0, 0, 0]
    eq=i;
    D={}
    for m in range (6-int((len(i)+1)/2)):
        N.pop()
        R.pop()
    for k in range(int(720/factorial(6-int((len(i)+1)/2)))):
        p = 0
        for j in i:
            if not j == "o":
                D[j] = Brojevi[N[p]]
                p += 1
        for z in range(4**int(((len(i)-1)/2))):
            t=result()
            if t==broj:
                RESI()
                exit(0)
            o[0]+=1
            provera(o, 0, 4)
        provera2(N,0,R)
        o = [0, 0, 0, 0, 0]
print("Nema resenja :(");