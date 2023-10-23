package models

type Parking struct {
	ID          uint
	Address     string
	PlacesCount uint
	Photo       string
	Name        string
	//IsPaid            bool
	//IsOnlyForResident bool
}
