from bottle import post, request # o route
@post('/login') # o @route('/login', method='POST')
def do_login():

    try:
        data = request.json()
    except:
        raise ValueError
    if data is None:
        raise ValueError
    
    username = data['username']
    password = data['password']
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"