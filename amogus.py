import requests
from pymediainfo import MediaInfo as mi
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

logo=r"""
  __ _ _ __ ___   ___   __ _ _   _ ___ 
 / _` | '_ ` _ \ / _ \ / _` | | | / __|
( (_| | | | | | | (_) | (_| | |_| \__ \ 
 \__,_|_| |_| |_|\___/ \__, |\__,_|___/
repository:             __/ |Ver: 0.1.0
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
    for details in response.json()["results"]:
        aid = details["artistId"]
        cid = details["collectionId"]
        an = details["artistName"]
        cn = details["collectionName"]
        au = details["artworkUrl100"]
    return aid, cid, au, an, cn 

def download(url, filename):
    response = requests.get(url)
    f = open("output/" + filename, "wb")
    f.write(response.content)
    f.close()

def mediainfo(url):
    data = mi.parse(url)
    exif = data.image_tracks[0]
    file = data.general_tracks[0]

    fm = exif.format
    w = exif.width
    h = exif.height
    cs = exif.color_space
    css = exif.chroma_subsampling
    bd = exif.bit_depth
    cm = exif.compression_mode
    ss = exif.stream_size
    icc = exif.colorspace_icc
    if icc == None:
        color_space = cs
    else:
        color_space = cs + "-" + icc 
    if fm == "JPEG":
        ext = "jpg"
    elif fm == "PNG":
        ext = "png"
    fn_meta = f"{w}x{h}-[{color_space}].{ext}"
    return fn_meta 

def filename(a, c, m):
    filename = f"{a}-{c}-{m}"
    return filename

def get_source(art):
    p = PurePosixPath(unquote(urlparse(art).path)).parts
    if p[9] == "source":
        url = f"http://a1.mzstatic.com/us/r30/{p[3]}/{p[4]}/{p[5]}/{p[6]}/{p[7]}/{p[8]}/{p[9]}"
        isSource = "SOURCE"
    else:
        print("Cannot get Source image. Open Issue on Github.")
        isSource = "ENCODE"
        url = re.sub(r"100x100bb.jpg", f"1x1sy.jpg", art)
    return url, isSource

def main(i, region_code):
    parsed = parse_request(i, region_code)
    cover_url = get_source(parsed[2])
    meta = mediainfo(cover_url[0])
    aid = str(parsed[0])
    cid = str(parsed[1])
    filename = str(parsed[0]) + "-" + str(parsed[1]) + "-" + meta
    print(f"[{cover_url[1]}] {parsed[4]}")
    download(cover_url[0], filename)

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
                main(i, region_code)

        else:
            main(album_id, region_code)
    else:
        print("Wrong input")
