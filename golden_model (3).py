def alu_golden(op, a, b):
    a &= 0xFF
    b &= 0xFF

    if op == "ADD":
        s = a + b
        return s & 0xFF, 1 if s > 0xFF else 0

    if op == "SUB":
        d = a - b
        carry = 1 if a < b else 0
        return d & 0xFF, carry

    if op == "AND":
        return a & b, 0

    if op == "OR":
        return a | b, 0

    if op == "XOR":
        return a ^ b, 0

    if op == "SHL":
        carry = (a >> 7) & 1
        return (a << 1) & 0xFF, carry

    if op == "SHR":
        carry = a & 1
        return a >> 1, carry

    if op == "SRA":
        carry = a & 1
        sign = (a >> 7) & 1
        return (a >> 1) | (sign << 7), carry

    raise ValueError(f"unknown op {op}")
