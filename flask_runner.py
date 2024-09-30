import van_flask.app as grow_flask


app = grow_flask.createApp()
app.run(host='0.0.0.0', port=80, debug=True)
