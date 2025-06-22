import math
def square(side):
    square = math.ceil(side ** 2)
    print(square)
side = float(input("Введите сторону квадрата: "))
square(side)