#!/bin/sh

set -e

CERT_DIR="/certs"

if [ ! -f "$CERT_DIR/mosquitto.crt" ]; then
  echo "[cert-gen] 🔐 Gerando certificado TLS..."

  openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout "$CERT_DIR/mosquitto.key" \
    -out "$CERT_DIR/mosquitto.crt" \
    -subj "/CN=mqtt-broker"

  chmod 600 "$CERT_DIR/mosquitto.key"
  chmod 644 "$CERT_DIR/mosquitto.crt"

  echo "[cert-gen] ✅ Certificado gerado com sucesso."
else
  echo "[cert-gen] ✔ Certificado já existe, pulando..."
fi
