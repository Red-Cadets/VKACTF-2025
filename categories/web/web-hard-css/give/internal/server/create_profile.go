package server

import (
	"css/internal/auth"
	"css/internal/models"
	"css/pkg/db"
	"log"
	"os"
)

func createFilatova(db *db.Postgres) {

	admin_username := os.Getenv("ADMIN_USERNAME")
	admin_email := os.Getenv("ADMIN_EMAIL")
	admin_number := os.Getenv("ADMIN_NUMBER")
	admin_pass := os.Getenv("ADMIN_PASSWORD")
	admin_atomid := os.Getenv("ADMIN_ATOMID")

	admin := &models.User{
		Username: admin_username,
		Email:    admin_email,
		Number:   admin_number,
		Password: admin_pass,
		AtomID:   admin_atomid,
	}

	var existingUser models.User
	if err := db.DB.Where("Username = ?", admin.Username).First(&existingUser).Error; err == nil {
		log.Printf("Admin user '%s' already exists, skipping creation", admin.Username)
		return
	}
	if err := auth.RegisterUser(admin); err != nil {
		log.Fatalf("Failed to create admin user: %v", err)
	}
	log.Println("Admin user created successfully")
}
