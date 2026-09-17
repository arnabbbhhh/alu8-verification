# alu8 — a Python verification harness around a real VHDL ALU

A small 8-bit ALU (`rtl/alu8.vhd`) verified by a real GHDL simulation, checked against
a pure-Python golden model. This is not a mockup — every number quoted below came
from actually running the simulator and the scoreboard script.

## What's in here

- `rtl/alu8.vhd` — the design under test. ADD, SUB, AND, OR, XOR, SHL, SHR, SRA.
- `tb/alu8_tb.vhd` — a file-driven testbench. Reads stimulus from `vectors.txt`,
  drives the DUT, and dumps `opcode a b result carry` to `dut_results.txt`.
- `py/vectors.py` — the stimulus generator (16 directed edge cases + 400 randomised
  vectors, 50 per opcode), with functional-coverage bucket tags.
- `py/golden_model.py` — the reference model the DUT is checked against.
- `py/generate_vectors.py` — writes `vectors.txt` for the testbench.
- `py/scoreboard.py` — reads `dut_results.txt`, re-derives the same vectors, diffs
  against the golden model, tracks coverage, and writes `regression_report.txt`,
  `coverage.csv` and `summary.json`.
- `work/buggy_report.txt` / `work/fixed_report.txt` — the two real regression runs
  described below.

## The real bug this caught

The first version of the SRA (arithmetic shift right) case was copy-pasted from
SHR (logical shift right) and never updated to sign-extend:

```vhdl
when "111" =>                      -- SRA (arithmetic, shift by 1)
  result <= '0' & a(7 downto 1);   -- BUG: should sign-extend with a(7)
  carry  <= a(0);
```

Running the harness against that version: **383/416 passed, 33 real failures**,
every one of them an SRA vector with a negative operand (`work/buggy_report.txt`).

Fix — sign-extend with the original MSB instead of zero-filling:

```vhdl
when "111" =>
  result <= a(7) & a(7 downto 1);  -- FIX
  carry  <= a(0);
```

Re-running the identical 416 vectors: **416/416 passed, 0 failures**
(`work/fixed_report.txt`).

Functional coverage settled at 87.5% (21/24 defined buckets) — the three misses
are a `random` bucket defined for SHL/SHR/SRA that the current classifier can
never actually assign, since every shift vector already lands in a more specific
bucket. That's a real, known gap in the coverage model, not a hidden one.

## Reproducing this yourself

Requires GHDL (`apt install ghdl`) and Python 3.

```bash
cd work
python3 ../py/generate_vectors.py
ghdl -a --std=08 alu8.vhd
ghdl -a --std=08 alu8_tb.vhd
ghdl -e --std=08 alu8_tb
ghdl -r --std=08 alu8_tb
python3 scoreboard.py
```
