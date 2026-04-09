from flask import Flask, render_template, request, redirect, url_for
from db import init_db, save_reply, get_all_replies
from ai_helper import generate_email_reply, improve_email_reply

app = Flask(__name__)

init_db()


@app.route("/")
def home():
    return render_template("index.html", generated_reply=None)



@app.route("/generate", methods=["POST"])
def generate():
    try:
        original_email = request.form.get("original_email", "").strip()
        tone = request.form.get("tone", "formal")
        reply_length = request.form.get("reply_length", "short")

        if not original_email:
            return render_template(
                "index.html",
                generated_reply=None,
                error="Please enter an email first."
            )

        generated_reply = generate_email_reply(original_email, tone, reply_length)

        return render_template(
            "index.html",
            original_email=original_email,
            tone=tone,
            reply_length=reply_length,
            generated_reply=generated_reply
        )
    except Exception as e:
        print("Generate route error:", str(e))
        return render_template(
            "index.html",
            generated_reply=None,
            error="Something went wrong while generating the reply."
        )


@app.route("/save", methods=["POST"])
def save():
    original_email = request.form.get("original_email", "").strip()
    tone = request.form.get("tone", "formal")
    reply_length = request.form.get("reply_length", "short")
    generated_reply = request.form.get("generated_reply", "").strip()

    if original_email and generated_reply:
        save_reply(original_email, tone, reply_length, generated_reply)

    return redirect(url_for("history"))



@app.route("/improve", methods=["POST"])
def improve():
    try:
        original_email = request.form.get("original_email", "").strip()
        tone = request.form.get("tone", "formal")
        reply_length = request.form.get("reply_length", "short")
        generated_reply = request.form.get("generated_reply", "").strip()

        improved_reply = improve_email_reply(generated_reply)

        return render_template(
            "index.html",
            original_email=original_email,
            tone=tone,
            reply_length=reply_length,
            generated_reply=improved_reply
        )
    except Exception as e:
        print("Improve route error:", str(e))
        return render_template(
            "index.html",
            generated_reply=None,
            error="Something went wrong while improving the reply."
        )


@app.route("/history")
def history():
    replies = get_all_replies()
    return render_template("history.html", replies=replies)


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)