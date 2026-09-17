from backend.heroes import filter_hero

def test_filter_hero():
    list_hero = filter_hero([{'hero_id':1,'games':35},{'hero_id':2,'games':1},{'hero_id':44,'games':100}])
    assert list_hero == [{'hero_id':1,'games':35},{'hero_id':44,'games':100}]

def test_filter_hero_game_border():
    list_hero = filter_hero([{'hero_id':1,'games':20},{'hero_id':2,'games':19},{'hero_id':3,'games':21}])
    assert list_hero == [{'hero_id':1,'games':20},{'hero_id':3,'games':21}]

def test_filter_hero_empty():
     list_hero = filter_hero([])
     assert list_hero == []

def test_filter_hero_less_20_game():
    list_hero = filter_hero([{'hero_id':1,'games':5},{'hero_id':2,'games':6},{'hero_id':3,'games':5}])
    assert list_hero == []