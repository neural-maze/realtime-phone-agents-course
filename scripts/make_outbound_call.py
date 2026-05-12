"""
Interactive application to make outbound calls using the configured telephony provider.

This script provides a user-friendly interface to initiate calls through the API.
"""

import sys

import requests
from loguru import logger


def print_banner():
    """Print welcome banner."""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           📞  OUTBOUND CALL CENTER SYSTEM  📞            ║
║                                                           ║
║     Make AI-powered phone calls with ease!                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_section_header(title: str):
    """Print a section header."""
    print(f"\n{'═' * 60}")
    print(f"  {title}")
    print(f"{'═' * 60}\n")


def get_input(prompt: str, example: str = "", validator=None) -> str:
    """
    Get user input with validation.

    Args:
        prompt: Prompt text to display
        example: Example value to show
        validator: Optional validation function

    Returns:
        Validated user input
    """
    while True:
        if example:
            print(f"📝 {prompt}")
            print(f"   Example: {example}")
            value = input("   → ").strip()
        else:
            value = input(f"📝 {prompt}\n   → ").strip()

        if not value:
            print("   ❌ This field is required. Please enter a value.\n")
            continue

        if validator:
            is_valid, message = validator(value)
            if not is_valid:
                print(f"   ⚠️  {message}\n")
                retry = input("   Continue anyway? (y/n): ").strip().lower()
                if retry == "y":
                    return value
                continue

        return value


def validate_phone_number(number: str) -> tuple[bool, str]:
    """
    Validate phone number format.

    Args:
        number: Phone number to validate

    Returns:
        Tuple of (is_valid, message)
    """
    if not number.startswith("+"):
        return False, "Phone number should be in E.164 format (starting with +)"
    if len(number) < 10:
        return False, "Phone number seems too short"
    if not number[1:].replace(" ", "").isdigit():
        return False, "Phone number should only contain digits after the +"
    return True, ""


def validate_url(url: str) -> tuple[bool, str]:
    """
    Validate URL format.

    Args:
        url: URL to validate

    Returns:
        Tuple of (is_valid, message)
    """
    if not (url.startswith("http://") or url.startswith("https://")):
        return False, "URL should start with http:// or https://"
    return True, ""


def make_call(
    from_number: str,
    to_number: str,
    voice_agent_url: str,
    api_base_url: str = "http://localhost:8000",
) -> dict:
    """
    Initiate an outbound call through the API.

    Args:
        from_number: Provider phone number to call from
        to_number: Phone number to call to
        voice_agent_url: URL of the voice agent to connect to
        api_base_url: Base URL of the API

    Returns:
        Response dictionary containing the provider call identifier

    Raises:
        requests.exceptions.RequestException: If the API call fails
    """
    endpoint = f"{api_base_url}/call"

    payload = {
        "from": from_number,
        "to": to_number,
        "voice_agent_url": voice_agent_url,
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        error_detail = e.response.text if e.response is not None else str(e)
        raise Exception(f"HTTP error: {error_detail}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")


def confirm_details(from_number: str, to_number: str, voice_agent_url: str) -> bool:
    """
    Ask user to confirm the call details.

    Args:
        from_number: Provider phone number
        to_number: Recipient phone number
        voice_agent_url: Voice agent URL

    Returns:
        True if user confirms, False otherwise
    """
    print_section_header("📋 CONFIRM CALL DETAILS")
    print(f"   From (Provider):  {from_number}")
    print(f"   To (Recipient):   {to_number}")
    print(f"   Voice Agent URL:  {voice_agent_url}")
    print()

    while True:
        confirm = input("   Proceed with the call? (yes/no): ").strip().lower()
        if confirm in ["yes", "y"]:
            return True
        elif confirm in ["no", "n"]:
            return False
        print("   Please enter 'yes' or 'no'")


def main():
    """Main function to run the interactive call application."""
    # Disable loguru for cleaner output
    logger.remove()

    print_banner()

    print("Welcome! Let's set up your outbound call.\n")
    print("ℹ️  Phone numbers should be in E.164 format (e.g., +1234567890)")
    print(
        "ℹ️  Voice agent URL should be publicly accessible (e.g., via ngrok, Runpod, etc.)\n"
    )

    # Step 1: Get provider number
    print_section_header("STEP 1: Provider Phone Number")
    from_number = get_input(
        "Enter your provider phone number (the number to call FROM)",
        example="+11234567890",
        validator=validate_phone_number,
    )

    # Step 2: Get Voice Agent URL
    print_section_header("STEP 2: Voice Agent URL")
    voice_agent_url = get_input(
        "Enter your Voice Agent URL (where your API is running)",
        example="https://abc123.ngrok.io",
        validator=validate_url,
    )

    # Step 3: Get recipient number
    print_section_header("STEP 3: Recipient Phone Number")
    to_number = get_input(
        "Enter the phone number to call (the number to call TO)",
        example="+10987654321",
        validator=validate_phone_number,
    )

    # Step 4: Confirm and make the call
    if not confirm_details(from_number, to_number, voice_agent_url):
        print("\n❌ Call cancelled by user.\n")
        return 0

    print_section_header("📞 INITIATING CALL")
    print("   Please wait...\n")

    try:
        result = make_call(from_number, to_number, voice_agent_url)
        call_id = result.get("call_id") or result.get("sid", "Unknown")
        provider = result.get("provider", "configured provider")

        print("   ✅ SUCCESS! Call initiated successfully!\n")
        print(f"   📌 Provider: {provider}")
        print(f"   📌 Call ID: {call_id}")
        print(f"   📱 The phone at {to_number} should be ringing now...\n")
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║  Your call is connecting! Check your phone.              ║")
        print("╚═══════════════════════════════════════════════════════════╝\n")
        return 0

    except Exception as e:
        print("   ❌ ERROR: Failed to initiate call\n")
        print(f"   Details: {str(e)}\n")
        print("   Troubleshooting tips:")
        print("   • Make sure your API is running (http://localhost:8000)")
        print("   • Verify your telephony provider credentials in the .env file")
        print("   • Check that the voice agent URL is publicly accessible")
        print("   • Ensure phone numbers are in E.164 format\n")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user.\n")
        sys.exit(0)
