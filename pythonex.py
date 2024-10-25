def counter(x,y,z=None):
    """
    Υπολογίζει τους πόντους
    x -- η πρώτη κάρτα
    y -- η δεύτερη κάρτα
    z -- η τρίτη καρτα(σε περίπτωση που ανοιχτεί)
    >>> print(counter("2!","3!"))
    0
    >>> print(counter("10","10"))
    10
    >>> print(counter("2","2"))
    2
    >>> counter("A","A")==1
    True
    >>> counter("Q!","K!","K!")==10
    True
    """
    for i in range(2,10):
        if x[0]==str(i) and y[0]==str(i):
            return i
    if x[0]=="A" and y[0]=="A":
        return 1
    elif x[0]+x[1]=="10" and y[0]+y[1]=="10":
        return 10
    elif (x[0]=="J" and y[0]=="J") or (x[0]=="Q" and y[0]=="Q") or (x[0]=="K" and y[0]=="K"):
        return 10
    elif (x[0]=="Q" and y[0]=="K") or (x[0]=="K" and y[0]=="Q"):
        if (x[0]==z[0]) or (y[0]==z[0]):
            return 10
        else:
            return 0
    else:
        return 0

def start_list(a):
    """Φτιαχνει τη λίστα που περιεχει τα "Χ"
    a -- επίπεδο δυσκολίας
    >>> print(start_list(1))
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    >>> len(start_list(2))==40
    True
    >>> len(start_list(3))==52
    True
    """
    list_x=[]
    if a==1:
        arithmos_stoixeiwn = range(0,16)
    elif a==2:
        arithmos_stoixeiwn = range(0,40)
    else:
        arithmos_stoixeiwn = range(0,52)
    for i in arithmos_stoixeiwn:
        list_x.append("X")
    return list_x

def list_changer(a,c,pos,card):
    """
    Ανοιγει την καρτα στην λιστα των "Χ"
    a -- επίπεδο δυσκολίας
    c -- Η λίστα με τα στοιχεία που βλέπει ο χρήστης
    pos -- η θέση της κάρτας μέσα στη λίστα
    card -- Η κάρτα που επιλεχθηκε
    >>> c = start_list(1)
    >>> b = list_changer(1,c,0,"A")
    >>> print(b)
    ['A', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    >>> c=start_list(3)
    >>> b=list_changer(3,c,51,"A")
    >>> print(b)
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'A']
    """
    list_x=c
    list_x[pos]=card
    return list_x

def dwse_thesi_kartas(p,i,a):
    """
    p -- αριθμός παίκτη
    i -- αριθμός κάρτας
    a -- επίπεδο δυσκολίας
    """
    thesi=[]
    if a==1:
        x,y=int(input("Παίκτη"+" "+str(p)+": Δώστε γραμμή και στήλη"+" "+str(i)+"ης"+" "+"κάρτας:")),int(input())
        while (x>4 or y>4):
            print("Λανθασμένη θεση,προσπαθήστε ξανά")
            x,y=int(input("Παίκτη"+" "+str(p)+": Δώστε γραμμή και στήλη"+" "+str(i)+"ης"+" "+"κάρτας:")),int(input()) 
    elif a==2:
        x,y=int(input("Παίκτη"+" "+str(p)+": Δώστε γραμμή και στήλη"+" "+str(i)+"ης"+" "+"κάρτας:")),int(input())
        while (x>4 or y>10):
            print("Λανθασμένη θεση,προσπαθήστε ξανά")
            x,y=int(input("Παίκτη"+" "+str(p)+": Δώστε γραμμή και στήλη"+" "+str(i)+"ης"+" "+"κάρτας:")),int(input()) 
    elif a==3:
        x,y=int(input("Παίκτη"+" "+str(p)+": Δώστε γραμμή και στήλη"+" "+str(i)+"ης"+" "+"κάρτας:")),int(input())
        while (x>4 or y>13):
            print("Λανθασμένη θεση,προσπαθήστε ξανά")
            x,y=int(input("Παίκτη"+" "+str(p)+": Δώστε γραμμή και στήλη"+" "+str(i)+"ης"+" "+"κάρτας:")),int(input()) 
    thesi.append(x)
    thesi.append(y)
    return thesi 

def chosen_card(a,c,x,y,cards,p,i):
    """
    Ανοιγει την καρτα στην λιστα των "Χ"
    a -- επίπεδο δυσκολίας
    c -- Η λίστα με τα στοιχεία που βλέπει ο χρήστης
    x -- Η γραμμή της κάρτας που επέλεξε
    y -- Η στήλη της κάρτας που επέλεξε
    cards -- Η τράπουλα
    p -- Ο αριθμός του παίκτη
    i -- Ο αριθμός της κάρτας
    >>> c=start_list(1)
    >>> cards=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q']
    >>> print(chosen_card(1,c,1,1,cards,1,2))
    a
    >>> chosen_card(1,c,3,4,cards,1,1)=='m'
    True
    """
    stiles = len(cards) // 4
    list_x = c
    k = list_x.count("X")
    if k==0:
        print("Ολες οι καρτες εχουν ανοιχτει")
    else:
        if x==1:
            pos = y-1
        elif x==2:
            pos = y+stiles-1
        elif x==3:
            pos=y+stiles*2-1
        elif x==4:
            pos=y+stiles*3-1
        while list_x[pos]!="X":
            print("Η καρτα που ζητησατε εχει ηδη ανοιχτει.Δωστε εγκυρη θεση καρτας.")
            thesi=dwse_thesi_kartas(p,i,a)
            x=thesi[0]
            y=thesi[1]
            if x==1:
                pos = y-1
            elif x==2:
                pos = y+stiles-1
            elif x==3:
                pos=y+stiles*2-1
            elif x==4:
                pos=y+stiles*3-1
    chosen_card = ''
    if x==1:
        chosen_card = cards[y-1]
    elif x==2:
        deiktis = y+stiles-1        
        chosen_card = cards[deiktis]
    elif x==3:
        deiktis = y + stiles*2-1
        chosen_card = cards[deiktis]
    elif x==4:
        deiktis = y+stiles*3-1
        chosen_card = cards[deiktis]
    return chosen_card
