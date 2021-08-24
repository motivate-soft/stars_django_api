import json
from smtplib import SMTPException

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status, exceptions
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.template import loader
from django.core.mail import send_mail, EmailMultiAlternatives
from .serializers import UserSerializer
from django_api.settings.base import DEFAULT_EMAIL_To

# not working for custom setting variables // imports django settings, not app's setting
# from django.conf import settings


CustomUser = get_user_model()

PENDING = 'P'
APPROVED = 'A'
BLOCKED = 'B'
STATUS_CHOICES = (
    ('Pending', PENDING),
    ('APPROVED', APPROVED),
    ('BLOCKED', BLOCKED),
)


class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


# user create api not permissions to all
class CustomUserCreate(APIView):
    def post(self, request):
        if request.user.role != 'S':
            raise exceptions.AuthenticationFailed(
                'You are not allowed to perform this action',
                'authorization_failed',
            )
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        if request.user.role != 'S':
            raise exceptions.AuthenticationFailed(
                'You are not allowed to perform this action',
                'authorization_failed',
            )
        # status_dic = dict(STATUS_CHOICES)
        # request.data['status'] = status_dic[request.data['status']]
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if request.user.role != 'S':
            raise exceptions.AuthenticationFailed(
                'You are not allowed to perform this action',
                'authorization_failed',
            )
        # status_dic = dict(STATUS_CHOICES)
        # request.data['status'] = status_dic[request.data['status']]
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # if request.user.role != 'S':
        #     raise exceptions.AuthenticationFailed(
        #         'You are not allowed to perform this action',
        #         'authorization_failed',
        #     )
        return self.destroy(request, *args, **kwargs)


@csrf_exempt
@require_http_methods(["POST"])
def send_contact_email(request):
    data = json.loads(request.body)
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]
    message = data["message"]
    try:
        send_mail("%s %s" % (first_name, last_name), message, email, [DEFAULT_EMAIL_To])
        return JsonResponse({'status': 'ok'})
    except SMTPException as e:
        return JsonResponse({'error': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def send_apply_email(request):
    data = json.loads(request.body)
    subject = 'Application email'
    body = loader.render_to_string('email/application_email.txt', data)
    email_message = EmailMultiAlternatives(subject, body, data['email'], [DEFAULT_EMAIL_To])
    try:
        email_message.send()
        return JsonResponse({'status': 'ok'})
    except SMTPException as e:
        return JsonResponse({'error': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#
# def send_mail(self, subject_template_name, email_template_name,
#               context, from_email, to_email, html_email_template_name=None):
#     subject = loader.render_to_string(subject_template_name, context)
#     # Email subject *must not* contain newlines
#     subject = ''.join(subject.splitlines())
#     body = loader.render_to_string(email_template_name, context)
#
#     email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
#     if html_email_template_name is not None:
#         html_email = loader.render_to_string(html_email_template_name, context)
#         email_message.attach_alternative(html_email, 'text/html')
#
#     email_message.send()
