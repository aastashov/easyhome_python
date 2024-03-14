from __future__ import annotations  # noqa: D100

from django.db import models

from unixtimestampfield.fields import UnixTimeStampField


class ChatType(models.TextChoices):
    """Use this class to define the chat type choices."""

    private = "private"
    supergroup = "supergroup"


class Chat(models.Model):
    """Use this model to store the chat data."""

    chat_id = models.BigIntegerField(default=0, blank=True)
    username = models.CharField(max_length=100, default="", blank=True)
    title = models.CharField(max_length=100, default="", blank=True)
    c_type = models.CharField(max_length=20, choices=ChatType.choices, default=ChatType.private)
    created = UnixTimeStampField(auto_now=True, auto_now_add=True)
    enable = models.BooleanField(default=True)
    diesel = models.BooleanField(default=True)
    lalafo = models.BooleanField(default=True)
    house = models.BooleanField(default=True)
    photo = models.BooleanField(default=True)
    usd = models.CharField(max_length=100, default="0:0")
    kgs = models.CharField(max_length=100, default="0:0")

    user = models.OneToOneField(to="auth.User", on_delete=models.CASCADE, null=True, related_name="chat")

    def __str__(self) -> str:
        """Return the string representation of the Chat model."""
        name = self.title if self.title else self.username
        return f"{name} {self.get_c_type_display()!r} (#{self.pk})"


class Image(models.Model):
    """Use this model to store the images' data."""

    path = models.CharField(max_length=255, default="", unique=True)

    apartment = models.ForeignKey("easyhome.Apartment", on_delete=models.CASCADE, related_name="images")

    created = UnixTimeStampField(auto_now=True, auto_now_add=True)

    def __str__(self) -> str:
        """Return the string representation of the Image model."""
        return f"{self.apartment.topic} ({self.path})"


class Site(models.TextChoices):
    """Use this class to define the site choices."""

    undefined = "", "Undefined"
    diesel = "diesel", "diesel"
    lalafo = "lalafo", "lalafo"
    house = "house", "house"


class Currency(models.IntegerChoices):
    """Use this class to define the currency choices."""

    undefined = 0, "-"
    usd = 1, "USD"
    kgs = 2, "KGS"


class Apartment(models.Model):
    """Use this model to store the apartment data."""

    external_id = models.BigIntegerField()  # FIXME: Change to CharField
    url = models.CharField(max_length=255, default="")
    topic = models.CharField(max_length=255, default="")
    phone = models.CharField(max_length=255, default="", blank=True)
    rooms = models.IntegerField(default=0, blank=True)
    body = models.TextField(default="", blank=True)
    price = models.IntegerField(default=0, blank=True)
    currency = models.IntegerField(choices=Currency.choices, default=Currency.undefined)
    area = models.IntegerField(default=0, blank=True)
    city = models.CharField(max_length=100, default="", blank=True)
    room_type = models.CharField(max_length=100, default="", blank=True)
    site = models.CharField(max_length=20, choices=Site.choices, default=Site.undefined)
    floor = models.IntegerField(default=0, blank=True)
    max_floor = models.IntegerField(default=0, blank=True)
    district = models.CharField(max_length=255, default="", blank=True)
    lat = models.FloatField(default=0.0, blank=True)
    lon = models.FloatField(default=0.0, blank=True)

    images_count = models.IntegerField(default=0)  # FIXME: Redundant field
    is_deleted = models.BooleanField(default=False)  # FIXME: Change to datetime field

    created = UnixTimeStampField(auto_now=True, auto_now_add=True)  # FIXME: Rename to created_at and change to datetime

    # TODO: Need to add a field for the last update and last seen

    def __str__(self) -> str:
        """Return the string representation of the Apartment model."""
        return f"{self.topic} {self.get_site_display()!r} (#{self.pk})"


class Answer(models.Model):
    """Use this model to store the answers' data."""

    dislike = models.BooleanField(default=False)

    chat = models.ForeignKey("easyhome.Chat", on_delete=models.CASCADE, related_name="answers")
    apartment = models.ForeignKey("easyhome.Apartment", on_delete=models.CASCADE, related_name="answers")

    created = UnixTimeStampField(auto_now=True, auto_now_add=True)

    def __str__(self) -> str:
        """Return the string representation of the Answer model."""
        return f"{self.chat_id} => {self.apartment_id} ({self.dislike})"


class Feedback(models.Model):
    """Use this model to store the feedback data."""

    username = models.CharField(max_length=100, default="")
    body = models.TextField(default="")

    chat = models.ForeignKey("easyhome.Chat", on_delete=models.CASCADE, related_name="feedbacks")

    created = UnixTimeStampField(auto_now=True, auto_now_add=True)

    def __str__(self) -> str:
        """Return the string representation of the Feedback model."""
        return self.username if self.username else self.chat


class TelegramMessageKind(models.TextChoices):
    """Use this class to define the telegram message kind choices."""

    apartment = "Apartment"
    photo = "Photo"
    description = "Description"


class TgMessage(models.Model):
    """Use this model to store the telegram messages."""

    message_id = models.IntegerField(default=0)
    kind = models.CharField(max_length=50, choices=TelegramMessageKind.choices, default=TelegramMessageKind.apartment)

    apartment = models.ForeignKey("easyhome.Apartment", on_delete=models.CASCADE, related_name="messages")
    chat = models.ForeignKey("easyhome.Chat", on_delete=models.CASCADE, related_name="messages")

    created = UnixTimeStampField(auto_now=True, auto_now_add=True)

    def __str__(self) -> str:
        """Return the string representation of the TgMessage model."""
        return f"{self.message_id}"
