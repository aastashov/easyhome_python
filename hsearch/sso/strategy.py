from django.contrib.auth.models import User
from social_django.strategy import DjangoStrategy

from hsearch.hsearch.models import Chat


class SSOStrategy(DjangoStrategy):
    def create_user(self, *args, **kwargs) -> User:
        chat_id = kwargs.pop("uid", "")
        title = kwargs.pop("fullname", "")

        user: User = self.storage.user.create_user(*args, **kwargs)
        chat = user.chat
        if not chat.chat_id:
            exist_chat = Chat.objects.filter(chat_id=chat_id).first()
            if exist_chat:
                chat.delete()
                chat = exist_chat
            chat.user = user

        chat.username = kwargs["username"]
        chat.chat_id = chat_id
        chat.title = title
        chat.save(update_fields=["user", "username", "chat_id", "title"])
        return user
