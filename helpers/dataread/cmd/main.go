package main

import (
	"context"
	"database/sql"
	"log/slog"
	"os"

	_ "github.com/jackc/pgx/v5/stdlib"
)

func main() {
	// Set up slog for structured logging
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	slog.SetDefault(logger)

	// Connect to Postgres
	dsn := os.Getenv("POSTGRES_DSN")
	db, err := sql.Open("pgx", dsn)
	if err != nil {
		slog.Error("failed to connect to database", "error", err)
		os.Exit(1)
	}
	defer db.Close()

	// Read a value (example: SELECT version())
	var version string
	err = db.QueryRowContext(context.Background(), "SELECT version()").Scan(&version)
	if err != nil {
		slog.Error("failed to query database", "error", err)
		os.Exit(1)
	}

	slog.Info("Postgres version", "version", version)
}
