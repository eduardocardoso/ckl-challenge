import logging

logger = logging.getLogger(__name__)

from time import mktime
import datetime

import feedparser
from django.utils import timezone


class RSSFeed:
    """
    Class to parse RSS feed and extract relevant information
    """

    def __init__(self, feed_url):
        self.feed_url = feed_url
        self.feed_data = None
        self.channel_info = None
        self.entries = None

    @classmethod
    def _time_struct_to_datetime(cls, time_struct):
        """
        Feedparser already provides date fields parsed as time.time_struct in utc,
        this method converts it to a tz-aware datetime.
        """

        unix_time = mktime(time_struct)
        tz_aware = datetime.datetime.fromtimestamp(unix_time).replace(tzinfo=timezone.utc)
        return tz_aware

    def _parse_feed_data(self):
        if self.feed_data is None:
            try:
                self.feed_data = feedparser.parse(self.feed_url)

                if not self.feed_data.version.startswith('rss'):
                    raise ValueError('Feed does not contain valid rss information.')

            except ValueError, e:
                raise e
            except Exception, e:
                logger.error(e)
                raise ValueError('Failed to parse data from url, is it a valid RSS feed url?')

    def _parse_channel_info(self):
        if self.channel_info is None:
            self._parse_feed_data()

            updated = self.feed_data.feed.get('updated_parsed')

            # Some feeds do not provide last updated time
            if updated:
                updated = RSSFeed._time_struct_to_datetime(updated)

            self.channel_info = {
                'title': self.feed_data.feed.title,
                'subtitle': self.feed_data.feed.get('subtitle'),
                'url': self.feed_data.feed.get('link'),
                'language': self.feed_data.feed.get('language'),
                'updated': updated,
                'rss_url': self.feed_url
            }

    def _parse_entries_info(self):
        if self.entries is None:
            self.entries = []
            for entry in self.feed_data.entries:

                pub_date = RSSFeed._time_struct_to_datetime(entry.published_parsed)

                title = entry.title
                summary = entry.get('summary')
                url = entry.get('link')

                # Because ATOM feeds may provide more than one content feedparser provides the content as a list
                content = entry.get('content')
                if content and isinstance(content, list):
                    content = content[0]
                if isinstance(content, dict):
                    content = content.get('value')

                authors = list(author['name'] for author in entry.get('authors', []))
                tags = list(tag['term'] for tag in entry.get('tags', []))

                entry_info = {
                    'entry_info': {
                        'title': title,
                        'summary': summary,
                        'url': url,
                        'pub_date': pub_date,
                        'content': content,
                    },
                    'authors': authors,
                    'tags': tags
                }
                self.entries.append(entry_info)

    def get_channel_info(self):
        self._parse_channel_info()
        return self.channel_info

    def get_entries_info(self):
        self._parse_entries_info()
        return self.entries