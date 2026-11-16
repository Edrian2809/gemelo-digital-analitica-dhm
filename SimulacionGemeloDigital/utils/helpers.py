# utils/helpers.py
def caj(n):
    return "{:,.0f} caj".format(n)

def monto(n):
    return "C$ {:,.0f}".format(n)

def margen_ajustado(margen, delta_p):
    den = 1.0 + delta_p
    if abs(den) < 1e-6:
        return margen
    return (margen + delta_p) / den