# Thats one sussy artwork Downloader
![amogus](https://user-images.githubusercontent.com/89069925/147856498-ce8049f1-1248-4f25-a425-da7dc9b404f7.jpg)
## Usage:
Download Artwork in the best possible Quality from Apple Music in JPEG (Lossy) and PNG (Lossless)
```
Apple Music URL: {link}
```

## Installation
You need MediaInfo-CLI tools installed and added to your path. Here are various Methods to do that on Various Operating systems:

#### Debian, Ubuntu:
```
sudo apt-get install mediainfo
```
#### Arch Linux:
```
sudo pacman -S mediainfo
```
#### Mac OS (via Homebrew):
```
brew install media-info
```
#### Windows
Install the mediainfo CLI via scoop.sh or add the binary from their official website to your path
```
scoop install mediainfo
``` 

#### Termux
``` 
pkg install mediainfo
```
### Installing Amogus:

```bash
git clone https://github.com/R3AP3/amogus.git
```
Install Python, this should work on any version. Then install the requirements:
```python
pip install -r requirements.txt
```
## How to use:

#### Config settings:
Check the `config.ini` to configure your path or switch to a completely unnecessary experimental mode

Start the Script by running:
```
python amogus.py
```
Then paste in an Apple Music URL

The Pictures get saved to the specified path or if none is specified it downloads to the root folder of the script.

You can input Artist URLS aswell they are kind of experimental ish tho so dont be sad when the operation crashes at some point (be sure to open an issue so i can take a look at the error)

## To-Do:

- Animated Artworks
- Fancy out the UI
- Filters

## Screenshot:
![grafik](https://user-images.githubusercontent.com/89069925/147856427-7653deeb-a6e8-46ae-9e4b-944897b45031.png)## Issues:
It seems like libmediainfo is causing some problems sometimes for some people. If you encounter any error copy your terminal output with the error and open an issue.

If you encounter any other issues then feel free to open an Issue aswell.
