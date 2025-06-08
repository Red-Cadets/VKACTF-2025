package handlers

import (
	"css/internal/auth"
	"css/internal/models"
	"net/http"
	"regexp"
	"time"

	"github.com/gin-gonic/gin"
)

var CurrentUser *models.User

func RegisterPage(ctx *gin.Context) {
	ctx.HTML(http.StatusOK, "register.html", gin.H{})
}

func RegisterHandler(ctx *gin.Context) {

	user := &models.User{
		Username: ctx.PostForm("Username"),
		Email:    ctx.PostForm("Email"),
		Number:   ctx.PostForm("Number"),
		Password: ctx.PostForm("Password"),
	}

	if !isValidPass(user.Password) {
		ctx.HTML(http.StatusOK, "register.html", gin.H{
			"ErrorMessage": "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.",
			"LastUpdate":   time.Now().Format("2006-01-02 15:04:05"),
		})
		return
	}

	if err := auth.RegisterUser(user); err != nil {
		ctx.HTML(http.StatusOK, "register.html", gin.H{
			"ErrorMessage": "Failed to register account",
			"LastUpdate":   time.Now().Format("2006-01-02 15:04:05"),
		})
		return
	}
	CurrentUser = user

	ctx.Redirect(http.StatusSeeOther, "/generating/")

}

func isValidPass(pass string) bool {

	re := regexp.MustCompile(`^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$`)
	return re.MatchString(pass)
}
