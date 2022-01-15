# -*- coding: utf-8 -*-
from configparser import ConfigParser
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath
from pymediainfo import MediaInfo
import requests, re, os, wget

logo="  __ _ _ __ ___   ___   __ _ _   _ ___ \n / _` | '_ ` _ \ / _ \ / _` | | | / __|\n| (_| | | | | | | (_) | (_| | |_| \__ \ \n \__,_|_| |_| |_|\___/ \__, |\__,_|___/\nrepository:             __/ |Ver: 0.0.11\ngithub.com/R3AP3/amogus|___/           "

def get_collectionids(album_id, region_code):
    response = requests.get(f'https://itunes.apple.com/lookup?id={album_id}&country={region_code}&entity=album')
    data = response.json()["results"]
    idlist = []
    for i in range(len(data)):
        if i == 0:
            print(data[i])
        else:
            dict_raw = data[i]
            collection_id = dict_raw["collectionId"]
            idlist.append(collection_id)
    return idlist;

def download_covers(album_id, region_code):
    response = requests.get(f'https://itunes.apple.com/lookup?id={album_id}&country={region_code}&entity=album')
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
    regex = r"100x100bb.jpg"
    print(f'Downloading...:\n')
    for i in img_formats:
        image_url = f"/1x1sy-100.{i}"
        image_hq = re.sub(regex, image_url, art_url, 1)
        if i == 'jpg':
            mi = MediaInfo.parse(image_hq)
            image_track = mi.image_tracks[0]
            print(f'Resolution:     {image_track.width}x{image_track.height}\nBit Depth:      {image_track.bit_depth} bits\nColor Space:    {image_track.color_space}\n')
        wget.download(image_hq, file_path + f'{artist_name}_{album_name}-{image_track.width}x{image_track.height}_{image_track.color_space}_{image_track.bit_depth}bit.{i}')
        print(f"  [{i}]  Done!")

os.system('cls' if os.name == 'nt' else 'clear')

cfg = ConfigParser()
cfg.read('config.ini')
file_path = cfg.get('settings', 'file_path')
img_set = cfg.get('settings', 'img_formats')

if img_set == 'normal':
    img_formats = ["jpg","png"]
elif img_set == 'experimental':
    img_formats = ["jpg","png","webp","heic"]
else:
    print("Config Error: img_formats")
    exit()
print(logo)
while True:
    val = input("\nApple Music URL: ")
    if 'http' in val:
        url_parts = PurePosixPath(unquote(urlparse(val).path)).parts
        album_id = url_parts[4]
        region_code = url_parts[1]
        if '/artist/' in val:
            idlist = get_collectionids(album_id, region_code)
            for i in idlist:
                download_covers(i, region_code)
        else:
            download_covers(album_id, region_code)
        
    else:
        print("Wrong input")
