from pymongo import MongoClient
import json
from pprint import pprint

connection = 'CONNECTION URL REMOVED'
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
    def __init__(self, trends=None, as_of=None, location=None):
        '''Initialize trends'''
        if trends:
            self.as_of = as_of
            self.location = location
            self._trends = self._filter(trends)
        else:
            self._trends = []

    def __iter__(self):
        '''Iterate through trends'''
        return iter(self._trends)

    def __getitem__(self, index):
        '''Get trend by its index'''
        return self._trends[index]
    
    def add_trends_to_others(self, trends, as_of, location):
        '''Add new trends to self._trends, so in the end
        every trend that users are tracking will be pushed in one time'''
        for trend in trends:
            trend = Trend(trend, as_of, location).filter_trend()
            self._trends.append(trend)

    def _already_in_db(self, trend: dict) -> bool:
        '''
        Finds if specific trend is already in data base.
        Looks for trend_name and location. As there can be trends with same
        name but with different locations.

        if trend is already present in DB, return True
        if it is not return False
        '''
        if collection.find_one({'name': trend['name'], 'country': trend['country']}):
            return True
        return False

    def push_to_db(self):
        '''
        Push trends to DB. 
        If some trend is already present in DB then its 'tweet_volume' and 'added_at' 
        parameters are added to analytics object.
        If trend is fresh and is not present in DB, then it's info is added to DB

        Each trend object has the following structure:
        {
            'name': name,
            'added_at': added_at,
            'country': country
            'analytics': {
                timestamp: tweet_volume,
                ...
            }
        }

        Return deleted trends, those that cannot be tracked anymore
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
        
        # print the following info for debugging reasons
        print(f'added to DB: {added_to_db}, modified: {modified}, deleted: {len(deleted)}')
        return deleted

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
                self._delete_trend_from_DB(d_trend['name'], d_trend['country'])
                deleted_from_db.append(d_trend)
        
        return deleted_from_db

    def _delete_trend_from_DB(self, name, country):
        '''Delete trend with a given name from the DB'''
        collection.delete_one({'name': name, 'country': country})

    def _filter(self, trends):
        ''' Filter trend's info '''
        for i, trend in enumerate(trends):
            trends[i] = Trend(trend, self.as_of, self.location).filter_trend()
        return trends
    
    def get_trend_from_db(self, trend_name: str, country: str) -> dict:
        '''Gets info about given trend in db'''
        return collection.find_one({'name': trend_name, 'country': country})


if __name__ == '__main__':
    trends_adt = TrendsADT()
    tr = trends_adt.get_trend_from_db('#RCBvKKR', 'Worldwide')
    pprint(tr)
