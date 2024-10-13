# https://www.geeksforgeeks.org/how-to-generate-large-prime-numbers-for-rsa-algorithm/
# Large Prime Generation for RSA
import secrets

class PrimeNumberGen:
    """Generation of Prime numbers and checking if prime"""
    # Pre generated primes
    first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                         31, 37, 41, 43, 47, 53, 59, 61, 67,
                         71, 73, 79, 83, 89, 97, 101, 103,
                         107, 109, 113, 127, 131, 137, 139,
                         149, 151, 157, 163, 167, 173, 179,
                         181, 191, 193, 197, 199, 211, 223,
                         227, 229, 233, 239, 241, 251, 257,
                         263, 269, 271, 277, 281, 283, 293,
                         307, 311, 313, 317, 331, 337, 347, 349]

    @staticmethod
    def nBitRandom(n):
        if n < 0: raise ValueError(f"n must be an unsigned int! Current n:\n\n{n}\n")
        if not isinstance(n, int):
            raise TypeError("n must be an integer")
        return secrets.SystemRandom().randrange(pow(2, (n - 1)) + 1, pow(2, n) - 1)

    @staticmethod
    def getLowLevelPrime(n):
        """Generate a prime candidate divisible
        by first primes"""
        while True:
            # Obtain a random number
            pc = PrimeNumberGen.nBitRandom(n)

            # Test divisibility by pre-generated
            # primes
            for divisor in PrimeNumberGen.first_primes_list:
                if pc % divisor == 0 and divisor ** 2 <= pc:
                    break
            else:
                return pc

    @staticmethod
    def isMillerRabinPassed(mrc):
        """Run 20 iterations of Rabin Miller Primality test. Use to check if mrc is prime"""
        maxDivisionsByTwo = 0
        ec = mrc - 1
        while ec % 2 == 0:
            ec >>= 1
            maxDivisionsByTwo += 1
        assert (2 ** maxDivisionsByTwo * ec == mrc - 1)

        def trialComposite(round_tester):
            if pow(round_tester, ec, mrc) == 1:
                return False
            for i in range(maxDivisionsByTwo):
                if pow(round_tester, 2 ** i * ec, mrc) == mrc - 1:
                    return False
            return True

        # Set number of trials here
        numberOfRabinTrials = 20
        for i in range(numberOfRabinTrials):
            round_tester = secrets.SystemRandom().randrange(2, mrc)
            if trialComposite(round_tester):
                return False
        return True

    @staticmethod
    def generate(nBit: int) -> int:
        """
        Generates an nBit prime number
        :param nBit: The bit size of the number
        :return: Random nBit prime number as an int
        """
        if not isinstance(nBit, int):
            raise TypeError("nBit must be an integer")
        while True:
            prime_candidate = PrimeNumberGen.getLowLevelPrime(nBit)
            if not PrimeNumberGen.isMillerRabinPassed(prime_candidate):
                continue
            return prime_candidate
