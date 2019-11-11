# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
        
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    
    def __init__ (self, phrase):
        '''
        Takes a string phrase as an argument to the class' constructor (__init__ method()) 
        '''
        self.phrase = phrase.lower()
        
    def get_phrase(self):
        return self.phrase
    
    def is_phrase_in(self, text):
        '''
        Take in a phrase (string) and returns True if the whole phase is present in the text,
        false otherwise. This method should not be case sensitive. Words in phrase are separated
        by a single space. Words in text may contain punctuations and spaces (may contain more 
        than one spaces, provided that each word in the phrase is present in its entirety and appears
        consecutively in the text
        '''


        #To compare, remove punctuations and extra whitespaces in text. To ensure that a phrase 
        #trigger with the phrase 'purple cow' does not fire on 'purple cows', add a whitespace
        #to the end of the phrase and text
        
        #change text to lowercase
        lowercase_text = text.lower()
        
        #replace punctuations in text with whitespaces 
        for letter in string.punctuation:
            lowercase_text = lowercase_text.replace(letter, ' ')
        
        #split words in string argument text into list items
        words_in_text = lowercase_text.split()
        
        #join list into a string with a single white space between words and at the end of string
        filtered_text = ' '.join(words_in_text) + ' '
        phrase = self.get_phrase() + ' '
        
        #compare 
        return phrase in filtered_text
 

# Problem 3
# TODO: TitleTrigger
class TitleTrigger (PhraseTrigger):
    '''
    TitleTrigger fires when a news item's title containas a given phrase
    '''
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())
    

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    '''
    DescriptionTrigger fires when a news item's description containas a given phrase
    '''
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())
    
# TIME TRIGGERS      
# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__ (self, time):
        '''
        Takes in time in EST as a string in the format of "3 Oct 2016 17:00:10"
        '''
        #use strptime() method convert time from a string to datetime
        pubdate = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        
        #change timezone to EST time
        pubdate_EST_time = pubdate.replace(tzinfo=pytz.timezone("EST"))
        
        #save time as an argument to the class' constructor
        self.pubdate = pubdate_EST_time

        
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger (TimeTrigger):
    '''
    BeforeTrigger fires when a story is published strictly before the trigger's time
    '''
    def evaluate (self, story):
        #ensure story's pubdate are in EST time
        return story.get_pubdate().replace(tzinfo=pytz.timezone("EST")) < self.pubdate


class AfterTrigger (TimeTrigger):
    '''
    AfterTrigger fires when a story is published strictly after the trigger's time
    '''
    def evaluate (self, story):
        #ensure story's pubdate are in EST time
        return story.get_pubdate().replace(tzinfo=pytz.timezone("EST")) > self.pubdate


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    '''
    NotTrigger takes another trigger as argument to its constructor and invert the output
    (evaluate) of this other trigger
    '''
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)
        
# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    '''
    AndTrigger takes two triggers as arguments to its constructor and should fire on a news story
    only if BOTH of the inputted triggers would fire on that item.
    '''
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate (self, story):
        evaluate1 = self.trigger1.evaluate(story)
        evaluate2 = self.trigger2.evaluate(story)
        return evaluate1 and evaluate2
            

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    '''
    OrTrigger takes two triggers as arguments to its constructor and should fire on a news story
    if EITHER of the inputted triggers would fire on that item.
    '''
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate (self, story):
        evaluate1 = self.trigger1.evaluate(story)
        evaluate2 = self.trigger2.evaluate(story)
        return evaluate1 or evaluate2

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    triggered_news = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                triggered_news.append(story)
    return triggered_news



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # lines: ['t1,TITLE,election', 't2,DESCRIPTION,Trump', 't3,DESCRIPTION,Clinton', 
    #         't4,AFTER,3 Oct 2016 17:00:10', 't5,AND,t2,t3', 't6,AND,t1,t4', 'ADD,t5,t6']
    # The first element in the line is either the keyword ADD or the name of the trigger.
    # Lines starting with keyword ADD specifies which triggers should be in the trigger list. 
    # LInes that does not start with the keyword ADD define named triggers. A trigger definition
    # should create a trigger and associate it witha name (use a dictionary).
    print(lines)
    trigger_dict = {}
    trigger_list = []
    for line in lines:
        trigger_def = line.split(',')
        if trigger_def[1] == 'TITLE':
            trigger_dict[trigger_def[0]] = TitleTrigger(trigger_def[2])
        elif trigger_def[1] == 'DESCRIPTION':
            trigger_dict[trigger_def[0]] = DescriptionTrigger(trigger_def[2])
        elif trigger_def[1] == 'AFTER':
            trigger_dict[trigger_def[0]] = AfterTrigger(trigger_def[2])
        elif trigger_def[1] == 'BEFORE':
            trigger_dict[trigger_def[0]] = BeforeTrigger(trigger_def[2])
        elif trigger_def[1] == 'NOT':
            trigger_dict[trigger_def[0]] = NotTrigger(trigger_def[2])
        elif trigger_def[1] == 'AND':
            trigger_dict[trigger_def[0]] = AndTrigger(trigger_def[2], trigger_def[3])
        elif trigger_def[1] == 'OR':
            trigger_dict[trigger_def[0]] = OrTrigger(trigger_def[2], trigger_def[3])  
        elif trigger_def[0] == 'AND':
            for i in range (1, len(trigger_def)):
                trigger_list.append(trigger_dict[trigger_def[i]])
    return trigger_list


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

