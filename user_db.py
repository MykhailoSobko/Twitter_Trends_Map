from pymongo import MongoClient
from trends_adt import TrendsADT
import hashlib
from pprint import pprint

connection = 'mongodb+srv://admin01:4A9wGWOpPVdcXZ56@trends-map-project.jjtxk.mongodb.net/app?retryWrites=true&w=majority'
client = MongoClient(connection)

db = client['app']
collection = db['users']


class User:
    """User class. Works with MongoDB. Each user is stored in DB
    User has unique username, encrypted password, and trends user is
    tracking, which are stored in a list.
    Each user object has the following structure:
    {
        "username": username
        "password": encrypted_password
        "track": [
            (trend_name, country_name),
            ...,
            ]
    }
    """

    def __init__(self, username: str, passwrd: str):
        self.username = username
        self.password = passwrd
        self.logged_in = None

        # contains trends user is trackng
        # set with tuples: (trend_name, country)
        self.track_trends = []

    def check_password(self, password):
        """Return True if the password is valid for this
        user, false otherwise."""
        return password == self.password

    def add_user(self):
        """Register user and add user to db.
        user object has the following structure:
        {
            'username': username,
            'password': password,
            'tracked': []
        }
        """
        user = {
            'username': self.username,
            'password': self.password,
            'track': self.track_trends
        }
        collection.insert_one(user)

    def logout(self):
        """Logout user."""
        self.logged_in = False
        print('logged out')

    def add_trend_to_track(self, trend_name: str, country: str):
        """User can choose trands to track.
        info is added in a form of tuple: (trend_name, country).

        First check if such trend is tracked already by the user,
        if not, then add new trend to the array.

        Then add that trend to the DB, to 'track' field"""
        if len(self.track_trends) == 5:
            raise TooManyTracked('You cannot track more than 5 trends')
        if (trend_name, country) not in set(self.track_trends):
            self.track_trends.append((trend_name, country))
            self._add_track_trend_to_db(trend_name, country)

        # mb here add a custom exception that is raised when the specific
        # trend is already tracked by the user

    def get_all_info_for_user(self, username: str):
        """Gets trends info which user is tracking and returns them as dictionaries"""
        user_info = collection.find_one({'username': username})
        tracked = user_info['tracked']

        # get all trends info from db, using Trends ADT
        # get_trend_from_db(self, trend_name: str, country: str)
        tr_info = []
        deleted = []
        adt = TrendsADT()
        for trend in tracked:
            tr_name = tracked[0]
            loc = tracked[1]
            db_trend = adt.get_trend_from_db(tr_name, loc)
            if db_trend:
                tr_info.append(db_trend)
            else:
                deleted.append(trend)

        return tr_info, deleted

    def check_trend_growth(self, statistic):
        statistic_lst = []
        for date in statistic["analytics"]:
            if statistic["analytics"][date] is not None:
                statistic_lst.append(statistic["analytics"][date])

        growth = statistic_lst[-1] - statistic_lst[-2]
        return growth/100

    def _add_track_trend_to_db(self, trend_name, country):
        """Add new trend to track to the DB. Adds to
        specific user's 'track' array a new trend in format:
        (trend_name, country)"""
        collection.update_one({'username': self.username},
                              {'$push': {'track': (trend_name, country)}})

    def delete_trend_from_tracked(self, trend_name, country):
        """Remove trend from tracked ones."""
        collection.update_one({'username': self.username},
                              {'$pull': {'track': (trend_name, country)}})

        self.track_trends.remove((trend_name, country))
        print(f'removed from tracked: {trend_name, country}')


class Authenticator:
    def __init__(self):
        """Construct an authenticator to manage
        users logging in and out."""
        # to keep track of users
        self.users = {}
        self.current_user = None

    def register(self, username, password):
        """Add user to users set. Add new user to DB"""
        if not self.user_exists(username):
            self.users[username] = User(username, password)
            self.users[username].add_user()  # add user to DB
            # if user refistered, by default login.
            self.users[username].logged_in = True
            self.current_user = self.users[username]
            print(f'logged in as {username}')
        else:
            raise UserAlreadyExistsError('The username is already taken')

    def user_exists(self, name):
        """If user is present, returns whole info about the user,
        in other case returns None"""
        return collection.find_one({'username': name})

    def login(self, username, password):
        """Login the user"""
        # mb here create new user instance if username and password are correct and exist in db,
        # so if program shuts down we will not have problems with 'self.users' dict.
        # if program finished being executed self.users is emptied, so next time, when we try to
        # log in key errors will be raised.

        user = self.user_exists(username)

        if user:
            recieved_pw = user['password']
            if password == recieved_pw:
                self.current_user = User(username, password)
                self.current_user.logged_in = True
            else:
                raise IncorrectCredentials('Password or username is invalid')
        else:
            raise IncorrectCredentials('Password or username is invalid')

    def is_logged_in(self, username):
        if username in self.users:
            return self.users[username].is_logged_in
        return False


class UserAlreadyExistsError(Exception):
    '''Raised when the username exists in DB'''


class IncorrectCredentials(Exception):
    '''Raised when user logs in passing incorrect
    password or username'''


class TooManyTracked(Exception):
    '''Raised when more than 5 trends are being tracked'''


if __name__ == '__main__':
    auth = Authenticator()
    auth.login('tania', '1234455')