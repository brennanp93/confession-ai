import os

import openai
from flask import Flask, redirect, render_template, request, url_for, session

app = Flask(__name__)
app.secret_key = "tuna"
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        description = request.form["description"].capitalize()
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=generate_prompt(description),
            temperature=0.7,
            max_tokens=100,
        )
        return redirect(
            url_for("index", result=response.choices[0].text, input=description)
        )
    result = request.args.get("result")
    print(result, "result is here <<<--")
    input = request.args.get("input")
    session["user_input"] = input
    session["output"] = result
    return render_template("index.html", result=result, input=input)


@app.route("/share/twitter")
def share_twitter():
    user_input = session["user_input"]
    output = session["output"].lstrip()
    url = "https://movie-finder-ai.herokuapp.com/"
    text = f'Amazing! I described a movie as:\n"{user_input}" \nand the AI correctly guessed it was:\n{output} \nCan you challenge its movie guessing skills?\nTry it now at'
    tweet_url = f"https://twitter.com/intent/tweet?url={url}&text={text}"
    return redirect(tweet_url)


@app.route("/")
def clear_prompt():
    return redirect("/")


def generate_prompt(movie_description):
    return """Forgive me, Father, for I have sinned. 

Confession: Father, forgive me, for I have sinned. It's been a month since my last confession. I lied to my friend about something important. 
Penitent: May God bless you for coming forward. Lying is a common human weakness. Let us reflect on the importance of honesty and consider ways to amend the situation. Say three Hail Marys as a sign of your repentance.

# Confession: Father, I've been struggling with anger lately. I snapped at my coworker, and I feel guilty about it.
# Penitent: It takes courage to admit our struggles. Let us seek God's guidance to control our emotions. Pray for patience and understanding. As your penance, meditate on the Serenity Prayer.

# Confession:  Father, I've been gossiping about others, and I know it's wrong.
# Penitent: Gossiping can harm relationships and sow discord. Acknowledge the harm caused, and strive for kindness in your words. As a penance, reflect on the Golden Rule and say a prayer for those you may have affected.

# Confession: Father, I've neglected my daily prayers and feel distant from God.
# Penitent: God's love is always there for you. Reconnect through prayer, and remember that God is understanding. As your penance, spend some quiet time in prayer, expressing gratitude and seeking guidance.

# Confession:  Father, I've been greedy and materialistic, placing importance on possessions rather than spiritual growth.
# Penitent: Material temptations are common, but true fulfillment comes from spiritual nourishment. Reflect on the teachings of simplicity and generosity. As a penance, consider volunteering or making a charitable contribution.

Confession:{}
Penitent:""".format(
        movie_description.capitalize()
    )
