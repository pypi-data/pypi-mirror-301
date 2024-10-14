def mean(data):
    return sum(data) / len(data)

def median(data):
    data.sort()
    n = len(data)
    if n % 2 == 0:
        return (data[n // 2 - 1] + data[n // 2]) / 2
    else:
        return data[n // 2]

def mode(data):
    freq = {}
    for i in data:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1
    max_freq = max(freq.values())
    modes = [k for k, v in freq.items() if v == max_freq]
    return modes

def standard_deviation(data):
    m = mean(data)
    return (sum([(x - m) ** 2 for x in data]) / len(data)) ** 0.5