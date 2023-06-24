# -*- coding : utf-8 -*-
from package.name import create_app


app = create_app()


if __name__ == '__main__':
    app.run(
        host=app.config.get("APP_HOST", None),
        port=app.config.get("APP_PORT", None)
    )

