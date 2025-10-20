#!/bin/bash

echo "Initializing SQS queues..."

# Create SQS queues
awslocal sqs create-queue --queue-name model-serving-queue
awslocal sqs create-queue --queue-name model-serving-dlq

# Create queue with attributes (e.g., dead letter queue configuration)
DLQ_ARN=$(awslocal sqs get-queue-attributes \
    --queue-url http://localhost:4566/000000000000/model-serving-dlq \
    --attribute-names QueueArn \
    --query 'Attributes.QueueArn' \
    --output text)

awslocal sqs set-queue-attributes \
    --queue-url http://localhost:4566/000000000000/model-serving-queue \
    --attributes '{
        "VisibilityTimeout": "5",
        "MessageRetentionPeriod": "86400",
        "RedrivePolicy": "{\"deadLetterTargetArn\":\"'$DLQ_ARN'\",\"maxReceiveCount\":\"3\"}"
    }'

echo "SQS queues created successfully:"
awslocal sqs list-queues

echo "LocalStack initialization complete!"
