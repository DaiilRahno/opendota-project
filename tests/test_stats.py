from backend.stats import calculate_average_kda,calculate_kda,get_best_and_worst_matches

def test_calculate_kda():
    assert calculate_kda(10,5,10) == 4.0

def test_calculate_kda_devision_zero():
    assert calculate_kda(10,0,10) == 20.0

def test_calculate_average_kda():
    assert calculate_average_kda(
        [
        {
        "kda":4.83
        },
        {
    
        "kda":7.00
        }

         ]) == 5.92

def test_calculate_average_kda_empty():
    assert calculate_average_kda([]) == 0

def test_get_best_worst_matches():
    best_matches,worst_match = get_best_and_worst_matches([{'kda':12.00},{'kda':1.11},{'kda':5.99}]) 
    assert best_matches['kda'] == 12.00 
    assert worst_match['kda'] == 1.11

def  test_get_best_worst_matches_empty():
    best_matches,worst_match = get_best_and_worst_matches([])
    assert best_matches is None
    assert worst_match is None
