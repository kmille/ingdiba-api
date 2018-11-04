# Client for the Showcase API

docs: https://developer.ing.com/openbanking/get-started  

## Setup
1. Sign-up, create an app, subscribe to the Showcase API (described in https://developer.ing.com/openbanking/get-started)
2. Generate 2 certificates
    - One for the API-Server communication (client ssl)
    - openssl genrsa -out server1.key 2048
    - openssl req -sha256 -new -key server1.key -out server1.csr
    - openssl x509 -req -sha256 -days 365 -in server1.csr -signkey server.key -out server_public1.crt
    - one you sign your http requests with
    - openssl genrsa -out server2.key 2048
    - openssl req -sha256 -new -key server2.key -out server2.csr
    - openssl x509 -req -sha256 -days 365 -in server2.csr -signkey server2.key -out server_public2.crt
    - upload both
4. you have to wait until your app is activated (not in status: pending)
3. play arround with diba.py
