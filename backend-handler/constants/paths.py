from .train_color import TrainColor

class Path:

    def __init__(self,
            id: int,
            cityOneId: int,
            cityTwoId: int,
            trainColor: TrainColor,
            length: int) -> None:
        self.id: int = id
        self.cityOneId: int = cityOneId
        self.cityTwoId: int = cityTwoId
        self.trainColor: TrainColor = trainColor
        self.length: int = length

_PATHS: list[dict] = [
    {
        "id": 0,
        "cityOneId": 33,
        "cityTwoId": 2,
        "trainColor": TrainColor.WILD,
        "length": 3
    },
    {
        "id": 1,
        "cityOneId": 33,
        "cityTwoId": 31,
        "trainColor": TrainColor.WILD,
        "length": 1
    },
    {
        "id": 2,
        "cityOneId": 33,
        "cityTwoId": 31,
        "trainColor": TrainColor.WILD,
        "length": 1
    },
    {
        "id": 3,
        "cityOneId": 31,
        "cityTwoId": 2,
        "trainColor": TrainColor.WILD,
        "length": 4
    },
    {
        "id": 4,
        "cityOneId": 31,
        "cityTwoId": 24,
        "trainColor": TrainColor.WILD,
        "length": 1
    },
    {
        "id": 5,
        "cityOneId": 31,
        "cityTwoId": 24,
        "trainColor": TrainColor.WILD,
        "length": 1
    },
    {
        "id": 6,
        "cityOneId": 24,
        "cityTwoId": 28,
        "trainColor": TrainColor.PINK,
        "length": 5
    },
    {
        "id": 7,
        "cityOneId": 24,
        "cityTwoId": 28,
        "trainColor": TrainColor.GREEN,
        "length": 5
    },
    {
        "id": 8,
        "cityOneId": 28,
        "cityTwoId": 14,
        "trainColor": TrainColor.YELLOW,
        "length": 3
    },
    {
        "id": 9,
        "cityOneId": 28,
        "cityTwoId": 14,
        "trainColor": TrainColor.PINK,
        "length": 3
    },
    {
        "id": 10,
        "cityOneId": 14,
        "cityTwoId": 22,
        "trainColor": TrainColor.WILD,
        "length": 3
    },
    {
        "id": 11,
        "cityOneId": 22,
        "cityTwoId": 8,
        "trainColor": TrainColor.WILD,
        "length": 3
    },
    {
        "id": 12,
        "cityOneId": 14,
        "cityTwoId": 8,
        "trainColor": TrainColor.BLACK,
        "length": 6
    },
    {
        "id": 13,
        "cityOneId": 28,
        "cityTwoId": 27,
        "trainColor": TrainColor.ORANGE,
        "length": 5
    },
    {
        "id": 14,
        "cityOneId": 28,
        "cityTwoId": 27,
        "trainColor": TrainColor.WHITE,
        "length": 5
    },
    {
        "id": 15,
        "cityOneId": 24,
        "cityTwoId": 27,
        "trainColor": TrainColor.BLUE,
        "length": 6
    },
    {
        "id": 16,
        "cityOneId": 14,
        "cityTwoId": 12,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 17,
        "cityOneId": 12,
        "cityTwoId": 27,
        "trainColor": TrainColor.ORANGE,
        "length": 3
    },
    {
        "id": 18,
        "cityOneId": 31,
        "cityTwoId": 9,
        "trainColor": TrainColor.YELLOW,
        "length": 6
    },
    {
        "id": 19,
        "cityOneId": 2,
        "cityTwoId": 9,
        "trainColor": TrainColor.WILD,
        "length": 4
    },
    {
        "id": 20,
        "cityOneId": 27,
        "cityTwoId": 9,
        "trainColor": TrainColor.PINK,
        "length": 3
    },
    {
        "id": 21,
        "cityOneId": 9,
        "cityTwoId": 35,
        "trainColor": TrainColor.BLUE,
        "length": 4
    },
    {
        "id": 22,
        "cityOneId": 2,
        "cityTwoId": 35,
        "trainColor": TrainColor.WHITE,
        "length": 6
    },
    {
        "id": 23,
        "cityOneId": 27,
        "cityTwoId": 6,
        "trainColor": TrainColor.RED,
        "length": 3
    },
    {
        "id": 24,
        "cityOneId": 27,
        "cityTwoId": 6,
        "trainColor": TrainColor.YELLOW,
        "length": 3
    },
    {
        "id": 25,
        "cityOneId": 22,
        "cityTwoId": 6,
        "trainColor": TrainColor.WHITE,
        "length": 5
    },
    {
        "id": 26,
        "cityOneId": 22,
        "cityTwoId": 29,
        "trainColor": TrainColor.WILD,
        "length": 3
    },
    {
        "id": 27,
        "cityOneId": 9,
        "cityTwoId": 7,
        "trainColor": TrainColor.ORANGE,
        "length": 6
    },
    {
        "id": 28,
        "cityOneId": 35,
        "cityTwoId": 7,
        "trainColor": TrainColor.BLACK,
        "length": 4
    },
    {
        "id": 29,
        "cityOneId": 7,
        "cityTwoId": 21,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 30,
        "cityOneId": 7,
        "cityTwoId": 21,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 31,
        "cityOneId": 6,
        "cityTwoId": 21,
        "trainColor": TrainColor.PINK,
        "length": 4
    },
    {
        "id": 32,
        "cityOneId": 29,
        "cityTwoId": 6,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 33,
        "cityOneId": 29,
        "cityTwoId": 8,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 34,
        "cityOneId": 21,
        "cityTwoId": 11,
        "trainColor": TrainColor.WILD,
        "length": 1
    },
    {
        "id": 35,
        "cityOneId": 21,
        "cityTwoId": 11,
        "trainColor": TrainColor.WILD,
        "length": 1
    },
    {
        "id": 36,
        "cityOneId": 6,
        "cityTwoId": 11,
        "trainColor": TrainColor.BLACK,
        "length": 4
    },
    {
        "id": 37,
        "cityOneId": 6,
        "cityTwoId": 11,
        "trainColor": TrainColor.ORANGE,
        "length": 4
    },
    {
        "id": 38,
        "cityOneId": 11,
        "cityTwoId": 20,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 39,
        "cityOneId": 11,
        "cityTwoId": 20,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 40,
        "cityOneId": 6,
        "cityTwoId": 20,
        "trainColor": TrainColor.RED,
        "length": 4
    },
    {
        "id": 41,
        "cityOneId": 8,
        "cityTwoId": 20,
        "trainColor": TrainColor.YELLOW,
        "length": 5
    },
    {
        "id": 42,
        "cityOneId": 29,
        "cityTwoId": 20,
        "trainColor": TrainColor.BLUE,
        "length": 3
    },
    {
        "id": 43,
        "cityOneId": 8,
        "cityTwoId": 10,
        "trainColor": TrainColor.GREEN,
        "length": 6
    },
    {
        "id": 44,
        "cityOneId": 20,
        "cityTwoId": 5,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 45,
        "cityOneId": 20,
        "cityTwoId": 5,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 46,
        "cityOneId": 5,
        "cityTwoId": 10,
        "trainColor": TrainColor.WILD,
        "length": 1
    },
    {
        "id": 47,
        "cityOneId": 5,
        "cityTwoId": 10,
        "trainColor": TrainColor.WILD,
        "length": 1
    },
    {
        "id": 48,
        "cityOneId": 8,
        "cityTwoId": 5,
        "trainColor": TrainColor.RED,
        "length": 4
    },
    {
        "id": 49,
        "cityOneId": 9,
        "trainColor": TrainColor.GREEN,
        "cityTwoId": 6,
        "length": 4
    },
    {
        "id": 50,
        "cityOneId": 9,
        "cityTwoId": 21,
        "trainColor": TrainColor.RED,
        "length": 5
    },
    {
        "id": 51,
        "cityOneId": 20,
        "cityTwoId": 13,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 52,
        "cityOneId": 5,
        "cityTwoId": 13,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 53,
        "cityOneId": 10,
        "cityTwoId": 18,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 54,
        "cityOneId": 18,
        "cityTwoId": 13,
        "trainColor": TrainColor.GREEN,
        "length": 3
    },
    {
        "id": 55,
        "cityOneId": 18,
        "cityTwoId": 0,
        "trainColor": TrainColor.YELLOW,
        "length": 4
    },
    {
        "id": 56,
        "cityOneId": 18,
        "cityTwoId": 0,
        "trainColor": TrainColor.ORANGE,
        "length": 4
    },
    {
        "id": 57,
        "cityOneId": 0,
        "cityTwoId": 15,
        "trainColor": TrainColor.BLUE,
        "length": 5
    },
    {
        "id": 58,
        "cityOneId": 15,
        "cityTwoId": 18,
        "trainColor": TrainColor.RED,
        "length": 6
    },
    {
        "id": 59,
        "cityOneId": 15,
        "cityTwoId": 3,
        "trainColor": TrainColor.PINK,
        "length": 4
    },
    {
        "id": 60,
        "cityOneId": 0,
        "cityTwoId": 3,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 61,
        "cityOneId": 17,
        "cityTwoId": 0,
        "trainColor": TrainColor.WILD,
        "length": 1
    },
    {
        "id": 62,
        "cityOneId": 0,
        "cityTwoId": 25,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 63,
        "cityOneId": 0,
        "cityTwoId": 25,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 64,
        "cityOneId": 17,
        "cityTwoId": 25,
        "trainColor": TrainColor.BLACK,
        "length": 3
    },
    {
        "id": 65,
        "cityOneId": 13,
        "cityTwoId": 17,
        "trainColor": TrainColor.WHITE,
        "length": 3
    },
    {
        "id": 66,
        "cityOneId": 26,
        "cityTwoId": 17,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 67,
        "cityOneId": 26,
        "cityTwoId": 13,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 68,
        "cityOneId": 11,
        "cityTwoId": 26,
        "trainColor": TrainColor.PINK,
        "length": 2
    },
    {
        "id": 69,
        "cityOneId": 11,
        "cityTwoId": 26,
        "trainColor": TrainColor.BLUE,
        "length": 2
    },
    {
        "id": 70,
        "cityOneId": 25,
        "cityTwoId": 3,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 71,
        "cityOneId": 21,
        "cityTwoId": 4,
        "trainColor": TrainColor.BLUE,
        "length": 4
    },
    {
        "id": 72,
        "cityOneId": 7,
        "cityTwoId": 4,
        "trainColor": TrainColor.RED,
        "length": 3
    },
    {
        "id": 73,
        "cityOneId": 26,
        "cityTwoId": 4,
        "trainColor": TrainColor.GREEN,
        "length": 2
    },
    {
        "id": 74,
        "cityOneId": 26,
        "trainColor": TrainColor.WHITE,
        "cityTwoId": 4,
        "length": 2
    },
    {
        "id": 75,
        "cityOneId": 26,
        "cityTwoId": 23,
        "trainColor": TrainColor.GREEN,
        "length": 5
    },
    {
        "id": 76,
        "cityOneId": 17,
        "cityTwoId": 23,
        "trainColor": TrainColor.YELLOW,
        "length": 4
    },
    {
        "id": 77,
        "cityOneId": 25,
        "cityTwoId": 23,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 78,
        "cityOneId": 25,
        "cityTwoId": 34,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 79,
        "cityOneId": 25,
        "cityTwoId": 34,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 80,
        "cityOneId": 23,
        "cityTwoId": 34,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 81,
        "cityOneId": 4,
        "cityTwoId": 23,
        "trainColor": TrainColor.BLACK,
        "length": 3
    },
    {
        "id": 82,
        "cityOneId": 4,
        "cityTwoId": 23,
        "trainColor": TrainColor.ORANGE,
        "length": 3
    },
    {
        "id": 83,
        "cityOneId": 34,
        "cityTwoId": 19,
        "trainColor": TrainColor.ORANGE,
        "length": 2
    },
    {
        "id": 84,
        "cityOneId": 34,
        "cityTwoId": 19,
        "trainColor": TrainColor.BLACK,
        "length": 2
    },
    {
        "id": 85,
        "cityOneId": 19,
        "cityTwoId": 1,
        "trainColor": TrainColor.YELLOW,
        "length": 2
    },
    {
        "id": 86,
        "cityOneId": 19,
        "cityTwoId": 1,
        "trainColor": TrainColor.RED,
        "length": 2
    },
    {
        "id": 87,
        "cityOneId": 1,
        "cityTwoId": 16,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 88,
        "cityOneId": 1,
        "cityTwoId": 16,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 89,
        "cityOneId": 19,
        "cityTwoId": 16,
        "trainColor": TrainColor.BLUE,
        "length": 3
    },
    {
        "id": 90,
        "cityOneId": 32,
        "cityTwoId": 16,
        "trainColor": TrainColor.WILD,
        "length": 3
    },
    {
        "id": 91,
        "cityOneId": 30,
        "cityTwoId": 16,
        "trainColor": TrainColor.BLACK,
        "length": 5
    },
    {
        "id": 92,
        "cityOneId": 7,
        "cityTwoId": 32,
        "trainColor": TrainColor.PINK,
        "length": 6
    },
    {
        "id": 93,
        "cityOneId": 4,
        "cityTwoId": 32,
        "trainColor": TrainColor.WHITE,
        "length": 4
    },
    {
        "id": 94,
        "cityOneId": 32,
        "cityTwoId": 23,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 95,
        "cityOneId": 23,
        "cityTwoId": 19,
        "trainColor": TrainColor.WHITE,
        "length": 2
    },
    {
        "id": 96,
        "cityOneId": 23,
        "cityTwoId": 19,
        "trainColor": TrainColor.GREEN,
        "length": 2
    },
    {
        "id": 97,
        "cityOneId": 30,
        "cityTwoId": 32,
        "trainColor": TrainColor.WILD,
        "length": 2
    },
    {
        "id": 98,
        "cityOneId": 7,
        "cityTwoId": 30,
        "trainColor": TrainColor.WILD,
        "length": 3
    },
    {
        "id": 99,
        "cityOneId": 35,
        "cityTwoId": 30,
        "trainColor": TrainColor.WILD,
        "length": 6
    }
]

PATH_MAP: dict[int, Path] = {}

for path in _PATHS:
    PATH_MAP[path['id']] =  Path(
        id=path['id'],
        cityOneId=path['cityOneId'],
        cityTwoId=path['cityTwoId'],
        trainColor=path['trainColor'],
        length=path['length']
    )

PATH_VALUE: dict[int, int] = {
    1: 1,
    2: 2,
    3: 4,
    4: 7,
    5: 10,
    6: 15
}
