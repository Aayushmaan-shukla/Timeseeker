import speech_recognition as sr
import spotipy
import pyttsx3
from rapidfuzz import process
from spotipy import SpotifyOAuth
import re
engine = pyttsx3.init()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='a21ee1673b174c0ba59da83aa87bb7c1',
    client_secret='ca04edd66acb41d19cc525be416ba718',
    redirect_uri='https://open.spotify.com/',
    scope="user-modify-playback-state,user-read-playback-state"))

def keyword():
    recog = sr.Recognizer()
    micro = sr.Microphone()
    print("say Jarvis")
    while True:
        with micro as source:
            recog.adjust_for_ambient_noise(source)
            audio = recog.listen(source)
        try:
            cmd = recog.recognize_google(audio).lower()
            if 'Jarvis' in cmd:
                engine.say("Bitch")
                engine.runAndWait()
            return True
        except sr.UnknownValueError:
            continue

words_to_numbers = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50
}

# Helper function to convert words to time format
def convert_words_to_time(cmd):
    cmd = cmd.lower()

    # Remove any non-word characters except spaces
    cmd= re.sub(r'[^\w\s]', '', cmd)

    # Regex pattern to match spoken time like 'two thirty two' or '4 32'
    word_pattern = r'(\w+)\s+(\w+)'
    number_pattern = r'(\d+)\s*(\d*)'
    match = re.search(word_pattern, cmd)
    if match:
        # Try converting words into numbers using the dictionary
        minutes_word, seconds_word = match.groups()
        minutes = words_to_numbers.get(minutes_word, None)
        seconds = words_to_numbers.get(seconds_word, None)
        if minutes is not None and seconds is not None:
            return f"{minutes}:{seconds:02}"
        elif minutes is not None:
            return f"{minutes}:00"
    match = re.search(number_pattern, cmd)
    if match:
        minutes, seconds = match.groups()
        if len(minutes) > 2:
            minutes, seconds = minutes[:-2], minutes[-2:]
        if not seconds:
            seconds = "00"  # If no seconds, default to 00
        return f"{int(minutes)}:{int(seconds):02}"

    return None

def fuzzy_match_time(cmd):
    time_formats = ["1:00", "2:30", "3:45", "4:34", "5:15", "10:00", "20:00"]
    #finding best match
    best_match, confidence = process.extractOne(cmd, time_formats)
    print(f"Fuzzy match result: {best_match} with confidence: {confidence}")
    return best_match if confidence > 80 else None


def time():
    recog = sr.Recognizer()
    micro = sr.Microphone()
    with (micro as source):
        print("Please say the time:")
        recog.adjust_for_ambient_noise(source)
        audio = recog.listen(source)
        try:
            # Recognize the time command
            cmd = recog.recognize_google(audio)
            print(f"Recognized command: {cmd}")
            # words to time
            time_str = convert_words_to_time(cmd)
            if time_str is not None:
                minutes, seconds = map(int, time_str.split(':'))
                milliseconds = (minutes * 60 + seconds) * 1000
                print(f"Time in milliseconds: {milliseconds}")
                return milliseconds
            else:
                print("Could not understand the time format.")
                return None
        except ValueError:
            print("Could not understand time, make sure it is in 'minutes:seconds' format.")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio, try again.")
            return None
def spotify(position_ms):
    playinfo = sp.current_playback()
    if playinfo and playinfo['is_playing']:
        sp.seek_track(position_ms)
        print(f"seeked to {position_ms} ms.")
    else:
        print("No such song")
if keyword():
    time_in_ms = time()
    if time_in_ms is not None:
        spotify(time_in_ms)

