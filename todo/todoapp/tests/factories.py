import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):

    class Meta:
        model = get_user_model()

    email = factory.Sequence(lambda n: f"user-{n}@example.com")
    username = factory.Sequence(lambda n: f'username-{n}')
    password = factory.PostGenerationMethodCall('set_password',
                                                'fake-password')

    @classmethod
    def _created(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""

        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)
