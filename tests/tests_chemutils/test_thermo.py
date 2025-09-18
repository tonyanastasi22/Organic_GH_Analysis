from chemutils.thermo import delta_g_from_h_s
def test_delta_g_from_h_s_units_and_value():
    dg = delta_g_from_h_s(-100.0, 150.0, 298.15)
    assert abs(dg + 144.7225) < 1e-6
