from vectors import generate_vectors, OPS


def to_bits(v, width):
    return format(v, f"0{width}b")


def main():
    vecs = generate_vectors()
    with open("vectors.txt", "w") as f:
        for op, a, b, bucket, is_random in vecs:
            f.write(f"{OPS[op]} {to_bits(a, 8)} {to_bits(b, 8)}\n")
    print(f"wrote {len(vecs)} vectors to vectors.txt")


if __name__ == "__main__":
    main()
