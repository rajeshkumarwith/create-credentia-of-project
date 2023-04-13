from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

@csrf_exempt
def google_login(request):
    if request.method == 'POST':
        flow = Flow.from_client_config(
            settings.GOOGLE_OAUTH2_CLIENT_CONFIG,
            scopes=['openid', 'email', 'profile'],
            redirect_uri=request.build_absolute_uri(reverse('google-auth-callback')),
            state=request.COOKIES.get('csrftoken')
        )

        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials
        email = credentials.id_token['email']
        first_name = credentials.id_token['given_name']
        last_name = credentials.id_token['family_name']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(email, email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        token, _ = Token.objects.get_or_create(user=user)
        response = JsonResponse({'token': token.key})

        return response

class GoogleLoginCallback(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(GoogleLoginCallback, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        flow = Flow.from_client_config(
            settings.GOOGLE_OAUTH2_CLIENT_CONFIG,
            scopes=['openid', 'email', 'profile'],
            redirect_uri=request.build_absolute_uri(reverse('google-auth-callback')),
            state=request.COOKIES.get('csrftoken')
        )

        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)

        return HttpResponseRedirect('/')

class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request
