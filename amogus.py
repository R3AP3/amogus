import os
import argparse
import requests
from pathlib import PurePosixPath
from urllib.parse import unquote, urlparse


logo = r"""
  __ _ _ __ ___   ___   __ _ _   _ ___
 / _` | '_ ` _ \ / _ \ / _` | | | / __|
( (_| | | | | | | (_) | (_| | |_| \__ \
 \__,_|_| |_| |_|\___/ \__, |\__,_|___/
repository:             __/ |Ver: 0.2.0
github.com/R3AP3/amogus|___/           """


def get_collectionids(album_id: str, region_code: str):
    response = requests.get('https://itunes.apple.com/' +
                            f'lookup?id={album_id}&country={region_code}' +
                            '&entity=album&limit=200&sort=recent')

    data = response.json()["results"]
    print("Downloading Artist: " + data[0]["artistName"])
    idlist = []

    for i in enumerate(data):
        idlist.append(data[i]['collectionId'])
        # if i != 0:
        #     idlist.append(data[i]["collectionId"])

    return idlist


def parse_request(album_id, region_code):
    response = requests.get('https://itunes.apple.com/' +
                            f'lookup?id={album_id}&country={region_code}' +
                            '&entity=album')

    data = response.json()["results"][0]
    filename = "{} [{}]".format(
        data['collectionNam'],
        data['collectionName'])

    print(data['artistName'], data['collectionName'])

    return data["artworkUrl100"], filename


def download_pic(url, filename):
    r = requests.get(url)
    ext = r.headers["content-type"].split("/")[1]

    with open(f"cover/{filename}.{ext}", "wb") as f:
        f.write(r.content)


def get_source(art):
    p = PurePosixPath(
        unquote(urlparse(art).path)).parts

    if p[9] == "source":
        return "http://a1.mzstatic.com/us/r30/" + \
               f"{p[3]}/{p[4]}/{p[5]}/{p[6]}/{p[7]}/{p[8]}/{p[9]}"
    else:
        return art


def routine(album_id, region_code):
    cover_url, filename = parse_request(album_id, region_code)
    download_pic(
            get_source(cover_url), filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("link",
                        help="link of album/artist")
    url = parser.parse_args().link

    if not os.path.exists("cover"):
        os.makedirs("cover")

    # url = input("Apple Music URL: ")

    if 'http' in url:
        parts = PurePosixPath(
                unquote(urlparse(url).path)).parts

        if parts[2] == "artist":
            for id in get_collectionids(parts[4], parts[1]):
                routine(id, parts[1])

        else:
            routine(parts[4], parts[1])
    else:
        print("Wrong input, no 'https' in link")
