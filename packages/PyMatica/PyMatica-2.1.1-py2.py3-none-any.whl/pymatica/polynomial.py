# pymatica/polynomial.py

class Polynomial:
    def __init__(self, coefficients):
        self.coefficients = coefficients  # Coefficients from highest degree to constant term

    def evaluate(self, x):
        return sum(coef * (x ** i) for i, coef in enumerate(reversed(self.coefficients)))

    def add(self, other):
        length = max(len(self.coefficients), len(other.coefficients))
        result = [0] * length
        for i in range(length):
            a = self.coefficients[i] if i < len(self.coefficients) else 0
            b = other.coefficients[i] if i < len(other.coefficients) else 0
            result[i] = a + b
        return Polynomial(result)

    def subtract(self, other):
        length = max(len(self.coefficients), len(other.coefficients))
        result = [0] * length
        for i in range(length):
            a = self.coefficients[i] if i < len(self.coefficients) else 0
            b = other.coefficients[i] if i < len(other.coefficients) else 0
            result[i] = a - b
        return Polynomial(result)

    def multiply(self, other):
        result = [0] * (len(self.coefficients) + len(other.coefficients) - 1)
        for i, a in enumerate(self.coefficients):
            for j, b in enumerate(other.coefficients):
                result[i + j] += a * b
        return Polynomial(result)

    def differentiate(self):
        if len(self.coefficients) == 1:
            return Polynomial([0])  # Derivative of a constant is zero
        result = [coef * (len(self.coefficients) - 1 - i) for i, coef in enumerate(self.coefficients[:-1])]
        return Polynomial(result)

    def __str__(self):
        terms = []
        for i, coef in enumerate(reversed(self.coefficients)):
            if coef:
                term = f"{coef}x^{len(self.coefficients) - 1 - i}" if len(self.coefficients) - 1 - i > 0 else str(coef)
                terms.append(term)
        return " + ".join(terms)

    def __call__(self, x):
        return self.evaluate(x)

    def roots(self):
        """Finds the roots of the polynomial using numpy's roots method."""
        if len(self.coefficients) == 0:
            return []
        # For polynomials of degree 2 or higher
        from numpy import roots
        return roots(self.coefficients)
