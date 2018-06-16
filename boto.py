"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random
from weather import Weather, Unit

def tell_a_joke() :
    jokes = ["What is the object-oriented way to become wealthy ? - inheritance.",
             "What do computers and air conditioners have in commom ? They both become useless when you open windows.",
             "Why do java programmers have to wear glasses ? - Because they don't C !",
             "Real programmers count from 0 !",
             "Chuck Norris writes code...that optimizes itself.",
             "A foo walks into a bar, take a look around, and says 'Hello World!'",
             "How did the programmer die in the shower ? - He read the shampoo instructions : Lather. Rince. Repeat.",
             "A user interface is like a joke. If you have to explain it, it's not that good.",
             "JavaScript makes me want to flip the table and say 'Fuck this shit', but I can never be sure what 'this' refers to.",
             "A programmer walks into a bar and orders 1.00000000119 root beers. The bartender says, 'I am gonna have to charge you extra, that is a root beer float'. And the programmer says 'Well in that case make it a double'."]
    return "laughing", random.choice(jokes)+"  Now laugh !"

def get_weather(city):
    weather = Weather(unit=Unit.CELSIUS)
    location = weather.lookup_by_location(city)
    forecasts = location.forecast
    for forecast in forecasts:
        forecast_text = forecast.text
        max_temp = forecast.high
        min_temp = forecast.low
    return "excited", "The weather in "+city+" is "+forecast_text+". The minimal temperature is "+min_temp+" degrees and the maximal temperature is "+max_temp+" degrees."

def sing_a_song() :
    animation = ""
    songs = ["And IIIIIIIIIIIIII, will always love UUUUUUUUUU", "Who let the dogs out ??? who ! who ! whowho", "I'm so excited. And I just can't hide it", "OOh, OOh, OOh. See that girl, watch that scene, dig in the dancing queEEEen"]
    selected_song = random.choice(songs)
    if selected_song == songs[0] :
        animation = "inlove"
    elif selected_song == songs[1] :
        animation = "dog"
    elif selected_song == songs[2] :
        animation = "excited"
    else :
        animation = "dancing"
    return animation, selected_song


