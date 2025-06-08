package main

import (
	"css/internal/server"
	"os"
)

func main() {

	port := os.Getenv("SERVICE_PORT")

	Server := server.New()
	Server.Run(":" + port)
}
