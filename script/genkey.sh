export NGROK_DOMAIN=132g.net
cd tls

openssl genrsa -out ca.key 2048
openssl req -new -x509 -days 5000 -nodes -key ca.key -subj "/CN=$NGROK_DOMAIN" -extensions v3_ca -out ca.crt

# server 
openssl genrsa -out server.key 2048
openssl req -out server.csr -key server.key -new -subj "/CN=$NGROK_DOMAIN"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 5000

# client
openssl genrsa -out client.key 2048
openssl req -out client.csr -key client.key -new -subj "/CN=$NGROK_DOMAIN"
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 5000

cd - 
#rm *.key
#rm *.pem
#rm *.crt
#rm *.csr
