from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def create_map():
    return render_template('YOUR HTML FILE NAME')


if __name__ == "__main__":
    app.run()
