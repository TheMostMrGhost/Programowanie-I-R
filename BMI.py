print("Podaj swoja mase ciala w kilogramach:\n")
masa=float(input())
print("Podaj swój wzrost w metrach")
wzrost=float(input())

bmi=masa/(wzrost**2)

print("BMI={0}".format(bmi))
if(bmi<18.5):
    print("Niedowaga")
elif(bmi>=18.5 and bmi <25):
    print("Masa prawidłowa")
elif(bmi>=25 and bmi<30):
    print("Nadwaga")
else:
    print("Otyłość")