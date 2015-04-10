from flask import Flask, request


app = Flask(__name__)

@app.route('/sauron', methods=['POST'])
def sauron():
    print request.form
    print request.remote_addr
    print request.user_agent

    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
