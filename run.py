from sys import argv

from app import app

if __name__ == '__main__':
    if "dev" in argv:
        app.run(host='0.0.0.0', threaded=True, debug=True)
    else:
        app.run(host='0.0.0.0', threaded=True)
