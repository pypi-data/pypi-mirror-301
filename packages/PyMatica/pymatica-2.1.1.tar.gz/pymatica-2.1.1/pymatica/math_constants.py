class MathConstants:
    PI = 3.141592653589793  # Ratio of circumference to diameter of a circle
    E = 2.718281828459045   # Base of the natural logarithm
    PHI = 1.618033988749895  # Golden ratio
    GOLDEN_RATIO = PHI      # Alias for PHI
    SQRT2 = 1.4142135623730951  # Square root of 2
    SQRT3 = 1.7320508075688772  # Square root of 3
    SQRT5 = 2.23606797749979  # Square root of 5
    LOG2E = 1.4426950408889634  # log base 2 of e
    LOG10E = 0.4342944819032518  # log base 10 of e
    SQRTPI = 1.772453850905516  # Square root of π

    @staticmethod
    def get_constant(name):
        constants = {
            'pi': MathConstants.PI,
            'e': MathConstants.E,
            'phi': MathConstants.PHI,
            'golden_ratio': MathConstants.GOLDEN_RATIO,
            'sqrt2': MathConstants.SQRT2,
            'sqrt3': MathConstants.SQRT3,
            'sqrt5': MathConstants.SQRT5,
            'log2e': MathConstants.LOG2E,
            'log10e': MathConstants.LOG10E,
            'sqrtpi': MathConstants.SQRTPI,
        }
        return constants.get(name.lower(), None)


