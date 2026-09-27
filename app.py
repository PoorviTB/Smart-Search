from flask import Flask, render_template, request
import requests
import re

app = Flask(__name__)

HEADERS = {
    "User-Agent": "SmartSearch/1.0"
}


def clean_question(question):
    question = question.lower().strip()

    patterns = [
        r"^what is ",
        r"^what are ",
        r"^who is ",
        r"^who was ",
        r"^where is ",
        r"^when was ",
        r"^when is ",
        r"^why is ",
        r"^why are ",
        r"^how does ",
        r"^how do ",
        r"^how is ",
        r"^explain ",
        r"^tell me about ",
        r"^define ",
    ]

    for pattern in patterns:
        question = re.sub(pattern, "", question)

    question = question.replace("?", "").strip()

    abbreviations = {
        "ai": "artificial intelligence",
        "ml": "machine learning",
        "dl": "deep learning",
        "nlp": "natural language processing",
        "iot": "internet of things",
        "api": "application programming interface",
        "cpu": "central processing unit",
        "gpu": "graphics processing unit",
        "aws": "amazon web services",
        "js": "javascript",
    }

    if question in abbreviations:
        question = abbreviations[question]

    return question


def wikipedia_search(topic):
    """Search Wikipedia and return the best page title."""

    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "list": "search",
        "srsearch": topic,
        "format": "json",
        "srlimit": 5
    }

    response = requests.get(
        url,
        params=params,
        headers=HEADERS,
        timeout=10
    )

    data = response.json()

    results = data.get("query", {}).get("search", [])

    if not results:
        return None

    # Prefer results that contain programming/technology terms
    topic_lower = topic.lower()

    for result in results:
        title = result["title"].lower()

        if topic_lower in title:
            return result["title"]

    return results[0]["title"]


def get_summary(title):
    """Get Wikipedia page summary."""

    url = (
        "https://en.wikipedia.org/api/rest_v1/page/summary/"
        + requests.utils.quote(title)
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=10
    )

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "title": data.get("title", title),
        "summary": data.get("extract", ""),
        "image": data.get("thumbnail", {}).get("source"),
        "url": data.get("content_urls", {})
                   .get("desktop", {})
                   .get("page")
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():

    question = request.form.get("topic", "").strip()

    if not question:
        return render_template(
            "index.html",
            result="Please enter a question or topic.",
            topic=""
        )

    try:

        # Convert question to topic
        topic = clean_question(question)

        # Search Wikipedia
        best_match = wikipedia_search(topic)

        if not best_match:
            return render_template(
                "index.html",
                result="❌ No information found.",
                topic=question
            )

        # Get page information
        page = get_summary(best_match)

        if not page or not page["summary"]:
            return render_template(
                "index.html",
                result="❌ Information could not be found.",
                topic=question
            )

        return render_template(
            "index.html",
            result=page["summary"],
            topic=page["title"],
            image=page["image"],
            source=page["url"]
        )

    except Exception as e:

        print("SEARCH ERROR:", e)

        return render_template(
            "index.html",
            result="❌ Something went wrong while searching.",
            topic=question
        )


if __name__ == "__main__":
    app.run(debug=True)