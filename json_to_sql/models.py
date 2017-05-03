import peewee
from peewee import *


db = MySQLDatabase('Database', user='username',passwd='passwd')

class Business(peewee.Model):
    """
    {
    "business_id":"encrypted business id",
    "name":"business name",
    "neighborhood":"hood name",
    "address":"full address",
    "city":"city",
    "state":"state -- if applicable --",
    "postal code":"postal code",
    "latitude":latitude,
    "longitude":longitude,
    "stars":star rating, rounded to half-stars,
    "review_count":number of reviews,
    "is_open":0/1 (closed/open),
    "attributes":["an array of strings: each array element is an attribute"],
    "categories":["an array of strings of business categories"],
    "hours":["an array of strings of business hours"],
    "type": "business"
    }
    """
    bid = peewee.PrimaryKeyField()
    business_id = peewee.CharField()  # encrypted ID with letters, numbers, and symbols
    name = peewee.CharField()
    address = peewee.CharField()
    city = peewee.CharField()
    postal_code = peewee.CharField()
    state = peewee.CharField(max_length=3)  # XGL
    latitude = peewee.CharField()
    longitude = peewee.CharField()
    stars = peewee.DecimalField()  # star rating rounded to half-stars
    review_count = peewee.BigIntegerField()
    is_open = peewee.BooleanField()
    neighborhoods = peewee.CharField() 
    # categories = None # list of category names

    class Meta:
        database = db

class Category(peewee.Model):
    """
    Derived from Business.categories Field.
    """
    id = peewee.PrimaryKeyField()
    business_id = peewee.CharField()
    category_name = peewee.CharField()

    class Meta:
        database = db

class Attribute(peewee.Model):
   id = peewee.PrimaryKeyField()
   business_id = peewee.CharField()
   attribute_name = peewee.CharField()
   flag =  peewee.BooleanField()
   
   class Meta:
       database = db

class Review(peewee.Model):
    """
    {
      'type': 'review',
      'business_id': (encrypted business id),
      'user_id': (encrypted user id),
      'stars': (star rating),
      'text': (review text),
      'date': (date, formatted like '2012-03-14', %Y-%m-%d in strptime notation),
    }
    """
    rid = peewee.PrimaryKeyField()
    business_id = peewee.CharField()
    user_id = peewee.CharField()
    stars = peewee.IntegerField()
    text = peewee.TextField()
    date = peewee.DateField(formats="%Y-%m-%d")  # '2012-03-14', %Y-%m-%d in strptime notation
    useful_votes = peewee.IntegerField()
    funny_votes = peewee.IntegerField()
    cool_votes = peewee.IntegerField()

    class Meta:
        database = db

class User(peewee.Model):
    """
    {
    "user_id":"encrypted user id",
    "name":"first name",
    "review_count":number of reviews,
    "yelping_since": date formatted like "2009-12-19",
    "friends":["an array of encrypted ids of friends"],
    "useful":"number of useful votes sent by the user",
    "funny":"number of funny votes sent by the user",
    "cool":"number of cool votes sent by the user",
    "fans":"number of fans the user has",
    "elite":["an array of years the user was elite"],
    "average_stars":floating point average like 4.31,
    "compliment_hot":number of hot compliments received by the user,
    "compliment_more":number of more compliments received by the user,
    "compliment_profile": number of profile compliments received by the user,
    "compliment_cute": number of cute compliments received by the user,
    "compliment_list": number of list compliments received by the user,
    "compliment_note": number of note compliments received by the user,
    "compliment_plain": number of plain compliments received by the user,
    "compliment_cool": number of cool compliments received by the user,
    "compliment_funny": number of funny compliments received by the user,
    "compliment_writer": number of writer compliments received by the user,
    "compliment_photos": number of photo compliments received by the user,
    "type":"user"
    }
    """
    uid = peewee.PrimaryKeyField()
    user_id = peewee.CharField()
    name = peewee.CharField()
    review_count = peewee.IntegerField()
    yelping_since = peewee.DateField(formats="%Y-%m-%d")  # '2012-03-14', %Y-%m-%d in strptime notation
    useful = peewee.IntegerField()
    funny = peewee.IntegerField()
    cool = peewee.IntegerField()
    fans = peewee.IntegerField()
    average_stars = peewee.FloatField()
    compliment_hot = peewee.IntegerField()
    compliment_more = peewee.IntegerField()
    compliment_profile = peewee.IntegerField()
    compliment_cute = peewee.IntegerField()
    compliment_list = peewee.IntegerField()
    compliment_note = peewee.IntegerField()
    compliment_plain = peewee.IntegerField()
    compliment_cool = peewee.IntegerField()
    compliment_funny = peewee.IntegerField()
    compliment_writer = peewee.IntegerField()
    compliment_photos = peewee.IntegerField()

    class Meta:
        database = db

class Friend(peewee.Model):
   id = peewee.PrimaryKeyField()
   user_id = peewee.CharField()
   friends = peewee.CharField()
   
   class Meta:
       database = db

class Elite(peewee.Model):
   id = peewee.PrimaryKeyField()
   user_id = peewee.CharField()
   elite_date = peewee.DateField(formats="%Y-%m-%d")  # '2012-03-14', %Y-%m-%d in strptime notation
   
   class Meta:
       database = db

class Checkin(peewee.Model):
    """
    {
      'type': 'checkin',
      'business_id': (encrypted business id),
      'checkin_info': {
            '0-0': (number of checkins from 00:00 to 01:00 on all Sundays),
            '1-0': (number of checkins from 01:00 to 02:00 on all Sundays), 
            ... 
            '14-4': (number of checkins from 14:00 to 15:00 on all Thursdays),
            ...
            '23-6': (number of checkins from 23:00 to 00:00 on all Saturdays)
      } # if there was no checkin for an hour-day block it will not be in the dict
    }
    """
    cid = peewee.PrimaryKeyField()
    business_id = peewee.CharField()
    sunday_count = peewee.IntegerField(default=0)
    monday_count = peewee.IntegerField(default=0)
    tuesday_count = peewee.IntegerField(default=0)
    wednesday_count = peewee.IntegerField(default=0)
    thursday_count = peewee.IntegerField(default=0)
    friday_count = peewee.IntegerField(default=0)
    saturday_count = peewee.IntegerField(default=0)

    class Meta:
        database = db

class Tip(peewee.Model):
    """
    {
        'type': 'tip',
        'text': (tip text),
        'business_id': (encrypted business id),
        'user_id': (encrypted user id),
        'date': (date, formatted like '2012-03-14'),
        'likes': (count),
    }
    """
    tip_id = peewee.PrimaryKeyField()
    business_id = peewee.CharField()
    text = peewee.TextField()
    user_id = peewee.CharField()
    date = peewee.DateField(formats="%Y-%m-%d")  # '2012-03-14', %Y-%m-%d in strptime notation
    likes = peewee.IntegerField()

    class Meta:
        database = db
