package auth

import (
	"css/internal/models"
	"css/internal/utils"
	"css/pkg/db"
	"errors"
)

func AuthUser(login, password string) (*models.User, error) {

	db, err := db.New()
	if err != nil {
		return nil, err
	}

	var user *models.User

	if err := db.DB.Where("Username = ?", login).First(&user).Error; err != nil {
		return nil, errors.New("user not found")
	}

	if user != nil && !utils.CheckPasswordHash(password, user.Password) {
		return nil, errors.New("invalid password")
	}

	return user, nil

}
