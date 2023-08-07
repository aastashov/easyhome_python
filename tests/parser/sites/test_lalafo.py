from collections.abc import Callable

from bs4 import BeautifulSoup

from hsearch.hsearch.models import Currency, Site
from hsearch.parser.entity import ApartmentEntity
from hsearch.parser.sites.lalafo import Lalafo


def test_get_announcement_pages_map(parser_datasets: Callable[[str], BeautifulSoup]) -> None:
    parsed_first_page = parser_datasets("lalafo_first_page.html")

    lalafo_site = Lalafo()
    announcement_map = lalafo_site.get_announcement_pages_map(parsed_first_page)
    assert announcement_map == {
        44023237: "https://lalafo.kg/bishkek/ads/sdaetsa-kvartira-70-kv-m-id-44023237",
        47192310: "https://lalafo.kg/bishkek/ads/sdaetsa-3-komnatnaa-kvartira-v-centre-goroda-semejnym-id-47192310",
        47649283: "https://lalafo.kg/bishkek/ads/dolgosrocnaa-arenda-kvartir-id-47649283",
        49106708: "https://lalafo.kg/bishkek/ads/sdau-dvuhkomnatnuu-kvartiru-studiu-62-id-49106708",
        50933880: "https://lalafo.kg/dzhalal-abad/ads/sdaetsa-2kom-studia-kvartira-zalal-abad-mik-sputnik-id-50933880",
        57876429: "https://lalafo.kg/bishkek/ads/2-komnaty-s-mebelu-polnostu-id-57876429",
        59239634: "https://lalafo.kg/bishkek/ads/1-komnata-s-mebelu-polnostu-id-59239634",
        70362318: "https://lalafo.kg/bishkek/ads/sdau-2kv-73m-na-dlitelnyj-srok-rajon-alamedin-1-bez-mebeli-id-70362318",
        70702084: "https://lalafo.kg/bishkek/ads/vremanka-id-70702084",
        78570346: "https://lalafo.kg/bishkek/ads/2-komnaty-s-mebelu-polnostu-id-78570346",
        80121087: "https://lalafo.kg/bishkek/ads/sdau-odna-komnatnuu-kvartiru-rajon-id-80121087",
        80141384: "https://lalafo.kg/bishkek/ads/1000-melocejkarpinka-1-komnata-s-mebelu-polnostu-cena16000-id-80141384",
        80974934: "https://lalafo.kg/bishkek/ads/srocno-sdau-v-arendu-3k-studiu-ili-ze-id-80974934",
        81513603: "https://lalafo.kg/bishkek/ads/toktogula-manasa-admiral-id-81513603",
        82820855: "https://lalafo.kg/bishkek/ads/gbiskek-9mkr-dom-3-kv-26-3-etaz-id-82820855",
        83804195: "https://lalafo.kg/bishkek/ads/4-komnaty-s-mebelu-polnostu-id-83804195",
        83813398: "https://lalafo.kg/bishkek/ads/citaem-vnimatelno-id-83813398",
        84788449: "https://lalafo.kg/bishkek/ads/sdau-2-kv-v-otlicnom-rajone-id-84788449",
        85005459: "https://lalafo.kg/bishkek/ads/sdau-v-3-komnatnoj-kvartire-kojka-id-85005459",
        85799536: "https://lalafo.kg/baktuu-dolonotu/ads/1-komnata-s-mebelu-casticno-id-85799536",
        86447641: "https://lalafo.kg/bishkek/ads/citat-vnimatelno-id-86447641",
        86817346: "https://lalafo.kg/karakol/ads/sdaetsa-2-3komkvartira-so-vsemi-id-86817346",
        87680475: "https://lalafo.kg/bishkek/ads/sdau-v-arendu-2h-komkv-id-87680475",
        87871473: "https://lalafo.kg/bishkek/ads/1-komnata-s-mebelu-polnostu-id-87871473",
        88257715: "https://lalafo.kg/bishkek/ads/sdaetsa-svetlaa-3h-komnatnaa-kvartira-id-88257715",
        88842208: "https://lalafo.kg/bishkek/ads/2-bedroom-fully-furnished-id-88842208",
        89533456: "https://lalafo.kg/bishkek/ads/1-komnata-s-mebelu-polnostu-id-89533456",
        90252119: "https://lalafo.kg/bishkek/ads/1-komnata-s-mebelu-polnostu-id-90252119",
        93187043: "https://lalafo.kg/bishkek/ads/kok-zar-1-komnata-s-mebelu-polnostu-cena16000-id-93187043",
        93384997: "https://lalafo.kg/bishkek/ads/sdau-2h-komnatnuu-kvartiru-v-rajone-id-93384997",
        93515824: "https://lalafo.kg/bishkek/ads/sdaetsa-1-komnatnaa-kvartira-id-93515824",
        96077754: "https://lalafo.kg/bishkek/ads/dolgosrocnaa-arenda-kvartir-id-96077754",
        96121788: "https://lalafo.kg/bishkek/ads/dolgosrocnaa-arenda-kvartir-id-96121788",
        96889293: "https://lalafo.kg/bishkek/ads/sdau-s-iula-bez-posrednikov-3-id-96889293",
        100793215: "https://lalafo.kg/bishkek/ads/dolgosrocnaa-arenda-kvartir-id-100793215",
        101307625: "https://lalafo.kg/bishkek/ads/6-komnat-i-bolee-s-mebelu-polnostu-id-101307625",
        101685613: "https://lalafo.kg/bishkek/ads/dolgosrocnaa-arenda-kvartir-id-101685613",
        102050600: "https://lalafo.kg/bishkek/ads/rabocij-gorodok-id-102050600",
        104959183: "https://lalafo.kg/bishkek/ads/sdaetsa-v-arendu-absolutno-novaa-3-h-id-104959183",
        106360434: "https://lalafo.kg/bishkek/ads/dolgosrocnaa-arenda-kvartir-id-106360434",
        106479876: "https://lalafo.kg/bishkek/ads/sdaetsa-komnata-id-106479876",
        107487422: "https://lalafo.kg/bishkek/ads/sdaetsa-2h-komnatnaa-kvartira-60m2-id-107487422",
        107495362: "https://lalafo.kg/bishkek/ads/1-komnata-s-mebelu-polnostu-id-107495362",
    }


