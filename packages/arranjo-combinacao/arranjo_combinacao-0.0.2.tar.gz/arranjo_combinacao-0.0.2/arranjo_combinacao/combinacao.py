from math import factorial


def calcular_combinacao(k, n):
        resultado = factorial(k) / (factorial(k - n)*(factorial(n)))
        return resultado