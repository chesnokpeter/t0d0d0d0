package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/go-co-op/gocron"
	"github.com/streadway/amqp"
)

type Message struct {
	Delay   int    `json:"delay"`
	Content string `json:"message"`
	Queue   string `json:"queue_after_delay"`
}

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func main() {
	rabbit_url := os.Getenv("RABBIT_URL")

	conn, err := amqp.Dial(rabbit_url)
	failOnError(err, "failed to connect to rabbitmq")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"sheduler",
		true,
		false,
		false,
		false,
		nil,
	)
	failOnError(err, "failed to declare a queue")

	msgs, err := ch.Consume(
		q.Name,
		"",
		true,
		false,
		false,
		false,
		nil,
	)
	failOnError(err, "failed to register a consumer")

	scheduler := gocron.NewScheduler(time.UTC)

	forever := make(chan bool)

	go func() {
		for d := range msgs {
			fmt.Println("fsdfdfd")
			var msg Message
			err := json.Unmarshal(d.Body, &msg)
			if err != nil {
				log.Printf("error parsing message: %s", err)
				continue
			}

			startTime := time.Now().Add(time.Duration(msg.Delay) * time.Second)
			scheduler.Every(1).Second().StartAt(startTime).Do(sendToQueue, msg.Content, msg.Queue)
		}
	}()

	scheduler.StartAsync()

	log.Printf(" [*] Waiting for messages. To exit press CTRL+C")
	<-forever
}

func sendToQueue(content string, queue string) {
	fmt.Println(content)

	conn, err := amqp.Dial("amqp://guest:guest@localhost:5672/")
	failOnError(err, "failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		queue,
		true,
		false,
		false,
		false,
		nil,
	)
	failOnError(err, "failed to declare a queue")

	err = ch.Publish(
		"",
		q.Name,
		false,
		false,
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(content),
		})
	failOnError(err, "failed to publish a message")

}
