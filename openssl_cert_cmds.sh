# Root CA Certificate
# Root Key
openssl genrsa -out CAroot.key 2048

# Root CSR
openssl req -new -key CAroot.key -out CAroot.csr

# Root Certificate
openssl req -x509 -days 1825 -key CAroot.key -in CAroot.csr -out CAroot.crt
cat CAroot.crt CAroot.key > CAroot.pem

# Server Certificate
# Server Key
openssl genrsa -out server11.key 2048

# Server CSR
openssl req -new -key server11.key -out serverX.csr

# Server Certificate
openssl x509 -req -days 1825 -in serverX.csr -CA CAroot.pem -CAkey CAroot.key -CAcreateserial -out serverX.crt
cat serverX.crt serverX.key > serverX.pem