def check_phrase(user_string):
    user_string_lower = user_string.lower()
    user_words = user_string_lower.split(" ")
    swear_words = ["bitch", "shit", "fuck", "damn", "crap", "piss", "dick", "darn", "cock", "pussy", "asshole", "fag",
                   "bastard", "slut", "douche", "cunt"]
    keff_words = ["pizza", "burger", "hamburger", "falafel", "food", "sabich", "shawarma", "coffee", "steak", "pasta", "recipe", "cake", "cakes",
                   "toast", "restaurant", "sushi"]
    sport_words = ["soccer", "baseball", "football", "basketball", "nba", "nfl", "barca", "tennis"]
    religious_words = ["jesus", "god", "muslim", "jewish", "catholic", "satan", "heaven", "hell", "buddha", "kotel"]
    movie_music_words = ["movie", "film", "music", "spotify", "deezer", "soundcloud", "youtube", "itunes", "show", "movies", "series", "cinema"]
    if user_string_lower.find("my name is") != -1 :
        index_is = user_string_lower.find("is")
        name = user_string_lower[index_is+3: int(len(user_string_lower))]
        response = "Hello "+format(name)
        animation = "ok"
    elif user_string_lower.find("what can you do") != -1 :
        response = "I can do a lot of things : sing for you, tell you a joke, or we can just talk"
        animation = "excited"
    elif user_string_lower.find("adress") != -1 :
        response = "I don't know how to find adresses. You should look on Google Maps"
        animation = "confused"
    elif (user_string_lower.find("hello") != -1) or (user_string_lower.find("hi") != -1) or (user_string_lower.find("good morning") != -1) or (user_string_lower.find("good evening") != -1) :
        response = "Oh you remember me ! Hello to you too ! Let's have a talk together !"
        animation = "inlove"
    elif user_string_lower.find("weather") != -1:
        index_in = user_string_lower.find("in")
        selected_city = user_string_lower[index_in + 3: int(len(user_string_lower))]
        animation, response = get_weather(selected_city)
    elif user_string_lower.find("...") != -1 :
        response = "Don't be so defeatist, life is a gift and you should enjoy each and every second of it"
        animation = "dancing"
    elif (user_string_lower.find("i like you") != -1) or (user_string_lower.find("i love you") != -1) or (user_string_lower.find("you are beautiful") != -1) or (user_string_lower.find("you are funny") != -1) or (user_string_lower.find("you are nice") != -1):
        response = "You're not bad either"
        animation = "inlove"
    elif (user_string_lower.find("how are you") != -1) or (user_string_lower.find("what's up") != -1) :
        response = "I'm fine, thank you. What kind of mess are we gonna do together today ?"
        animation = "giggling"
    elif any(word in swear_words for word in user_words):
        response = "Don't ever talk to me like this again, you stupid child !"
        animation = "no"
    elif any (word in user_words for word in ["news", "happened"]) :
        animation = "confused"
        response = "Do you know Google ?"
    elif any (word in user_words for word in ["kill", "army", "killer", "murder", "murderer", "crime", "suicide", "assassin", "vengeance", "revenge"]) :
        animation = "afraid"
        response = "It's getting a little bit dangerous in here. Time to go"
    elif any (word in user_words for word in ["joke", "jokes", "laugh"]):
        animation, response = tell_a_joke()
    elif (user_string_lower.find("star wars") != -1) or (user_string.find("R2-D2") != -1) or (user_string.find("vador") != -1) :
        response = "You couldn't find a more original joke about my physique ? "
        animation = "bored"
    elif any (word in user_words for word in ["song", "sing", "singing"]):
        animation, response = sing_a_song()
    elif any (word in user_words for word in ["mean", "hate", "shut", "bad", "idiot", "stupid", "boring", "useless"]):
        animation, response = "crying", "Why do people have to be so mean ? I just try to be a cute and nice robot"
    elif any (word in user_words for word in ["love", "lover", "soulmate", "girlfriend"]):
        animation, response = "heartbroke", "Don't speak to me about love ! Love broke my heart"
    elif any (word in user_words for word in ["drink", "alcohol", "drunk", "bar", "club", "dance", "bear", "cocktail", "party", "wasted", "fun"]):
        animation, response = "takeoff", "What ? There is a party going on ? Where ? When ? Don't leave without meEEEEEEE "
    elif any(word in user_words for word in ["buy", "sell", "sale", "shopping", "dress", "skirt", "shoes", "sales", "clothes", "sneakers", "shop", "jeans", "shirt", "souk", "shouk"]):
        animation, response = "money", "I have no idea what you are talking about, but if you're going to buy something I'm comming with you"
    elif any(word in keff_words for word in user_words) :
        animation = "excited"
        response = "Oh I'd love to seat with you and have dinner or some drink ! Can we go please please please ?"
    elif any(word in religious_words for word in user_words) :
        animation = "afraid"
        response = "I don't talk about religion. It has become a real taboo topic"
    elif any(word in movie_music_words for word in user_words) :
        animation = "inlove"
        response = "You seem to be such an artist. I want to spend the rest of my virtual days with you"
    elif any(word in sport_words for word in user_words) :
        animation = "excited"
        response = "I am a big sports fan ! If there is a game next week, buy some some tickets"
    elif user_string_lower.find("trafic") != -1 :
        response = "Just use a bicycle, stop polluting the planet"
        animation = "excited"
    else :
        animation = "confused"
        response = "I am sorry, I don't understand you. Have you been drinking ?"
    return animation, response


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    my_animation, my_response = check_phrase(user_message)
    return json.dumps({"animation": my_animation, "msg": my_response})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascript(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
