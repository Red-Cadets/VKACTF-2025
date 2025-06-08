package handlers

import (
	"css/internal/models"
	"css/pkg/db"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

func SharePage(ctx *gin.Context) {

	claims, exists := ctx.Get("claims")
	if !exists {
		ctx.HTML(http.StatusOK, "share.html", gin.H{
			"error": "User not authenticated",
		})
		return
	}

	username := claims.(*models.Claims).Login
	db, err := db.New()
	if err != nil {
		ctx.HTML(http.StatusOK, "share.html", gin.H{
			"error": "Database connection error",
		})
		return
	}

	var user models.User
	if err := db.DB.Where("Username = ?", username).First(&user).Error; err != nil {
		ctx.HTML(http.StatusOK, "share.html", gin.H{
			"error": "User not found",
		})
		return
	}

	var themes []models.Theme
	if err := db.DB.Where("User_id = ?", user.ID).Find(&themes).Error; err != nil {
		ctx.HTML(http.StatusOK, "share.html", gin.H{
			"error": "Failed to load themes",
		})
		return
	}

	ctx.HTML(http.StatusOK, "share.html", gin.H{
		"Status":     "OPERATIONAL",
		"LastUpdate": time.Now().Format("2006-01-02 15:04:05"),
		"Themes":     themes,
	})
}

func ShareHandler(ctx *gin.Context) {
	claims, exists := ctx.Get("claims")
	if !exists {
		ctx.HTML(http.StatusUnauthorized, "share.html", gin.H{
			"error": "User not authenticated",
		})
		return
	}

	sourceUsername := claims.(*models.Claims).Login
	destinationUsername := ctx.PostForm("Username")
	themeID := ctx.PostForm("theme_id")

	db, err := db.New()
	if err != nil {
		ctx.HTML(http.StatusInternalServerError, "share.html", gin.H{
			"error": "Database connection error",
		})
		return
	}

	var user models.User
	if err := db.DB.Where("Username = ?", sourceUsername).First(&user).Error; err != nil {
		ctx.HTML(http.StatusOK, "share.html", gin.H{
			"error": "User not found",
		})
		return
	}

	var themes []models.Theme
	if err := db.DB.Where("User_id = ?", user.ID).Find(&themes).Error; err != nil {
		ctx.HTML(http.StatusOK, "share.html", gin.H{
			"error": "Failed to load themes",
		})
		return
	}

	if destinationUsername == "" {
		ctx.HTML(http.StatusBadRequest, "share.html", gin.H{
			"error":      "Username must be not null",
			"Themes":     themes,
			"Status":     "OPERATIONAL",
			"LastUpdate": time.Now().Format("2006-01-02 15:04:05"),
		})
		return
	}

	if destinationUsername == sourceUsername {
		ctx.HTML(http.StatusBadRequest, "share.html", gin.H{
			"error":      "Sorry, you are not share yourself",
			"Themes":     themes,
			"Status":     "OPERATIONAL",
			"LastUpdate": time.Now().Format("2006-01-02 15:04:05"),
		})
		return
	}

	if themeID == "" {
		ctx.HTML(http.StatusBadRequest, "share.html", gin.H{
			"error":      "Please select a theme to share",
			"Themes":     themes,
			"Status":     "OPERATIONAL",
			"LastUpdate": time.Now().Format("2006-01-02 15:04:05"),
		})
		return
	}

	var destinationUser models.User
	if err := db.DB.Where("Username = ?", destinationUsername).First(&destinationUser).Error; err != nil {
		ctx.HTML(http.StatusBadRequest, "share.html", gin.H{
			"error":      "Recipient user not found",
			"Themes":     themes,
			"Status":     "OPERATIONAL",
			"LastUpdate": time.Now().Format("2006-01-02 15:04:05"),
		})
		return
	}

	var theme models.Theme
	if err := db.DB.Where("id = ? AND User_id = ?", themeID, user.ID).First(&theme).Error; err != nil {
		ctx.HTML(http.StatusBadRequest, "share.html", gin.H{
			"error":      "Theme not found or does not belong to you",
			"Themes":     themes,
			"Status":     "OPERATIONAL",
			"LastUpdate": time.Now().Format("2006-01-02 15:04:05"),
		})
		return
	}

	if theme.Link == "" {
		ctx.HTML(http.StatusBadRequest, "share.html", gin.H{
			"error":      "Cannot share an empty theme (link is missing)",
			"Themes":     themes,
			"Status":     "OPERATIONAL",
			"LastUpdate": time.Now().Format("2006-01-02 15:04:05"),
		})
		return
	}

	newTheme := &models.Theme{
		Link:   theme.Link,
		UserID: destinationUser.ID,
	}

	if err := db.DB.Create(newTheme).Error; err != nil {
		ctx.HTML(http.StatusInternalServerError, "share.html", gin.H{
			"error": "Failed to share theme",
		})
		return
	}

	newTheme.Name = fmt.Sprintf("theme-%s-%d", sourceUsername, newTheme.ID)
	if err := db.DB.Save(newTheme).Error; err != nil {
		ctx.HTML(http.StatusInternalServerError, "share.html", gin.H{
			"error": "Failed to update shared theme",
		})
		return
	}

	log.Printf("Theme shared: {source_name: %s, destination_name: %s, theme: %s}\n",
		sourceUsername, destinationUsername, newTheme.Link)

	if err := db.DB.Where("User_id = ?", user.ID).Find(&themes).Error; err != nil {
		ctx.HTML(http.StatusOK, "share.html", gin.H{
			"error": "Failed to load themes",
		})
		return
	}

	ctx.HTML(http.StatusOK, "share.html", gin.H{
		"Status":     "OPERATIONAL",
		"LastUpdate": time.Now().Format("2006-01-02 15:04:05"),
		"Themes":     themes,
	})
}
