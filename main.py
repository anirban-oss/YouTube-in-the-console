from twitchrealtimehandler import TwitchImageGrabber
import xml.etree.ElementTree as ElementTree
from moviepy.editor import VideoFileClip
from skimage.transform import resize
from getkey import getkey, keys
from replit import clear, audio
from pytube import YouTube
from html import unescape
import threading
import math
import glob
import time
import os

isOwner = os.path.exists("/tmp/audioStatus.json")

# thx @hecker40
def fg(r, g, b):
  return f"\033[38;2;{int(r)};{int(g)};{int(b)}m"
def bg(r, g, b):
  return f"\033[48;2;{int(r)};{int(g)};{int(b)}m"
reset = "\033[0m"

# thx @ColoredHue
def hide_cursor():
  print("\033[?25l", end="", flush=True)
def show_cursor():
  print("\033[?25h", end="", flush=True)

for file in glob.glob("*.mp3"):
  os.remove(file)

for file in glob.glob("*.mp4"):
  os.remove(file)

show_cursor()

print("How would you like to calculate screen size?")
print("1: The Automatic Way")
print("2: The Cool Way")
option = input("> ")

if option == "1":
  size = os.get_terminal_size()
  width = size.columns
  height = size.lines
else:
  clear()
  print("You're about to be asked questions so we can get the correct screen size. You may be asked to see which character appears in the corner, but oftern this is obscured by buttons. To remove them, click off the screen")
  print()
  input("Press enter to continue > ")
  clear()
  
  chars = "0123456789abcdef"
  msg = "Which character appears in the top right corner of the screen? > "
  
  print(chars*len(chars))
  print()
  c = input(msg).lower()
  clear()
  
  for x in chars:
    print(" "*chars.find(c)+x+" "*(len(chars)-chars.find(c)-1), end="", flush=False)
  print("\n", flush=True)
  c2 = input(msg).lower()
  clear()
  
  width = chars.find(c2)*len(chars)+chars.find(c)+1
  
  for x in chars:
    for y in chars:
      print(" "*(width-1), y, sep="", flush=False)
  print(flush=True)
  c = input(msg).lower()
  clear()
  
  i = 0
  for x in chars:
    for y in chars:
      if y == c:
        print(" "*(width-1), chars[i], sep="", flush=False)
        i += 1
      else:
        print(flush=False)
  print(flush=True)
  c2 = input(msg).lower()

  height = len(chars)**2 - (chars.find(c2) * len(chars) + chars.find(c)) + math.ceil((len(msg) + 1) / width) + 1

clear()
print("Choose an option")
print("1: Download from YouTube")
print("2: Livestream from Twitch")

if isOwner:
  print("3: Custom MP4s")
  option = input("> ")
  youtube = option != "2" and option != "3"
  twitch = option == "2"
  custom = option == "3"
else:
  option = input("> ")
  youtube = option != "2"
  twitch = option == "2"
  custom = False

clear()
if youtube:
  url = input("Enter a YouTube video url > ")
elif custom:
  print("Upload an mp4 file to continue")
  while len(glob.glob("*.mp4")) == 0:
    time.sleep(3)
else:
  url = input("Enter a Twitch livestream url > ")

if isOwner and not twitch:
  clear()
  playAudio = input("Do you want audio? y/n > ") == "y"
  if playAudio:
    audio.play_tone(0.01, 262, 0)
    input("Press enter to continue > ")
else:
  playAudio = False

if youtube:
  clear()
  enableCaptions = input("Do you want captions? y/n > ") == "y"
else:
  enableCaptions = False

clear()
print("Choose a quality")
print("1: 1x Resolution")
print("2: 4x Resolution (Warning: Glitchy)")
option = input("> ")

fourRes = option == "2"

pixWidth = width
pixHeight = height

if not fourRes:
  pixWidth //= 2
  pixHeight -= 1
else:
  pixHeight *= 2
  pixWidth -= 12
  pixHeight -= 2

# This fixes a bug and also lets me download in a very easy format
# adapted from https://stackoverflow.com/a/69004322/17766761
def xml_caption_to_dict(xml):
  segments = []
  root = ElementTree.fromstring(xml)
  count_line = 0
  for i, child in enumerate(list(root.findall("body/p"))):
    text = "".join(child.itertext()).strip()
    if not text:
      continue
    count_line += 1
    caption = unescape(text.replace("\n", " ").replace("  ", " "),)
    try:
      duration = float(child.attrib["d"])
    except KeyError:
      duration = 0.0
    start = float(child.attrib["t"])
    try:
      end2 = float(root.findall("body/p")[i+2].attrib["t"])
    except:
      end2 = float(root.findall("body/p")[i].attrib["t"]) + duration
    line = {
      "start": start / 1000,
      "end": end2 / 1000,
      "text": caption,
    }
    segments.append(line)
  return segments

