from typing import *
from numpy import *
from .graphing import *

PI = 2 * acos(0)
Degrees = PI / 180


def summation(n: float | int, i: float | int, expr: Callable) -> float:
    total = 0
    for j in range(n, i + 1):
        total += expr(j)
    return total


def product(n: int, i: int, expr: Callable) -> float:
    total = 1
    for j in range(n, i):
        total *= expr(j)
    return total


def clamp(num: float, low: float, high: float) -> float:
    if (num > low) and (num < high):
        return num
    else:
        if num < low:
            return low
        if num > high:
            return high


def sign(num: float) -> int:
    return int(num / abs(num))


def factorial(num: int) -> int:
    if num == 0:
        return 1
    if num == 1:
        return 1
    return num * factorial(num - 1)


def binToDec(num: int) -> int:
    digits = [int(i) for i in list(str(num))]
    total = 0
    for j in range(0, len(digits)):
        total += (2 ** j) * (digits[j])
    return total


def mapRange(value: int | float,
             min1: float,
             max1: float,
             min2: float,
             max2: float) -> float:
    return (value - min1) / (max1 - min1) * (max2 - min2) + min2


class Vector2:
    def __init__(self,
                 x: float | int,
                 y: float | int):
        self.x = x
        self.y = y
        self.length = sqrt(self.x * self.x + self.y * self.y)

    def __str__(self) -> str:
        return f"{self.x}i + {self.y}j"

    def __add__(self, other: Self) -> Self:
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> Self:
        return Vector2(self.x * other, self.y * other)

    def normalize(self) -> Self:
        return Vector2(self.x / self.length, self.y / self.length)


class Vector3:
    def __init__(self,
                 x: float | int,
                 y: float | int,
                 z: float | int):
        self.x = x
        self.y = y
        self.z = z
        self.length = sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __str__(self) -> str:
        return f"{self.x}i + {self.y}j + {self.z}k"

    def __add__(self, other: Self | float) -> Self:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Self) -> Self:
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: float) -> Self:
        return Vector3(self.x * other, self.y * other, self.z * other)

    def normalize(self) -> Self:
        return Vector3(self.x / self.length, self.y / self.length, self.z / self.length)


def dot(a: Vector2 | Vector3,
        b: Vector2 | Vector3) -> Vector2 | Vector3:
    if isinstance(a, Vector2) and isinstance(b, Vector2):
        return Vector2(a.x * b.x, a.y * b.y)
    elif isinstance(a, Vector3) and isinstance(b, Vector3):
        return Vector3(a.x * b.x, a.y * b.y, a.z * b.z)
    else:
        raise TypeError("Cannot multiply Vector 2 and Vector 3")


def cross(a: Vector2 | Vector3,
          b: Vector2 | Vector3) -> Vector3 | float:
    if (isinstance(a, Vector2)) and (isinstance(b, Vector2)):
        return (a.x * b.y) - (a.y * b.x)
    elif isinstance(a, Vector3) and isinstance(b, Vector3):
        return Vector3(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)
    else:
        raise TypeError("Cannot multiply Vector 2 and Vector 3")


def distance(a: Vector2 | Vector3 | Coord,
             b: Vector2 | Vector3 | Coord):
    if (isinstance(a, Vector2)) and (isinstance(b, Vector2)):
        return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)
    elif isinstance(a, Vector3) and isinstance(b, Vector3):
        return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2 + (b.z - a.z) ** 2)
    elif isinstance(a, Coord) and isinstance(b, Coord):
        return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2 + (b.z - a.z) ** 2)
    else:
        raise TypeError("Error in Calculation")


def encryptDecryptBinary(binaryCode: str, operations: str = ""):
    bits = []
    for i in binaryCode:
        if i == " ":
            continue
        else:
            bits.append(int(i))
    if operations == "":
        return binaryCode
    else:
        for i in list(operations):
            if i.isnumeric():
                continue
            if i == "I":
                bits = [int(not bool(i)) for i in bits]
            if i == "F":
                bits.reverse()
            if i == "S":
                n = (operations[operations.index(i) + 1])
                if n.isnumeric():
                    bits = [bits[i] for i in range(-int(n), len(bits) - int(n))]
                else:
                    raise Exception("There should be a number after S")
            if i == "X":
                code = "".join([str(i) for i in bits])
                part1 = list(code[0:4])
                part2 = list(code[4:])
                part1.reverse()
                part2.reverse()
                bits = [int(i) for i in part1] + [int(i) for i in part2]
            if i == "W":
                code = "".join([str(i) for i in bits])
                part1 = list(code[0:4])
                part2 = list(code[4:])
                part1 = [part1[i] for i in range(-1, len(part1) - 1)]
                part2 = [part2[i] for i in range(-1, len(part1) - 1)]
                bits = [int(i) for i in part1] + [int(i) for i in part2]

    return "".join([str(i) for i in bits])


def binaryToAscii(binary: str):
    codes = chunks(binary, 8)
    finalMsg = []
    for i in codes:
        if len(i) == 8:
            finalMsg.append(chr(int(i, 2)))
        else:
            raise ValueError("Each byte must be 8 bits long")
    return "".join(finalMsg)
