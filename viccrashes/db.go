package viccrashes

import (
	"database/sql"
	"log"
	// sqlite3 golang driver
	_ "github.com/mattn/go-sqlite3"
)

var db *sql.DB

// InitDB initializes a database instance
func InitDB(driverName string, dataSourceName string) {
	var err error
	db, err = sql.Open(driverName, dataSourceName)
	if err != nil {
		log.Fatal(err)
	}

	if err = db.Ping(); err != nil {
		log.Fatal(err)
	}
}
