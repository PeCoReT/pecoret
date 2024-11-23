import cvss
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.api.serializers.cvss_calculator import (
    CVSS4CalculatorSerializer, CVSS4CalculatedSerializer,
    CVSS31CalculatorSerializer, CVSS31CalculatedSerializer
)
from backend.api.serializers.render import RenderMarkdownSerializer
from backend.api.serializers.report_template import ReportTemplateSerializer
from backend.models.finding import Severity
from backend.utils import cvss4


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
        serializer = RenderMarkdownSerializer(data=request.data, context={'request': request})
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
