from t0d0d0d0.coreback.models.authcode import AuthcodeModel
from t0d0d0d0.coreback.repos.defaults.redis import RedisDefaultRepo


class AuthcodeRepo(RedisDefaultRepo[AuthcodeModel]):
    model = AuthcodeModel
    reponame = 'authcode'
