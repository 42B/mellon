from zope import component
from zope import interface
from . import IAuthenticationProvider
from .. import IFlaskRequest
from flask import request
from flask_restless import ProcessingException
from . import exc

def api_authentication_preprocessor(*args, **kwargs):
    if not IFlaskRequest.providedBy(request):
        interface.alsoProvides(request, IFlaskRequest)
    try:
        auth_enabled = False
        for provider in component.subscribers([request], IAuthenticationProvider):
            auth_enabled = True
            provider()
            return # if it makes it here, then auth was ok
    except exc.MellonAPIAuthenticationException:
        pass
    if auth_enabled:
        raise ProcessingException(description='Not Authorized', code=401)

@interface.implementer(IAuthenticationProvider)
@component.adapter(IFlaskRequest)
class BasicAuth(object):
    def __init__(self, context):
        self.context = context
    
    def __call__(self):
        raise exc.MellonAPIAuthenticationException()