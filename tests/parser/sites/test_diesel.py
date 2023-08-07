from collections.abc import Callable

from bs4 import BeautifulSoup

from hsearch.hsearch.models import Currency, Site
from hsearch.parser.entity import ApartmentEntity
from hsearch.parser.sites.diesel import Diesel


def test_get_announcement_pages_map(parser_datasets: Callable[[str], BeautifulSoup]) -> None:
    parsed_first_page = parser_datasets("diesel_first_page.html")

    diesel_site = Diesel()
    announcement_map = diesel_site.get_announcement_pages_map(parsed_first_page)
    assert announcement_map == {
        240572895: "https://diesel.elcat.kg/index.php?showtopic=240572895",
        292456984: "https://diesel.elcat.kg/index.php?showtopic=292456984",
        292507681: "https://diesel.elcat.kg/index.php?showtopic=292507681",
        292507687: "https://diesel.elcat.kg/index.php?showtopic=292507687",
        293062641: "https://diesel.elcat.kg/index.php?showtopic=293062641",
        293089164: "https://diesel.elcat.kg/index.php?showtopic=293089164",
        293100958: "https://diesel.elcat.kg/index.php?showtopic=293100958",
        293129136: "https://diesel.elcat.kg/index.php?showtopic=293129136",
        293129317: "https://diesel.elcat.kg/index.php?showtopic=293129317",
        293129481: "https://diesel.elcat.kg/index.php?showtopic=293129481",
        293140886: "https://diesel.elcat.kg/index.php?showtopic=293140886",
        293163352: "https://diesel.elcat.kg/index.php?showtopic=293163352",
        293163975: "https://diesel.elcat.kg/index.php?showtopic=293163975",
        293164134: "https://diesel.elcat.kg/index.php?showtopic=293164134",
        293164247: "https://diesel.elcat.kg/index.php?showtopic=293164247",
        293165978: "https://diesel.elcat.kg/index.php?showtopic=293165978",
        293166229: "https://diesel.elcat.kg/index.php?showtopic=293166229",
        293166810: "https://diesel.elcat.kg/index.php?showtopic=293166810",
        293167491: "https://diesel.elcat.kg/index.php?showtopic=293167491",
        293167502: "https://diesel.elcat.kg/index.php?showtopic=293167502",
        293167736: "https://diesel.elcat.kg/index.php?showtopic=293167736",
        293167738: "https://diesel.elcat.kg/index.php?showtopic=293167738",
        293168003: "https://diesel.elcat.kg/index.php?showtopic=293168003",
        293168127: "https://diesel.elcat.kg/index.php?showtopic=293168127",
        293168161: "https://diesel.elcat.kg/index.php?showtopic=293168161",
        293168221: "https://diesel.elcat.kg/index.php?showtopic=293168221",
        293168435: "https://diesel.elcat.kg/index.php?showtopic=293168435",
        293168580: "https://diesel.elcat.kg/index.php?showtopic=293168580",
        293168645: "https://diesel.elcat.kg/index.php?showtopic=293168645",
        293168685: "https://diesel.elcat.kg/index.php?showtopic=293168685",
        293168825: "https://diesel.elcat.kg/index.php?showtopic=293168825",
        293168843: "https://diesel.elcat.kg/index.php?showtopic=293168843",
        293168854: "https://diesel.elcat.kg/index.php?showtopic=293168854",
        293168860: "https://diesel.elcat.kg/index.php?showtopic=293168860",
        293168869: "https://diesel.elcat.kg/index.php?showtopic=293168869",
        293168882: "https://diesel.elcat.kg/index.php?showtopic=293168882",
        293168888: "https://diesel.elcat.kg/index.php?showtopic=293168888",
        293168890: "https://diesel.elcat.kg/index.php?showtopic=293168890",
        293168895: "https://diesel.elcat.kg/index.php?showtopic=293168895",
    }


def test_parse_apartment(parser_datasets: Callable[[str], BeautifulSoup]) -> None:
    parsed_apartment = parser_datasets("diesel_293167502.html")

    diesel_site = Diesel()
    apartment = diesel_site.parse_apartment(parsed_apartment)
    assert apartment == ApartmentEntity(
        external_id=293168645,
        site=Site.diesel,
        external_url="https://diesel.elcat.kg/index.php?showtopic=293168645",
        title="Сдаю на длительный срок 2 комнатную квартиру район старого аэропорта",
        price=40000,
        currency=Currency.kgs,
        phone="+996501221262",
        rooms=2,
        city="Бишкек",
        body=(
            "Сдаю на длительный срок 2 комнатную квартиру район "
            "старого аэропорта, рядом Детской больницы Джал \n"
            "Кирпичный дом 4/5 без лифта и газа\n"
            "Квартира уютная 63 кв.м с мебелью и бытовыми техниками "
            "(спальная, кух . гарнитур, телевизор, стиральная машина "
            "холодильник,кондиционер, эл.плита и т.д.\n"
            "Есть отдельный навес для парковки легковой автомашины\n"
            "40000 сом вместе с комун. услугами \n"
            "Депозит 10000 сом\n"
            "0501221262"
        ),
        images_list=[
            "https://diesel.elcat.kg/uploads/monthly_08_2023/post-201843-0-99134500-1691318874_thumb.jpeg",
            "https://diesel.elcat.kg/uploads/monthly_08_2023/post-201843-0-40477100-1691318892_thumb.jpeg",
            "https://diesel.elcat.kg/uploads/monthly_08_2023/post-201843-0-82806400-1691318907_thumb.jpeg",
            "https://diesel.elcat.kg/uploads/monthly_08_2023/post-201843-0-98532200-1691318919_thumb.jpeg",
            "https://diesel.elcat.kg/uploads/monthly_08_2023/post-201843-0-08959200-1691318932_thumb.jpeg",
            "https://diesel.elcat.kg/uploads/monthly_08_2023/post-201843-0-63831000-1691318952_thumb.jpeg",
            "https://diesel.elcat.kg/uploads/monthly_08_2023/post-201843-0-13174500-1691318967_thumb.jpeg",
            "https://diesel.elcat.kg/uploads/monthly_08_2023/post-201843-0-42414900-1691318982_thumb.jpeg",
            "https://diesel.elcat.kg/uploads/monthly_08_2023/post-201843-0-29617100-1691319017_thumb.jpeg",
        ],
        room_type="квартира",
        area=63,
    )
