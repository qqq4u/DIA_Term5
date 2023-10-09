package api

import (
	"DIA_Term5/internal/components/card"
	list "DIA_Term5/internal/components/cards_list"
	"github.com/gin-gonic/gin"
	"log"
)

func StartServer() {
	log.Println("Server start up")

	r := gin.Default()

	// loads all html in templates dir
	r.LoadHTMLGlob("templates/*")

	r.GET("/home", func(c *gin.Context) {
		list.Render("/home", c)
	})

	r.GET("/parking/:id", func(c *gin.Context) {
		card.Render("/parking/:id", c)
	})

	r.Static("/image", "./resources")
	r.Static("/styles", "./styles")

	// listen and serve on 127.0.0.1:8080
	err := r.Run()
	if err != nil {
		log.Fatalln(err)
	}
}
