import time
from iqoptionapi_simple import IQ_Option

username = "your_email@domain.com"
password = "your_password"
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

ranking = IQ.get_ranking()
print("get_ranking", ranking)

ranking = IQ.get_ranking_traders_id()
print("get_ranking_traders_id", ranking)

traders_mood = IQ.get_traders_mood(asset="AUDUSD")
print("get_traders_mood", traders_mood)

inputs = IQ.get_traders_input_binary(asset="EURUSD")
print("get_traders_input_binary", inputs)

inputs = IQ.get_traders_input_digital(asset="EURUSD")
print("get_traders_input_digital", inputs)

assets = IQ.get_all_assets()
print("get_all_assets", assets)

assets = IQ.get_assets_open()
print("get_assets_open", assets)

assets = IQ.get_assets_open_binary()
print("get_assets_open_binary", assets)

assets = IQ.get_assets_open_turbo()
print("get_assets_open_turbo", assets)

assets = IQ.get_assets_open_digital()
print("get_assets_open_digital", assets)

asset_exist = IQ.assets_exist(asset="EURUSD")
print("assets_exist", asset_exist)

is_open = IQ.assets_is_open(asset="EURUSD")
print("assets_is_open", asset_exist)

iasset_name = IQ.get_asset_name_by_id(asset_id=1)
print("get_asset_name_by_id", iasset_name)

candles = IQ.get_candles("EURUSD", 60, 200, time.time())
print("get_candles", candles)

list_candles = []
IQ.get_candles_realtime("EURUSD", 60, buffer=1, waiting_time=1, max_candles=5, list_candles=list_candles)
print("get_candles_realtime", list_candles)

IQ.get_candles_realtime_v2("EURUSD", 60, buffer=1, waiting_time=1, stop_stream=False, callback=print)
print("get_candles_realtime", list_candles)
