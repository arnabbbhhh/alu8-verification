import random

OPS = {
    "ADD": "000",
    "SUB": "001",
    "AND": "010",
    "OR":  "011",
    "XOR": "100",
    "SHL": "101",
    "SHR": "110",
    "SRA": "111",
}


def classify(op, a, b):
    if op == "ADD":
        if a == 0 and b == 0:
            return "zero"
        if a + b > 255:
            return "overflow"
        return "random"
    if op == "SUB":
        if a == b:
            return "zero_result"
        if a < b:
            return "borrow"
        return "random"
    if op in ("AND", "OR", "XOR"):
        if a == 0 and b == 0:
            return "all_zero"
        if a == 0xFF and b == 0xFF:
            return "all_one"
        return "random"
    if op == "SHL":
        return "msb_one" if (a >> 7) & 1 else "msb_zero"
    if op == "SHR":
        return "lsb_one" if a & 1 else "lsb_zero"
    if op == "SRA":
        return "negative" if (a >> 7) & 1 else "positive"
    return "random"


def total_buckets():
    return {
        "ADD": {"zero", "overflow", "random"},
        "SUB": {"zero_result", "borrow", "random"},
        "AND": {"all_zero", "all_one", "random"},
        "OR":  {"all_zero", "all_one", "random"},
        "XOR": {"all_zero", "all_one", "random"},
        "SHL": {"msb_one", "msb_zero", "random"},
        "SHR": {"lsb_one", "lsb_zero", "random"},
        "SRA": {"negative", "positive", "random"},
    }


def generate_vectors(seed=4471, n_random_per_op=50):
    rnd = random.Random(seed)
    vectors = []

    directed = [
        ("ADD", 0, 0), ("ADD", 255, 255),
        ("SUB", 5, 5), ("SUB", 3, 9),
        ("AND", 0, 0), ("AND", 255, 255),
        ("OR", 0, 0), ("OR", 255, 255),
        ("XOR", 0, 0), ("XOR", 255, 255),
        ("SHL", 0b10000000, 0), ("SHL", 0b00000001, 0),
        ("SHR", 0b00000001, 0), ("SHR", 0b00000010, 0),
        ("SRA", 0b10000000, 0), ("SRA", 0b01111111, 0),
    ]
    for op, a, b in directed:
        vectors.append((op, a, b, classify(op, a, b), False))

    for op in OPS:
        for _ in range(n_random_per_op):
            a = rnd.randint(0, 255)
            b = rnd.randint(0, 255)
            vectors.append((op, a, b, classify(op, a, b), True))

    return vectors
