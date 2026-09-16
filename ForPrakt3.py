chislo = int(input("Введите число: "))
for i in range(1,chislo+1):
    if i % 7 == 0 and i % 5 != 0 :
        print(i)