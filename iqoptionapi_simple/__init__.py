import time
from datetime import datetime
from dateutil import tz
from iqoptionapi import stable_api, country_id as Country

def timestamp_converter(date_time, format='%d/%m/%Y %H:%M:%S'):

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
    """ """

    __version__ = "0.0.1"

    def __init__(self, email, password, active_account_type="PRACTICE"):
        super().__init__(email, password, active_account_type=active_account_type)

    def is_connected(self):
        """
            @type method
            @description Return True if id connected.
            @return 
        """

        return self.check_connect()

    def get_profile(self):
        """
            @type method
            @description Get profile.
            @return 
        """

        return self.get_profile_ansyc()

    def get_balance(self):
        """
            @type method
            @description Get balance.
            @return 
        """

        return super().get_balance()

    def get_currency(self):
        """
            @type method
            @description Get currency.
            @return 
        """

        return super().get_currency()

    def reset_practice_balance(self):
        """
            @type method
            @description Reset balance in PRACTICE wallet.
            @return 
        """

        return super().reset_practice_balance()

    def change_balance(self, type="PRACTICE"):
        """
            @type method
            @description Change wallet.
            @return 
        """

        return super().change_balance(type)

    def get_leader_board(self, country, from_position, to_position, near_traders_count, user_country_id=0, near_traders_country_count=0, top_country_count=0, top_count=0, top_type=2):
        """
            @type method
            @description Get leader board.
            @return 
        """

        self.api.leaderboard_deals_client = None
        try_out = 5
        country_id = Country.ID[country]
        self.api.Get_Leader_Board(country_id, user_country_id, from_position, to_position,near_traders_country_count, near_traders_count, top_country_count, top_count, top_type)

        while self.api.leaderboard_deals_client == None and try_out != 0:
            try_out -= 1
            time.sleep(1)
        return self.api.leaderboard_deals_client

    def get_ranking(self, country="Worldwide", from_position=1, to_position=10, near_traders_count=0):
        """
            @type method
            @description Get ranking traders by country.
            @return 
        """

        ranking = self.get_leader_board(country, from_position, to_position, near_traders_count)
        if ranking:
            ranking = ranking['result']['positional']
        return ranking

    def get_ranking_traders_id(self, country="Worldwide", from_position=1, to_position=10, near_traders_count=0):
        """
            @type method
            @description Get ranking traders by id.
            @return 
        """

        id_list = []
        ranking = self.get_leader_board(country, from_position, to_position, near_traders_count)
        if ranking:
            for n in ranking['result']['positional']:
                id = ranking['result']['positional'][n]['user_id']
                id_list.append(id)
        return id_list

    def get_trader_info(self, user_id=None):
        """
            @type method
            @description Get trader info.
            @return 
        """

        return self.get_user_profile_client(user_id)

    def get_trader_info_leaderboard(self, user_id, counutry_id):
        """
            @type method
            @description Get trader leaderboard info by id.
            @return 
        """

        return self.request_leaderboard_userinfo_deals_client(user_id, counutry_id)

    def get_trader_availability(self, user_id):
        """
            @type method
            @description Get trader availability by id.
            @return 
        """

        return self.get_users_availability(user_id)

    def trader_is_online(self, user_id):
        """
            @type method
            @description Return if trader is online.
            @return 
        """

        trader_status = False
        trader_info = self.get_users_availability(user_id)
        if len(trader_info) > 0:
            if len(trader_info['statuses']) > 0:
                trader_status = trader_info['statuses']['0']['status']
                if trader_status == 'online':
                    trader_status = True
        return trader_status

    def get_traders_mood(self, asset):
        """
            @type method
            @description get traders mood.
            @return 
        """
        self.start_mood_stream(asset)
        mood = super().get_traders_mood(asset)
        self.stop_mood_stream(asset)
        return mood

    def get_trader_by_id(self, user_id):
        """
            @type method
            @description get trader info by id.
            @return 
        """

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

    def get_traders_input_binary(self, asset, buffersize=10):
        """
            @type method
            @description get traders input for binary options.
            @return 
        """

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

    def get_traders_input_digital(self, asset, buffersize=1):
        """
            @type method
            @description get traders input for digital options.
            @return 
        """

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
        """
            @type method
            @description Get all assets.
            @return 
        """

        return self.get_all_open_time()
        
    def get_assets_open(self):
        """
            @type method
            @description Get all assets open in all operation.
            @return 
        """

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
        """
            @type method
            @description Get all assets open in binary operation.
            @return 
        """

        assets = self.get_all_open_time()
        assets_type = assets['binary']
        assets_opened = []

        for activo_name in assets_type:
            assets_opened.append(activo_name)

        return assets_opened

    def get_assets_open_turbo(self):
        """
            @type method
            @description Get all assets open in turbo operation.
            @return 
        """

        assets = self.get_all_open_time()
        assets_type = assets['turbo']
        assets_opened = []

        for activo_name in assets_type:
            assets_opened.append(activo_name)

        return assets_opened

    def get_assets_open_digital(self):
        """
            @type method
            @description Get all assets open in digital operation.
            @return 
        """

        assets = self.get_all_open_time()
        assets_type = assets['digital']
        assets_opened = []

        for activo_name in assets_type:
            assets_opened.append(activo_name)

        return assets_opened

    def assets_exist(self, assets_name, type_operation='all'):
        """
            @type method
            @description Return if asset exist.
            @return 
        """

        assets = self.get_all_open_time()

        if type_operation == 'all':
            for type_operation in assets:
                if assets_name in assets[type_operation]:
                    return True
        else:
            for assets_name in assets[type_operation]:
                return True
        return False

    def assets_is_open(self, assets_name, type_operation='all'):
        """
            @type method
            @description Return if asset is open.
            @return 
        """

        assets = self.get_all_open_time()

        if type_operation == 'all':
            for type_operation in assets:
                if assets_name in assets[type_operation]:
                    if assets[type_operation][assets_name]['open']:
                        return True
        else:
            if type_operation in assets:
                if assets_name in assets[type_operation]:
                    if assets[type_operation][assets_name]['open']:
                        return True

        return False

    def get_asset_name_by_id(self, asset_id):
        """
            @type method
            @description Get asset name by id.
            @return 
        """

        return self.get_name_by_activeId(asset_id)

    def set_candle_asset(self, candle, asset):
        """
            @type method
            @description Set candle color key.
            @return 
        """

        candle['asset'] = asset

    def set_candle_size(self, candle, size):
        """
            @type method
            @description Set candle size key.
            @return 
        """

        candle['size'] = size

    def set_candle_color(self, candle):
        """
            @type method
            @description Set candle asset key.
            @return 
        """
        
        if candle['open'] > candle['close']:
            candle['color'] = 'red'
        elif candle['open'] < candle['close']:
            candle['color'] = 'green'
        else:
            candle['color'] = 'grey'

    def get_candles(self, asset, size, number_candles, last_candle_time):
        """
            @type method
            @description Get last candles.
            @return 
        """

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

    def get_candles_realtime(self, asset, intervals, buffer=1, waiting_time=1, max_candles=5):
        """
            @type method
            @description Get candles in real time.
            @return 
        """

        run_stream = True
        in_candle = 1

        # Start a candle stream.
        self.start_candles_stream(asset, intervals, buffer)

        try:

            # Scroll through incoming candles taking values.
            while run_stream:

                # Check max candles.
                if in_candle == max_candles:
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


                    self.set_candle_asset(candles[candle], asset)
                    self.set_candle_color(candles[candle])

                    yield candles[candle]

                    in_candle += 1

        except ValueError as error:
            pass
        finally:
            self.stop_candles_stream(asset, intervals)

        return