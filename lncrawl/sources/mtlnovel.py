# -*- coding: utf-8 -*-
import logging
import re
from lncrawl.core.crawler import Crawler

logger = logging.getLogger(__name__)
search_url = '%s/wp-admin/admin-ajax.php?action=autosuggest&q=%s'


class MtlnovelCrawler(Crawler):
    base_url = [
        'http://www.mtlnovel.com/',
        'http://id.mtlnovel.com/',
        'http://fr.mtlnovel.com/',
        'http://es.mtlnovel.com/',
    ]

    def search_novel(self, query):
        query = query.lower().replace(' ', '%20')
        #soup = self.get_soup(search_url % query)

        results = []
        for url in self.base_url:
            list_url = search_url % (url, query)
            data = self.get_json(list_url)['items'][0]['results']

            for item in data[:10]:
                url = item['permalink']
                results.append({
                    'url': url,
                    'title': re.sub(r'</?strong>', '', item['title']),
                })
            # end for
        # end for

        return results
    # end def

    def read_novel_info(self):
        '''Get novel title, autor, cover etc'''
        self.novel_url = self.novel_url.replace('https://', 'http://')
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)

        self.novel_title = soup.select_one('article .entry-title, h1').text.strip()
        logger.info('Novel title: %s', self.novel_title)

        try:
            self.novel_cover = self.absolute_url(
                soup.select_one('.post-content amp-img[fallback]')['src'])
        except Exception as e:
            logger.debug('Could not find novel cover. Error %s', e)
        logger.info('Novel cover: %s', self.novel_cover)

        try:
            self.novel_author = soup.select('table.info a[href*="/novel-author/"]').text.strip()
        except Exception as e:
            logger.debug('Could not find novel author. Error %s', e)
        logger.info('Novel author: %s', self.novel_author)

        for item in soup.select('div.ch-list amp-list'):
            data = self.get_json(item['src'])
            for chapter in data['items']:
                chap_id = 1 + len(self.chapters)
                vol_id = 1 + len(self.chapters) // 100
                if len(self.chapters) % 100 == 0:
                    self.volumes.append({'id': vol_id})
                # end if
                self.chapters.append({
                    'id': chap_id,
                    'volume': vol_id,
                    'url':  chapter['permalink'],
                    'title': chapter['no'] + " " + chapter['title'],
                })
            # end for
        # end for
    # end def

    def download_chapter_body(self, chapter):
        '''Download body of a single chapter and return as clean html format.'''
        url = chapter['url'].replace('https://', 'http://')
        logger.info('Downloading %s', url)
        soup = self.get_soup(url)
        contents = soup.select_one('.post-content .par')
        return self.extract_contents(contents)
    # end def
# end class
