package background

import (
	"context"
	"log"
	"net/http"
	"time"

	"github.com/getsentry/sentry-go"

	"github.com/comov/hsearch/structs"
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
	for index := range apartments {
		apartment := apartments[index]
		res, err := http.Get(apartment.Url)
		if err != nil {
			log.Println("[garbage.checkApartment.Get] error:", err)
			continue
		}

		if res.StatusCode == 404 {
			err := m.st.DeleteApartment(ctx, apartment)
			if err != nil {
				log.Println("[garbage.checkApartmentAndDelete.DeleteApartment] error:", err)
				continue
			}
			log.Println("[garbage.checkApartmentAndDelete] deleted", apartment.Id)
		}
	}
}
