'''
@author: Souvik Das
Institute: University at Buffalo
'''

import demoji, re, datetime
import preprocessor


# demoji.download_codes()


class TWPreprocessor:
    @classmethod
    def preprocess(cls, tweet):
        '''
        Do tweet pre-processing before indexing, make sure all the field data types are in the format as asked in the project doc.
        :param tweet:
        :return: dict
        '''
        dict = {}
        twitter_user = tweet.user
        clean_text = _text_cleaner(tweet.full_text)

        dict['poi_name'] = twitter_user.screen_name  # should not be set to anything for non POIs
        dict['poi_id'] = twitter_user.id    # should not be set to anything for non POIs
        dict['verified'] = twitter_user.verified
        dict['country'] = _get_country(tweet.lang)
        dict['id'] = tweet.id

        if(tweet.in_reply_to_status_id != None):
            dict['replied_to_tweet_id'] = tweet.in_reply_to_status_id
            dict['reply_text'] = clean_text[0]
        if(tweet.in_reply_to_user_id != None):
            dict['replied_to_user_id'] = tweet.in_reply_to_user_id

        dict['tweet_text'] = tweet.full_text
        dict['tweet_lang'] = tweet.lang
        dict['text_' + tweet.lang] = tweet.full_text
        dict['hashtags'] = _get_entities(tweet, type = 'hashtags')
        dict['mentions'] = _get_entities(tweet, type = 'mentions')
        dict['tweet_urls'] = _get_entities(tweet, type = 'urls')
        dict['tweet_emoticons']= clean_text[1]
        dict['tweet_date'] = _get_tweet_date(tweet._json['created_at'])
        dict['geolocation'] = tweet.geo

        return dict

def _get_country(lang):
    if(lang == 'hi'):
        return 'India'
    elif (lang == 'en'):
        return 'USA'
    else:
        return 'Mexico'

def _get_entities(tweet, type=None):
    result = []
    if type == 'hashtags':
        hashtags = tweet.entities['hashtags']

        for hashtag in hashtags:
            result.append(hashtag['text'])
    elif type == 'mentions':
        mentions = tweet.entities['user_mentions']

        for mention in mentions:
            result.append(mention['screen_name'])
    elif type == 'urls':
        urls = tweet.entities['urls']

        for url in urls:
            result.append(url['url'])

    return result


def _text_cleaner(text):
    emoticons_happy = list([
        ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
        ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
        '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
        'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
        '<3'
    ])
    emoticons_sad = list([
        ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
        ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
        ':c', ':{', '>:\\', ';('
    ])
    all_emoticons = emoticons_happy + emoticons_sad

    emojis = list(demoji.findall(text).keys())
    clean_text = demoji.replace(text, '')

    for emo in all_emoticons:
        if (emo in clean_text):
            clean_text = clean_text.replace(emo, '')
            emojis.append(emo)

    clean_text = preprocessor.clean(text)
    # preprocessor.set_options(preprocessor.OPT.EMOJI, preprocessor.OPT.SMILEY)
    # emojis= preprocessor.parse(text)

    return clean_text, emojis


def _get_tweet_date(tweet_date):
    return _hour_rounder(datetime.datetime.strptime(tweet_date, '%a %b %d %H:%M:%S +0000 %Y'))


def _hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
            + datetime.timedelta(hours=t.minute // 30))
