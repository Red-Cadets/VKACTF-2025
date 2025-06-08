package handlers

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

func CreatePage(ctx *gin.Context) {
	ctx.HTML(http.StatusOK, "create.html", gin.H{
		"Status":     "OPERATIONAL",
		"LastUpdate": time.Now().Format("2006-01-02 15:04:05"),
	})
}
