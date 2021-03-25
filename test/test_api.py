from iqoptionapi_simple import IQ_Option

def test_login():

    username = "julian.santos.trash@gmail.com"
    password = "mypassisiqoption"
    conection = False
    reason = None

    IQ = IQ_Option(email=username, password=password)
    conection, reason = IQ.connect()
    assert conection == True

    def test_profile():
        profile = IQ.get_profile()
        assert profile != None

    def test_balance():
        
        balance = IQ.get_balance()
        assert balance != None

        balance = IQ.get_balance_v2()
        assert balance != None

    def test_currency():
        currency = IQ.get_currency()
        assert currency != None

    def test_ranking():
        ranking = IQ.get_ranking()
        assert ranking != None

    def test_ranking_by_id():
        ranking = IQ.get_ranking_traders_id()
        assert ranking != None

    test_profile()

    test_balance()

    test_currency()

    test_ranking()

    test_ranking_by_id()