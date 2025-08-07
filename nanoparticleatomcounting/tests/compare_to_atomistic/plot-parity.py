"""
parity.py  –  Plot parity (y = x) comparisons between two CSV files.

Usage
-----
    python parity.py file_A.csv file_B.csv  [--show]

The two input files must share the same column headers
(e.g., Perimeter, Interface, Surface, Total).  
A separate parity plot is produced for each shared column.
PNG files are written alongside the CSVs; pass --show to display
the figures interactively as well.
"""
import sys
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def read_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_a", help="first CSV file")
    ap.add_argument("csv_b", help="second CSV file")
    ap.add_argument("--show", action="store_true",
                    help="show the plots on screen (in addition to saving)")
    return ap.parse_args()

def main() -> None:
    args = read_args()

    # after reading and stripping whitespace
    df_a = pd.read_csv(args.csv_a)
    df_b = pd.read_csv(args.csv_b)

    df_a.columns = df_a.columns.str.strip()
    df_b.columns = df_b.columns.str.strip()

    # --- make the names consistent ---
    df_a = df_a.rename(columns={"Interfacial": "Interface"})   # <— key line
    # ---------------------------------

    common_cols = df_a.columns.intersection(df_b.columns)
    if common_cols.empty:
        sys.exit("Error: the two files share no common column headers.")

    out_dir = Path(".")  # write PNGs to the current directory

    # ---------- parity plots ----------
    for col in common_cols:
        x = df_a[col]
        y = df_b[col]

        # axis limits: a little padding around the combined min/max
        lo = min(x.min(), y.min())
        hi = max(x.max(), y.max())
        pad = 0.05 * (hi - lo)
        lo, hi = lo - pad, hi + pad

        plt.figure(figsize=(4, 4))
        plt.scatter(x, y, c="tab:blue")
        plt.plot([lo, hi], [lo, hi], "k--", lw=1)  # y = x reference
        plt.xlabel(f"{col} – file A")
        plt.ylabel(f"{col} – file B")
        plt.title(f"Parity plot: {col}")
        plt.xlim(lo, hi)
        plt.ylim(lo, hi)
        plt.tight_layout()

        out_path = out_dir / f"parity_{col.lower()}.png"
        plt.savefig(out_path, dpi=150)
        if args.show:
            plt.show()
        else:
            plt.close()

        print(f"Saved {out_path}")

if __name__ == "__main__":
    main()

