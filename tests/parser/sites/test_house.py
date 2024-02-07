from collections.abc import Callable  # noqa: I002

from bs4 import BeautifulSoup

from easyhome.easyhome.models import Currency, Site
from easyhome.parser.entity import ApartmentEntity
from easyhome.parser.sites.house import House


def test_get_announcement_pages_map(parser_datasets: Callable[[str], BeautifulSoup]) -> None:
    parsed_first_page = parser_datasets("house_first_page.html")

    announcement_map = House().get_announcement_pages_map(parsed_first_page)
    assert announcement_map == {
        "143143565ae557fecb240-08753936": "https://www.house.kg/details/143143565ae557fecb240-08753936",
        "652750265a608b3c761f0-19990394": "https://www.house.kg/details/652750265a608b3c761f0-19990394",
        "57757265ab61a313ac85-24950498": "https://www.house.kg/details/57757265ab61a313ac85-24950498",
        "854874464e1b86a8bff79-27497024": "https://www.house.kg/details/854874464e1b86a8bff79-27497024",
        "336702665ae568e1e3b52-48081225": "https://www.house.kg/details/336702665ae568e1e3b52-48081225",
        "268655765ae41e0458b57-51099695": "https://www.house.kg/details/268655765ae41e0458b57-51099695",
        "639603565c34f27cda315-56925605": "https://www.house.kg/details/639603565c34f27cda315-56925605",
        "496026565bd138b6b5fc7-83600641": "https://www.house.kg/details/496026565bd138b6b5fc7-83600641",
        "784360465c360fdf3b889-93143449": "https://www.house.kg/details/784360465c360fdf3b889-93143449",
        "764795365ae547e5ff438-95609793": "https://www.house.kg/details/764795365ae547e5ff438-95609793",
    }


def test_parse_apartment(parser_datasets: Callable[[str], BeautifulSoup]) -> None:
    parsed_apartment = parser_datasets("house_08753936.html")

    apartment = House().parse_apartment(parsed_apartment)
    assert apartment == ApartmentEntity(
        external_id="143143565ae557fecb240-08753936",
        site=Site.house,
        external_url="https://www.house.kg/details/143143565ae557fecb240-08753936",
        title="1-комн. кв., 52 м2",
        price=900,
        currency=Currency.usd,
        phone="996556454354",
        rooms=1,
        city="Бишкек",
        body=(
            'Сдается 1-комнатная квартира ПОМЕСЯЧНО в районе '
            'Филармонии \n'
            '\n'
            'В шаговой доступности находятся площадь Ала-Тоо, парк '
            'им. Панфилова, белый дом, дом правительства, тц '
            '"caravan", тц "бишкек парк", кинотеатр "россия", стадион '
            'им. Долона омурзакова, Филармония , ТЦ Алма, ТЦ IMALL и '
            'много другое.\n'
            '\n'
            'В квартире есть все необходимое :\n'
            '-бытовая техника\n'
            '-мебель\n'
            '-высокоскоростной интернет wi-fi\n'
            '-кабельное телевидение\n'
            '-кондиционер\n'
            '- холодильник \n'
            '- микроволновая печь \n'
            '- постельные принадлежности и др. \n'
            '\n'
            'Ничего не надо покупать!\n'
            'Заходи и живи !\n'
            '\n'
            'Просьба агентством недвижимости не беспокоить!\n'
            '\n'
            'Цена 900$ + депозит \n'
            'Коммунальные услуги входит в стоимость(ТСЖ,газ, вода, '
            'отопление, электричество и интернет)'
        ),
        images_list=[
            "https://cdn.house.kg/house/images/1/5/9/159694016f3f4f1f6347f11e144dbcff_640x480.jpg",
            "https://cdn.house.kg/house/images/7/4/b/74bfe5c08f1d2099ba0a1aaafe44dc59_640x480.jpg",
            "https://cdn.house.kg/house/images/9/0/a/90a73fda83bb0a9802c895563b1f86f8_640x480.jpg",
            "https://cdn.house.kg/house/images/c/8/a/c8a6251134edc2eebdcd7381c0d4aa4d_640x480.jpg",
            "https://cdn.house.kg/house/images/3/1/1/3116540c8ea0f2f594d21914ee53f2e0_640x480.jpg",
            "https://cdn.house.kg/house/images/0/7/c/07c3fcca18f2932e2d51f48119b000cb_640x480.jpg",
            "https://cdn.house.kg/house/images/1/3/7/13753c8e4112676f27a60bef9c5338da_640x480.jpg",
            "https://cdn.house.kg/house/images/5/6/1/561c92884d3d2f6703eb3a24035d0813_640x480.jpg",
            "https://cdn.house.kg/house/images/f/e/0/fe0e295520dcaccf58a62a04928cacd0_640x480.jpg",
            "https://cdn.house.kg/house/images/d/8/b/d8bd98567fc26e093b815666f4142318_640x480.jpg",
            "https://cdn.house.kg/house/images/6/d/a/6da761ba521cb90b5e52d5105e733f63_640x480.jpg",
            "https://cdn.house.kg/house/images/f/0/5/f05157b98eba191aa9dca74a64f7144a_640x480.jpg",
        ],
        room_type="",
        floor=7,
        max_floor=10,
        district="Академия Наук",
        area=52,
        lat=42.8802,
        lon=74.5807,
        is_deleted=False,
    )
