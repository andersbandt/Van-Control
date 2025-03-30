
# import needed modules
import vf.app as grow_flask

# get app
app = grow_flask.createApp()
app.run(host='0.0.0.0', port=80, debug=True)