def getFrame():
  global currentFrame
  while True:
    start = time.time()
    currentFrame = imageGrabber.grab()
    duration = time.time()-start
    time.sleep(max(1/fps-duration, 0))

if not twitch:
  if youtube:
    clear()
    print("Downloading Video...")
    
    yt = YouTube(url)
    vid = yt.streams.filter(file_extension="mp4").first()
    vid.download()
  
  clear()
  print("Opening Video...")
  
  filename = glob.glob("*.mp4")[0]
  os.replace(filename, "video.mp4")
  vid = VideoFileClip("video.mp4")
  
  clear()
  print("Resizing Video...")
  
  vidWidth, vidHeight = vid.size
  ratio = min(pixWidth / vidWidth, pixHeight / vidHeight)
  
  vid = vid.resize(ratio)
  
  if playAudio:
    clear()
    print("Extracting Audio...")
  
    vidAudio = vid.audio
    vidAudio.write_audiofile("audio.mp3", logger=None)
  
  if enableCaptions:
    clear()
    print("Downloading Captions...")
  
    captions = yt.captions
    if "en" in captions:
      captions = captions.get_by_language_code("en")
    elif "a.en" in captions:
      captions = captions.get_by_language_code("a.en")
    else:
      enableCaptions = False
  
    if enableCaptions:
      captions = xml_caption_to_dict(captions.xml_captions)
  
  hide_cursor()
  clear()
  
  if playAudio:
    source = audio.play_file("audio.mp3")
else:
  clear()
  print("Connecting...")
  fps = 4

  try:
    imageGrabber = TwitchImageGrabber(
      twitch_url = url,
      quality = "160p",
      blocking = True,
      rate = fps,
    )
  except ValueError:
    imageGrabber = TwitchImageGrabber(
      twitch_url = url,
      quality = "480p",
      blocking = True,
      rate = fps,
    )
  
  currentFrame = None

  threading.Thread(target=getFrame).start()

  while currentFrame is None:
    time.sleep(0.1)

start = time.time()

paused = False
stop = False

def controls():
  global paused, start, playAudio, source
  while stop is False:
    key = getkey()
    if key == " " or key == "k":
      paused = not paused
    elif key == keys.LEFT:
      start += 10
      if playAudio:
        source.paused = True
        playAudio = False
    elif key == keys.RIGHT:
      start -= 10
      if playAudio:
        source.paused = True
        playAudio = False
    elif key == "r":
      if playAudio:
        source.paused = True
        source = audio.play_file("audio.mp3")
      start = time.time()
    if playAudio:
      if key == "+" or key == "=":
        source.volume += 0.1
      elif key == "-":
        if source.volume - 0.1 > 0:
          source.volume -= 0.1

if not twitch:
  thread = threading.Thread(target=controls)
  thread.start()

try:
  while True:
    if not twitch:
      t = time.time() - start
      frame = vid.make_frame(t=t)
    else:
      frame = currentFrame
      vidWidth = len(frame[0])
      vidHeight = len(frame)
      ratio = min(pixWidth / vidWidth, pixHeight / vidHeight)*2
      frame = resize(frame, (pixHeight*ratio, pixWidth*ratio))
      for column in range(len(frame)):
        for row in range(len(frame[column])):
          frame[column][row] = [x*255 for x in frame[column][row]]
    text = "\033c"
    if fourRes:
      for column in range(0, len(frame), 2):
        for row in range(len(frame[column])):
          try:
            text += bg(*frame[column][row])+fg(*frame[column + 1][row])+"▄"
          except IndexError:
            text += reset+fg(*frame[column][row])+"▀"
        text += "\n"
    else:
      for column in frame:
        for pixel in column:
          text += bg(*pixel)+"  "
        text += "\n"
    text += reset
    if enableCaptions:
      for caption in captions:
        if caption["start"] < t and caption["end"] > t:
          text += "\n"
          text += caption["text"].center(width)
    print(text, end="", flush=True)
    time.sleep(0.25)
    if paused:
      if playAudio:
        source.paused = True
      pauseStart = time.time()
      while paused:
        pass
      start += time.time() - pauseStart
      if playAudio:
        source.paused = False
except OSError:
  clear()
  print("Video Finished! Don't forget to like and subscribe!")
  stop = True
except KeyboardInterrupt:
  stop = True