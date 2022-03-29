import requests, os
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

logo = r"""
  __ _ _ __ ___   ___   __ _ _   _ ___
 / _` | '_ ` _ \ / _ \ / _` | | | / __|
( (_| | | | | | | (_) | (_| | |_| \__ \
 \__,_|_| |_| |_|\___/ \__, |\__,_|___/
repository:             __/ |Ver: 0.2.0
github.com/R3AP3/amogus|___/           """

def get_collectionids(album_id, region_code):
    response = requests.get(f'https://itunes.apple.com/lookup?id={album_id}&country={region_code}&entity=album&limit=200&sort=recent')
    data = response.json()["results"]
    idlist = []
    for i in range(len(data)):
        if i == 0:
            print("Downloading Artist: " + data[i]["artistName"])
        else:
            dict_raw = data[i]
            collection_id = dict_raw["collectionId"]
            idlist.append(collection_id)
    return idlist

def parse_request(album_id, region_code):
    response = requests.get(f'https://itunes.apple.com/lookup?id={album_id}&country={region_code}&entity=album')
    details = response.json()["results"][0]
    filename = str(details["artistId"]) + " - " + str(details["collectionId"])
    download_status = str(details["artistName"]) + " - " + str(details["collectionName"])
    cover_url = details["artworkUrl100"]
    return cover_url, download_status, filename

def download_picture_with_correct_extension(url, filename, download_status):
    r = requests.get(url)
    ext = r.headers["content-type"].split("/")[1]
    with open(f"cover/{filename}.{ext}", "wb") as f:
        f.write(r.content)

def get_source(art):
    p = PurePosixPath(unquote(urlparse(art).path)).parts
    if p[9] == "source":
        url = f"http://a1.mzstatic.com/us/r30/{p[3]}/{p[4]}/{p[5]}/{p[6]}/{p[7]}/{p[8]}/{p[9]}"
    return url

def make_dir():
    if not os.path.exists("cover"):
        os.makedirs("cover")

def routine(album_id, region_code):
    cover_url, download_status, filename = parse_request(album_id, region_code)
    cover_url = get_source(cover_url)
    download_picture_with_correct_extension(cover_url, filename, download_status)
    print(download_status)

def main():
    val = input("\nApple Music URL: ")
    if 'http' in val:
        url_parts = PurePosixPath(unquote(urlparse(val).path)).parts
        if url_parts[2] == "artist":
            idlist = get_collectionids(url_parts[4], url_parts[1])
            for i in idlist:
                routine(i, url_parts[1])
        else:
            routine(url_parts[4], url_parts[1])
    else:
        print("Wrong input")

print(logo)
make_dir()

while True:
    main()

