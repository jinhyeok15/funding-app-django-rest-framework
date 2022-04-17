import configparser
import jwt

filename = "funding/conf.ini"

config = configparser.ConfigParser()
config.read(filename)

def get_conf(env):
    token = config.get(env, "TOKEN")
    secret = config.get(env, "SECRET")
    return jwt.decode(
        token, secret,
        algorithms=['HS256']
    )


if __name__=="__main__":
    print(get_conf("DEV"))
