from typing import Tuple
def oxygen_demand_CxHyOzNw(x:int, y:int, z:int, w:int) -> float:
    return x + y/4 - z/2
def balanced_products_CxHyOzNw(x:int, y:int, z:int, w:int) -> Tuple[float,float,float]:
    return float(x), y/2.0, w/2.0
