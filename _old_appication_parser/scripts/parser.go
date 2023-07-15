package main

import (
	"log"

	"github.com/comov/hsearch/configs"
	"github.com/comov/hsearch/parser"
)

func main() {
	//var site = parser.DieselSite()
	cfg := &configs.Config{}
	var site = parser.HouseSite(cfg)
	//var site = parser.LalafoSite()

	//doc, err := parser.GetDocumentByUrl(site.Url())
	//if err != nil {
	//	log.Fatalln(err)
	//}

	apartmentsLinks, err := parser.FindApartmentsLinksOnSite(site, cfg)
	if err != nil {
		log.Fatalln(err)
	}

	for id, link := range apartmentsLinks {
		log.Println(id, link)
	}
}
