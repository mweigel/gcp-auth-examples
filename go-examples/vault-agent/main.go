package main

import (
	"context"
	"encoding/json"
	"flag"
	"io"
	"os"
	"time"

	"cloud.google.com/go/storage"
	"golang.org/x/oauth2"
	"google.golang.org/api/option"
)

// Type representing the token data acquired from Vault agent.
type TokenData struct {
	ExpiresAtSeconds int64  `json:"expires_at_seconds"`
	Token            string `json:"token"`
	TokenTTL         int64  `json:"token_ttl"`
}

type FileTokenSource struct {
	path string
}

func (ts FileTokenSource) readToken() (*TokenData, error) {
	jsonFile, err := os.Open(ts.path)
	if err != nil {
		return nil, err
	}
	defer jsonFile.Close()

	jsonData, err := io.ReadAll(jsonFile)
	if err != nil {
		return nil, err
	}

	tokenData := &TokenData{}

	err = json.Unmarshal([]byte(jsonData), tokenData)
	if err != nil {
		return nil, err
	}

	return tokenData, nil
}

func (ts FileTokenSource) Token() (*oauth2.Token, error) {
	tokenData, err := ts.readToken()
	if err != nil {
		return nil, err
	}

	oauth2Token := &oauth2.Token{
		AccessToken: tokenData.Token,
		Expiry:      time.Unix(tokenData.ExpiresAtSeconds, 0),
	}

	return oauth2Token, nil
}

func newTokenSource(path string) *FileTokenSource {
	return &FileTokenSource{
		path: path,
	}
}

func upload_blob(tokenSource *FileTokenSource, project, bucket, source, destination string) {
	ctx := context.Background()
	client, err := storage.NewClient(ctx, option.WithTokenSource(tokenSource))
	if err != nil {
		panic("Could not create storage client.")
	}

	wc := client.Bucket(bucket).Object(destination).NewWriter(ctx)
	defer wc.Close()

	wc.Write([]byte("This is a test."))
}

func main() {
	project := flag.String("project", "", "GCP project")
	bucket := flag.String("bucket", "", "Destination bucket")
	source := flag.String("source", "", "Source file name")
	destination := flag.String("destination", "", "Destination file name")
	token := flag.String("token", "", "Token file name")

	flag.Parse()

	tokenSource := newTokenSource(*token)
	upload_blob(tokenSource, *project, *bucket, *source, *destination)
}
