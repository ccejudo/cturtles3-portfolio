#!/bin/bash
# Script to test backend routes of the portfolio

printf '########## Testing route: /register \t Method: GET ##########\n'
curl -s -D - 'https://mlh-cristopher-portfolio.duckdns.org/register'
printf '\n\n'

printf '########## Testing route: /login \t Method: GET ##########\n'
curl -s -D - 'https://mlh-cristopher-portfolio.duckdns.org/login'
printf '\n\n'

printf '########## Testing route: /register \t Method: POST ##########\n'
printf '#### Testing NO user NO password ###\n'
curl -s -D - --request POST 'https://mlh-cristopher-portfolio.duckdns.org/register'
printf '\n\n'
printf '#### Testing NO password ###\n'
curl -s -D - -X POST -d 'username=test' 'https://mlh-cristopher-portfolio.duckdns.org/register'
printf '\n\n'

printf '########## Testing route: /login \t Method: POST ##########\n'
printf '#### Testing NO user NO password ###\n'
curl -s -D - --request POST 'https://mlh-cristopher-portfolio.duckdns.org/login'
printf '\n\n'
printf '#### Testing INCORRECT user ###\n'
curl -s -D - -X POST -d 'username=test' 'https://mlh-cristopher-portfolio.duckdns.org/login'
printf '\n\n'
