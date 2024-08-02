# -*- coding : utf-8 -*-
from flask import Flask
from test.demo import sp


app = Flask(sp.base_package.__package__)
sp.init_app(app)


if __name__ == '__main__':
    app.run()
else:
    app.run_with_outside_server()
