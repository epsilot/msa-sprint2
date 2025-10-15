package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

func main() {
	serviceVersion := os.Getenv("SERVICE_VERSION")

	http.HandleFunc("/ping", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "pong")
	})

	http.HandleFunc("/index", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "This is booking-service: %s", serviceVersion)
	})

	log.Println("Server running on :8080")
    log.Println("Server version 0.0.5")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
