import datetime as dt

def ls_to_matrix(ls, row_length):

    ls_of_ls = [ls[i:i+row_length] for i in range(0, len(ls), row_length)]

    return ls_of_ls

def calculate_age(birthdate, date):

    years = date.year - birthdate.year - ((date.month, date.day) < (birthdate.month, birthdate.day))
    
    if (date.month, date.day) < (birthdate.month, birthdate.day):
        time_to_birthday = dt.datetime(date.year, birthdate.month, birthdate.day) - dt.datetime(date.year, date.month, date.day)
        age = years + (365 - time_to_birthday.days) / 365
    else:
        time_after_birthday = dt.datetime(date.year, date.month, date.day) - dt.datetime(date.year, birthdate.month, birthdate.day)
        age = years + time_after_birthday.days / 365

    return round(age, 2)
