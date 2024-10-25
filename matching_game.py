from arxikes_synarthseis import *
from pythonex import *
from zhtoumena_xrhsth import *

num_of_players = numberofplayers()
level = difficulty()
trapoula=trapoula(level)
kartes = anakatema(trapoula,level)
kartes = stoixeia_trapoulas(kartes,level)
print('Η παρακάτω τράπουλα έχει εμφανισθεί για την διευκόλυνση του ελέγχου ανοίγματος της κάρτας')
print_board(kartes)
print('Καλωσήλθατε στο Matching Game')
print('Τώρα αρχίζει το παιχνίδι')
kartes_pou_vlepei_xrhsths = start_list(level)
print_board(kartes_pou_vlepei_xrhsths)
pontoi = []
for i in range(0,num_of_players):
  pontoi.append(0)
telos = False
player = 1

while player <= num_of_players and telos == False:
    num_of_cards = 1
    my_card1,my_card2 = '',''   
    while num_of_cards <= 2 and telos == False:
      epilogi_kartas = dwse_thesi_kartas(player,num_of_cards,level)  
      if num_of_cards == 1:    
        my_card1 = chosen_card(level,kartes_pou_vlepei_xrhsths,epilogi_kartas[0],epilogi_kartas[1],kartes,player,num_of_cards)
        pos1 = kartes.index(my_card1)
        k = list_changer(level,kartes_pou_vlepei_xrhsths,pos1,my_card1)
      else:
        my_card2 = chosen_card(level,kartes_pou_vlepei_xrhsths,epilogi_kartas[0],epilogi_kartas[1],kartes,player,num_of_cards)
        pos2 = kartes.index(my_card2)
        k = list_changer(level,kartes_pou_vlepei_xrhsths,pos2,my_card2)
          
      kartes_pou_vlepei_xrhsths = k
      print_board(kartes_pou_vlepei_xrhsths)
      num_of_cards += 1
   
    if my_card2[0]==my_card1[0]=='J':
      pontoi[player-1] = pontoi[player-1] + counter(my_card1,my_card2)
      print('Επιτυχές ταίριασμα +',counter(my_card1,my_card2),'πόντοι! Παίκτη ',player,' έχεις συνολικά ',pontoi[player-1],' πόντους.')
      anapodes_kartes = kartes_pou_vlepei_xrhsths.count('X')
      if anapodes_kartes == 0:
        telos = True
      else: 
        print('Παίκτη ',player,' παίζεις ξανά')
    elif my_card2[0]==my_card1[0]=='K':
      pontoi[player-1] = pontoi[player-1] + counter(my_card1,my_card2)
      print('Επιτυχές ταίριασμα +',counter(my_card1,my_card2),'πόντοι! Παίκτη ',player,' έχεις συνολικά ',pontoi[player-1],' πόντους.')
      anapodes_kartes = kartes_pou_vlepei_xrhsths.count('X')
      if anapodes_kartes == 0:
        telos = True 
      else:
        if num_of_players-player==1:
          player=1
          print('Παίκτη',num_of_players,'χάνεις τη σειρά σου')
        elif num_of_players-player==0:
          player=2
          print('Παίκτη',player-1,'χάνεις τη σειρά σου')
        else:
          player+=2
          print('Παίκτη',player-1,'χάνεις τη σειρά σου')
    elif (my_card1[0]=='K' and my_card2[0]=='Q') or (my_card1[0]=='Q' and my_card2[0]=='K'):
      print('Παίκτη ',player,'πρέπει να ανοίξεις άλλο ένα φύλλο')
      epilogi_kartas = dwse_thesi_kartas(player,3,level)
      my_card3 = chosen_card(level,kartes_pou_vlepei_xrhsths,epilogi_kartas[0],epilogi_kartas[1],kartes,player,num_of_cards)
      pos3 = kartes.index(my_card3)
      anapodes_kartes = kartes_pou_vlepei_xrhsths.count('X')
      if anapodes_kartes == 0:
        telos = True 
      if telos == False:
        k = list_changer(level,kartes_pou_vlepei_xrhsths,pos3,my_card3)
        kartes_pou_vlepei_xrhsths = k
        print_board(kartes_pou_vlepei_xrhsths)        
        if counter(my_card1,my_card2,my_card3) > 0:
          pontoi[player-1] = pontoi[player-1] + counter(my_card1,my_card2,my_card3)
          print('Επιτυχές ταίριασμα +',counter(my_card1,my_card2,my_card3),'πόντοι! Παίκτη ',player,' έχεις συνολικά ',pontoi[player-1],' πόντους.')
          if my_card1[0]==my_card3[0]:
            kartes_pou_vlepei_xrhsths[pos2]="X"
          elif my_card2[0]==my_card3[0]:
            kartes_pou_vlepei_xrhsths[pos1]="X"
        else:
          kartes_pou_vlepei_xrhsths[pos1]="X"
          kartes_pou_vlepei_xrhsths[pos2]="X"
          kartes_pou_vlepei_xrhsths[pos3]="X"
      if player >= num_of_players:
          player = 0
      player += 1
    else:
      if counter(my_card1,my_card2) > 0:
        pontoi[player-1] = pontoi[player-1] + counter(my_card1,my_card2)
        print('Επιτυχές ταίριασμα +',counter(my_card1,my_card2),'πόντοι! Παίκτη ',player,' έχεις συνολικά ',pontoi[player-1],' πόντους.')
      else:
        kartes_pou_vlepei_xrhsths[pos1]="X"
        kartes_pou_vlepei_xrhsths[pos2]="X"
      if player == num_of_players:
          player = 0
      player += 1

    anapodes_kartes = kartes_pou_vlepei_xrhsths.count('X')
    if anapodes_kartes == 0:
      telos = True 

max_pontoi = 0
max_pontoi = pontoi[0]
i = 1
while i <= num_of_players:
  if max_pontoi < pontoi[i-1]:
    max_pontoi = pontoi[i-1]
  i += 1
i, nikites = 0,0
while i <= num_of_players:
  if  max_pontoi == pontoi[i-1]:
    kerdise = i
    nikites += 1
  i += 1
if nikites == 1:
  print('Ο νικητής του παιχνιδιού είναι ο παίκτης ',kerdise,' με ',max_pontoi,' πόντους')
else:
  print('Υπήρχε ισοπαλία μεταξύ των παικτών:')
  i = 0
  while i <= num_of_players-1:
    if max_pontoi == pontoi[i]:
      print (i+1)
    i += 1
  print('Οι οποίοι μάζεψαν ', max_pontoi,' πόντους')



      

    


