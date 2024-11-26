WEBHOOK_SECRET='d9ded68b21e8ab8a5a135918554897f11c13784301b77f61a6ad93ba7c6a6927'
WEBHOOK_URL='https://magi-chamber.fly.dev/webhook' 
# WEBHOOK_URL='https://localhost:8888/webhook'

PAYLOAD='{}'  # Empty JSON payload
SIGNATURE='sha256='$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$WEBHOOK_SECRET" | sed 's/^.* //')
curl -X POST \
-H "Content-Type: application/json" \
-H "X-Hub-Signature-256: $SIGNATURE" \
-d "$PAYLOAD" \
"$WEBHOOK_URL"