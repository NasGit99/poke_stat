#!/bin/bash

aws ecr --region us-east-1 | docker login -u AWS -p <encrypted_token <repo_uri>

eval $(aws ecr get-login --region eu-west-1 --profile )



docker tag 6bafe78f8778 aws_account_id.dkr.ecr.us-east-1.amazonaws.com/pokestat:latest

