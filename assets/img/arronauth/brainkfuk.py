def brainfuck_decode(code):
    tape = [0] * 30000  # Cinta de memoria de tamaño 30000
    pointer = 0  # Puntero de posición en la cinta
    output = ""  # Cadena de salida

    # Diccionario de correspondencias de paréntesis para bucles
    loop_map = {}

    # Construir mapa de paréntesis
    loop_stack = []
    for i, c in enumerate(code):
        if c == "[":
            loop_stack.append(i)
        elif c == "]":
            if len(loop_stack) == 0:
                raise ValueError("Error de sintaxis: paréntesis no balanceados")
            start = loop_stack.pop()
            loop_map[start] = i
            loop_map[i] = start

    if len(loop_stack) > 0:
        raise ValueError("Error de sintaxis: paréntesis no balanceados")

    # Ejecutar el código Brainfuck
    i = 0
    while i < len(code):
        c = code[i]

        if c == ">":
            pointer += 1
        elif c == "<":
            pointer -= 1
        elif c == "+":
            tape[pointer] = (tape[pointer] + 1) % 256
        elif c == "-":
            tape[pointer] = (tape[pointer] - 1) % 256
        elif c == ".":
            output += chr(tape[pointer])
        elif c == ",":
            raise NotImplementedError("La entrada de datos no está implementada")
        elif c == "[" and tape[pointer] == 0:
            i = loop_map[i]
        elif c == "]" and tape[pointer] != 0:
            i = loop_map[i]

        i += 1

    return output


# Ejemplo de uso
code = "++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>>---.+++++++++++..<<++.>++.>-----------.++.++++++++.<+++++.>++++++++++++++.<+++++++++.---------.<.>>-----------------.-------.++.++++++++.------.+++++++++++++.+.<<+.."
output = brainfuck_decode(code)
print("Salida:", output)

