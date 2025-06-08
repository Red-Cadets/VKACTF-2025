package middleware

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func RedirectIfAuthenticated() gin.HandlerFunc {
	return func(ctx *gin.Context) {

		isAuthenticated := ctx.GetBool("IsAuthenticated")
		if isAuthenticated {
			ctx.Redirect(http.StatusSeeOther, "/")
			ctx.Abort()
			return
		}
		ctx.Next()

	}
}
