package handlers

import (
	"css/internal/auth"
	"css/internal/utils"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

func LoginPage(ctx *gin.Context) {
	ctx.HTML(http.StatusOK, "login.html", gin.H{
		"LastUpdate": time.Now().Format("2006-01-02 15:04:05"),
	})
}

func LoginHandler(ctx *gin.Context) {
	username := ctx.PostForm("Username")
	password := ctx.PostForm("Password")

	user, err := auth.AuthUser(username, password)
	if err != nil {
		ctx.HTML(http.StatusOK, "login.html", gin.H{
			"ErrorMessage": "Invalid login or password",
			"LastUpdate":   time.Now().Format("2006-01-02 15:04:05"),
		})
		return
	}

	token, err := utils.GenerateJWTtoken(user.Username)
	if err != nil {
		ctx.HTML(http.StatusOK, "login.html", gin.H{
			"ErrorMessage": "Error generating token",
			"LastUpdate":   time.Now().Format("2006-01-02 15:04:05"),
		})
		return
	}

	ctx.SetCookie("Authorization", token, 3600, "/", "", false, true)
	ctx.Set("IsAuthenticated", true)
	ctx.Redirect(http.StatusSeeOther, "/profile/")
}
