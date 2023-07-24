# -*- coding : utf-8 -*-
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from package.name import create_app


app = create_app()


if __name__ == '__main__':
    mounts = None if app.config.get("APPLICATION_ROOT", "/") == "/" else {app.config.get("APPLICATION_ROOT", "/"): app}
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, mounts=mounts)
    app.run(
        host=app.config.get("APP_HOST", None),
        port=app.config.get("APP_PORT", None),
        threaded=app.config.get("APP_THREAD", None),
        processes=app.config.get("APP_PROCESS", None),
        use_reloader=True
    )
