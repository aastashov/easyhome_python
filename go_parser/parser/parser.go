package parser

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"regexp"
	"sync"
	"time"

	"github.com/PuerkitoBio/goquery"

	"github.com/comov/hsearch/configs"
	"github.com/comov/hsearch/structs"
)

type (
	Site interface {
		FullHost() string
		Url() string
		Name() string
		UseProxy() bool
		Selector() string

		GetApartmentsMap(doc *goquery.Document) ApartmentsMap
		IdFromHref(href string) (uint64, error)
		ParseNewApartment(href string, exId uint64, doc *goquery.Document) *structs.Apartment
	}
)

// Diesel [NOT]: Тема-негативка. Только факты. Арендаторам и Арендодателям внимание!
const negativeTheme = 2477961

type ApartmentsMap = map[uint64]string

var (
	intRegex  = regexp.MustCompile(`\d+`)
	textRegex = regexp.MustCompile(`[a-zA-Zа-яА-Я]+`)
)

// FindApartmentsLinksOnSite - load new apartments from the site and all find apartments
func FindApartmentsLinksOnSite(site Site, cfg *configs.Config) (ApartmentsMap, error) {
	doc, err := GetDocumentByUrl(site.Url(), cfg, site.UseProxy())
	if err != nil {
		return nil, err
	}

	apartments := make(ApartmentsMap)

	switch site.Name() {
	case structs.SiteLalafo:
		apartments = site.GetApartmentsMap(doc)
	case structs.SiteHouse:
		apartments = site.GetApartmentsMap(doc)
	default:
		apartments = DefaultParser(site, doc)
	}

	delete(apartments, negativeTheme)
	return apartments, nil
}

type loadApartments struct {
	cfg        *configs.Config
	apartments []*structs.Apartment
	add        chan *structs.Apartment
	wg         sync.WaitGroup
	ctx        context.Context
}

func (l *loadApartments) loadApartment(site Site, id uint64, href string) {
	defer l.wg.Done()

	doc, err := GetDocumentByUrl(href, l.cfg, site.UseProxy())
	if err != nil {
		log.Printf("Can't load apartment %s with an error %s\f", href, err)
		return
	}

	apartment := site.ParseNewApartment(href, id, doc)
	if apartment != nil {
		l.add <- apartment
	}
}

func (l *loadApartments) addApartment() {
	for {
		select {
		case apartment := <-l.add:
			l.apartments = append(l.apartments, apartment)
		case <-l.ctx.Done():
			return
		}
	}
}

// LoadApartmentsDetail - выгружает и парсит apartments по href
func LoadApartmentsDetail(apartmentsList map[uint64]string, site Site, cfg *configs.Config) []*structs.Apartment {
	// fixme: это ёбаный костыль!
	lo := loadApartments{
		cfg:        cfg,
		apartments: make([]*structs.Apartment, 0),
		add:        make(chan *structs.Apartment, len(apartmentsList)),
	}

	ctx, cancel := context.WithCancel(context.Background())
	lo.ctx = ctx
	defer cancel()
	defer close(lo.add)

	go lo.addApartment()

	for id, href := range apartmentsList {
		lo.wg.Add(1)
		go lo.loadApartment(site, id, href)
	}

	lo.wg.Wait()
	time.Sleep(time.Second * 1) // fixme: особенно это. Типа ожидать чтоб добавить в список последний apartment
	return lo.apartments
}

// GetDocumentByUrl - получает страницу по http, читает и возвращает объект goquery.Document
func GetDocumentByUrl(targetUrl string, cfg *configs.Config, useProxy bool) (*goquery.Document, error) {
	request, err := http.NewRequest("GET", targetUrl, nil)
	if err != nil {
		log.Println("[GetDocumentByUrl.NewRequest] error:", err)
		return nil, err
	}

	request.Close = true

	var proxy func(*http.Request) (*url.URL, error) = nil
	if useProxy {
		proxy = http.ProxyURL(&url.URL{
			Scheme: "http",
			User:   url.UserPassword(cfg.ProxyUser, cfg.ProxyPass),
			Host:   cfg.ProxyHost,
		})
	}

	client := &http.Client{Transport: &http.Transport{Proxy: proxy}}
	res, err := client.Do(request)
	if err != nil {
		log.Println("[GetDocumentByUrl.Do] error:", err)
		return nil, err
	}

	defer func() {
		err := res.Body.Close()
		if err != nil {
			log.Println("[GetDocumentByUrl.defer.Close] error:", err)
		}
	}()

	if res.StatusCode != 200 {
		return nil, fmt.Errorf("status code error: %d %s", res.StatusCode, res.Status)
	}

	return goquery.NewDocumentFromReader(res.Body)
}

func DefaultParser(site Site, doc *goquery.Document) ApartmentsMap {
	var mapResponse = make(ApartmentsMap, 0)
	doc.Find(site.Selector()).Each(func(i int, s *goquery.Selection) {
		href, ok := s.Attr("href")
		if !ok {
			log.Println("Can't find href")
			return
		}

		apartmentId, err := site.IdFromHref(href)
		if err != nil {
			log.Println("Can't get Id from href with an error", err)
			return
		}

		u, err := url.Parse(href)
		if err != nil {
			log.Println("Can't parse href to error with an error", err)
			return
		}

		mapResponse[apartmentId] = fmt.Sprintf("%s%s", site.FullHost(), u.RequestURI())
	})
	return mapResponse
}
