
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Post(Item):
    # define the fields for your item here like:
    id_ = Field()
    shortcode = Field()
    display_url = Field()
    caption = Field()
    comment_count = Field()
    tagged_user = Field()
    likes_count = Field()
    is_ad = Field()
    loc_id = Field()
    loc_lat = Field()
    loc_lon = Field()
    loc_name = Field()
    owner_id = Field()
    owner_username = Field()
    owner_fullname = Field()
    taken_at_timestamp = Field()
    pass
