package main

import (
	"log"
	"net/http"

	"github.com/jiqiang/api.jiqiang.me/viccrashes"
	"github.com/julienschmidt/httprouter"
)

func main() {
	viccrashes.InitDB("sqlite3", "./viccrashes.sqlite3")

	router := httprouter.New()
	router.GET("/viccrashes/count", viccrashes.GetAccidentsCount)
	log.Fatal(http.ListenAndServe(":8080", router))
}
