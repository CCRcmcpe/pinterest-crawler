
from src import PinterestScraper, PinterestConfig


configs = PinterestConfig(search_keywords="leopard 2a6", # Search word
                          file_lengths=2000,     # total number of images to download (default = "100")
                          image_quality="orig", # image quality (default = "orig")
                          bookmarks="")         # next page data (default= "")

PinterestScraper(configs).download_images(r'E:\leopard')     # download images directly
#print(PinterestScraper(configs).get_urls())     # just bring image links
