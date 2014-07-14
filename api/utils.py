#!flask/bin/python
import bs4
import requests

from .models import Post


class Utils(object):
    YCOMBINATOR_URL = 'https://news.ycombinator.com/news'
    YCOMBINATOR_BASE_URL = 'https://news.ycombinator.com/'

    def scrap_hn(self):
        response = requests.get(self.YCOMBINATOR_URL)
        soup = bs4.BeautifulSoup(response.text)

        title_anchors = soup.select('table td.title a')
        subtext_tds = soup.select('table td.subtext')
        zipped_items = zip(title_anchors, subtext_tds)

        for index, item in enumerate(zipped_items):
            # If the item is a proper tuple, go ahead.
            if len(item) == 2:
                anchor, subtext = item
                subtext_soup = bs4.BeautifulSoup(unicode(subtext))

                post, created = Post.objects.get_or_create(
                    hn_id=self.get_hn_id(subtext_soup),
                )
                post.__dict__.update(
                    post_index_main=index + 1,
                    post_index_newest=index + 1,
                    title=anchor.getText(),
                    url=self.get_link(anchor),
                    score=self.get_score(subtext_soup),
                    author=self.get_author(subtext_soup),
                    comments=self.get_comments(subtext_soup),
                    posted_ago=self.get_posted_ago(subtext_soup)
                )
                Post.objects.filter(post_index_main=post.post_index_main).exclude(id=post.id).delete()
                post.save()

    def get_link(self, anchor):
        link = anchor.attrs.get('href')
        if link.startswith('item'):
            link = '%s%s' % (self.YCOMBINATOR_BASE_URL, link)
        return link

    def get_score(self, soup):
        score = soup.select('span[id^=score]')
        return score[0].getText() if len(score) > 0 else ''

    def get_author(self, soup):
        author = soup.select('a[href^=user]')
        return author[0].getText() if len(author) > 0 else ''

    def get_comments(self, soup):
        num_comments = soup.select('a[href^=item]')
        return num_comments[0].getText() if len(num_comments) > 0 else ''

    def get_hn_id(self, soup):
        hn_id = soup.select('a[href^=item]')
        if len(hn_id) > 0:
            comments_href = hn_id[0].attrs.get('href')
            return int(comments_href.replace('item?id=', ''))
        return 0

    def get_posted_ago(self, soup):
        subtext_context = unicode(soup).split(' ')
        try:
            ago_index = subtext_context.index('ago')
            posted_ago = "%s %s %s" % (subtext_context[ago_index - 2], subtext_context[ago_index - 1], subtext_context[ago_index])
        except ValueError:
            posted_ago = "No comments"

        return posted_ago
