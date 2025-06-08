package utils

import (
	"css/internal/models"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

var jwtSecret = GenerateKey()

func GenerateJWTtoken(login string) (string, error) {

	experimentationTime := time.Now().Add(time.Hour * 24)

	claims := &models.Claims{
		Login: login,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(experimentationTime),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)

	return token.SignedString(jwtSecret)
}

func VerifyJWTtoken(tokenString string) (*models.Claims, error) {

	claims := &models.Claims{}

	token, err := jwt.ParseWithClaims(tokenString, claims, func(t *jwt.Token) (interface{}, error) {

		return jwtSecret, nil
	})

	if err != nil || !token.Valid {
		return nil, err
	}

	return claims, nil
}
