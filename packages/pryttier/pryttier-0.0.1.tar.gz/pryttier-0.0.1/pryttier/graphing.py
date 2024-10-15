import matplotlib
import matplotlib.pyplot as plt
from typing import *
from os import PathLike
from .tools import *
from .math import *
import pandas as pd

import numpy as np
import enum


class GraphStyle(enum.Enum):
    DEFAULT = 'default'
    CLASSIC = 'classic'
    GRAYSCALE = 'grayscale'
    GGPLOT = 'ggplot'
    SEABORN = 'seaborn-v0_8'
    FAST = 'fast'
    BMH = 'bmh'
    SOLARIZED_LIGHT = 'Solarize_Light2'
    SEABORN_NOTEBOOK = 'seaborn-v0_8-notebook'


class ColorMap(enum.Enum):
    ACCENT = "Accent"
    BLUES = "Blues"
    BRBG = "BrBG"
    BUGN = "BuGN"
    BUPU = "BuPu"
    CMRMAP = "CMRmap"
    DARK2 = "Dark_2"
    GNBU = "GnBu"
    GRAYS = "Grays"
    GREENS = "Greens"
    GREYS = "Greys"
    ORRD = "OrRd"
    ORANGES = "Oranges"
    PRGN = "PRGn"
    PAIRED = "Paired"
    PASTEL1 = "Pastel1"
    PASTEL2 = "Pastel2"
    PIYG = "PiYG"
    PUBU = "PuBu"
    PUBUGN = "PuBuGn"
    PUOR = "PuOr"
    PURD = "PuRd"
    PURPLES = "Purples"
    RDBU = "RdBu"
    RDGY = "RdGy"
    RDPU = "RdPu"
    RDYLBU = "RdYlBu"
    RDYLGN = "RdYlGn"
    REDS = "Reds"
    SET1 = "Set1"
    SET2 = "Set2"
    SET3 = "Set3"
    SPECTRAL = "Spectral"
    WISTIA = "Wistia"
    YLGN = "YlGn"
    YLGNBU = "YlGnBu"
    YLORBT = "YlOrBt"
    YLORRD = "YlOrRd"
    AFMHOT = "afmhot"
    AUTUMN = "autumn"
    BINARY = "binary"
    BONE = "bone"
    BRG = "brg"
    BWR = "bwr"
    CIVIDIS = "cividis"
    COOL = "cool"
    COOLWARM = "coolwarm"
    COPPER = "copper"
    CUBEHELIX = "cubehelix"
    FLAG = "flag"
    GIST_EARTH = "gist_earth"
    GIST_GRAY = "gist_gray"
    GIST_HEAT = "gist_heat"
    GIST_NCAR = "gist_ncar"
    GIST_RAINBOW = "gist_rainbow"
    GIST_STERN = "gist_stern"
    GIST_YARG = "gist_yarg"
    GIST_YERG = "gist_yerg"
    GNUPLOT = "gnuplot"
    GNUPLOT2 = "gnuplot_2"
    GRAY = "gray"
    GREY = "grey"
    HOT = "hot"
    HSV = "hsv"
    INFERNO = "inferno"
    JET = "jet"
    MAGMA = "magma"
    NIPY_SPECTRAL = "nipy_spectral"
    OCEAN = "ocean"
    PINK = "pink"
    PLASMA = "plasma"
    PRISM = "prism"
    RAINBOW = "rainbow"
    SEISMIC = "seismic"
    SPRING = "spring"
    SUMMER = "summer"
    TAB10 = "tab_10"
    TAB20 = "tab_20"
    TAB20B = "tab_20_b"
    TAB20C = "tab_20_c"
    TERRAIN = "terrain"
    TRUBO = "trubo"
    TWILIGHT = "twilight"
    TWILIGHT_SHIFTED = "twilight_shifted"
    VIRIDIS = "viridis"
    WINTER = "winter"


