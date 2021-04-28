import json
from pprint import pprint
from pymongo import MongoClient

connection = 'CONNECTION URL WAS REMOVED DUE TO SAFETY REASONS'
client = MongoClient(connection)

db = client['app']
collection = db['trends']


class Trend:
    '''Filter info about trend and adds some additional info to each trend'''
    def __init__(self, trend: dict, added_at: str, location: str):
        self.added_at = added_at
        self.trend = trend
        self.location = location


    def filter_trend(self):
        '''
        Adds date to trend, country and removes unuseful info about it
        Add to each trend analytics object to keep track of change of tweet_volume.
        '''
        del self.trend['url']
        del self.trend['promoted_content']
        del self.trend['query']
        self.trend['added_at'] = self.added_at
        self.trend['country'] = self.location
        self.trend['analytics'] = {self.added_at: self.trend['tweet_volume']}

        del self.trend['tweet_volume'] # don't need it as it is present in analytics now
        return self.trend


class TrendsADT:
    def __init__(self, trends: list):
        '''Initialize trends'''
        self.as_of = trends[0]["as_of"]
        self.location = trends[0]["locations"][0]['name']
        self._trends = self._filter(trends[0]["trends"])


    def __iter__(self):
        '''Iterate through trends'''
        return iter(self._trends)


    def __getitem__(self, index):
        '''Get trend by its index'''
        return self._trends[index]


    def _already_in_db(self, trend: dict) -> bool:
        '''
        Finds if specific trend's name is already in data base
        if trend is already present in DB, return True
        if it is not return False
        '''
        if collection.find_one({'name': trend['name']}):
            return True
        return False


    def push_to_db(self):
        '''
        Push trends to DB. 
        If some trend is already present in DB then its 'tweet_volume' and 'added_at' 
        parameters are added to analytics object.
        If trend is fresh and is not present in DB, then it's info is added to DB
        '''
        deleted = self._compare_trends()  # keep track of trends that aren't in top50

        added_to_db = 0
        modified = 0
        for trend in self._trends:
            if not self._already_in_db(trend):
                collection.insert_one(trend)
                added_to_db += 1
            else:
                # if trend is present in DB, just add to
                # analytics array timestamp and fresh teewt_volume
                new_time_stamp = trend['added_at']
                new_tweet_volume = trend['analytics'][new_time_stamp]
                if new_tweet_volume:
                    collection.update_one({'name': trend['name']}, \
                        {'$set': {'analytics.' + new_time_stamp: new_tweet_volume}})
                    modified += 1

        return added_to_db, modified, len(deleted)


    def _compare_trends(self):
        '''
        Compare trends in db with obtained from the Twitter API 
        If in db there is a trend that we don't meet in obtained from
        Twitter API list -> we delete this trend from db
        '''
        db_trends = collection.find({}) # get all trends from db
        deleted_from_db = []
        
        for d_trend in db_trends:
            present = False
            for fresh_trend in self._trends:
                if d_trend['name'] == fresh_trend['name']:
                    present = True
            
            # if trend from DB is not found among fresh trends, then it is
            # not in top50 anymore, so delete that old trend from DB.
            if not present:
                self._delete_trend_from_DB(d_trend['name'])
                deleted_from_db.append(d_trend)
        
        return deleted_from_db


    def _delete_trend_from_DB(self, name):
        '''Delete trend with a given name from the DB'''
        collection.delete_one({'name': name})


    def _filter(self, trends):
        ''' Filter trend's info '''
        for i, trend in enumerate(trends):
            trends[i] = Trend(trend, self.as_of, self.location).filter_trend()

        return trends
