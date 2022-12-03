import time

import aria2p
import requests
import json
import os
import urllib
import sys


class Scraper:

    def __init__(self, config):
        self.config = config

        self.aria2 = aria2p.API(aria2p.Client(
            host="http://127.0.0.1",
            port=6800,
            secret=""
        ))

    # Set config for bookmarks (next page)
    def setConfig(self, config):
        self.config = config

    # Download images
    def download_images(self, save_dir):
        # prev get links
        results = self.get_urls()

        try:
            os.makedirs(save_dir)
            print("Directory ", save_dir, " Created ")
        except FileExistsError:
            pass

        downloads = []

        for url in results:
            try:
                print("Add ::: ", url)

                options = {'dir': save_dir, 'out': url.split("/")[-1], 'continue': True,
                           'max-tries': 5, 'auto-file-renaming': False,
                           'split': 1}
                downloads.append(self.aria2.add_uris([url], options))
            except Exception as e:
                print(e)

        while any(downloads):
            download = downloads.pop(0)
            while True:
                download.update()
                if download.has_failed:
                    self.aria2.remove([download])
                    downloads.append(self.aria2.add_uris([download.files[0].uris[0].values()[0]], download.options))
                elif download.is_complete:
                    break
                else:
                    time.sleep(1)

    # get_urls return array
    def get_urls(self):
        count = 0
        while count < int(self.config.file_length):
            SOURCE_URL = self.config.source_url,
            DATA = self.config.image_data,
            URL_CONSTANT = self.config.search_url
            r = requests.get(URL_CONSTANT, params={
                             "source_url": SOURCE_URL, "data": DATA})
            jsonData = json.loads(r.content)
            resource_response = jsonData["resource_response"]
            data = resource_response["data"]
            results = data["results"]
            for i in results:
                count += 1
                yield i["images"][self.config.image_quality]["url"]

            try:
                self.config.bookmarks = resource_response["bookmark"]
            except:
                return
            finally:
                print("Creating links", count)

        #if len(str(resource_response["bookmark"])) > 1 : connect(query_string, bookmarks=resource_response["bookmark"])



