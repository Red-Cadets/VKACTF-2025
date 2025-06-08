package middleware

import (
	"css/internal/utils"

	"github.com/gin-gonic/gin"
)

func AuthMiddleware() gin.HandlerFunc {
	return func(ctx *gin.Context) {

		token, err := ctx.Cookie("Authorization")
		if err != nil {
			ctx.Set("IsAuthenticated", false)
			return
		}

		claims, err := utils.VerifyJWTtoken(token)
		if err != nil {
			ctx.Set("IsAuthenticated", false)
			return
		}

		ctx.Set("IsAuthenticated", true)
		ctx.Set("claims", claims)

		ctx.Next()
	}
}
