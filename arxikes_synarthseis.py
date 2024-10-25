
def trapoula(a):
    """Δημιουργεί την τράπουλα.
    >>> len(trapoula(3)) == 52
    True
    """
    trapoula = []
    if a==1:
        for t in ["10","K","Q","J"]:
            trapoula.append(str(t) + " " + "\u2665")
            trapoula.append(str(t) + " " + "\u2666")
            trapoula.append(str(t) + " " + "\u2663")
            trapoula.append(str(t) + " " + "\u2660")
    elif a==2:
        trapoula.append("A" + " " + "\u2665")
        trapoula.append("A" + " " + "\u2666")
        trapoula.append("A" + " " + "\u2663")
        trapoula.append("A" + " " + "\u2660")
        for t in range(2,11):
            trapoula.append(str(t) + " " + "\u2665")
            trapoula.append(str(t) + " " + "\u2666")
            trapoula.append(str(t) + " " + "\u2663")
            trapoula.append(str(t) + " " + "\u2660")
    elif a==3:
        for t in range(2,11):
            trapoula.append(str(t) + " " + "\u2665")
            trapoula.append(str(t) + " " + "\u2666")
            trapoula.append(str(t) + " " + "\u2663")
            trapoula.append(str(t) + " " + "\u2660")
        for t in ["A","K","Q","J"]:
            trapoula.append(str(t) + " " + "\u2665")
            trapoula.append(str(t) + " " + "\u2666")
            trapoula.append(str(t) + " " + "\u2663")
            trapoula.append(str(t) + " " + "\u2660")
    return trapoula

def anakatema(trapoula,a):
    """Ανακάτεμα της τράπουλας.
    >>> trapoula(3) != anakatema(trapoula(3),3)
    True
    >>> len(trapoula(2)) != len(anakatema(trapoula(2),2))
    False
    """ 
    import random
    random.shuffle(trapoula)
    return trapoula

def stoixeia_trapoulas(trapoula,a):
    """Δίνεται η τράπουλα που θα χρησιμοποιηθεί στο υπόλοιπο παιχνίδι, 
    με βάση το επίπεδο δυσκολίας του παιχνιδιού.
    a -- επίπεδο δυσκολίας
            (1 == εύκολο
             2 == μέτριο
             3 == δύσκολο)
    >>> len(stoixeia_trapoulas(trapoula(1),1)) == 16
    True
    >>> print(len(stoixeia_trapoulas(trapoula(2),2)))
    40
    >>> dyskolo_paixnidi = stoixeia_trapoulas(trapoula(3),3)
    >>> len(dyskolo_paixnidi) == 52
    True
    """
    stoixeia_pinaka = []
    if a==1:
        arithmos_stoixeiwn = range(0,16)
    elif a==2:
        arithmos_stoixeiwn = range(0,40)
    else:
        arithmos_stoixeiwn = range(0,52)
    for i in arithmos_stoixeiwn:
        stoixeia_pinaka.append(trapoula[i])
    return stoixeia_pinaka

def print_board(stoixeia,dwse_thesi_kartas=None):
    """Εμφανίζει τον πίνακα της τράπουλας.
    """
    stiles = len(stoixeia) // 4
    y = 1
    k = 0
    while y <= 4:
        y_str, x = '', 1
        while x <= stiles:
            y_str = y_str + stoixeia[k] + ' '  
            k += 1                                     
            x += 1
        y += 1
        print(y_str)


