import random

def generate_full_card(bin_code):
    card_number = bin_code
    while len(card_number) < 15:
        card_number += str(random.randint(0, 9))
    checksum = get_luhn_checksum(card_number)
    card_number += str(checksum)
    expiry = f"{random.randint(1,12):02d}/{random.randint(24,29)}"
    cvv = f"{random.randint(100,999)}"
    return {
        'card_number': card_number,
        'expiry': expiry,
        'cvv': cvv
    }

def get_luhn_checksum(number):
    digits = [int(d) for d in reversed(number)]
    total = sum(digits[::2])
    for d in digits[1::2]:
        total += sum(divmod(2*d, 10))
    return (10 - (total % 10)) % 10
