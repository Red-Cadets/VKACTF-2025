package handlers

import (
	"css/internal/models"
	"css/pkg/db"
	"net/http"

	"github.com/gin-gonic/gin"
)

func DeleteThemeHandler(ctx *gin.Context) {
	claims, exists := ctx.Get("claims")
	if !exists {
		ctx.HTML(http.StatusUnauthorized, "profile.html", gin.H{
			"error": "User not authenticated",
		})
		return
	}

	username := claims.(*models.Claims).Login
	themeID := ctx.PostForm("theme_id")
	if themeID == "" {
		ctx.HTML(http.StatusBadRequest, "profile.html", gin.H{
			"error": "Theme ID is required",
		})
		return
	}

	db, err := db.New()
	if err != nil {
		ctx.HTML(http.StatusInternalServerError, "profile.html", gin.H{
			"error": "Database connection error",
		})
		return
	}

	var user models.User
	if err := db.DB.Where("Username = ?", username).First(&user).Error; err != nil {
		ctx.HTML(http.StatusInternalServerError, "profile.html", gin.H{
			"error": "User not found",
		})
		return
	}

	var theme models.Theme
	if err := db.DB.Where("id = ? AND User_id = ?", themeID, user.ID).First(&theme).Error; err != nil {
		ctx.HTML(http.StatusBadRequest, "profile.html", gin.H{
			"error": "Theme not found or does not belong to you",
		})
		return
	}

	if err := db.DB.Delete(&theme).Error; err != nil {
		ctx.HTML(http.StatusInternalServerError, "profile.html", gin.H{
			"error": "Failed to delete theme",
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

	ctx.Redirect(http.StatusSeeOther, "/profile/")

	ctx.HTML(http.StatusOK, "profile.html", gin.H{
		"Username": user.Username,
		"Email":    user.Email,
		"Number":   user.Number,
		"AtomID":   user.AtomID,
		"Themes":   themes,
		"message":  "Theme deleted successfully",
	})

}
