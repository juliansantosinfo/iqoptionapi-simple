import time
from datetime import datetime
from dateutil import tz
from iqoptionapi import stable_api, country_id as Country


__version__ = "0.0.2"


def timestamp_converter(date_time, format='%d/%m/%Y %H:%M:%S'):
    """ Convert datetime in timestamp to timezone America/Sao Paulo."""

    if type(date_time) is int or type(date_time) is float:
        date_time = int(str(date_time)[0:10])
    else:
        return date_time
    
    date_time = datetime.utcfromtimestamp(date_time).strftime(format)
    date_time = datetime.strptime(date_time, format)
    date_time = date_time.replace(tzinfo=tz.gettz('GMT'))
    date_time = date_time.astimezone(tz.gettz('America/Sao Paulo'))

    return date_time.strftime(format)

      
class IQ_Option(stable_api.IQ_Option):
    """ This class is a wrapping that simplifies the use of iQOptionapi."""

    def __init__(self, email : str, password : str, active_account_type="PRACTICE"):
        super().__init__(email, password, active_account_type=active_account_type)

    def is_connected(self):
        """ Return True if id connected."""

        return self.check_connect()

    def get_profile(self):
        """ Get profile."""

        return self.get_profile_ansyc()

    def get_balance(self):
        """ Get balance."""

        return super().get_balance()

    def get_currency(self):
        """ Get currency."""

        return super().get_currency()

    def reset_practice_balance(self):
        """ Reset balance in PRACTICE wallet."""

        return super().reset_practice_balance()

    def change_balance(self, type="PRACTICE"):
        """ Change wallet."""

        return super().change_balance(type)

    def get_leader_board(self, country : str, from_position : int, to_position : int, near_traders_count : int, user_country_id=0, near_traders_country_count=0, top_country_count=0, top_count=0, top_type=2):
        """ Get leader board."""

        self.api.leaderboard_deals_client = None
        try_out = 5
        country_id = Country.ID[country]
        self.api.Get_Leader_Board(country_id, user_country_id, from_position, to_position,near_traders_country_count, near_traders_count, top_country_count, top_count, top_type)

        while self.api.leaderboard_deals_client == None and try_out != 0:
            try_out -= 1
            time.sleep(1)
        return self.api.leaderboard_deals_client

    def get_ranking(self, country="Worldwide", from_position=1, to_position=10, near_traders_count=0):
        """ Get ranking traders by country."""

        ranking = self.get_leader_board(country, from_position, to_position, near_traders_count)
        if ranking:
            ranking = ranking['result']['positional']
        return ranking

    def get_ranking_traders_id(self, country="Worldwide", from_position=1, to_position=10, near_traders_count=0):
        """ Get ranking traders by id."""

        id_list = []
        ranking = self.get_leader_board(country, from_position, to_position, near_traders_count)
        if ranking:
            for n in ranking['result']['positional']:
                id = ranking['result']['positional'][n]['user_id']
                id_list.append(id)
        return id_list

    def get_trader_info(self, user_id : int):
        """ Get trader info."""

        return self.get_user_profile_client(user_id)

    def get_trader_info_leaderboard(self, user_id : int, counutry_id : int):
        """ Get trader leaderboard info by id."""

        return self.request_leaderboard_userinfo_deals_client(user_id, counutry_id)

    def get_trader_availability(self, user_id : int):
        """ Get trader availability by id."""

        return self.get_users_availability(user_id)

    def trader_is_online(self, user_id : int):
        """ Return if trader is online."""

        trader_status = False
        trader_info = self.get_users_availability(user_id)
        if len(trader_info) > 0:
            if len(trader_info['statuses']) > 0:
                trader_status = trader_info['statuses']['0']['status']
                if trader_status == 'online':
                    trader_status = True
        return trader_status

    def get_traders_mood(self, asset : str):
        """ Get traders mood."""
        self.start_mood_stream(asset)
        mood = super().get_traders_mood(asset)
        self.stop_mood_stream(asset)
        return mood

    def get_trader_by_id(self, user_id : int):
        """ Get trader info by id."""

        operations = []
        trader_info = self.get_trader_info(user_id)
        trader_operations = self.get_trader_availability(user_id)
        trader_operations = trader_operations['statuses']
        for operation in trader_operations:
            try:
                selected_asset_name = self.get_name_by_activeId(
                    operation['selected_asset_id'])
                operation['selected_asset_name'] = selected_asset_name
            except:
                continue

            operations.append(operation)
        trader_info['operations'] = operations
        return trader_info

    def get_traders_input_binary(self, asset : str, buffersize=10):
        """ Get traders input for binary options."""

        type_option = "live-deal-binary-option-placed"
        inputs_list = []
        try_out = 5

        # Start stream.
        self.subscribe_live_deal(type_option, asset, "binary", buffersize)
        self.subscribe_live_deal(type_option, asset, "turbo", buffersize)

        # Get inputs.
        while len(inputs_list) == 0 and try_out == 0:

            inputs_list_b = list(self.get_live_deal(type_option, asset, "binary"))
            inputs_list_t = list(self.get_live_deal(type_option, asset, "turbo"))

            inputs_list = inputs_list_b + inputs_list_t

            try_out -= 1

            time.sleep(1)

        self.unscribe_live_deal(type_option, asset, "binary")
        self.unscribe_live_deal(type_option, asset, "turbo")

        return inputs_list

    def get_traders_input_digital(self, asset : str, buffersize=1):
        """ Get traders input for digital options."""

        type_option = "live-deal-digital-option"
        inputs_list = []
        try_out = 5

        # Start stream.
        self.subscribe_live_deal(type_option, asset, "PT1M", buffersize)
        self.subscribe_live_deal(type_option, asset, "PT5M", buffersize)
        self.subscribe_live_deal(type_option, asset, "PT15M", buffersize)

         # Get inputs.
        while len(inputs_list) == 0 and try_out == 0:
                             
            inputs_list_1 = list(self.get_live_deal(type_option, asset, "PT1M"))
            inputs_list_5 = list(self.get_live_deal(type_option, asset, "PT5M"))
            inputs_list_15 = list(self.get_live_deal(type_option, asset, "PT15M"))

            inputs_list = inputs_list_1 + inputs_list_5 + inputs_list_15

            try_out -= 1

            time.sleep(1)

        self.unscribe_live_deal(type_option, asset, "PT1M")
        self.unscribe_live_deal(type_option, asset, "PT5M")
        self.unscribe_live_deal(type_option, asset, "PT15M")

        return inputs_list

    def get_all_assets(self):
        """ Get all assets."""

        return self.get_all_open_time()
        
    def get_assets_open(self):
        """ Get all assets open in all operation."""

        assets = self.get_all_open_time()
        assets_type = ""
        assets_opened = []

        for type_operation in assets:

            if type_operation not in ['turbo', 'digital']:
                continue

            assets_type = assets[type_operation]

            for activo_name in assets_type:
                if assets_type[activo_name]['open']:
                    assets_opened.append(activo_name)

        return assets_opened

    def get_assets_open_binary(self):
        """ Get all assets open in binary operation."""

        assets = self.get_all_open_time()
        assets_type = assets['binary']
        assets_opened = []

        for activo_name in assets_type:
            assets_opened.append(activo_name)

        return assets_opened

    def get_assets_open_turbo(self):
        """ Get all assets open in turbo operation."""

        assets = self.get_all_open_time()
        assets_type = assets['turbo']
        assets_opened = []

        for activo_name in assets_type:
            assets_opened.append(activo_name)

        return assets_opened

    def get_assets_open_digital(self):
        """ Get all assets open in digital operation."""

        assets = self.get_all_open_time()
        assets_type = assets['digital']
        assets_opened = []

        for activo_name in assets_type:
            assets_opened.append(activo_name)

        return assets_opened

    def assets_exist(self, asset : str, type_operation='all'):
        """ Return if asset exist."""

        assets = self.get_all_open_time()

        if type_operation == 'all':
            for type_operation in assets:
                if asset in assets[type_operation]:
                    return True
        else:
            for asset in assets[type_operation]:
                return True
        return False

    def assets_is_open(self, asset : str, type_operation='all'):
        """ Return if asset is open."""

        assets = self.get_all_open_time()

        if type_operation == 'all':
            for type_operation in assets:
                if asset in assets[type_operation]:
                    if assets[type_operation][asset]['open']:
                        return True
        else:
            if type_operation in assets:
                if asset in assets[type_operation]:
                    if assets[type_operation][asset]['open']:
                        return True

        return False

    def get_asset_name_by_id(self, asset_id : int) -> str:
        """ Get asset name by id."""

        return self.get_name_by_activeId(asset_id)

    def set_candle_asset(self, candle : dict, asset : str) -> None:
        """ Set candle color key."""

        candle['asset'] = asset

    def set_candle_size(self, candle : dict, size : int) -> None:
        """ Set candle size key."""

        candle['size'] = size

    def set_candle_color(self, candle : dict) -> None:
        """ Set candle asset key."""
        
        if candle['open'] > candle['close']:
            candle['color'] = 'red'
        elif candle['open'] < candle['close']:
            candle['color'] = 'green'
        else:
            candle['color'] = 'grey'

    def get_candles(self, asset : str, size : int, number_candles : int, last_candle_time) -> list:
        """ Get last candles."""

        candle = {}
        candles_data = super().get_candles(asset, size, number_candles, last_candle_time)

        for candle in candles_data:

            candle['from'] = timestamp_converter(candle['from'])
            candle['at'] = timestamp_converter(candle['at'])
            candle['to'] = timestamp_converter(candle['to'])

            self.set_candle_asset(candle, asset)
            self.set_candle_size(candle, size)
            self.set_candle_color(candle)
            

        return candles_data

    def get_candles_realtime(self, asset : str, intervals : int, buffer=1, waiting_time=1, max_candles=5, list_candles=[]):
        """ Get candles in real time."""

        run_stream = True
        in_candle = 1

        # Start a candle stream.
        self.start_candles_stream(asset, intervals, buffer)

        try:

            # Scroll through incoming candles taking values.
            while run_stream:

                # Check max candles.
                if in_candle > max_candles:
                    run_stream = False

                # Wait for the candle break.
                time.sleep(waiting_time)

                # The candle stream.
                candles = self.get_realtime_candles(asset,  intervals)

                for candle in candles:

                    # Converter dates.
                    candles[candle]['at'] = timestamp_converter(candles[candle]['at'])
                    candles[candle]['from'] = timestamp_converter(candles[candle]['from'])
                    candles[candle]['to'] = timestamp_converter(candles[candle]['to'])
                    candles[candle]['min_at'] = timestamp_converter(candles[candle]['min_at'])
                    candles[candle]['max_at'] = timestamp_converter(candles[candle]['max_at'])

                    # Define asset, size and color candle.
                    self.set_candle_asset(candles[candle], asset)
                    self.set_candle_color(candles[candle])

                    # Append in list and increment count.
                    list_candles.append(candles[candle])
                    in_candle += 1

        except ValueError as error:
            pass
        finally:
            self.stop_candles_stream(asset, intervals)

        return

    def get_candles_realtime_v2(self, asset : str, intervals : int, buffer=1, waiting_time=1, stop_stream=False, callback=None):
        """ Get candles in real time."""

        # Check callback.
        if not callback:
            return

        # Start a candle stream.
        self.start_candles_stream(asset, intervals, buffer)

        try:

            # Scroll through incoming candles taking values.
            while not stop_stream:

                # Wait for the candle break.
                time.sleep(waiting_time)

                # The candle stream.
                candles = self.get_realtime_candles(asset,  intervals)

                for candle in candles:

                    # Converter dates.
                    candles[candle]['at'] = timestamp_converter(candles[candle]['at'])
                    candles[candle]['from'] = timestamp_converter(candles[candle]['from'])
                    candles[candle]['to'] = timestamp_converter(candles[candle]['to'])
                    candles[candle]['min_at'] = timestamp_converter(candles[candle]['min_at'])
                    candles[candle]['max_at'] = timestamp_converter(candles[candle]['max_at'])

                    # Define asset, size and color candle.
                    self.set_candle_asset(candles[candle], asset)
                    self.set_candle_color(candles[candle])

                    # Append in list and increment count.
                    callback(candles[candle])

        except ValueError as error:
            pass
        finally:
            self.stop_candles_stream(asset, intervals)

        return
