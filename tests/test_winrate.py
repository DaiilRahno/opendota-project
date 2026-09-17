from backend.winrate import prepare_winrate

def test_prepare_winrate():
    res = prepare_winrate({'win':60,'lose':40})
    assert res == {
        'wins':60,
        'losses':40,
        'games':100,
        'winrate':60.0,
    }
def test_prepare_winrate_zero():
    res = prepare_winrate({'win':0,'lose':0})
    assert res == {
        'wins':0,
        'losses':0,
        'games':0,
        'winrate':0,
    }