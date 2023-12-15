package main

import (
	"context"
	"fmt"
	"log"
	"math/rand"
	"time"

	"github.com/go-faker/faker/v4"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// Data struct represents the structure of the document
type Data struct {
	Name  string `faker:"name"`
	Email string `faker:"email"`
	Job   string
	Text  string `faker:"sentence"`
}

// getRandomCollectionNames returns a random subset of collection names
func getRandomCollectionNames(collectionNames []string) []string {
	rand.Seed(time.Now().UnixNano())
	numCollections := rand.Intn(3) + 2 // Between 2 and 4 collections
	return collectionNames[:numCollections]
}

func main() {
	// MongoDB connection parameters
	clientOptions := options.Client().ApplyURI("mongodb://192.168.1.31:27017")
	client, err := mongo.Connect(context.Background(), clientOptions)
	if err != nil {
		log.Fatal(err)
	}
	defer client.Disconnect(context.Background())

	// Database and collection names
	dbNames := []string{"go1", "go2", "go3", "go4"}
	collectionNames := []string{"test1", "test2", "test3", "test4"}

	// Create a Faker instance
	faker.SetRandomMapAndSliceSize(10)

	// Iterate over databases
	for _, dbName := range dbNames {
		// Get the database
		db := client.Database(dbName)

		// Get a random subset of collection names
		collectionSubset := getRandomCollectionNames(collectionNames)

		// Iterate over collections
		for _, collectionName := range collectionSubset {
			// Get the collection
			collection := db.Collection(collectionName)

			// Track the current size of the data
			currentSize := 0

			// Define the target size (in bytes)
			targetSize := rand.Intn(10*1024*1024) + 1024*1024 // Between 10 MB and 100 MB

			// Iterate until the target size is reached
			for currentSize < targetSize {
				// Generate a document with random data
				var data Data
				data.Job = faker.TitleMale() // Manually set the job field
				err := faker.FakeData(&data)
				if err != nil {
					log.Fatal(err)
				}

				// Insert the document into the collection
				_, err = collection.InsertOne(context.Background(), data)
				if err != nil {
					log.Fatal(err)
				}

				// Update the current size of the data
				currentSize += len(fmt.Sprintf("%v", data))
			}
		}
	}
	fmt.Println("Data generation completed.")
}
