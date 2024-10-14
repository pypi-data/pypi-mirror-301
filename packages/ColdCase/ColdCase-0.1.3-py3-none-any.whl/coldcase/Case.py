from typing import Union

class BasicArithmetic:
    def multiply(self, *args:Union[int, float]) -> float:
        total = 1.00
        for num in args:
            total *= num
        return total
    def divide(self, *args:Union[int, float]) -> float:
        if not args:
            raise ValueError("Division requires at least one argument")
        total = args[0]
        for num in args[1:]:
            total /= num
        return total
  
    def add(self, *args:Union[int, float]) -> float:
        total = 00.00
        for num in args:
            total += num
        return total
   
    def subtract(self, *args:Union[int, float]) -> float:
        total = 00.00
        for num in args:
            total -= num
        return total
   
    def squareroot(self, num:Union[int, float]) -> float:
        if num < 0:
            raise ValueError("Square root of negative number is not possible")
        return num ** 0.5
   
    def mean(self, data):
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

    def standard_deviation(self, data):
        m = self.mean(data)
        return (sum([(x - m) ** 2 for x in data]) / len(data)) ** 0.5
    
    
math = BasicArithmetic()
assert math.multiply(2, 3, 4) == 24
assert math.multiply(2, 3, 4, 5) == 120
assert math.divide(2, 3, 4) == 0.16666666666666666
assert math.squareroot(4) == 2
