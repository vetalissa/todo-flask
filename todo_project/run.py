from apps.app import create_app

flask_app = create_app()

if '__main__' == __name__:
    flask_app.run(debug=True)
