import logging

logger = logging.getLogger(__name__)

import threading

from apscheduler.schedulers.blocking import BlockingScheduler
from django.utils import timezone
from django.db import IntegrityError

from .feed import RSSFeed

from .models import Article, Author, Outlet, Tag


def find_or_create_tag(term):
    try:
        return Tag.objects.get(term=term)
    except Tag.DoesNotExist:
        tag = Tag(term=term)
        tag.save()
        return tag


def find_or_create_author(outlet, name):
    try:
        return outlet.author_set.get(name=name)
    except Author.DoesNotExist:
        author = Author(name=name)
        outlet.author_set.add(author)
        return author


def check_outlet(outlet):
    logger.info('Parsing "%s" at url "%s"' % (outlet.name, outlet.rss_url))

    feed = RSSFeed(outlet.rss_url)
    updated = feed.get_channel_info()['updated']

    # Some feeds do not provide last updated time
    if updated is None:
        updated = timezone.now()

    if outlet.updated is None or updated > outlet.updated:
        logger.info('Feed was updated at %s, fetching new items' % updated.isoformat())
        entries = feed.get_entries_info()

        logger.info('Feed provided %s items.' % len(entries))

        for entry_info in entries:
            try:

                article = Article(**entry_info['entry_info'])

                authors = list(find_or_create_author(outlet, author) for author in entry_info['authors'])

                tags = list(find_or_create_tag(tag) for tag in entry_info['tags'])

                outlet.article_set.add(article)
                article.authors.add(*authors)
                article.tags.add(*tags)
            except IntegrityError, e:
                logger.warning('Failed to insert article, integrity error "%s"' % e)
            except Exception, e:
                logger.error('Failed parsing entry: %s\n%s' % (e, entry_info))

        outlet.updated = updated
        outlet.save()

    else:
        logger.info('Feed has not been updated since last check.')


def run():
    logger.debug('Running at %s' % timezone.now().isoformat())
    for outlet in Outlet.objects.all():
        check_outlet(outlet)
    logger.debug('Finished running at %s' % timezone.now().isoformat())


class Worker(threading.Thread):
    def __init__(self, hours=0, minutes=0, seconds=0):
        super(Worker, self).__init__()
        if not (hours or minutes or seconds):
            raise ValueError('Hours, minutes and seconds cannot be all equal to 0')

        self.scheduler = BlockingScheduler()
        self.job = self.scheduler.add_job(run, 'interval', hours=hours, minutes=minutes, seconds=seconds)

    def run(self):
        self.scheduler.start()

    def stop(self, *args):
        self.scheduler.shutdown()