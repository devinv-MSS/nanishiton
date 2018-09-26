from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    result = req.get("result")
    parameters = result.get("parameters")
    weapon_name = parameters.get("KOUMOKU")
    
    print("1111")

    scope = ['https://spreadsheets.google.com/feeds']

    #ダウンロードしたjsonファイルを同じフォルダに格納して指定する
    credentials = ServiceAccountCredentials.from_json_keyfile_name('kiduki01-76c7e41e3eee.json', scope)
        print("2222")
    gc = gspread.authorize(credentials)
    print("3333")
    # # 共有設定したスプレッドシートの名前を指定する
    worksheet = gc.open("KIDUKI").get_worksheet(1)
    print("4444")
    cell = worksheet.find(weapon_name)
    print("5555")
    text = str(cell.value) +"わ、"+ str(worksheet.cell(cell.row,cell.col+1).value) + "です"
    r = make_response(jsonify({'speech':text,'displayText':text}))
    r.headers['Content-Type'] = 'application/json'
    return r

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
