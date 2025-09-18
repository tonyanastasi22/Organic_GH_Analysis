def delta_g_from_h_s(dH_kJ_per_mol: float, S_J_per_molK: float, T_K: float = 298.15) -> float:
    return dH_kJ_per_mol - T_K * S_J_per_molK / 1000.0
