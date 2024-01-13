db = {
    "parkings": [
        {
            "parking_id": 1,
            "parking_name": "Насос ЭЦН-109а с электродвигателем ГЭА-6А",
            "parking_adress": """Новые! Упаковки, коробки, паспорта, ярлыки консервации, хранение - сухой склад!

 6шт. цена за шт.

 За опт - скидка!""",
            "parking_places_count": 25000,
        },
        {
            "parking_id": 2,
            "parking_name": "Двигатель РУ 19-300",
            "parking_adress": """После ремонта. ППР- 0 ч.

Без формуляра. С официальным происхождением.

Турбореактивный двигатель РУ 19-300 предназначен для установки на самолете в качестве дополнительной энергоустановки.""",
            "parking_places_count": 500000,
        },
        {
            "parking_id": 3,
            "parking_name": "Кабина самолета Boeing 737",
            "parking_adress": """Подойдет для реализации проектов: авиатренажер, авиасимулятор, развлекательный аттракцион, или любой другой.

Boeing 737 — узкофюзеляжный ближне-среднемагистральный пассажирский самолёт.""",
            "parking_places_count": 1000000,
        },
        {
            "parking_id": 4,
            "parking_name": "Авиационные колёса",
            "parking_adress": "",
            "parking_places_count": 200000,
        },
    ]
}


def getParkings():
    return db["parkings"]


def getParkingById(parking_id):
    for parking in db["parkings"]:
        if parking["parking_id"] == parking_id:
            return parking


def searchParkings(parking_name):
    parkings = getParkings()

    res = []

    for parking in parkings:
        if parking_name.lower() in parking["parking_name"].lower():
            res.append(parking)

    return res
