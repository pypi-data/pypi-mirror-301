# pymatica/basic_statistics.py

class BasicStatistics:
    @staticmethod
    def mean(data):
        return sum(data) / len(data)

    @staticmethod
    def median(data):
        n = len(data)
        if n == 0:
            return None
        sorted_data = sorted(data)
        mid = n // 2
        return (sorted_data[mid] + sorted_data[mid - 1]) / 2 if n % 2 == 0 else sorted_data[mid]

    @staticmethod
    def mode(data):
        frequency = {}
        for value in data:
            frequency[value] = frequency.get(value, 0) + 1
        max_count = max(frequency.values())
        return [key for key, count in frequency.items() if count == max_count]

    @staticmethod
    def variance(data):
        n = len(data)
        if n < 2:
            return None
        mean = BasicStatistics.mean(data)
        return sum((x - mean) ** 2 for x in data) / n

    @staticmethod
    def std_deviation(data):
        variance_value = BasicStatistics.variance(data)
        return variance_value ** 0.5 if variance_value is not None else None
