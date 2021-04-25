import flask

app = flask.Flask('__name__')
data = {"fruit": "bannana"}

@app.route('/')
def serve_home():
    return flask.render_template('pages/index.html', title="home")

# @app.route('/<path:path>')
# def get_page(path):
#     if path in ['results', 'sponsors']:
#         return flask.render_template(path)
#     elif path == 'blog':
#         return "blog!"
#     else:
#         return flask.render_template('base/404.html'), 404

@app.route('/articles/')
def serve_articles():
    return flask.render_template('articles/index.html')

@app.route('/sponsors/')
def serve_sponsors():
    pass

@app.route('/results/')
def serve_results():
    pass

if __name__ == '__main__':
    app.run(debug=True)
