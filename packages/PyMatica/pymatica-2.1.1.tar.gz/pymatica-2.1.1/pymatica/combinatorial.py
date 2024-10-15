class CombinatorialFunctions:
    @staticmethod
    def factorial(n):
        """Calculate the factorial of a non-negative integer n."""
        if n < 0:
            raise ValueError("Negative values are not allowed.")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    def combinations(n, r):
        """Calculate the number of combinations of n items taken r at a time."""
        if r > n:
            return 0
        return CombinatorialFunctions.factorial(n) // (CombinatorialFunctions.factorial(r) * CombinatorialFunctions.factorial(n - r))

    @staticmethod
    def permutations(n, r):
        """Calculate the number of permutations of n items taken r at a time."""
        if r > n:
            return 0
        return CombinatorialFunctions.factorial(n) // CombinatorialFunctions.factorial(n - r)

    @staticmethod
    def combinations_with_repetition(n, r):
        """Calculate the number of combinations of n items taken r at a time with repetition allowed."""
        return CombinatorialFunctions.combinations(n + r - 1, r)

    @staticmethod
    def binomial_coefficient(n, k):
        """Calculate the binomial coefficient C(n, k), also known as "n choose k"."""
        if k < 0 or k > n:
            return 0
        return CombinatorialFunctions.combinations(n, k)

    @staticmethod
    def generate_combinations(elements, r):
        """Generate all combinations of r elements from a list of elements."""
        from itertools import combinations
        return list(combinations(elements, r))

    @staticmethod
    def generate_permutations(elements, r):
        """Generate all permutations of r elements from a list of elements."""
        from itertools import permutations
        return list(permutations(elements, r))


