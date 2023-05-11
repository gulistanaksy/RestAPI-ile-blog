from rest_framework.throttling import SimpleRateThrottle, UserRateThrottle


# SimpleRateThrottle -- kulllanıcı giriş yaptıysa sorun yok. yapmadıysa kısıtla.
class RegisterThrottle(SimpleRateThrottle):
    scope = 'registerthrottle'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated or request.method == 'GET':  # kullanıcı  giriş yapmamışsa veya get isteği yapılmışsa önemseme
            return None  # Only throttle unauthenticated requests.

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }

# AnonRateThrottle   -- kullanıcı giriş yapmışsa sıkıntı yok. yapmadıysa IP'sini alır.


# UserRateThrottle -- kullanıcı girişi yapan veya yapmayan kişileri kısıtlar.
#class RegisterThrottle(UserRateThrottle):
#    scope = 'registerthrottle'