class ColorFunction(enum.Enum):
    MAGNITUDE = lambda u, v: np.sqrt(u ** 2 + v ** 2)
    SUM = lambda u, v: abs(u) + abs(v)
    DIFFERENCE = lambda u, v: abs(u) - abs(v)
    PRODUCT = lambda u, v: u * v


class Coord:
    def __init__(self, x: int | float, y: int | float, z: int | float = 0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Coord(self.x * other.x, self.y * other.y, self.z * other.z)

    def __truediv__(self, other):
        return Coord(self.x / other.x, self.y / other.y, self.z / other.z)

    def __abs__(self):
        return Coord(abs(self.x), abs(self.y), abs(self.z))


def distanceBetweenPoints(a: Coord, b: Coord):
    change = b - a
    return sqrt(change.x * change.x + change.y * change.y)


class Graph2D:
    def __init__(self, name: str = "Graph 2D", style: GraphStyle = GraphStyle.DEFAULT):
        plt.style.use(style)
        self.name = name
        self.subplots = 0

    def addAxes(self):
        self.ax = plt.axes()
        self.ax.set_title(self.name)

    def addSubplot(self, row: int, col: int):
        self.subplots += 1
        self.ax = plt.subplot(row, col, self.subplots)

    def setTitle(self, title: str):
        plt.title(title)

    def setXLabel(self, label: str):
        plt.xlabel(label)

    def setYLabel(self, label: str):
        plt.ylabel(label)

    def plotPoint(self, point: Coord, color: str = 'blue'):
        return self.ax.scatter(point.x, point.y, color=color)

    def plotPoints(self, *points: Coord, color: str = 'blue'):
        return self.ax.scatter([i.x for i in points], [j.y for j in points], color=color)

    def drawLine(self, start: Coord, end: Coord, color: str = 'blue', linestyle: str = "-"):
        return self.ax.plot([start.x, end.x], [start.y, end.y], color=color, linestyle=linestyle)

    def drawTriangle(self, a: Coord, b: Coord, c: Coord, color: str = 'blue', linestyle: str = "-"):
        sideA = self.drawLine(a, b, color=color, linestyle=linestyle)
        sideB = self.drawLine(b, c, color=color, linestyle=linestyle)
        sideC = self.drawLine(c, a, color=color, linestyle=linestyle)
        return sideA, sideB, sideC

    def functionPlot(self, func: Callable[[float | int], float | int], xrange=(-10, 10, 100), color='blue'):
        x = np.linspace(*xrange)
        y = apply(x, func)

        return self.ax.plot(x, y, color)

    def linePlot(self, xVals: Sequence, yVals: Sequence, color: str = 'blue'):
        if len(xVals) == len(yVals):
            return self.ax.plot(xVals, yVals, color)
        else:
            raise ValueError(f"Length of both arrays should be same. Lengths - X: {len(xVals)}, Y: {len(yVals)}")

    def scatterPlot(self, xVals: Sequence, yVals: Sequence, mapColor: bool = False,
                    cfunction: Callable | ColorFunction = (lambda x, y: x + y),
                    cmap: ColorMap = ColorMap.VIRIDIS, color: str = 'blue', colorBar: bool = False):
        c = apply2D(xVals, yVals, cfunction)
        if len(xVals) == len(yVals):
            if mapColor:
                sctr = self.ax.scatter(xVals, yVals, cmap=cmap.value, c=c)
                if colorBar:
                    plt.colorbar(sctr)
            elif not mapColor:
                sctr = self.ax.scatter(xVals, yVals, color=color)
        else:
            raise ValueError(f"Length of both arrays should be same. Lengths - X: {len(xVals)}, Y: {len(yVals)}")
        return sctr

    def plotCSV(self, csvFilePath: Union[str, PathLike], xHeader: str, yHeader: str, color: str = 'blue',
                dots: bool = False):
        data = pd.read_csv(csvFilePath)
        x = data[xHeader]
        y = data[yHeader]

        self.ax.plot(x, y, color)
        if dots:
            self.ax.scatter(x, y, c=color)

    @staticmethod
    def show():
        plt.show()
