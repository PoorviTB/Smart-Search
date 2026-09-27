from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():

    topic = request.form.get("topic", "").strip()

    if not topic:
        return render_template(
            "index.html",
            result="Please enter a topic.",
            topic=""
        )

    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + requests.utils.quote(topic)

        response = requests.get(
            url,
            headers={"User-Agent": "SmartSearch/1.0"},
            timeout=10
        )

        data = response.json()

        if response.status_code != 200:
            return render_template(
                "index.html",
                result="❌ Information not found for this topic.",
                topic=topic
            )

        title = data.get("title", topic)
        summary = data.get(
            "extract",
            "No information found for this topic."
        )

        return render_template(
            "index.html",
            result=summary,
            topic=title
        )

    except Exception as e:

        print("SEARCH ERROR:", e)

        return render_template(
            "index.html",
            result="❌ Information could not be found.",
            topic=topic
        )


if __name__ == "__main__":
    app.run(debug=True)