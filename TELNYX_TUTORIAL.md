# Telnyx Integration Tutorial

This guide explains how to configure the Phone Calling Agents Course to use Telnyx for telephony services.

## Overview

Telnyx is a global communications platform offering SIP trunking, programmable voice, and SMS services. You can use Telnyx as an alternative to Twilio for receiving and making phone calls.

## Prerequisites

1.  **Telnyx Account**: Sign up at [portal.telnyx.com](https://portal.telnyx.com).
2.  **Connection (SIP Trunk)**: Create a Connection in the Telnyx Mission Control Portal.
3.  **Phone Number**: Purchase a phone number and associate it with your Connection.
4.  **XML Controller**: Configure the webhook URL in your Connection's "XML Controller" settings.

## Configuration

Update your `.env` file with your Telnyx credentials:

```bash
TELNYX__ACCOUNT_SID=YOUR_CONNECTION_SID
TELNYX__API_KEY=YOUR_API_KEY_V2
TELNYX__PHONE_NUMBER=+1234567890
```

*Note: The implementation requires mapping the Telnyx API to the existing Twilio interface. See `src/infrastructure/telephony/twilio.py` for details on extending the provider.*

## Resources

-   **Telnyx Dashboard**: https://portal.telnyx.com
-   **Programmable Voice**: https://developers.telnyx.com/api/v2/programmable-voice