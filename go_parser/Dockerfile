FROM golang:1.21-alpine3.18 AS builder

RUN apk --no-cache add git gcc g++
COPY . /srv

RUN set -x \
    && cd /srv/ \
    && go build -ldflags="-X 'main.Release=${RELEASE}'" -o /go/bin/hsearch cmd/hsearch/*.go


FROM alpine:3.18
RUN apk add --no-cache ca-certificates

COPY --from=builder /go/bin/ /usr/local/bin/

CMD ["hsearch"]
