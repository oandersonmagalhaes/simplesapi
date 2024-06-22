#!/bin/bash
awslocal kinesis create-stream --stream-name samplestream --shard-count  1
awslocal sns create-topic --name sampletopic
awslocal sqs create-queue --queue-name samplequeue
awslocal sqs create-queue --queue-name samplequeueb
awslocal sns subscribe --topic-arn arn:aws:sns:us-east-1:000000000000:sampletopic --protocol sqs --notification-endpoint arn:aws:sqs:us-east-1:000000000000:samplequeue
awslocal sns subscribe --topic-arn arn:aws:sns:us-east-1:000000000000:sampletopic --protocol sqs --notification-endpoint arn:aws:sqs:us-east-1:000000000000:samplequeueb
awslocal s3api create-bucket --bucket samplebucket