import json

from vectors import generate_vectors, OPS, total_buckets
from golden_model import alu_golden


def parse_bits(s):
    return int(s, 2)


def main():
    vecs = generate_vectors()
    with open("dut_results.txt") as f:
        lines = [l.strip() for l in f if l.strip()]

    assert len(lines) == len(vecs), (
        f"vector count mismatch: sim produced {len(lines)}, expected {len(vecs)}"
    )

    hit_buckets = {op: set() for op in OPS}
    failures = []
    passed = 0

    n_directed = sum(1 for v in vecs if not v[4])
    n_random = sum(1 for v in vecs if v[4])

    log_lines = []
    log_lines.append(f"$ python run_regression.py --vectors {len(vecs)} --seed 4471")
    log_lines.append(f"streaming stimulus: {n_directed} directed, {n_random} randomised")

    for i, (line, (op, a, b, bucket, is_random)) in enumerate(zip(lines, vecs)):
        op_bits, a_bits, b_bits, res_bits, carry_bit = line.split()
        dut_result = parse_bits(res_bits)
        dut_carry = int(carry_bit)

        ref_result, ref_carry = alu_golden(op, a, b)
        ok = (dut_result == ref_result) and (dut_carry == ref_carry)
        hit_buckets[op].add(bucket)

        if ok:
            passed += 1
            if i < 6:
                log_lines.append(
                    f"  [PASS] vec {i:04d}  op={op:<4} a=0x{a:02X} b=0x{b:02X}  "
                    f"dut=0x{dut_result:02X} ref=0x{ref_result:02X}"
                )
        else:
            failures.append((i, op, a, b, dut_result, dut_carry, ref_result, ref_carry, bucket))
            log_lines.append(
                f"  [FAIL] vec {i:04d}  op={op:<4} a=0x{a:02X} b=0x{b:02X}  "
                f"dut=0x{dut_result:02X} ref=0x{ref_result:02X}  <-- mismatch"
            )

    total = len(vecs)
    defined = total_buckets()
    defined_count = sum(len(v) for v in defined.values())
    hit_count = sum(len(hit_buckets[op] & defined[op]) for op in OPS)
    coverage_pct = 100.0 * hit_count / defined_count

    log_lines.append("...")
    log_lines.append(
        f"{passed}/{total} passed \u00b7 {len(failures)} bug(s) logged \u00b7 coverage {coverage_pct:.1f}%"
    )

    for idx, (i, op, a, b, dr, dc, rr, rc, bucket) in enumerate(failures[:3]):
        log_lines.append(
            f"bug_{idx+1:04d}: {op} mismatch on vector {i} (bucket={bucket}): "
            f"a=0b{a:08b} b=0b{b:08b} -> dut=0b{dr:08b} ref=0b{rr:08b}"
        )

    report = "\n".join(log_lines)
    print(report)

    with open("regression_report.txt", "w") as f:
        f.write(report + "\n")

    with open("coverage.csv", "w") as f:
        f.write("op,bucket,hit\n")
        for op in OPS:
            for bucket in sorted(defined[op]):
                f.write(f"{op},{bucket},{1 if bucket in hit_buckets[op] else 0}\n")

    with open("summary.json", "w") as f:
        json.dump(
            {
                "total": total,
                "passed": passed,
                "failed": len(failures),
                "coverage_pct": round(coverage_pct, 1),
                "failures": [
                    {
                        "vector": i, "op": op, "a": a, "b": b,
                        "dut_result": dr, "dut_carry": dc,
                        "ref_result": rr, "ref_carry": rc, "bucket": bucket,
                    }
                    for (i, op, a, b, dr, dc, rr, rc, bucket) in failures
                ],
            },
            f,
            indent=2,
        )


if __name__ == "__main__":
    main()
