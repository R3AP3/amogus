# -*- coding: utf-8 -*-
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath
import requests, re, os, wget
os.system('cls' if os.name == 'nt' else 'clear')

img_formats = ["png","jpg"]

logo="""\33[31m
  __ _ _ __ ___   ___   __ _ _   _ ___ 
 / _` | '_ ` _ \ / _ \ / _` | | | / __|
| (_| | | | | | | (_) | (_| | |_| \__ \ 
 \__,_|_| |_| |_|\___/ \__, |\__,_|___/
repository:             __/ |Ver: 0.0.8
github.com/R3AP3/amogus|___/           \33[0m"""

def request_img(val):
    parts = PurePosixPath(unquote(urlparse(val).path)).parts
    album_id = parts[4]
    region_code = parts [1]

    response = requests.get((f'https://itunes.apple.com/lookup?id={album_id}&country={region_code}&entity=album'))

    for details in response.json()["results"]:
        collection_id = details["collectionId"]
        artist_id = details["artistId"]
        artist_name = details["artistName"]
        album_name = details["collectionName"]
        art_url = details["artworkUrl100"]
        copy_right = details["copyright"]
        release_date = details["releaseDate"]
        genre_name = details["primaryGenreName"]

    meta_data = f"""
Artist:         {artist_name} [{artist_id}]
Album:          {album_name} [{collection_id}]
Date:           {release_date}
Copyright:      {copy_right}
Genre:          {genre_name}
"""

    print(meta_data)

    regex = r"/100x100bb.jpg"
    print(f"Downloading...:\n")
    for i in img_formats:
        image_url = f"/1x1sy-100.{i}"
        hq_image = re.sub(regex, image_url, art_url, 1)
        naming_scheme = f'Covers/{artist_name} - {album_name} [{artist_id} - {collection_id}].{i}'
        wget.download(hq_image, naming_scheme)
        print(f"  [{i}]  Done!")

print(logo)
while True:
    val = input("\nApple Music URL: ")
    if 'http' in val:
        request_img(val)

#added a way to exit the loop
    elif val in [ 'exit','quit','Exit','QUIT' ]:
        print('Exiting...')
        exit()
    else:
        print("Wrong input")
