
def german_to_us_numbers(german_number):
    us_number=german_number.replace(".","").replace(",",".")
    us_number=float(us_number)
    return us_number