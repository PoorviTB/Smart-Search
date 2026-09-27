from flask import Flask, render_template, request
import wikipedia

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
            result="Please enter a topic."
        )

    try:
        # Search for the topic
        results = wikipedia.search(topic)

        if not results:
            return render_template(
                "index.html",
                result="❌ Information not found for this topic."
            )

        # Take the closest result
        best_match = results[0]

        # Get information
        summary = wikipedia.summary(
            best_match,
            sentences=5
        )

        return render_template(
            "index.html",
            result=summary,
            topic=best_match
        )

    except wikipedia.exceptions.DisambiguationError as e:

        # If there are many meanings, use the first option
        try:
            summary = wikipedia.summary(
                e.options[0],
                sentences=5
            )

            return render_template(
                "index.html",
                result=summary,
                topic=e.options[0]
            )

        except:
            return render_template(
                "index.html",
                result="❌ Please try a more specific topic."
            )

    except Exception as e:

        return render_template(
            "index.html",
            result="❌ Information could not be found."
        )


if __name__ == "__main__":
    app.run(debug=True)
    