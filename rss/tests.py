import datetime
import json

from django.utils import timezone, dateparse
from django.test import TestCase, RequestFactory

from rss.feed import RSSFeed
from rss.models import Article, Author, Outlet, Tag
from rss import views



# Create your tests here.

class RSSFeedTestCase(TestCase):
    valid_rss = """
    <?xml version="1.0" encoding="utf-8"?>
    <rss version="2.0">
    <channel>
    <title>Sample Feed</title>
    <description>For documentation &lt;em&gt;only&lt;/em&gt;</description>
    <link>http://example.org/</link>
    <pubDate>Sat, 07 Sep 2002 00:00:01 GMT</pubDate>
    <item>
    <author>Samble Author</author>
    <title>First entry title</title>
    <link>http://example.org/entry/3</link>
    <description>Watch out for &lt;span style="background-image:
    url(javascript:window.location='http://example.org/')"&gt;nasty
    tricks&lt;/span&gt;</description>
    <pubDate>Thu, 05 Sep 2002 00:00:01 GMT</pubDate>
    <guid>http://example.org/entry/3</guid>
    <category><![CDATA[Sample Tag]]></category>
    </channel>
    </rss>
    """

    invalid_rss = """
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom"
    xml:base="http://example.org/"
    xml:lang="en">
    <title type="text">Sample Feed</title>
    <subtitle type="html">
    For documentation &lt;em&gt;only&lt;/em&gt;
    </subtitle>
    <link rel="alternate" href="/"/>
    <link rel="self"
    type="application/atom+xml"
    href="http://www.example.org/atom10.xml"/>
    <rights type="html">
    &lt;p>Copyright 2005, Mark Pilgrim&lt;/p>&lt;
    </rights>
    <id>tag:feedparser.org,2005-11-09:/docs/examples/atom10.xml</id>
    <generator
    uri="http://example.org/generator/"
    version="4.0">
    Sample Toolkit
    </generator>
    <updated>2005-11-09T11:56:34Z</updated>
    <entry>
    <title>First entry title</title>
    <link rel="alternate"
    href="/entry/3"/>
    <link rel="related"
    type="text/html"
    href="http://search.example.com/"/>
    <link rel="via"
    type="text/html"
    href="http://toby.example.com/examples/atom10"/>
    <link rel="enclosure"
    type="video/mpeg4"
    href="http://www.example.com/movie.mp4"
    length="42301"/>
    <id>tag:feedparser.org,2005-11-09:/docs/examples/atom10.xml:3</id>
    <published>2005-11-09T00:23:47Z</published>
    <updated>2005-11-09T11:56:34Z</updated>
    <summary type="text/plain" mode="escaped">Watch out for nasty tricks</summary>
    <content type="application/xhtml+xml" mode="xml"
    xml:base="http://example.org/entry/3" xml:lang="en-US">
    <div xmlns="http://www.w3.org/1999/xhtml">Watch out for
    <span style="background: url(javascript:window.location='http://example.org/')">
    nasty tricks</span></div>
    </content>
    </entry>
    </feed>
    """

    def setUp(self):
        self.valid_feed = RSSFeed(self.valid_rss)
        self.invalid_feed = RSSFeed(self.invalid_rss)

    def test_valid_channel_info(self):
        channel_info = self.valid_feed.get_channel_info()

        self.assertEqual(channel_info['title'], u'Sample Feed')
        self.assertEqual(channel_info['subtitle'], u'For documentation <em>only</em>')
        self.assertEqual(channel_info['url'], u'http://example.org/')
        self.assertEqual(channel_info['language'], None)
        self.assertEqual(channel_info['updated'], datetime.datetime(2002, 9, 7, 0, 0, 1, tzinfo=timezone.utc))

    def test_valid_entry_info(self):
        entries = self.valid_feed.get_entries_info()
        entry = entries[0]
        entry_info = entry['entry_info']

        self.assertEqual(entry_info['title'], u'First entry title')
        self.assertEqual(entry_info['summary'], u'Watch out for <span>nasty\n    tricks</span>')
        self.assertEqual(entry_info['url'], u'http://example.org/entry/3')
        self.assertEqual(entry_info['pub_date'], datetime.datetime(2002, 9, 5, 0, 0, 1, tzinfo=timezone.utc))
        self.assertEqual(entry_info['content'], None)

    def test_invalid_feed(self):
        self.assertRaises(ValueError, self.invalid_feed.get_channel_info)
        self.assertRaises(ValueError, self.invalid_feed.get_entries_info)


class RestAPITestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.outlet1 = Outlet.objects.create(name='Sample Feed', description="Description", url='http://example.org',
                                             language='en-US',
                                             updated=None)
        self.outlet2 = Outlet.objects.create(name='Sample Feed 2', description="Description 2",
                                             url='http://example2.org',
                                             language='en-GB',
                                             updated=datetime.datetime(2002, 9, 7, 0, 0, 1, tzinfo=timezone.utc))
        self.author1 = Author(name='Author')
        self.author2 = Author(name='Author 2', profile='http://plus.google.com/Author2', twitter='@author2')
        self.outlet1.author_set.add(self.author1)
        self.outlet1.author_set.add(self.author2)

        self.article1 = Article(title='Title', summary='Summary', url='http://example.com/articles/1',
                                pub_date=datetime.datetime(2002, 9, 7, 0, 0, 1, tzinfo=timezone.utc), content='Content')
        self.article2 = Article(title='Title 2', summary='Summary 2', url='http://example.com/articles/2',
                                pub_date=datetime.datetime(2002, 9, 7, 0, 1, 1, tzinfo=timezone.utc),
                                content='Content 2')
        self.outlet1.article_set.add(self.article1)
        self.outlet1.article_set.add(self.article2)
        self.article1.authors.add(self.author1, self.author2)
        self.article2.authors.add(self.author1)

        self.tag1 = Tag.objects.create(term='Tag')
        self.tag2 = Tag.objects.create(term='Tag 2')
        self.article1.tags.add(self.tag1)
        self.article2.tags.add(self.tag2)

    def test_outlets_api(self):
        expected = [self.outlet1.__data__(), self.outlet2.__data__()]  # Ordered by name

        outlets_response = views.outlets(self.factory.get('/rss/outlets/'))

        self.assertEqual(outlets_response.status_code, 200)

        deserialized_data = json.loads(outlets_response.content)

        self.assertEqual(deserialized_data, expected)


    def test_outlet_api(self):
        expected = self.outlet1.__data__()

        outlets_response = views.outlet(self.factory.get('/rss/outlets/1/'), self.outlet1.id)

        self.assertEqual(outlets_response.status_code, 200)

        deserialized_data = json.loads(outlets_response.content)

        self.assertEqual(deserialized_data, expected)

    def test_authors_api(self):
        expected = [self.author1.__data__(), self.author2.__data__()]  # Ordered by name

        response = views.authors(self.factory.get('/rss/outlets/1/authors/'), self.outlet1.id)

        self.assertEqual(response.status_code, 200)

        deserialized_data = json.loads(response.content)

        self.assertEqual(deserialized_data, expected)

    def test_author_api(self):
        expected = self.author1.__data__()

        response = views.author(self.factory.get('/rss/outlets/1/authors/1'), self.outlet1.id, self.author1.id)

        self.assertEqual(response.status_code, 200)

        deserialized_data = json.loads(response.content)

        self.assertEqual(deserialized_data, expected)

    def test_all_authors_api(self):
        expected = [self.author1.__data__(), self.author2.__data__()]  # Ordered by name

        response = views.all_authors(self.factory.get('/rss/authors/'))

        self.assertEqual(response.status_code, 200)

        deserialized_data = json.loads(response.content)

        self.assertEqual(deserialized_data, expected)

    def test_articles_api(self):
        expected = [self.article2.__data__(),
                    self.article1.__data__()]  # Ordered by publication date from newest to oldest

        response = views.articles(self.factory.get('/rss/outlets/1/articles/'), self.outlet1.id)

        self.assertEqual(response.status_code, 200)

        deserialized_data = parse(response.content, 'date')

        self.assertEqual(deserialized_data, expected)

    def test_article_api(self):
        expected = self.article1.__data__()

        response = views.article(self.factory.get('/rss/outlets/1/articles/1'), self.outlet1.id, self.article1.id)

        self.assertEqual(response.status_code, 200)

        deserialized_data = parse(response.content, 'date')

        self.assertEqual(deserialized_data, expected)

    def test_all_articles_api(self):
        expected = [self.article2.__data__(),
                    self.article1.__data__()]  # Ordered by publication date from newest to oldest

        response = views.all_articles(self.factory.get('/rss/articles/'))

        self.assertEqual(response.status_code, 200)

        deserialized_data = parse(response.content, 'date')

        self.assertEqual(deserialized_data, expected)

    def test_tags_api(self):
        expected = [self.tag1.__data__(), self.tag2.__data__()]

        response = views.tags(self.factory.get('/rss/tags'))

        self.assertEqual(response.status_code, 200)

        deserialized_data = parse(response.content)

        self.assertEqual(deserialized_data, expected)

    def test_article_by_tags_api(self):
        expected = [self.article1.__data__()]

        response = views.articles_by_tag(self.factory.get('/rss/tags/Tag/articles/'), 'Tag')

        self.assertEqual(response.status_code, 200)

        deserialized_data = parse(response.content, 'date')

        self.assertEqual(deserialized_data, expected)


def parse(data, datetime_field=None):
    """
    API response serializes datetime fields as string and json.loads does not parse it back as a datetime.
    This function takes care of it

    :param data: The JSON serialized string
    :param datetime_field: The key on the dictionary that contains a datetime field
    :return: The deserialized data
    """

    parsed_data = json.loads(data)
    if datetime_field:
        if isinstance(parsed_data, list):
            for item in parsed_data:
                date = item.get(datetime_field)
                if date:
                    item[datetime_field] = dateparse.parse_datetime(date)
        elif isinstance(parsed_data, dict):
            date = parsed_data.get(datetime_field)
            if date:
                parsed_data[datetime_field] = dateparse.parse_datetime(date)

    return parsed_data