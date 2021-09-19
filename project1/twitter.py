'''
@author: Souvik Das
Institute: University at Buffalo
'''

import tweepy


class Twitter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler("TfDQ92hEO3ToWtvt7UrlG6tKQ", "8btQr6X2rx9YhEFHjWePKCE1HAQ0dzfTZLzgsmLLxXy7n2utR3")
        self.auth.set_access_token("1432402312958521344-sSWtqVPerATh3mJ3uPLz4GGBPFM4KN", "b77OeviiJPmVzbMfdffrh93VS2DGKSjl7JWNMyudrDJbX")
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def _meet_basic_tweet_requirements(self):
        '''
        Add basic tweet requirements logic, like language, country, covid type etc.
        :return: boolean
        '''
        raise NotImplementedError

    def get_tweets_by_poi_screen_name(self, screen_name, count):
        '''
        Use user_timeline api to fetch POI related tweets, some postprocessing may be required.
        :return: List
        '''
        
        tweets_by_poi = tweepy.Cursor(self.api.user_timeline, screen_name = screen_name).items(count);
        # tweets_by_poi = self.api.user_timeline(screen_name = screen_name, count = count, include_rts = True, tweet_mode = 'extended')

        return tweets_by_poi

    def get_tweets_by_lang_and_keyword(self, keyword_name, count, lang):
        '''
        Use search api to fetch keywords and language related tweets, use tweepy Cursor.
        :return: List
        '''
        tweets_by_lang_and_keyword = self.api.search(q = keyword_name, count = count, lang = lang, tweet_mode = 'extended')

        return tweets_by_lang_and_keyword

    def get_replies(self):
        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        '''
        raise NotImplementedError
