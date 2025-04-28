def generate_full_card(bin_code):
    import random

    while True:
        card = bin_code + ''.join(str(random.randint(0,9)) for _ in range(9))
        total = 0
        reverse_digits = card[::-1]
        for i, d in enumerate(reverse_digits):
            n = int(d)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        if total % 10 == 0:
            return card
