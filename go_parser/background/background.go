package background

import (
	"context"

	"github.com/PuerkitoBio/goquery"

	"github.com/comov/hsearch/configs"
	"github.com/comov/hsearch/parser"
	"github.com/comov/hsearch/structs"
)

type (
	Storage interface {
		WriteApartments(ctx context.Context, apartment []*structs.Apartment) (int, error)
		ReadChatsForMatching(ctx context.Context, enable int) ([]*structs.Chat, error)
		ReadNextApartment(ctx context.Context, chat *structs.Chat) (*structs.Apartment, error)
		CleanFromExistApartments(ctx context.Context, apartments map[uint64]string, siteName string) error

		ReadAllApartments(ctx context.Context) ([]*structs.Apartment, error)
		DeleteApartment(ctx context.Context, apartment *structs.Apartment) error

		UpdateSettings(ctx context.Context, chat *structs.Chat) error
	}

	Bot interface {
		SendApartment(ctx context.Context, apartment *structs.Apartment, chat *structs.Chat) error
		SendError(where string, err error, chatId int64)
	}

	Site interface {
		Name() string
		UseProxy() bool
		FullHost() string
		Url() string
		Selector() string

		GetApartmentsMap(doc *goquery.Document) parser.ApartmentsMap
		IdFromHref(href string) (uint64, error)
		ParseNewApartment(href string, exId uint64, doc *goquery.Document) *structs.Apartment
	}

	Manager struct {
		st            Storage
		bot           Bot
		cnf           *configs.Config
		sitesForParse []Site
	}
)

// NewManager - initializes the new background manager
func NewManager(cnf *configs.Config, st Storage, bot Bot) *Manager {
	var _sitesForParse []Site

	if cnf.DisabledParseDiesel != true {
		_sitesForParse = append(_sitesForParse, parser.DieselSite(cnf))
	}

	if cnf.DisabledParseLalafo != true {
		_sitesForParse = append(_sitesForParse, parser.LalafoSite(cnf))
	}

	if cnf.DisabledParseHouse != true {
		_sitesForParse = append(_sitesForParse, parser.HouseSite(cnf))
	}

	return &Manager{
		st:            st,
		bot:           bot,
		cnf:           cnf,
		sitesForParse: _sitesForParse,
	}
}

// StartGrabber - starts the process of finding new apartments
func (m *Manager) StartGrabber() {
	m.grabber()
}

// StartMatcher - starts the search process for chats
func (m *Manager) StartMatcher() {
	m.matcher()
}

// StartGarbageCollector - runs garbage collection in the form of old records that no longer make sense
func (m *Manager) StartGarbageCollector() {
	m.garbage()
}
