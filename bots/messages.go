package bots

import (
	"fmt"
	"github.com/aastashov/house_search_assistant/structs"
	"log"
)

const startMessage = `
Это бот для поиска квартир. Основное его приемущество это скрытие просмотренных квартир. Доступные команды:

/start - запуск бота
/help - справка по командам
/stop - исключит Вас из списка пользователей для рассылки и остановит бота
/search - включит поиск квартир, бот будет отправлять Вам новые квартиры как найдет
/bookmarks - список сохраненных квартир
`

const helpMessage = `
Справка по командам:

/start - запуск бота
/help - эта команда
/stop - исключит Вас из списка пользователей для рассылки и остановит бота
/search - включит поиск квартир, бот будет отправлять Вам новые квартиры как найдет
/bookmarks - список сохраненных квартир

Справка по работе кнопок:

🔜 - пропускает квартиру на 1 час
❤ - добавляет в изюранное
❌ - больше не показывать эту квартиру
💔 - убрать их избранного
`

const templateMessage = `
Цена: %s
Комнат: %s
Номер: %s

%s
`

func DefaultMessage(offer *structs.Offer) string {
	return fmt.Sprintf(templateMessage,
		offer.Price,
		offer.RoomNumber,
		offer.Phone,
		offer.Topic,
	)
}

func (b *Bot) bookmarksMessages(offers []*structs.Offer, chat int64) {
	for _, offer := range offers {
		err := b.SendOffer(offer, &structs.User{Chat: chat}, nil, "")
		if err != nil {
			log.Println("[bookmarksMessages.SendOffer] error:", err)
		}
	}
}
