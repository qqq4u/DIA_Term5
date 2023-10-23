package repository

import (
	"DIA_Term5/internal/models"
	"strings"
)

var PlacesTypes = []models.ParkingPlaceType{
	models.ParkingPlaceType{Name: "Bicycle"},
	models.ParkingPlaceType{Name: "Car"},
	models.ParkingPlaceType{Name: "Moto"},
}

var Parkings = []models.Parking{
	//можно сделать платные и только для резидентов
	{ID: 1, Address: "2-я Бауманская ул., 5, стр. 4, Москва", PlacesCount: 50, Photo: "https://avatars.mds.yandex.net/get-altay/4042551/2a0000017ff34c689a12e3a273a014adda95/XXXL", Name: "Парковка возле главного здания"},
	{ID: 2, Address: "Кондрашёвский тупик, 3А, Москва", PlacesCount: 150, Photo: "https://avatars.mds.yandex.net/get-altay/5496626/2a0000017d8a027ac8eb10299ff64fb16a54/XXXL", Name: "Парковка возле лефортовского тоннеля"},
	{ID: 3, Address: "Бригадирский пер., 3-5, Москва", PlacesCount: 30, Photo: "https://avatars.mds.yandex.net/get-altay/367512/2a0000015b964287e1d109be1d60b20bc110/XXXL", Name: "Парковка возле корпуса Энергомашиностроения"},
	{ID: 4, Address: "Рубцовская набережная, 2/18, Москва", PlacesCount: 20, Photo: "https://avatars.mds.yandex.net/get-altay/374295/2a0000015b39be913f074a37ac1e07cfb2c7/XXXL", Name: "Парковка возле УЛК"},
	//{ID: 5, Address: "", PlacesCount: 20, Photo: "", Name: "Парковка возле 11 общежития"},
}

var Places = []models.ParkingPlace{
	models.ParkingPlace{
		ID:        1,
		Number:    "1A",
		Type:      PlacesTypes[0],
		IsDeleted: false,
	},
	models.ParkingPlace{
		ID:        2,
		Number:    "2A",
		Type:      PlacesTypes[1],
		IsDeleted: false,
	},
	models.ParkingPlace{
		ID:        3,
		Number:    "3A",
		Type:      PlacesTypes[1],
		IsDeleted: false,
	},
	models.ParkingPlace{
		ID:        4,
		Number:    "4A",
		Type:      PlacesTypes[1],
		IsDeleted: false,
	},
	models.ParkingPlace{
		ID:        5,
		Number:    "5A",
		Type:      PlacesTypes[2],
		IsDeleted: false,
	},
}

func GetItemById(list []models.ParkingPlace, id uint) models.ParkingPlace {
	for i := 0; i < len(list); i++ {
		if id == list[i].ID {
			return list[i]
		}
	}
	return models.ParkingPlace{}
}

func GetParkingById(list []models.Parking, id uint) models.Parking {
	for i := 0; i < len(list); i++ {
		if id == list[i].ID {
			return list[i]
		}
	}
	return models.Parking{}
}

func GetItemByNumber(list []models.ParkingPlace, name string) []models.ParkingPlace {
	res := make([]models.ParkingPlace, 0)
	for i := 0; i < len(list); i++ {
		if strings.Contains(strings.ToLower(list[i].Number), strings.ToLower(name)) {
			res = append(res, list[i])
		}
	}
	return res
}

func GetParkingByName(list []models.Parking, name string) []models.Parking {
	res := make([]models.Parking, 0)
	for i := 0; i < len(list); i++ {
		if strings.Contains(strings.ToLower(list[i].Name), strings.ToLower(name)) {
			res = append(res, list[i])
		}
	}
	return res
}
