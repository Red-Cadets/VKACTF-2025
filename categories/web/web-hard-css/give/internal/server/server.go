package server

import (
	"css/internal/handlers"
	"css/internal/models"
	"css/pkg/db"
	"log"

	"github.com/gin-gonic/gin"
)

type Server struct {
	router *gin.Engine
	db     *db.Postgres
}

func New() *Server {

	db, err := db.New()
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}

	if err := db.DB.AutoMigrate(&models.User{}, &models.Theme{}); err != nil {
		log.Fatalf("Failed to migrate database: %v", err)
	}

	createFilatova(db)

	r := gin.Default()
	r.LoadHTMLGlob("internal/templates/*.html")
	r.Static("/static/styles", "./internal/static/styles")
	handlers.RegisterHandlers(r)

	return &Server{
		router: r,
		db:     db,
	}
}

func (s *Server) Run(addr string) error {
	return s.router.Run(addr)
}
