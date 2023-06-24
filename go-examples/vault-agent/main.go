package main

import (
	"context"
	"fmt"

	"golang.org/x/oauth2"
	iam "google.golang.org/api/iam/v1"
	"google.golang.org/api/option"
)

type FileTokenSource struct{}

func (FileTokenSource) Token() (*oauth2.Token, error) {
	token := &oauth2.Token{
		AccessToken: "",
	}

	return token, nil
}

func main() {
	tokenSource := FileTokenSource{}
	service, err := iam.NewService(context.Background(), option.WithTokenSource(tokenSource))
	if err != nil {
		panic("Unable to create IAM service")
	}

	resource := "projects/-/serviceAccounts/"
	response, err := service.Projects.ServiceAccounts.Keys.List(resource).Do()
	if err != nil {
		panic("Unable to list service account keys")
	}

	for _, key := range response.Keys {
		fmt.Printf("Listing key: %v", key.Name)
	}
}
