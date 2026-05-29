from bing_image_downloader import downloader

foods = [
    "idli", "dosa", "chapati", "fried rice",
    "biryani", "pongal", "poori",
    "curd rice", "sambar rice", "paneer curry",
    "salad", "apple", "banana", "burger", "pizza"
]

for food in foods:
    downloader.download(food, limit=200, output_dir='dataset_raw', adult_filter_off=True)