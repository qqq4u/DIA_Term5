package models

type ParkingPlaceType struct {
	Name string
}

type ParkingPlace struct {
	ID        uint
	Number    string
	Type      ParkingPlaceType
	IsDeleted bool
	Floor     uint
}
