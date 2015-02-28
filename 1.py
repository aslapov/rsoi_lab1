import requests
from flask import Flask, request
app = Flask(__name__)


class AppData:
    key = "qevs11vu5t1eg6mhm7laq38jep"
    secret = "j5lfm3po41gb00jqa2i4gpl6ra"
    Website = "http://127.0.0.1:5000/"
    redirect_for_login = "http://127.0.0.1:5000/callback"
    redirect_for_logout = "http://127.0.0.1:5000/logout"
    redirect_for_get_userdata = "http://127.0.0.1:5000/get_userdata"
    authcode = "authorization_code"
    access_token = ""


def get_aut_request():
    return "https://secure.meetup.com/oauth2/authorize?client_id={0}" \
           "&response_type=code&redirect_uri={1}".format(AppData.key, AppData.redirect_for_login)


@app.route("/")
def homepage():
    url = '<a href={0}>Click for login</a><br>' \
          '<a href={1}>My profile</a><br>' \
          '<a href={2}>Click for logout</a>'.format(get_aut_request(),
                                                    AppData.redirect_for_get_userdata,
                                                    AppData.redirect_for_logout)
    return url


@app.route("/callback")
def callback():
    if not AppData.access_token:
        error = request.args.get('error', '')
        if error:
            return "Error: " + error
        code = request.args.get('code')
        print("Code value: ",code)
        AppData.access_token = get_token(code)
        return "Authorization is completed"
    return "You authorized already"


@app.route("/get_userdata")
def get_userdata():
    if AppData.access_token:
        headers = {"Authorization" : "Bearer " + AppData.access_token}
        response_json = requests.get("https://api.meetup.com/2/member/self/", headers=headers).json()
        print("response_json = ", response_json)
        if "errors" in response_json:
            return response_json["message"]
        return ("User data:<br><br>username: " + response_json["name"] +
            "<br>city:" + response_json["city"] +
            "<br>country:" + response_json["country"])
    return "You are not authorized yet"


@app.route("/logout")
def logout():
    if AppData.access_token:
        post_data = {"access_token": AppData.access_token}
        requests.post("https://secure.meetup.com/oauth2/deauthorize", data=post_data)
        AppData.access_token = ""
        return "Goodbye"
    return "Error: you not authorized yet"


def get_token(code):
    post_data = {"client_id": AppData.key,
                 "client_secret": AppData.secret,
                 "grant_type": AppData.authcode,
                 "redirect_uri": AppData.redirect_for_login,
                 "code": code}
    response = requests.post("https://secure.meetup.com/oauth2/access", data=post_data)
    print("status", response.status_code)
    token_json = response.json()
    print("Token JSON = ",token_json)
    token = token_json["access_token"] if "access_token" in token_json.keys() else ""
    print("token = ",token)
    return token


if __name__ == "__main__":
    app.run(debug=True, port=5000)