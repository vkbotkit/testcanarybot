import six


from .. import objects


class api:
    __slots__ = ('http', '_method', '_string')

    def __init__(self, http, method, string = None):
        self.http = http
        self._method = method    
        self._string = string


    def __getattr__(self, method):
        self._string = self._string + "." if self._string else ""

        return api(self.http, self._method, (self._string if self._method else '') + method)

    async def __call__(self, **kwargs):
        for k, v in six.iteritems(kwargs):
            if isinstance(v, (list, tuple)):
                kwargs[k] = ','.join(str(x) for x in v)

        return await self._method(self._string, kwargs)
