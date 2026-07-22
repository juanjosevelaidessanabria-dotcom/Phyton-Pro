import random

caracteres = ["+","-","/","*","!","&","$","#","?","=","@","a","b","c","d","e","f","g","h","i","j","k","l","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0"]
lenght = int(input("Indica el largo de la contraseña:"))
password = []
for i in range(lenght):
    password.append(random.choice(caracteres))
print("La contraseña generada es:")
for i in range(lenght):
    print(password[i])