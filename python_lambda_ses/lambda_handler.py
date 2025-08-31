import os
import json
import html
import boto3

# Use SESv2 (recommended)
ses = boto3.client("sesv2", region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"))

FROM_EMAIL = os.environ.get("FROM_EMAIL")
DEFAULT_TO = os.environ.get("DEFAULT_TO")  # optional

def lambda_handler(event, context):
    """
    Expected payload (either direct event or API Gateway body):
    {
      "email": "recipient@example.com",
      "subject": "Hello",
      "message": "Welcome to our mailing list!"
    }
    """
    try:
        body = _parse_event(event)

        to_email = body.get("email") or DEFAULT_TO
        subject = body.get("subject", "Hello from Lambda + SES")
        message = body.get("message", "It works! ✅")

        if not FROM_EMAIL:
            return _resp(500, {"error": "Missing FROM_EMAIL env var"})
        if not to_email:
            return _resp(400, {"error": "Missing 'email' in payload and DEFAULT_TO not set"})

        # Build both Text and HTML bodies
        text_body = message
        html_body = f"<p>{html.escape(message)}</p>"

        ses.send_email(
            FromEmailAddress=FROM_EMAIL,
            Destination={"ToAddresses": [to_email]},
            Content={
                "Simple": {
                    "Subject": {"Data": subject},
                    "Body": {
                        "Text": {"Data": text_body},
                        "Html": {"Data": html_body}
                    }
                }
            }
        )

        return _resp(200, {"ok": True, "sent_to": to_email})
    except Exception as e:
        print("Error:", repr(e))
        return _resp(500, {"ok": False, "error": str(e)})

def _parse_event(event):
    """
    Supports:
    - Direct Lambda test: event is the JSON
    - API Gateway: event.body is JSON string
    """
    if not event:
        return {}
    if isinstance(event, dict) and "body" in event:
        try:
            return json.loads(event.get("body") or "{}")
        except json.JSONDecodeError:
            return {}
    if isinstance(event, str):
        try:
            return json.loads(event)
        except json.JSONDecodeError:
            return {}
    return event  # assume already a dict

def _resp(status, body):
    # Works for direct invoke or API Gateway (if you later add a trigger)
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body)
    }
