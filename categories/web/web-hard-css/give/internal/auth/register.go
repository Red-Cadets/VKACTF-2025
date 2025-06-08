package auth

import (
	"css/internal/models"
	"css/internal/utils"
	"css/pkg/db"
	"errors"
	"fmt"
	"os"

	"gorm.io/gorm"
)

func RegisterUser(user *models.User) error {
	db, err := db.New()
	if err != nil {
		return err
	}

	fmt.Println("DB connection established...")

	var existingUser *models.User

	if err := db.DB.Where("Username = ?", user.Username).First(&existingUser).Error; err != nil {
		if err != gorm.ErrRecordNotFound {
			return fmt.Errorf("error checking existing user: %v", err)
		}
	} else {
		return errors.New("user already exists")
	}

	hashedPassword, err := utils.HashPassword(user.Password)
	if err != nil {
		return fmt.Errorf("error hashing password: %v", err)
	}

	user.Password = hashedPassword

	admin_username := os.Getenv("ADMIN_USERNAME")

	if user.Username != admin_username {
		user.AtomID = GenerateAtomID(user)
	}

	if err := db.DB.Create(user).Error; err != nil {
		return fmt.Errorf("error creating user: %v", err)
	}

	return nil

}
