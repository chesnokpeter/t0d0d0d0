package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"sync"
	"time"

	"github.com/streadway/amqp"
)

type Message struct {
	Delay   int    `json:"delay"`
	Content string `json:"message"`
	Queue   string `json:"queue_after_delay"`
	SentAt  time.Time
}

type MessageQueue struct {
	mu       sync.Mutex
	messages []Message
}

func (mq *MessageQueue) Add(msg Message) {
	mq.mu.Lock()
	defer mq.mu.Unlock()
	mq.messages = append(mq.messages, msg)
}

func (mq *MessageQueue) RemoveExpired() []Message {
	mq.mu.Lock()
	defer mq.mu.Unlock()

	now := time.Now()
	var readyMessages []Message
	var remainingMessages []Message

	for _, msg := range mq.messages {
		if now.Sub(msg.SentAt) >= time.Duration(msg.Delay)*time.Second {
			readyMessages = append(readyMessages, msg)
		} else {
			remainingMessages = append(remainingMessages, msg)
		}
	}

	mq.messages = remainingMessages
	return readyMessages
}

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

var (
	rabbitURL = os.Getenv("RABBIT_URL")
	conn      *amqp.Connection
	ch        *amqp.Channel
)

func init() {
	var err error
	conn, err = amqp.Dial(rabbitURL)
	failOnError(err, "failed to connect to rabbitmq")

	ch, err = conn.Channel()
	failOnError(err, "failed to open a channel")
}

func main() {
	defer conn.Close()
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

	messageQueue := &MessageQueue{}

	go func() {
		for d := range msgs {
			var msg Message
			err := json.Unmarshal(d.Body, &msg)
			if err != nil {
				log.Printf("error parsing message: %s", err)
				continue
			}
			msg.SentAt = time.Now()
			messageQueue.Add(msg)
			fmt.Println(msg.Delay)
		}
	}()

	ticker := time.NewTicker(1 * time.Minute)
	defer ticker.Stop()

	for range ticker.C {
		readyMessages := messageQueue.RemoveExpired()
		for _, msg := range readyMessages {
			sendToQueue(msg.Content, msg.Queue)
		}
	}
}

func sendToQueue(content string, queue string) {
	q, err := ch.QueueDeclare(
		queue, // name
		true,  // durable
		false, // delete when unused
		false, // exclusive
		false, // no-wait
		nil,   // arguments
	)
	failOnError(err, "Failed to declare a queue")

	err = ch.Publish(
		"",     // exchange
		q.Name, // routing key
		false,  // mandatory
		false,  // immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(content),
		})
	failOnError(err, "Failed to publish a message")
}
