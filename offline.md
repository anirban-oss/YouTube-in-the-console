### Thanks to [@ElijahSeele](https://replit.com/@ElijahSeele) for creating this post
# To get it to work offline

Using this method I got it to work offline (on my computer rather than Replit). Sound doesn't work because the `pyaudio` module isn't a drop-in replacement for the Replit `audio` module. If someone has a solution for sound, please comment and let us know and I will update this accordingly. If you don't even want to try to make sound work, then don't install `pyaudio` and delete line 3. Video however is flawless after a few tweaks.

##

### First install these Python modules:
As long as you can install them on your OS, then it will work.
* `python3-pyaudio`
* `python3-pip`
* `python3-moviepy`

Then install `ffmpeg`

Use pip to install `getkey` and `pytube`


### The following command will do all this for you on any Debian/Ubuntu based Linux distro:
``` bash
sudo apt install -y python3-pyaudio python3-pip python3-moviepy ffmpeg; pip install pytube; pip install getkey
```

### Edit the Py file
* Change line 6 of `main.py` to `import pyaudio` so that it doesn't crash. Or give up and delete it entirely.
* Change line 15 `isOwner = os.path.exists("/tmp/audioStatus.json")` to `isOwner = True`. Only do this if you intend to tweak it into submission because that kills the program. However, I think it's a necessary step towards making audio work.
Finally, add to the beginning of the Py file somewhere these lines (will work on any OS):

### Finally, add to the beginning of the Py file somewhere these lines (will work on any OS):
``` python
clear = lambda: print("\033[H\033[2J", end="", flush=True)
```
### *Edits:*

 * *The clear code snippet was added by [@KanavGupta7](https://replit.com/@KanavGupta7)*
* *Can anyone change this to support sound? We'd be greatful*