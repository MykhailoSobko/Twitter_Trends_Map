from api_work import get_json
from trends_adt import TrendsADT
from pymongo import MongoClient
from pprint import pprint

connection = 'CONNECTION URL'
client = MongoClient(connection)

db = client['app']
collection = db['users']


class Tracker:
    ''' Track trends with this class '''
    def __init__(self):
        self.to_track = {}

    def get_all_users_trends(self):
        '''Connect to db and get all trends users are tracking
        Forms to_track dictionary, where keys are countries, and
        values are sets with trend names'''
        users = collection.find({})
        tracked_by_users = set()
        for user in users:
            tracking = user['track']
            for trend in tracking:
                if not tuple(trend) in tracked_by_users:
                    tracked_by_users.add(tuple(trend))
        
        # form a dict out of set, where keys are counties,
        # vals are trend-names
        for trend in list(tracked_by_users):
            country = trend[1]
            trend_name = trend[0]
            # if cuntry not present in a dict, then create new key
            if country not in self.to_track:
                self.to_track[country] = set()
                self.to_track[country].add(trend_name)
            else:
                if trend_name not in self.to_track[country]:
                    self.to_track[country].add(trend_name)

    def pass_trends_to_db(self, raw_trends_info: list):
        '''
        Get json object with trends in a specific country
        Use: TrendsADT to store trends list
        '''
        trends_adt = TrendsADT()
        for elem in raw_trends_info:
            raw_trends = elem[0]
            as_of = elem[1]
            location = elem[2]
            # if raw_trends is empt list, skip
            if raw_trends:
                trends_adt.add_trends_to_others(raw_trends, as_of, location)

        # push trends to DB
        deleted = trends_adt.push_to_db()
        pprint(deleted)
        # delete trends that aren't in top-50 from to_track dict
        if deleted:
            for trend in deleted:
                location = trend['country']
                trend_name = trend['name']
                self.to_track[location].remove(trend_name)

    def get_trends_from_api(self):
        """
        Helper function to get trends that users are tracking
        (filter out only those trends that are being tracked by users)

        Return object with the following structure:
        [
            (
                list with dicts that contain trends info,
                as_of parameter
                location parameter
            )
            ...
        ]
        """
        tracked_trends_info = []
        for country in self.to_track:
            trend_json = get_json(country)
            trends_list = []
            for trend_name in self.to_track[country]:
                for raw_trend in trend_json["trends"]:
                    if trend_name == raw_trend["name"]:
                        trends_list.append(raw_trend)

            tracked_trends_info.append((trends_list, trend_json["as_of"], trend_json["locations"][0]["name"]))

        return tracked_trends_info


if __name__ == '__main__':
    t = Tracker()
    t.get_all_users_trends()
    # pprint(t.to_track)
    fresh = t.get_trends_from_api()
    t.pass_trends_to_db(fresh)
