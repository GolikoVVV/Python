def is_year_leap(year):
    return "True" if year % 4 == 0 else "False"
year = int(input("Введите число: "))
result = is_year_leap(year)
print("год ", + year, ": ", result)