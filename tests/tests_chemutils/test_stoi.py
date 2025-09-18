from chemutils.stoi import oxygen_demand_CxHyOzNw, balanced_products_CxHyOzNw
def test_hno_releases_o2():
    assert abs(oxygen_demand_CxHyOzNw(0,1,1,1) + 0.25) < 1e-12
def test_balanced_products_counts():
    co2, h2o, n2 = balanced_products_CxHyOzNw(2,4,0,2)
    assert (co2, h2o, n2) == (2.0, 2.0, 1.0)
