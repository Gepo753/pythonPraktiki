chislo = int(input("Введите число: "))
otvet = 10
while otvet<100:
    if chislo % otvet== 0:
        print(f"Делитель:{otvet}")
        break
    otvet+=1

