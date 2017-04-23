import tweepy
import re
import Cleaner_Settings

auth = tweepy.OAuthHandler(Cleaner_Settings.CONSUMER_KEY, Cleaner_Settings.CONSUMER_SECRET)
auth.set_access_token(Cleaner_Settings.ACCESS_TOKEN_KEY, Cleaner_Settings.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

replacements = {
    "witness" : "this dude I know",
    "witnesses" : "these dudes I know",
    "allegedly" : "kinda probably",
    "new study" : "tumblr post",
    "rebuild" : "avenge",
    "space" : "spaaace",
    "google glass" : "virtual boy",
    "smartphone" : "pokedex",
    "electric" : "atomic",
    "senator" : "elf-lord",
    " car " : " cat ",
    "election" : "eating contest",
    "congressional leader" : "river spirit",
    "homeland security" : "homestar runner",
    "could not be reached for comment" : "is guilty and everyone knows it"
}

class TwitterListener(tweepy.StreamListener) :

    def on_status(self, status) : # Will be called every time a new tweet is streamed
        origText = status.text
        newText = origText
        replaced = False

        for key in replacements.keys() :
            pattern = re.compile(re.escape(key), re.IGNORECASE) # Will be looking for 'key' while ignoring case
            while key in newText.lower() :
                newText = pattern.sub(replacements[key], newText) # .sub() only replaces the first instance so replace all instances
                replaced = True

        if replaced :
            if (len(newText) > 140) :
                newText = newText[0:140]
            api.update_status(newText)
            print ("Tweeted: " + newText)


    def on_error(self, status_code):
        if status_code == 420:
            print ("Rate limited")
            return False

stream = tweepy.Stream(api.auth, TwitterListener())
stream.userstream() # Streams tweets on bot's timeline