def test_parse_apartment(parser_datasets: Callable[[str], BeautifulSoup]) -> None:
    parsed_apartment = parser_datasets("lalafo_107495362.html")

    lalafo_site = Lalafo()
    apartment = lalafo_site.parse_apartment(parsed_apartment)
    assert apartment == ApartmentEntity(
        external_id=107495362,
        site=Site.lalafo,
        external_url="https://lalafo.kg/bishkek/ads/1-komnata-s-mebelu-polnostu-id-107495362",
        title="1 комната, С мебелью полностью",
        price=39990,
        currency=Currency.kgs,
        phone="+996708262262",
        rooms=1,
        floor=4,
        max_floor=4,
        district="8 мкр",
        city="Бишкек",
        body=(
            "Сдаю квартиру с новой мебелью и техникой. В районе с "
            "более свежим воздухом и отличной инфраструктурой. С "
            "отличным видом из окна в даль на зелень, а не окна в "
            "окна. Окна на запад.\n"
            "\n"
            "Новый удобный диван, отдельно кровать с подъемным "
            "механизмом, большой холодильник, кондиционер, высокие "
            "потолки, новая стенка, стеллаж и т.д. Микроволновая печь "
            "есть, тв поставлю, если нужно (55 дюймов с гугл тв, "
            "быстрым управлением и хорошей матрицей)\n"
            "\n"
            "Этаж 4, последний, на верху только мансарда.\n"
            "Все тихие. Лифта нет, так как дом малоэтажный.\n"
            "\n"
            "Рядом кафе, большой гипермаркет Глобус 27/7, Ортосайский "
            "рынок где много овощей и фруктов, хорошая столовая."
        ),
        images_list=[
            "https://img5.lalafo.com/i/posters/original/24/05/3e/3b70b9180f70e17a99da3443e9.jpeg",
            "https://img5.lalafo.com/i/posters/original/25/43/85/8678865025320c3b9d0803a23d.jpeg",
            "https://img5.lalafo.com/i/posters/original/32/bc/b0/4eedcf8bc805ec2598d7cea714.jpeg",
            "https://img5.lalafo.com/i/posters/original/45/10/81/71e4ef074d37622e2303d1a737.jpeg",
            "https://img5.lalafo.com/i/posters/original/89/c1/27/cf17f8b5dfeb67020142a1d993.jpeg",
        ],
        lat=42.8746212,
        lon=74.5697617,
    )
