package handlers

import (
	"css/internal/middleware"
	"css/internal/models"
	"fmt"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

func RegisterHandlers(router *gin.Engine) {

	router.Use(middleware.SecurityHeaders(), middleware.AuthMiddleware())

	public := router.Group("/")
	{
		public.GET("/", IndexPage)
		public.GET("/login/", middleware.RedirectIfAuthenticated(), LoginPage)
		public.POST("/login/", middleware.RedirectIfAuthenticated(), LoginHandler)
		public.GET("/register/", middleware.RedirectIfAuthenticated(), RegisterPage)
		public.POST("/register/", middleware.RedirectIfAuthenticated(), RegisterHandler)
		public.GET("/generating/", middleware.RedirectIfAuthenticated(), GeneratingPage)
	}

	protected := router.Group("/")
	protected.Use(func(ctx *gin.Context) {
		if !ctx.GetBool("IsAuthenticated") {
			ctx.Redirect(http.StatusSeeOther, "/login/")
			ctx.Abort()
			return
		}
		ctx.Next()
	})
	{
		protected.GET("/logout/", LogoutPage)
		protected.GET("/profile/", ProfilePage)
		protected.POST("/profile/delete", DeleteThemeHandler)
		protected.GET("/create/", CreatePage)
		protected.GET("/upload/", UploadPage)
		protected.POST("/upload/", UploadHandler)
		protected.GET("/share/", SharePage)
		protected.POST("/share/", ShareHandler)
	}
}

func IndexPage(ctx *gin.Context) {
	isAuthenticated := ctx.GetBool("IsAuthenticated")

	username := "GUEST"
	message := "Welcome to the Kollective System!"

	if isAuthenticated {
		if claims, exists := ctx.Get("claims"); exists {
			username = claims.(*models.Claims).Login
			message = fmt.Sprintf("Welcome, %s!", username)
		}
	}

	ctx.HTML(http.StatusOK, "index.html", gin.H{
		"Title":           "Main Interface",
		"Status":          "OPERATIONAL",
		"LastUpdate":      time.Now().Format("2006-01-02 15:04:05"),
		"IsAuthenticated": isAuthenticated,
		"message":         message,
	})
}
