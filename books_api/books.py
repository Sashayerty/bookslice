from flask import Flask, send_file

app = Flask(__name__)

@app.route('/book/<string:bookname>')
def book(bookname):
    return send_file(f'books/{bookname}.txt')

def main():
    app.run(debug=True, port='8080')


if __name__ == '__main__':
    main()