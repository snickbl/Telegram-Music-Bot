import hashlib
import itertools
import os
from urllib.parse import quote, unquote

import requests
from sqlalchemy.orm import Session

from engine import engine
from models import Cache


def zaqruzator(argument):
    word = argument
    songsList = {}
    url = f"https://i202.123muza.com/api/song/search/do?origin=textmp3.ru&query={word}"

    songs = requests.get(url).json()

    for index, song in enumerate(songs.get("songs")):
        songsList[index] = song
    return songsList


def polucatel(nomer, spisPes):
    song = spisPes.get(int(nomer))
    arttitle = song.get("artist") + "-" + song.get("title")
    arttitle = "".join(
        "-" if c in r'\\!"\'();:@&=+$,/?%#[\]\n' else c for c in arttitle
    )
    arttitle = arttitle[:2000]
    arttitle += "-textmp3.ru.mp3"
    arttitle = quote(arttitle, safe="-")

    title = quote(song.get("title"), safe="-()")
    artist = quote(song.get("artist"), safe="-")
    index = song.get("index")
    songID = song.get("id")

    song_hash = hashlib.sha256((artist + title).encode()).hexdigest()
    with Session(engine) as session:
        song = session.query(Cache).filter_by(hash=str(song_hash))
    if song.first():
        return song.first().path
    songs_directory = os.path.join(os.getcwd(), "songs")
    file_path = os.path.join(
        songs_directory, f"{unquote(artist)} - {unquote(title)}.mp3"
    )

    for limit, i in enumerate(itertools.cycle((0, 1, 2))):
        down_url = f"https://i20{i}.123muza.com/api/song/download/get/11/{arttitle}?origin=textmp3.ru&url=sid://{songID}&artist={artist}&title={title}&index={index}"
        print(limit, i)
        if limit >= 20:
            break

        res = requests.get(down_url)

        if len(res.content):
            with open(file_path, "wb") as f:
                f.write(res.content)
            song = Cache(hash=str(song_hash), path=file_path)
            with Session(engine) as session:
                session.add(song)
                session.commit()
            return file_path
