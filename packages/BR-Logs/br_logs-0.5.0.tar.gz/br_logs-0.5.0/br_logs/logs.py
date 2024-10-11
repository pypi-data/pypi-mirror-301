import asyncio 
import aiohttp
from typing import List
from datetime import datetime,timedelta

#Main class

class Logs:
    def __init__(
        self,
        session_id: str,
        server_id:int):
        """
        Initialize the Logs class with a session ID.

        :param session_id: Unique identifier for the BR-Logs system.
        :param server_id: Unique identifier for the server.
        """
        self.session_id = session_id
        self.server_id = server_id
    
    async def get_admin_actions(
        self, 
        nicknames: List[str],
        start_date:str,
        end_date:str,
        ) -> List[str]:
        """
        Asynchronously get all log entries related to the provided admin nicknames.

        :param nicknames: List of admin nicknames to filter actions.
        :param start_date: The start date to filter actions.
        :param end_date: The end date to filter actions.
        :return: A total count of log entries associated with the nickname.
        """
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Dates must be in a format of 'YYYY-MM-DD'")
        url = f"https://logs.blackrussia.online/gslogs/{self.server_id}/api/list-game-logs/"
        categories = [39,40,41,45]
        async with aiohttp.ClientSession() as session:
            cookie = {'sessionid': self.session_id}
            session.cookie_jar.update_cookies(cookie)
            results_by_nickname = {nickname: 0 for nickname in nicknames}  # Initialize counts
            tasks = []
            for nickname in nicknames:
                for category_id in categories:
                    async def fetch_paginated_data(nickname, category_id):
                        offset = 0
                        total_count = 0
                        while True:
                            params = {
                                'category_id__exact': category_id,
                                'player_name__exact': nickname,
                                'player_id__exact': '',
                                'player_ip__exact': '',
                                'transaction_amount__exact': '',
                                'balance_after__exact': '',
                                'transaction_desc__ilike': '',
                                'time__gte': f'{start_date}T00:00:00',
                                'time__lte': f'{end_date}T23:59:59',
                                'order_by': 'time',
                                'offset': offset,  # Incremental offset for pagination
                                'auto': "False"
                            }

                            async with session.get(url, params=params) as response:
                                data = await response.json()
                            
                            count = len(data)
                            if count == 0:
                                break

                            total_count += count
                            offset += count  # Increment offset for the next page

                        return nickname, total_count

                    tasks.append(fetch_paginated_data(nickname, category_id))

            all_results = await asyncio.gather(*tasks)

            for nickname, count in all_results:
                results_by_nickname[nickname] += count
        return results_by_nickname
    
    async def get_events(
        self,
        start_date:str,
        end_date:str
        ) -> int:
        """
        Asynchronously get all events of a server in a given period of time.
        :return : A count of events.
        """
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:("Dates must be in a format of 'YYYY-MM-DD'")

        url = f"https://logs.blackrussia.online/gslogs/{self.server_id}/api/list-game-logs/"
        async with aiohttp.ClientSession() as session:
            cookie = {'sessionid':self.session_id}
            session.cookie_jar.update_cookies(cookie)
            offset = 0
            total_count = 0
            while True:
                params = {
                    'category_id__exact': 41,
                    'time__gte': f'{start_date}T00:00:00',
                    'time__lte': f'{end_date}T23:59:59',
                    'order_by': 'time',
                    'transaction_desc__ilike': 'Создал мероприятие%',
                    'offset': offset,
                    'auto': "False"
                }
                async with session.get(url, params=params) as response:
                    data = await response.json()
                count = len(data)
                if count == 0:
                    break
                total_count += count
                offset += count
        return total_count
        
    
    async def get_last_rep(
        self,
        nickname:str,
        ) -> str:
        """
        Asynchronously get the last report of an admin.
        :param nickname: The nickname of the admin.
        :return Timestamp of the last rep"""
        url = f"https://logs.blackrussia.online/gslogs/{self.server_id}/api/list-game-logs/"
        today = datetime.now().strftime("%Y-%m-%d")
        three_days_ago = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
        async with aiohttp.ClientSession() as session:
            cookie = {'sessionid':self.session_id}
            session.cookie_jar.update_cookies(cookie)
            offset = 0
            total_count = 0
            while True:
                params = {
                    'player_name__exact': nickname,
                    'category_id__exact': 40,
                    'time__gte': f'{three_days_ago}T00:00:00',
                    'time__lte': f'{today}T23:59:59',
                    'order_by': 'time',
                    'transaction_desc__ilike': 'Жалоба от%',
                    'offset': offset,
                    'auto': "False",
                }
                async with session.get(url, params=params) as response:
                    data = await response.json()
                count = len(data)
                if count == 0:
                    break
                total_count += count
                offset += count
                last_rep = data[0]['time']
                timestamp = datetime.fromisoformat(last_rep)
                return timestamp