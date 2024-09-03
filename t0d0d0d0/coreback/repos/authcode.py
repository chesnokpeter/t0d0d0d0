from t0d0d0d0.coreback.repos.defaults.redis import RedisDefaultRepo
from t0d0d0d0.coreback.models.authcode import AuthcodeModel

class AuthcodeRepo(RedisDefaultRepo[AuthcodeModel]):
    model = AuthcodeModel
    reponame = 'authcode'