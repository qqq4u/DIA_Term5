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

var Places = []models.ParkingPlace{
	models.ParkingPlace{
		ID:        1,
		Number:    "1A",
		Type:      PlacesTypes[0],
		IsDeleted: false,
		Floor:     1,
	},
	models.ParkingPlace{
		ID:        2,
		Number:    "2A",
		Type:      PlacesTypes[1],
		IsDeleted: false,
		Floor:     1,
	},
	models.ParkingPlace{
		ID:        3,
		Number:    "3A",
		Type:      PlacesTypes[1],
		IsDeleted: false,
		Floor:     1,
	},
	models.ParkingPlace{
		ID:        4,
		Number:    "4A",
		Type:      PlacesTypes[1],
		IsDeleted: false,
		Floor:     2,
	},
	models.ParkingPlace{
		ID:        5,
		Number:    "5A",
		Type:      PlacesTypes[2],
		IsDeleted: false,
		Floor:     3,
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

func GetItemByNumber(list []models.ParkingPlace, name string) []models.ParkingPlace {
	res := make([]models.ParkingPlace, 0)
	for i := 0; i < len(list); i++ {
		if strings.Contains(strings.ToLower(list[i].Number), strings.ToLower(name)) {
			res = append(res, list[i])
		}
	}
	return res
}
