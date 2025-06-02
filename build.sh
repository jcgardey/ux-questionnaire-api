#!/bin/sh
docker build -t jcgardey/ux-questionnaire-api . --no-cache
docker push jcgardey/ux-questionnaire-api