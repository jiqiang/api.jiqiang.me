package viccrashes

import (
	"encoding/json"
	"log"
	"net/http"
	"strings"

	"github.com/julienschmidt/httprouter"
)

// GetAccidentsCount router
func GetAccidentsCount(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
	if r.Method != "GET" {
		http.Error(w, http.StatusText(405), 405)
		return
	}

	yearWhere := `WHERE SUBSTR(ACCIDENT_DATE, 1, 4) = "2017"`
	params := r.URL.Query()
	if yearList, ok := params["year"]; ok {
		yearWhere = `WHERE SUBSTR(ACCIDENT_DATE, 1, 4) IN ("` + strings.Join(yearList, `", "`) + `")`
	}

	type accidentCountOfTime struct {
		Count int    `json:"num_of_accidents"`
		Time  string `json:"time_of_day"`
	}

	var accidentCountTimeSeries []accidentCountOfTime

	sql := "SELECT COUNT(OBJECTID), ACCIDENT_TIME FROM crashes_last_five_years " + yearWhere + " GROUP BY ACCIDENT_TIME ORDER BY ACCIDENT_TIME ASC"
	rows, err := db.Query(sql)
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	for rows.Next() {
		var count int
		var time string
		err = rows.Scan(&count, &time)
		if err != nil {
			log.Fatal(err)
		}
		acot := accidentCountOfTime{count, time}
		accidentCountTimeSeries = append(accidentCountTimeSeries, acot)
	}
	err = rows.Err()
	if err != nil {
		log.Fatal(err)
	}

	js, err := json.Marshal(accidentCountTimeSeries)
	if err != nil {
		log.Fatal(err)
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write(js)
}
