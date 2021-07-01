#!/bin/bash
# Script to test backend routes of the portfolio

domain='http://mlh-cristopher-portfolio.duckdns.org'
endpoints=("/" "/register" "/login" "/about/cristopher" "/about/nhi" "/about/yenyu" "/health")

for endpoint in "${endpoints[@]}"
do
    url="${domain}${endpoint}"
    printf "#### Testing route: ${endpoint} ####\n"
    curl -s -D - -o /dev/null "${url}"
done
