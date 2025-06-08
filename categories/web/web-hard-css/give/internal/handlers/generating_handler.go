package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func GeneratingPage(ctx *gin.Context) {
	if CurrentUser == nil {
		ctx.Redirect(http.StatusSeeOther, "/login/")
		return
	}
	ctx.HTML(http.StatusOK, "generating.html", gin.H{
		"Username": CurrentUser.Username,
	})
}
