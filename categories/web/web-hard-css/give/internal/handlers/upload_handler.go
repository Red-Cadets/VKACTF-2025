package handlers

import (
	"css/internal/models"
	"css/pkg/db"
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
)

func UploadPage(ctx *gin.Context) {
	ctx.HTML(http.StatusOK, "upload.html", gin.H{
		"message":    "Upload your theme",
		"Status":     "OPERATIONAL",
		"LastUpdate": time.Now().Format("2006-01-02 15:04:05"),
	})
}

func UploadHandler(ctx *gin.Context) {
	claims, exists := ctx.Get("claims")
	if !exists {
		ctx.HTML(http.StatusUnauthorized, "upload.html", gin.H{
			"error": "User not authenticated",
		})
		return
	}

	username := claims.(*models.Claims).Login
	themeName := ctx.PostForm("theme_name")
	if themeName == "" {
		ctx.HTML(http.StatusBadRequest, "upload.html", gin.H{
			"error": "Theme name is required",
		})
		return
	}

	themeNameTrimmed := strings.TrimSpace(themeName)

	themeLink := fmt.Sprintf("https://cdn.jsdelivr.net/npm/darkmode-css@1.0.1/%s-mode.css", themeNameTrimmed)

	db, err := db.New()
	if err != nil {
		ctx.HTML(http.StatusInternalServerError, "upload.html", gin.H{
			"error": "Database connection error",
		})
		return
	}

	var user models.User
	if err := db.DB.Where("Username = ?", username).First(&user).Error; err != nil {
		ctx.HTML(http.StatusInternalServerError, "upload.html", gin.H{
			"error": "User not found",
		})
		return
	}

	var themeCount int64
	if err := db.DB.Model(&models.Theme{}).
		Where("User_id = ?", user.ID).
		Count(&themeCount).Error; err != nil {
		ctx.HTML(http.StatusInternalServerError, "upload.html", gin.H{
			"error": "Failed to check theme count",
		})
		return
	}

	const maxThemesPerUser = 10
	if themeCount >= maxThemesPerUser {
		ctx.HTML(http.StatusBadRequest, "upload.html", gin.H{
			"error":      fmt.Sprintf("You have reached the maximum limit of %d themes", maxThemesPerUser),
			"Status":     "OPERATIONAL",
			"LastUpdate": time.Now().Format("2006-01-02 15:04:05"),
		})
		return
	}

	theme := &models.Theme{
		Link:   themeLink,
		UserID: user.ID,
	}

	if err := db.DB.Create(theme).Error; err != nil {
		ctx.HTML(http.StatusInternalServerError, "upload.html", gin.H{
			"error": "Failed to save theme",
		})
		return
	}

	theme.Name = fmt.Sprintf("theme-%s-%d", username, theme.ID)

	if err := db.DB.Save(theme).Error; err != nil {
		ctx.HTML(http.StatusInternalServerError, "upload.html", gin.H{
			"error": "Failed to update theme",
		})
		return
	}

	errorMessage := ""
	if themeNameTrimmed != "dark" && themeNameTrimmed != "light" {
		errorMessage = "Warning: This theme is not officially supported."
	}

	ctx.HTML(http.StatusOK, "upload.html", gin.H{
		"error":      errorMessage,
		"Status":     "OPERATIONAL",
		"LastUpdate": time.Now().Format("2006-01-02 15:04:05"),
	})
}
