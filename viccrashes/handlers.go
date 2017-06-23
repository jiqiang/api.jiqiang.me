package viccrashes

import (
	"encoding/json"
	"log"
	"net/http"

	"github.com/julienschmidt/httprouter"
)

// GetAccidentsCount router
func GetAccidentsCount(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
	if r.Method != "GET" {
		http.Error(w, http.StatusText(405), 405)
		return
	}

	type accidentCountOfTime struct {
		Count int    `json:"num_of_accidents"`
		Time  string `json:"time_of_day"`
	}

	var accidentCountTimeSeries []accidentCountOfTime

	rows, err := db.Query("select count(OBJECTID), ACCIDENT_TIME from crashes_last_five_years group by ACCIDENT_TIME order by ACCIDENT_TIME asc")
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
