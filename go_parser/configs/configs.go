package configs

import (
	"fmt"
	"time"

	"github.com/caarlos0/env/v6"
	"github.com/getsentry/sentry-go"
	_ "github.com/joho/godotenv/autoload"
)

// Config - the structure that contains all the customizable application configurations
type Config struct {
	Release         string
	ParserFrequency string `env:"PARSER_FREQUENCY"`
	OrderRelevance  string `env:"ORDER_RELEVANCE"`
	TelegramToken   string `env:"TG_TOKEN"`
	TelegramChatId  int64  `env:"TG_CHAT_ID"`

	PgDatabase string `env:"DB_NAME"`
	PgName     string `env:"DB_USER"`
	PgPassword string `env:"DB_PASSWORD"`
	PgHost     string `env:"DB_HOST"`
	PgPort     int32  `env:"DB_PORT"`

	ProxyHost string `env:"PROXY_HOST"`
	ProxyUser string `env:"PROXY_USER"`
	ProxyPass string `env:"PROXY_PASSWORD"`

	DieselUseProxy  bool `env:"DIESEL_USE_PROXY"`
	HouseUseProxy   bool `env:"HOUSE_USE_PROXY"`
	LalafolUseProxy bool `env:"LALAFO_USE_PROXY"`

	DisabledGarbage bool `env:"DISABLED_GARBAGE"`
	DisabledGrabber bool `env:"DISABLED_GRABBER"`
	DisabledMatcher bool `env:"DISABLED_MATCHER"`

	DisabledParseDiesel bool `env:"DISABLED_PARSE_DIESEL"`
	DisabledParseLalafo bool `env:"DISABLED_PARSE_LALAFO"`
	DisabledParseHouse  bool `env:"DISABLED_PARSE_HOUSE"`

	FrequencyTime time.Duration
	RelevanceTime time.Duration

	GarbageTime  time.Duration
	PgConnString string
}

// GetConf - returns the application configuration
func GetConf() (*Config, error) {
	cfg := &Config{
		ParserFrequency:     "1m",
		OrderRelevance:      "2m",
		PgPassword:          "hsearch",
		PgHost:              "localhost",
		PgPort:              5432,
		DisabledGarbage:     false,
		DisabledGrabber:     false,
		DisabledMatcher:     false,
		DisabledParseDiesel: false,
		DisabledParseLalafo: false,
		DisabledParseHouse:  false,
		GarbageTime:         time.Hour, // every hour
	}

	err := env.Parse(cfg)
	if err != nil {
		return nil, err
	}

	err = sentry.Init(sentry.ClientOptions{
		SampleRate: 0.5,
	})

	if err != nil {
		return nil, err
	}

	//// In the settings we set the delay time as line 1m or 12h, then parse
	////  in time.

	// RelevanceTime
	cfg.FrequencyTime, err = time.ParseDuration(cfg.ParserFrequency)
	if err != nil {
		return nil, err
	}

	// RelevanceTime
	cfg.RelevanceTime, err = time.ParseDuration(cfg.OrderRelevance)
	if err != nil {
		return nil, err
	}

	cfg.PgConnString = fmt.Sprintf("dbname=%s user=%s password=%s host=%s port=%d",
		cfg.PgDatabase,
		cfg.PgName,
		cfg.PgPassword,
		cfg.PgHost,
		cfg.PgPort,
	)

	return cfg, nil
}
