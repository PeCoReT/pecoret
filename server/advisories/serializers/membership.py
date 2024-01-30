from django.contrib.auth.models import Group
from django_q.tasks import async_task
from rest_framework import serializers
from pecoret.core.serializers import ValuedChoiceField
from backend.models.advisory_membership import AdvisoryMembership, Roles
from backend.models.user import User
from backend.tasks import mail
from backend.serializers.user import MinimalUserSerializer
from backend.models.advisory import VisibilityChoices


class AdvisoryMembershipSerializer(serializers.ModelSerializer):
    role = ValuedChoiceField(choices=Roles.choices)
    user = MinimalUserSerializer()

    class Meta:
        model = AdvisoryMembership
        fields = ["pk", "role", "user", "active_until"]


class AdvisoryMembershipCreateSerializer(serializers.ModelSerializer):
    default_error_messages = {
        "not_sharable": "Advisories with this visibility setting cannot be shared!"
    }
    role = ValuedChoiceField(choices=Roles.choices)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = AdvisoryMembership
        fields = ["role", "pk", "active_until", "email"]

    def create(self, validated_data):
        email = validated_data.pop("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=self.get_unique_username_from_email(email),
                email=email, is_active=False
            )
            user.groups.add(Group.objects.get(name="Vendor"))
            user.save()
            context = {"user": user}
            async_task(mail.send_activation_mail, context, user.email)
        advisory_membership = AdvisoryMembership.objects.create(**validated_data, user=user)
        return advisory_membership

    def get_unique_username_from_email(self, email):
        while True:
            username = email.split('@')[0]
            name, idx = username, 1
            try:
                # user with current username exists, so add numeral
                User.objects.get(username=username)
                name = username + str(idx)
                idx += 1
            except User.DoesNotExist:
                username = name
                break
        return username

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if self.context["request"].advisory.visibility == VisibilityChoices.MEMBERS:
            self.fail("not_sharable")
        return validated_data
