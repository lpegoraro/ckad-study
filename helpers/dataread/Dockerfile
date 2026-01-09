FROM golang:1.25.5-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 go build -o data-reader

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/data-reader .
CMD ["./data-reader"]
