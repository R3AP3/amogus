# Thats one sussy artwork Downloader
![amogus](https://user-images.githubusercontent.com/89069925/147856498-ce8049f1-1248-4f25-a425-da7dc9b404f7.jpg)

## Usage:

Either input a `music.apple.com` url or specify a Artist or Album search query. 

```
usage: amogus.py [-h] [-s] [-a] [-r REGION_CODE] INPUT

Downloads Album Covers as their Source File from the Itunes Store

positional arguments:
  INPUT                 Apple Music URL or Album/Artist name

options:
  -h, --help            show this help message and exit
  -s, --search          search for an album
  -a, --artist          search for an artist
  -r REGION_CODE, --region REGION_CODE
                        specify a custom region (default is 'us', see all available region codes: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
```
Use the search by typing `--search` and add `--artist` to download all album covers of the desired artist.

Specifying a region code is optional.

### Installing Amogus:

```bash
git clone https://github.com/R3AP3/amogus.git
```
Install Python, this should work on any version. Then install the requirements:
```bash
pip install -r requirements.txt
```

