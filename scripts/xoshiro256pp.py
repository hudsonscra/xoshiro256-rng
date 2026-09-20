#!/usr/bin/env python3
"""Xoshiro256++ PRNG — implementação pura em Python, seed via SplitMix64."""
import argparse
import time

MASK64 = (1 << 64) - 1

def rotl(x: int, k: int) -> int:
    return ((x << k) | (x >> (64 - k))) & MASK64

class SplitMix64:
    def __init__(self, seed: int):
        self.state = seed & MASK64

    def next(self) -> int:
        self.state = (self.state + 0x9E3779B97F4A7C15) & MASK64
        z = self.state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK64
        return z ^ (z >> 31)

class Xoshiro256pp:
    def __init__(self, seed: int):
        sm = SplitMix64(seed)
        self.s = [sm.next() for _ in range(4)]

    def next(self) -> int:
        result = (rotl((self.s[0] + self.s[3]) & MASK64, 23) + self.s[0]) & MASK64
        t = (self.s[1] << 17) & MASK64

        self.s[2] ^= self.s[0]
        self.s[3] ^= self.s[1]
        self.s[1] ^= self.s[2]
        self.s[0] ^= self.s[3]
        self.s[2] ^= t
        self.s[3] = rotl(self.s[3], 45)

        return result

    def randint(self, lo: int, hi: int) -> int:
        """Uniforme em [lo, hi], sem viés de módulo (rejection sampling)."""
        range_size = hi - lo + 1
        limit = (2**64 // range_size) * range_size
        while True:
            r = self.next()
            if r < limit:
                return lo + (r % range_size)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lo", type=int, default=1)
    parser.add_argument("--hi", type=int, default=100)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else time.time_ns()
    rng = Xoshiro256pp(seed)
    print(rng.randint(args.lo, args.hi))
