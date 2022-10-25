import math


def time_since(t1: float, t2: float, time_format: str = "long") -> str:
    time_diff = t1 - t2
    if time_format == "long":
        num_dict = ["año", "mes", "día", "hora", "minuto", "segundo"]
    else:
        num_dict = ["a", "M", "d", "h", "m", "s"]
    num = [
        math.trunc(time_diff / 31536000),
        math.trunc(time_diff / 2628000 % 12),
        math.trunc(time_diff / 86400 % 30.41666666666667),
        math.trunc(time_diff / 3600 % 24),
        math.trunc(time_diff / 60 % 60),
        round(time_diff % 60, 1),
    ]

    i = 0
    j = 0
    time_arr = []
    while i < 2 and j < 6:
        if num[j] > 0:
            if time_format == "long":
                if num_dict[j] == "mes":
                    amount = 'es'
                else:
                    amount = 's'
                time_arr.append(f"{num[j]:g} {num_dict[j]}{amount if num[j] != 1 else ''}")
            else:
                time_arr.append(f"{num[j]}{num_dict[j]}")
            i += 1
        j += 1

    if time_format == "long":
        return " y ".join(time_arr)

    return "".join(time_arr)
