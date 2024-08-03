import cvss
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models.finding import Severity
from backend.serializers.auth import (LoginSerializer, LogoutSerializer, LoginResponseSerializer)
from backend.serializers.cvss_calculator import (
    CVSS4CalculatorSerializer, CVSS4CalculatedSerializer,
    CVSS31CalculatorSerializer, CVSS31CalculatedSerializer
)
from backend.serializers.render import RenderMarkdownSerializer
from backend.serializers.report_template import ReportTemplateSerializer
from backend.utils import cvss4
from pecoret.core.auth.ldap import sync_ldap_groups
from .throttle import AuthFlowThrottle


class LoginView(APIView):
    """this view handles the login process
    similar to:
    https://github.com/django/django/blob/4.1/django/contrib/auth/views.py#L67
    """
    throttle_classes = [AuthFlowThrottle]
    authentication_classes = []

    @extend_schema(
        operation_id='Login', summary='Authenticate for SessionAuth',
        tags=['Authentication'],
        request=LoginSerializer, responses=LoginResponseSerializer)
    @method_decorator(csrf_protect)
    def post(self, request, **kwargs):
        """handle the login process.
        use a method similar to the original django auth views but using JSON.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data.get("username"),
                password=serializer.validated_data.get("password"),
            )
            if hasattr(user, 'ldap_user') and user.ldap_user.group_names:
                sync_ldap_groups(user)
            if user:
                login(request, user)
                return Response(
                    LoginResponseSerializer(
                        {"user": user, "csrf_token": request.META["CSRF_COOKIE"]}
                    ).data
                )
            return Response(
                {"detail": "Invalid username and/or password!"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [SessionAuthentication]

    @extend_schema(
        operation_id='Logout', tags=['Authentication'],
        request=LogoutSerializer, responses=LogoutSerializer)
    @method_decorator(csrf_protect)
    def post(self, request, **kwargs):
        """Handle post request and perform logout.
        Use POST to prevent CSRF.
        """
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class AuthCheckView(APIView):
    """Check if the user is logged in.
    This view provides a way for the frontend to get the CSRF_COOKIE.

    original code linked below. just add our user information here for the top bar.
    https://medium.com/swlh/django-rest-framework-and-spa-session-authentication-with-docker-and-nginx-aa64871f29cd
    """

    authentication_classes = [SessionAuthentication]

    @extend_schema(
        operation_id='Check Authentication', tags=['Authentication'],
        description='Checks if current user is logged in. Retrieve CSRF Token',
        request={}, responses=LoginResponseSerializer)
    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            user = None
        else:
            user = request.user
        # no csrf_token set yet
        if not request.META.get('CSRF_COOKIE'):
            get_token(request)
        return Response(
            LoginResponseSerializer(
                {"user": user, "csrf_token": request.META.get("CSRF_COOKIE", None)}
            ).data
        )


class CVSS4CalculatorView(APIView):
    """
    calculates the severity and score based on a CVSS4 vector string
    """

    authentication_classes = [SessionAuthentication]

    @extend_schema(
        operation_id='CVSS 4.0 Calculator', tags=['CVSS Calculator'],
        request=CVSS4CalculatorSerializer, responses=CVSS4CalculatedSerializer)
    @method_decorator(csrf_protect)
    def post(self, request, **kwargs):
        serializer = CVSS4CalculatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        score, severity = cvss4.CVSS4Calculator().from_string(serializer.validated_data['vector'])
        data = {'score': score, 'severity': Severity[severity.upper()].label}
        serializer = CVSS4CalculatedSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CVSS31CalculatorView(APIView):
    """
    calculates the severity and score based on a CVSS3.1 vector string
    """
    authentication_classes = [SessionAuthentication]

    @extend_schema(
        operation_id='CVSS 3.1 Calculator', tags=['CVSS Calculator'],
        request=CVSS31CalculatorSerializer, responses=CVSS31CalculatedSerializer)
    @method_decorator(csrf_protect)
    def post(self, request, **kwargs):
        serializer = CVSS31CalculatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        c = cvss.CVSS3(serializer.validated_data['vector'])
        score, severity = c.scores()[0], c.severities()[0]
        if severity.upper() == 'NONE':
            severity = 'Informational'
        data = {'score': score, 'severity': Severity[severity.upper()].label}
        serializer = CVSS31CalculatedSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RenderMarkdownToHTML(APIView):
    """
    renders markdown to html as it would show in the report (without using custom templates)
    """
    authentication_classes = [SessionAuthentication]

    @extend_schema(
        operation_id='Render Markdown to HTML', tags=['Helpers'],
        request=RenderMarkdownSerializer, responses=RenderMarkdownSerializer)
    @method_decorator(csrf_protect)
    def post(self, request, **kwargs):
        serializer = RenderMarkdownSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReportTemplateView(APIView):
    authentication_classes = [SessionAuthentication]

    @extend_schema(
        operation_id='Get all report templates',
        description='Retrieve a list of available report templates',
        tags=['Report Templates'],
        request=None, responses=ReportTemplateSerializer)
    def get(self, request, **kwargs):
        data = []
        for item in settings.REPORT_TEMPLATES.keys():
            data.append({'name': item})
        serializer = ReportTemplateSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)
