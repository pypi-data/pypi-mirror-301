class NumberTheoryTools:
    @staticmethod
    def gcd(a, b):
        """Calculate the greatest common divisor (GCD) of a and b."""
        while b:
            a, b = b, a % b
        return abs(a)

    @staticmethod
    def lcm(a, b):
        """Calculate the least common multiple (LCM) of a and b."""
        return abs(a * b) // NumberTheoryTools.gcd(a, b)

    @staticmethod
    def is_prime(n):
        """Check if a number n is prime."""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    @staticmethod
    def prime_factors(n):
        """Return a list of all prime factors of n."""
        factors = []
        # Check for number of 2s that divide n
        while n % 2 == 0:
            if 2 not in factors:
                factors.append(2)
            n //= 2
        # Check for odd factors from 3 onwards
        for i in range(3, int(n**0.5) + 1, 2):
            while n % i == 0:
                if i not in factors:
                    factors.append(i)
                n //= i
        if n > 2:
            factors.append(n)
        return factors

    @staticmethod
    def generate_primes(limit):
        """Generate a list of all prime numbers up to a specified limit using the Sieve of Eratosthenes."""
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False  # 0 and 1 are not prime numbers
        for start in range(2, int(limit**0.5) + 1):
            if sieve[start]:
                for multiple in range(start * start, limit + 1, start):
                    sieve[multiple] = False
        return [num for num, is_prime in enumerate(sieve) if is_prime]

    @staticmethod
    def fibonacci(n):
        """Return the nth Fibonacci number."""
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b

    @staticmethod
    def euler_totient(n):
        """Calculate the Euler's Totient function φ(n), which counts the integers up to n that are coprime to n."""
        result = n  # Initialize result as n
        p = 2
        while p * p <= n:
            # Check if p divides n
            if n % p == 0:
                # If it does, subtract multiples of p from the result
                while n % p == 0:
                    n //= p
                result -= result // p
            p += 1
        # If n has a prime factor greater than sqrt(n)
        if n > 1:
            result -= result // n
        return result


