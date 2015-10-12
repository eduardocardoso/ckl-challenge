from django.db import models

# Create your models here.

class Outlet(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=100)
    rss_url = models.CharField('rss feed url', max_length=100)
    description = models.CharField(max_length=500, null=True)
    language = models.CharField(max_length=5, null=True)
    updated = models.DateTimeField('date updated', null=True)

    def __data__(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'rss_url': self.rss_url,
            'description': self.description,
            'language': self.language,
            'updated': self.updated.isoformat() if self.updated else None
        }

    def __unicode__(self):
        return self.name


class Author(models.Model):
    outlet = models.ForeignKey(Outlet)
    name = models.CharField(max_length=200)
    profile = models.CharField(max_length=100, null=True)
    twitter = models.CharField(max_length=50, null=True)

    def __data__(self):
        return {
            'id': self.id,
            'name': self.name,
            'profile': self.profile,
            'twitter': self.twitter,
        }

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    term = models.CharField(max_length=200)

    def __data__(self):
        return self.term

    def __unicode__(self):
        return self.term


class Article(models.Model):
    outlet = models.ForeignKey(Outlet)
    authors = models.ManyToManyField(Author)
    tags = models.ManyToManyField(Tag)

    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=400)
    url = models.CharField(max_length=250, unique=True)
    pub_date = models.DateTimeField('date published')
    content = models.TextField(null=True)

    def __data__(self):
        authors = list(author.__data__() for author in self.authors.all())
        tags = list(tag.__data__() for tag in self.tags.all())

        return {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'url': self.url,
            'date': self.pub_date,
            'content': self.content,
            'tags': tags,
            'authors': authors
        }

    def __unicode__(self):
        return self.title
