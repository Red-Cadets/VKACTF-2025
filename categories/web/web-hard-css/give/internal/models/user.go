package models

import (
	"gorm.io/gorm"
)

type User struct {
	gorm.Model
	Username string `gorm:"unique;not null" json:"Username"`
	Email    string `gorm:"not null" json:"Email"`
	Number   string `gorm:"not null" json:"Number"`
	Password string `gorm:"not null" json:"Password"`
	AtomID   string `gorm:"unique;not null" json:"AtomID"`
}
