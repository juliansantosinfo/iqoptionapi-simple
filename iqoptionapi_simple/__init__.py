import time
from typing import SupportsAbs
from iqoptionapi import stable_api

class IQ_Option(stable_api.IQ_Option):
    """ """

    __version__ = "0.0.1"

    def __init__(self, email, password, active_account_type="PRACTICE"):
        super().__init__(email, password, active_account_type=active_account_type)

    def is_connected(self):
        return self.check_connect()

    def get_profile(self):
        return self.get_profile_ansyc()

    def get_balance(self):
        return super().get_balance()

    def get_currency(self):
        return super().get_currency()

    def reset_practice_balance(self):
        return super().reset_practice_balance()

    def change_balance(self, type="PRACTICE"):
        return super().change_balance(type)

    def get_leader_board(self, country, from_position, to_position, near_traders_count, user_country_id=0, near_traders_country_count=0, top_country_count=0, top_count=0, top_type=2):
        self.api.leaderboard_deals_client = None
        country_id = Country.ID[country]
        self.api.Get_Leader_Board(country_id, user_country_id, from_position, to_position,near_traders_country_count, near_traders_count, top_country_count, top_count, top_type)

        while self.api.leaderboard_deals_client == None:
            pass
        return self.api.leaderboard_deals_client

    def get_ranking(self, country="Worldwide", from_position=1, to_position=10, near_traders_count=0):
        ranking = self.get_leader_board(country, from_position, to_position, near_traders_count)
        ranking = ranking['result']['positional']
        return ranking

    def get_ranking_traders_id(self, country="Worldwide", from_position=1, to_position=10, near_traders_count=0):
        id_list = []
        ranking = self.get_leader_board(country, from_position, to_position, near_traders_count)
        for n in ranking['result']['positional']:
            id = ranking['result']['positional'][n]['user_id']
            id_list.append(id)
        return id_list

    def get_trader_info(self, user_id=None):
        return self.get_user_profile_client(user_id)

    def get_trader_info_leaderboard(self, user_id, counutry_id):
        return self.request_leaderboard_userinfo_deals_client(user_id, counutry_id)

    def get_trader_availability(self, user_id):
        return self.get_users_availability(user_id)

    def trader_is_online(self, user_id):
        trader_status = False
        trader_info = self.get_users_availability(user_id)
        if len(trader_info) > 0:
            if len(trader_info['statuses']) > 0:
                trader_status = trader_info['statuses']['0']['status']
                if trader_status == 'online':
                    trader_status = True
        return trader_status

    def get_traders_mood(self, asset):
        run_stream = True
        self.start_mood_stream(asset)
        mood = super().get_traders_mood(asset)
        self.stop_mood_stream(asset)
        return mood

    def get_trader_by_id(self, user_id):
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
