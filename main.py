import builtins
from iqoptionapi_simple import IQ_Option

username = "julian.santos.trash@gmail.com"
password = "mypassisiqoption"
profile = None
conection = False
reason = None

IQ = IQ_Option(email=username, password=password)
conection, reason = IQ.connect()

profile = IQ.get_profile()
print("get_profile", profile)

balance = IQ.get_balance()
print("get_balance", balance)

currency = IQ.get_currency()
print("get_currency", currency)

ranking = IQ.get_ranking(country="BR")
print("get_ranking", ranking)

ranking = IQ.get_ranking_traders_id(country="BR")
print("get_ranking_traders_id", ranking)

traders_mood = IQ.get_traders_mood(asset="AUDUSD")
print("get_traders_mood", traders_mood)

inputs = IQ.get_traders_input_binary(asset="AUDUSD")
print("get_traders_input_binary", inputs)

inputs = IQ.get_traders_input_digital(asset="AUDUSD")
print("get_traders_input_digital", inputs)