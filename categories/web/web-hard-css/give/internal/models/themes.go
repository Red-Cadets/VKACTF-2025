package models

import "gorm.io/gorm"

type Theme struct {
	gorm.Model
	Name   string `gorm:"unique;not null" json:"Name"`
	Link   string `gorm:"not null" json:"Link"`
	UserID uint   `gorm:"not null" json:"User_id"`
}
