package card

import (
	"DIA_Term5/internal/api/repository"
	"DIA_Term5/internal/render"
	"github.com/gin-gonic/gin"
	"log"
	"strconv"
)

func Render(url string, c *gin.Context) {
	files := []string{
		"templates/place.gohtml",
	}

	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		log.Println(err)
	}
	list := repository.Places

	item := repository.GetItemById(list, uint(id))

	render.RenderTmpl(url, files, item, c)
}
