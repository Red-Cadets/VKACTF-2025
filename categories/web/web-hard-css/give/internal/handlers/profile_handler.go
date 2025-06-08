package handlers

import (
	"css/internal/models"
	"css/pkg/db"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

func ProfilePage(ctx *gin.Context) {

	claims, exists := ctx.Get("claims")
	if !exists {
		ctx.HTML(http.StatusOK, "profile.html", gin.H{
			"error": "User not authenticated",
		})
		return
	}

	username := claims.(*models.Claims).Login

	db, err := db.New()
	if err != nil {
		ctx.HTML(http.StatusOK, "profile.html", gin.H{
			"error": "Database connection error",
		})
		return
	}

	var user models.User
	if err := db.DB.Where("Username = ?", username).First(&user).Error; err != nil {
		ctx.HTML(http.StatusOK, "profile.html", gin.H{
			"error": "User not found",
		})
		return
	}

	var themes []models.Theme
	if err := db.DB.Where("User_id = ?", user.ID).Find(&themes).Error; err != nil {
		ctx.HTML(http.StatusOK, "profile.html", gin.H{
			"error": "Failed to load themes",
		})
		return
	}
	message := "Use, share, and create themes"

	ctx.HTML(http.StatusOK, "profile.html", gin.H{
		"Username":   user.Username,
		"Email":      user.Email,
		"Number":     user.Number,
		"AtomID":     user.AtomID,
		"Themes":     themes,
		"Title":      "Profile",
		"Status":     "OPERATIONAL",
		"LastUpdate": time.Now().Format("2006-01-02 15:04:05"),
		"message":    message,
	})
}
