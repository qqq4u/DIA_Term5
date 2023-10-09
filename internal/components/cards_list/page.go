package list

import (
	"DIA_Term5/internal/api/repository"
	"DIA_Term5/internal/models"
	"DIA_Term5/internal/render"
	"github.com/gin-gonic/gin"
)

func Render(url string, c *gin.Context) {
	files := []string{
		"templates/places_list.gohtml",
	}

	var data []models.ParkingPlace
	if c.Query("placeNumber") != "" {
		data = repository.GetItemByNumber(repository.Places, c.Query("placeNumber"))
	} else {
		data = repository.Places
	}

	render.RenderTmpl(url, files, gin.H{"data": data, "QueryParam": c.Query("starName")}, c)
}
