package background

import (
	"context"
	"github.com/comov/hsearch/structs"
	"log"
	"net/http"
	"time"

	"github.com/getsentry/sentry-go"
)

func (m *Manager) garbage() {
	// при первом запуске менеджера, он начнет первый сбор муслоа через 2 секунды,
	// а после изменится на время из настроек (sleep = m.cnf.GarbageTime)
	sleep := time.Second * 2

	log.Printf("[garbage] StartGarbageCollector Manager\n")
	ctx := context.Background()
	for {
		select {
		case <-time.After(sleep):
			sleep = m.cnf.GarbageTime

			apartments, err := m.st.ReadAllApartments(ctx)
			if err != nil {
				sentry.CaptureException(err)
				log.Printf("[garbage.ReadAllApartments] Error: %s\n", err)
			}
			m.checkApartmentAndDelete(ctx, apartments)
		}
	}
}

func (m *Manager) checkApartmentAndDelete(ctx context.Context, apartments []*structs.Apartment) {
	apartmentChan := make(chan *structs.Apartment, len(apartments))

	for index := range apartments {
		apartment := apartments[index]
		go m.checkApartment(apartmentChan, apartment)
	}

	for {
		select {
		case apartment := <-apartmentChan:
			if apartment.IsDeleted {
				err := m.st.DeleteApartment(ctx, apartment)
				if err != nil {
					log.Println("[checkApartmentAndDelete.DeleteApartment] error:", err)
				}
			}
		case <-ctx.Done():
			return
		}
	}
}

func (m *Manager) checkApartment(apartmentChan chan *structs.Apartment, apartment *structs.Apartment) {
	res, err := http.Get(apartment.Url)
	if err != nil {
		log.Println("[GetDocumentByUrl.Get] error:", err)
		return
	}

	apartment.IsDeleted = res.StatusCode == 404
	apartmentChan <- apartment
}
