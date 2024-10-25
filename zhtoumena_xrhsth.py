
def numberofplayers():
    while True:
        try:
            numberofplayers=int(input('Δώστε αριθμό παικτών: '))
            if numberofplayers >= 2:
                return numberofplayers
                break
            else:
                print('Παρακαλώ δώστε έγκυρη τιμή!...')
        except:
            print('Παρακαλώ δώστε έγκυρη τιμή!')
            continue

def difficulty():
    while True:
        try:
            difficulty = int(input('Δώστε επίπεδο δυσκολίας Εύκολο (1), Μέτριο (2), Δύσκολο (3): '))
            if difficulty == 1 or difficulty ==  2 or difficulty == 3:
                return difficulty
                break
            else:
                print("Παρακαλώ δώστε έγκυρο επίπεδο δυσκολίας...!")
        except:
            print("Παρακαλώ δώστε έγκυρο επίπεδο δυσκολίας!")
            continue

