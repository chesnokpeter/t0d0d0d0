package main

import (
	"fmt"
	"log"

	"github.com/caarlos0/env/v6"
)

// Config - структура для конфигурации.
type Config struct {
	Port     int    `env:"RABBIT_URL"`
	LogLevel string `env:"BOT_TOKEN"`
}

func get_config() {
	cfg := Config{}
	// Парсинг переменных окружения в структуру Config.
	if err := env.Parse(&cfg); err != nil {
		log.Fatalf("Failed to parse env vars: %v", err)
	}

	// Используем значения из структуры.
	fmt.Printf("Config: %+v\n", cfg)
}
