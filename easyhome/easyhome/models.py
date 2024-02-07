from __future__ import annotations  # noqa: D100

from django.db import models

from unixtimestampfield.fields import UnixTimeStampField


class Chat(models.Model):  # noqa: D101
    PRIVATE = "private"
    SUPERGROUP = "supergroup"
    TYPE_CHOICES = (
        (PRIVATE, "private"),
        (SUPERGROUP, "supergroup"),
    )
    user = models.OneToOneField(to="auth.User", on_delete=models.CASCADE, null=True, related_name="chat")
    chat_id = models.BigIntegerField(default=0, blank=True)
    username = models.CharField(max_length=100, default="", blank=True)
    title = models.CharField(max_length=100, default="", blank=True)
    c_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=PRIVATE)
    created = UnixTimeStampField(auto_now=True, auto_now_add=True)
    enable = models.BooleanField(default=True)
    diesel = models.BooleanField(default=True)
    lalafo = models.BooleanField(default=True)
    house = models.BooleanField(default=True)
    photo = models.BooleanField(default=True)
    usd = models.CharField(max_length=100, default="0:0")
    kgs = models.CharField(max_length=100, default="0:0")

    def __str__(self) -> str:  # noqa: D105
        name = self.title if self.title else self.username
        return f"{name} {self.get_c_type_display()!r} (#{self.pk})"


class Image(models.Model):  # noqa: D101
    apartment = models.ForeignKey("easyhome.Apartment", on_delete=models.CASCADE, related_name="images")
    path = models.CharField(max_length=255, default="", unique=True)
    created = UnixTimeStampField(auto_now=True, auto_now_add=True)

    def __str__(self) -> str:  # noqa: D105
        return f"{self.apartment.topic} ({self.path})"

    available_fields = [  # noqa: RUF012
        "apartment_id",
        "path",
        "created",
    ]

    def to_dict(self, fields_list: list) -> dict:  # noqa: D102
        return {field: getattr(self, field, None) for field in fields_list}


class Site(models.TextChoices):  # noqa: D101
    undefined = "", "Undefined"
    diesel = "diesel", "diesel"
    lalafo = "lalafo", "lalafo"
    house = "house", "house"


class Currency(models.IntegerChoices):  # noqa: D101
    undefined = 0, "-"
    usd = 1, "USD"
    kgs = 2, "KGS"


class Apartment(models.Model):  # noqa: D101
    external_id = models.BigIntegerField()
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

    images_count = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    created = UnixTimeStampField(auto_now=True, auto_now_add=True)

    # Inner information
    # deleted_at = models.DateTimeField(  # noqa: ERA001, RUF100
    #     verbose_name="Дата удаления на сайте.",  # noqa: ERA001
    #     null=True,  # noqa: ERA001
    #     blank=True,  # noqa: ERA001
    #     help_text="Если парсер получил 404 ошибку, то мы помечаем объявление как удаленное.",  # noqa: ERA001
    # )  # noqa: ERA001, RUF100
    # viewed_at = models.DateTimeField(  # noqa: ERA001, RUF100
    #     verbose_name="Дата последнего просмотра.",  # noqa: ERA001
    #     null=True,  # noqa: ERA001
    #     blank=True,  # noqa: ERA001
    #     help_text="Дата, когда парсер в последний раз видел это объявление на сайте.",  # noqa: ERA001
    # )  # noqa: ERA001, RUF100

    def __str__(self) -> str:  # noqa: D105
        return f"{self.topic} {self.get_site_display()!r} (#{self.pk})"


class Answer(models.Model):  # noqa: D101
    chat = models.ForeignKey("easyhome.Chat", on_delete=models.CASCADE, related_name="answers")
    apartment = models.ForeignKey("easyhome.Apartment", on_delete=models.CASCADE, related_name="answers")
    dislike = models.BooleanField(default=False)
    created = UnixTimeStampField(auto_now=True, auto_now_add=True)

    def __str__(self) -> str:  # noqa: D105
        return f"{self.chat_id} => {self.apartment_id} ({self.dislike})"


class Feedback(models.Model):  # noqa: D101
    username = models.CharField(max_length=100, default="")
    chat = models.ForeignKey("easyhome.Chat", on_delete=models.CASCADE, related_name="feedbacks")
    body = models.TextField(default="")
    created = UnixTimeStampField(auto_now=True, auto_now_add=True)

    def __str__(self) -> str:  # noqa: D105
        return self.username if self.username else self.chat


class TgMessage(models.Model):  # noqa: DJ008, D101
    APARTMENT = "apartment"
    PHOTO = "photo"
    DESCRIPTION = "description"
    KIND_CHOICES = (
        (APARTMENT, "Apartment"),
        (PHOTO, "Photo"),
        (DESCRIPTION, "Description"),
    )
    created = UnixTimeStampField(auto_now=True, auto_now_add=True)
    message_id = models.IntegerField(default=0)
    apartment = models.ForeignKey("easyhome.Apartment", on_delete=models.CASCADE, related_name="messages")
    chat = models.ForeignKey("easyhome.Chat", on_delete=models.CASCADE, related_name="messages")
    kind = models.CharField(max_length=50, choices=KIND_CHOICES, default=APARTMENT)
