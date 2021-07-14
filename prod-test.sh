#!/bin/bash
# Script to test backend routes of the portfolio

domain='https://www.mlh-cristopher-portfolio.duckdns.org'
endpoints=("/" "/register" "/login" "/about/cristopher" "/about/nhi" "/about/yenyu" "/health")
error=0

sleep 1

for endpoint in "${endpoints[@]}"
do
    url="${domain}${endpoint}"
    status=$(curl -s -o /dev/null -w "%{http_code}" "${url}")

    printf "#### Testing route: ${endpoint} -> Status: ${status} ####\n"

    if [[ $status -ne 200 ]]
    then
        error=1
    fi   
done

exit $error