#!/usr/bin/env python3
import numpy as np
import argparse

"""
3rd-Order Ambisonics 16ch (VCCM) Decoder Generator
--------------------------------------------------
Generates a pseudo-inverse decoding matrix for a 16-speaker array (VCCM layout
below), using ACN channel ordering with either N3D (orthonormalized) or SN3D
(Schmidt semi-normalized) spherical harmonics.

USAGE:
    python ambi_decoder_vccm.py
        -> Generates both 3OA_VCCM_SN3D.txt and 3OA_VCCM_N3D.txt

    python ambi_decoder_vccm.py --norm SN3D
        -> Generates only 3OA_VCCM_SN3D.txt

    python ambi_decoder_vccm.py --norm N3D
        -> Generates only 3OA_VCCM_N3D.txt

FLAGS:
    --norm {SN3D, N3D}
        Select normalization scheme:
            SN3D - Schmidt semi-normalized (AmbiX/typical DAWs)
            N3D  - Orthonormalized
        If omitted, both normalizations are generated.

Notes:
- The system is 16×16 for 3OA→16 speakers. We still use the pseudo-inverse for
  numerical robustness; if K is well-conditioned, pinv ~= inverse.

Reference:
- Heller, Lee, Benjamin (2008), "Is My Decoder Ambisonic?"
"""

# Format: [azimuth, elevation] (radians)
# Azimuth: 0 = front; pi/2 = left; pi = rear; 3pi/2 = right
# Elevation: 0 = horizontal; pi/2 = zenith; -pi/2 = nadir

# VCCM speaker array (first 8 on horizon, next 8 elevated by +pi/4 and offset -pi/8)
speakers = [
    [1 * np.pi / 4, 0],  # 1  left front bottom
    [0 * np.pi / 4, 0],  # 2  center bottom
    [7 * np.pi / 4, 0],
    [6 * np.pi / 4, 0],
    [5 * np.pi / 4, 0],
    [4 * np.pi / 4, 0],
    [3 * np.pi / 4, 0],
    [2 * np.pi / 4, 0],
    [(1 * np.pi / 4) - (np.pi / 8), np.pi / 4],  # 9  left front top
    [(0 * np.pi / 4) - (np.pi / 8), np.pi / 4],  # 10 right front top
    [(7 * np.pi / 4) - (np.pi / 8), np.pi / 4],
    [(6 * np.pi / 4) - (np.pi / 8), np.pi / 4],
    [(5 * np.pi / 4) - (np.pi / 8), np.pi / 4],
    [(4 * np.pi / 4) - (np.pi / 8), np.pi / 4],
    [(3 * np.pi / 4) - (np.pi / 8), np.pi / 4],
    [(2 * np.pi / 4) - (np.pi / 8), np.pi / 4],
]

# --- N3D real spherical harmonics (ACN order) ---
def w_i(azi, ele): return 1.0
def y_i(azi, ele): return np.sqrt(3.0) * np.cos(ele) * np.sin(azi)
def z_i(azi, ele): return np.sqrt(3.0) * np.sin(ele)
def x_i(azi, ele): return np.sqrt(3.0) * np.cos(azi) * np.cos(ele)

def v_i(azi, ele): return (np.sqrt(15.0) / 2.0) * (np.cos(ele) ** 2) * np.sin(2.0 * azi)
def t_i(azi, ele): return (np.sqrt(15.0) / 2.0) * np.sin(2.0 * ele) * np.sin(azi)
def r_i(azi, ele): return (np.sqrt(5.0) / 2.0) * (3.0 * (np.sin(ele) ** 2) - 1.0)
def s_i(azi, ele): return (np.sqrt(15.0) / 2.0) * np.sin(2.0 * ele) * np.cos(azi)
def u_i(azi, ele): return (np.sqrt(15.0) / 2.0) * (np.cos(ele) ** 2) * np.cos(2.0 * azi)

def q_i(azi, ele): return np.sqrt(35.0 / 8.0) * (np.cos(ele) ** 3) * np.sin(3.0 * azi)
def o_i(azi, ele): return (np.sqrt(105.0) / 2.0) * np.sin(ele) * (np.cos(ele) ** 2) * np.sin(2.0 * azi)
def m_i(azi, ele): return np.sqrt(21.0 / 8.0) * np.cos(ele) * (5.0 * (np.sin(ele) ** 2) - 1.0) * np.sin(azi)
def k_i(azi, ele): return 0.5 * np.sqrt(7.0) * np.sin(ele) * (5.0 * (np.sin(ele) ** 2) - 3.0)
def l_i(azi, ele): return np.sqrt(21.0 / 8.0) * np.cos(ele) * (5.0 * (np.sin(ele) ** 2) - 1.0) * np.cos(azi)
def n_i(azi, ele): return (np.sqrt(105.0) / 2.0) * np.sin(ele) * (np.cos(ele) ** 2) * np.cos(2.0 * azi)
def p_i(azi, ele): return np.sqrt(35.0 / 8.0) * (np.cos(ele) ** 3) * np.cos(3.0 * azi)

def sh16_n3d(azi, ele):
    """Return 16 real SH values at (azi, ele) in ACN order, N3D-normalized."""
    return np.array([
        w_i(azi, ele), y_i(azi, ele), z_i(azi, ele), x_i(azi, ele),
        v_i(azi, ele), t_i(azi, ele), r_i(azi, ele), s_i(azi, ele), u_i(azi, ele),
        q_i(azi, ele), o_i(azi, ele), m_i(azi, ele), k_i(azi, ele),
        l_i(azi, ele), n_i(azi, ele), p_i(azi, ele)
    ], dtype=np.float64)

def apply_normalization(sh_vec, norm):
    """
    Convert from N3D (input) to requested normalization.
    - If norm == 'N3D': pass-through.
    - If norm == 'SN3D': divide each order-l block by sqrt(2l+1).
    """
    if norm.upper() == 'N3D':
        return sh_vec
    if norm.upper() != 'SN3D':
        raise ValueError("norm must be 'SN3D' or 'N3D'")
    out = sh_vec.copy()
    out[1:4]  /= np.sqrt(3.0)  # l=1
    out[4:9]  /= np.sqrt(5.0)  # l=2
    out[9:16] /= np.sqrt(7.0)  # l=3
    return out

def build_decoder(norm='SN3D'):
    # Build K by evaluating SH at each speaker direction
    rows = []
    for azi, ele in speakers:
        sh_n3d = sh16_n3d(azi, ele)
        sh = apply_normalization(sh_n3d, norm)
        rows.append(sh)
    K = np.asarray(rows, dtype=np.float64)
    # Pseudo-inverse decoder (robust to conditioning)
    return np.linalg.pinv(K).T.round(7)

def write_decoder(norm):
    M = build_decoder(norm)
    outname = f"3OA_VCCM_{norm}.txt"
    with open(outname, "w") as f:
        for row in M:
            for element in row:
                f.write(f"{element};\n")
    print(f"Wrote {outname}")

def main():
    parser = argparse.ArgumentParser(description="3rd-order Ambisonics decoder for 16ch VCCM array (SN3D/N3D).")
    parser.add_argument("--norm", choices=["SN3D", "N3D"],
                        help="Normalization to use. If omitted, outputs both.")
    args = parser.parse_args()

    if args.norm:
        write_decoder(args.norm)
    else:
        for norm in ["SN3D", "N3D"]:
            write_decoder(norm)

if __name__ == "__main__":
    main()