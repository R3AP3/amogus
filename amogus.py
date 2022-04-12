import requests, os, argparse
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

logo = r"""
  __ _ _ __ ___   ___   __ _ _   _ ___
 / _` | '_ ` _ \ / _ \ / _` | | | / __|
( (_| | | | | | | (_) | (_| | |_| \__ \
 \__,_|_| |_| |_|\___/ \__, |\__,_|___/
repository:             __/ |Ver: 0.3.0
github.com/R3AP3/amogus|___/           
"""

parser = argparse.ArgumentParser(description="Downloads Album Covers as their Source File from the Itunes Store")
parser.add_argument("-s", "--search", dest='album_search', help="search for an album", action="store_true")
parser.add_argument("-a", "--artist", dest='artist_search', help="search for an artist", action="store_true")
parser.add_argument("-r", "--region", type=str, dest='region_code', help="specify a custom region (default is 'us', see all available region codes: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)", default="us", metavar="REGION_CODE")
parser.add_argument("input", type=str, help="Apple Music URL or Album/Artist name", metavar="INPUT")

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
    if ext == "jpeg":
        ext = "jpg"
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
    print(download_status)
    download_picture_with_correct_extension(cover_url, filename, download_status)
    

def search_query_itunes_artist(query, region_code):
    response = requests.get(f'https://itunes.apple.com/search?term={query}&entity=musicArtist&limit=25')
    data = response.json()["results"]
    for i in range(len(data)):
        print(f"[{i+1}] {data[i]['artistName']}")
    album_id = data[int(input("\nChoose the Artist to download: "))-1]["artistId"]
    idlist = get_collectionids(album_id, region_code)
    for i in idlist:
        routine(i, region_code)

def search_query_itunes_album(query, region_code):
    response = requests.get(f'https://itunes.apple.com/search?term={query}&entity=album&limit=25')
    data = response.json()["results"]
    for i in range(len(data)):
        print(f"[{i+1}] {data[i]['artistName']} - {data[i]['collectionName']}")
    album_id = data[int(input("\nChoose the album to download: "))-1]["collectionId"]
    print(album_id)
    routine(album_id, region_code)

def main(val):
    if 'https://music.apple.com' in val:
        url_parts = PurePosixPath(unquote(urlparse(val).path)).parts
        if url_parts[2] == "artist":
            idlist = get_collectionids(url_parts[4], url_parts[1])
            for i in idlist:
                routine(i, url_parts[1])
        else:
            routine(url_parts[4], url_parts[1])

print(logo)
make_dir()

args = parser.parse_args()

if args.album_search == True:
    if args.region_code == None:
        region_code = "us"
    else:
        region_code = args.region_code
    if args.artist_search == False:
        search_query_itunes_album(args.input, region_code)
    elif args.artist_search == True:
        search_query_itunes_artist(args.input, region_code)
elif args.album_search == False:
    main(args.input)