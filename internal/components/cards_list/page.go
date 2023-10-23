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

	var data []models.Parking
	if c.Query("parkingName") != "" {
		data = repository.GetParkingByName(repository.Parkings, c.Query("parkingName"))
	} else {
		data = repository.Parkings
	}

	render.RenderTmpl(url, files, gin.H{"data": data, "QueryParam": c.Query("parkingName")}, c)
}
