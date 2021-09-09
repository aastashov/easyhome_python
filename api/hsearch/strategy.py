from django.contrib.auth.models import User
from social_django.strategy import DjangoStrategy


class SSOStrategy(DjangoStrategy):
    def create_user(self, *args, **kwargs):
        chat_id = kwargs.pop("uid", "")
        title = kwargs.pop("fullname", "")

        user = self.storage.user.create_user(*args, **kwargs)  # type: User
        user.chat.username = kwargs["username"]
        user.chat.chat_id = chat_id
        user.chat.title = title
        user.chat.save(update_fields=["username", "chat_id", "title"])
        return user
