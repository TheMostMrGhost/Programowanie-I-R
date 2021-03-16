import time

print("Podaj dwie liczby zmiennoprzecinkowe:")
a=float(input("Podaj a:\n"))
b=float(input("Podaj b:\n"))

def suma(a,b):
    return a+b

def mnóż(a,b):
    return a*b

time_start_sum=time.perf_counter_ns()
print(suma(a,b))
time_stop_sum=time.perf_counter_ns()

time_start_mult=time.perf_counter_ns()
print(mnóż(a,b))
time_stop_mult=time.perf_counter_ns()
print("Czas dla dodawania:\n {0}".format(time_stop_sum-time_start_sum))
print("\nCzas dla mnożenia: \n {0}". format(time_stop_mult-time_start_mult))
print("Różnica czasów:\n{0}".format(time_stop_sum-time_start_sum -(time_stop_mult-time_start_mult)))