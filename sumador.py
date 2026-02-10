# ==============================
# Sumador–Restador 4 bits
# Salida: 5 bits (R4 R3 R2 R1 R0)
# Modo: 0 = suma, 1 = resta (complemento a 2)
# ==============================

def AND(a, b):
    return 1 if (a == 1 and b == 1) else 0

def OR(a, b):
    return 1 if (a == 1 or b == 1) else 0

def NOT(a):
    return 0 if a == 1 else 1


# XOR "construido" con AND/OR/NOT:
# XOR(a,b) = (a AND NOT(b)) OR (NOT(a) AND b)
def XOR(a, b):
    return OR(AND(a, NOT(b)), AND(NOT(a), b))


# Sumador completo: entradas a, b, cin -> salidas s, cout
def full_adder(a, b, cin):
    axb = XOR(a, b)
    s = XOR(axb, cin)
    cout = OR(AND(a, b), AND(cin, axb))
    return s, cout


# Convierte entero 0..15 a bits [b0,b1,b2,b3] (LSB primero)
# (Esto es interfaz de entrada, no el "circuito interno")
def int_to_4bits(n):
    bits = [0, 0, 0, 0]
    for i in range(4):
        bits[i] = 1 if (n % 2 == 1) else 0
        n = n // 2
    return bits


def bits4_to_str(bits4):
    # bits4 = [b0,b1,b2,b3]
    return f"{bits4[3]}{bits4[2]}{bits4[1]}{bits4[0]}"


def bits5_to_str(bits5):
    # bits5 = [b0,b1,b2,b3,b4] donde b4 es el MSB (carry final)
    return f"{bits5[4]}{bits5[3]}{bits5[2]}{bits5[1]}{bits5[0]}"


# Sumador-restador:
# A_bits, B_bits: [b0,b1,b2,b3]
# M: 0 suma, 1 resta
# Salida: bits5 = [R0,R1,R2,R3,R4] (R4 = carry final)
def add_sub_4bit_result5(A_bits, B_bits, M):
    if len(A_bits) != 4 or len(B_bits) != 4:
        raise ValueError("A_bits y B_bits deben tener 4 bits.")
    if M not in (0, 1):
        raise ValueError("M debe ser 0 (suma) o 1 (resta).")

    # Preparación de B: B' = B XOR M (bit a bit)
    Bp = [0, 0, 0, 0]
    for i in range(4):
        Bp[i] = XOR(B_bits[i], M)

    # Carry inicial: C0 = M (para el +1 del complemento a 2 en resta)
    carry = M

    R = [0, 0, 0, 0]
    for i in range(4):
        R[i], carry = full_adder(A_bits[i], Bp[i], carry)

    # Resultado de 5 bits: [R0,R1,R2,R3,R4]
    R5 = [R[0], R[1], R[2], R[3], carry]
    return R5, Bp


# ==============================
# PROGRAMA PRINCIPAL
# ==============================
print("Sumador–Restador de 4 bits")
print("Modo: 0 = Suma | 1 = Resta")
print("Salida: 5 bits (R4 R3 R2 R1 R0), donde R4 es el acarreo final\n")

A = int(input("Ingrese A (0–15): "))
B = int(input("Ingrese B (0–15): "))
M = int(input("Ingrese modo M (0 suma / 1 resta): "))

if not (0 <= A <= 15 and 0 <= B <= 15 and M in [0, 1]):
    print("\nEntrada inválida. Use A y B entre 0 y 15, y M en {0,1}.")
else:
    A_bits = int_to_4bits(A)
    B_bits = int_to_4bits(B)

    R5, Bp = add_sub_4bit_result5(A_bits, B_bits, M)

    print("\nA =", bits4_to_str(A_bits))
    print("B =", bits4_to_str(B_bits))
    print("Resultado (5 bits) =", bits5_to_str(R5))
