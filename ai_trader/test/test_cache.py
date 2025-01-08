# create a test for the DataCache class

from ai_trader.alpaca.cache import DataCache
import os
import sqlite3
import unittest

class TestAlpacaAPICache(unittest.TestCase):
    def test_data_cache(self):
        cache = DataCache(filename="test_news_cache.db")
        assert cache.db_file == "data/test_news_cache.db"
        assert os.path.exists(cache.db_file)
        conn = sqlite3.connect(cache.db_file)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='news'")
        assert c.fetchone() is not None
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='url_content'")
        assert c.fetchone() is not None
        conn.close()
        os.remove(cache.db_file)
        assert not os.path.exists(cache.db_file)

    def test_save_news(self):
        """
                "author": "AJ Fabino",
        "content": "",
        "created_at": "2022-03-02T21:31:02Z",
        "headline": "The Companies Pulling Their Business From Russia After The Ukraine Invasion",
        "id": 25939819,
        "images": [
            {
                "size": "large",
                "url": "https://cdn.benzinga.com/files/imagecache/2048x1536xUP/images/story/2012/investments-gb09c11151_1280.jpg"
            },
        ],
        "source": "benzinga",
        "summary": "Companies around the globe have answered\u00a0Russia\u2019s invasion of Ukraine by putting a hold on business or fully exiting operations in Russia.\n\nThis comes in addition to the harsh economic sanctions recently imposed on Russia that have collapsed the ruble.\n\nBelow is a list of the companies by sector that are holding or retiring business operations in Russia.",
        "symbols": [
            "AAPL",
        ],
        "updated_at": "2022-03-02T21:31:03Z",
        "url": "https://www.benzinga.com/news/22/03/25939819/the-companies-pulling-their-business-from-russia-after-the-ukraine-invasion"
        """
        if os.path.exists("data/test_news_cache.db"):
            os.remove("data/test_news_cache.db")
        cache = DataCache(filename="test_news_cache.db")
        news = [{
            "author": "Test Author", 
            "content": "Test Source", 
            "created_at": "2022-03-02T21:31:02Z",
            "headline": "Test Headline",
            "id": 1,
            "images": "https://test.com",
            "source": "Test Source",
            "summary": "Test Summary",
            "symbols": "AAPL",
            "updated_at": "2022-03-02T21:31:02Z",
            "url": "https://test.com"
        }]
        cache.save_news(news)
        conn = sqlite3.connect(cache.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM news")
        result = c.fetchone()
        assert result is not None
        assert result[0] == 1
        assert result[1] == "Test Author"
        assert result[2] == "Test Source"
        assert result[3] == "2022-03-02T21:31:02Z"
