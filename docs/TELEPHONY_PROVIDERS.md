# Telephony Providers

The call center supports Twilio by default and Telnyx through TeXML.

## Select a provider

Set `TELEPHONY__PROVIDER` in `.env`:

```bash
TELEPHONY__PROVIDER=twilio
```

or:

```bash
TELEPHONY__PROVIDER=telnyx
```

The outbound helper still posts to the local `POST /call` endpoint. The API chooses the provider from configuration.

## Twilio

Twilio uses the existing credentials:

```bash
TWILIO__ACCOUNT_SID=YOUR_TWILIO_ACCOUNT_SID
TWILIO__AUTH_TOKEN=YOUR_TWILIO_AUTH_TOKEN
```

Outbound calls are created with the Twilio REST API and point at:

```text
https://your-public-url/voice/telephone/incoming
```

## Telnyx

Telnyx uses the TeXML REST API so the app can reuse the same FastRTC telephone stream endpoint.

```bash
TELEPHONY__PROVIDER=telnyx
TELNYX__API_KEY=YOUR_TELNYX_API_KEY
TELNYX__ACCOUNT_SID=YOUR_TELNYX_ACCOUNT_SID
TELNYX__APPLICATION_SID=YOUR_TELNYX_TEXML_APPLICATION_SID
TELNYX__WEBHOOK_PATH=/call/telnyx/events
```

Create a TeXML Application in Telnyx, then configure its XML request URL to:

```text
https://your-public-url/voice/telephone/incoming
```

Outbound calls are created with:

```text
POST https://api.telnyx.com/texml/Accounts/{account_sid}/Calls
```

The app sends `ApplicationSid`, `To`, `From`, `Url`, and status callback fields. Telnyx then fetches the TeXML from `/voice/telephone/incoming`, which returns `<Connect><Stream>` instructions for `/voice/telephone/handler`.

Telnyx signs webhooks with `Telnyx-Signature-Ed25519` and `Telnyx-Timestamp`. The first integration only acknowledges lifecycle events at `/call/telnyx/events`; add signature verification before relying on those events for sensitive state changes.
