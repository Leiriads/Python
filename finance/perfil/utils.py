def calcula_total(obj, campo):
    total = 0
    for i in obj:
        total += getattr(i, campo)

    return total