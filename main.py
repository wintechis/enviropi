from flask import Flask
from routing import overview, get_file, get_table
from poll import DataPoll

def create_app() -> Flask:
    app = Flask(__name__)

    # generate secret key:  $ python -c 'import secrets; print(secrets.token_hex())'
    app.secret_key = 'bbe5ab933da0be71ffe196d77527a6a30b7eb73347ca029c6a7447ae3c3ca4e6'

    # create routing rules
    app.add_url_rule('/', view_func=overview)
    app.add_url_rule('/<filename>', view_func=get_file)
    app.add_url_rule('/table/<id>', view_func=get_table)

    return app


if __name__ == '__main__':
    app = create_app()
    t = DataPoll()
    t.start()
    app.run(host='0.0.0.0', port=5000, debug=True)