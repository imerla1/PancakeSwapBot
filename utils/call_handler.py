from twilio.rest import Client


def make_phone_call(logger, from_, to):
    account_sid = "AC4c8726d79b68ea452ad74313bbe90b9a"
    auth_token = "94d14a624d52aa70e425a07125fbfbc4"
    client = Client(account_sid, auth_token)

    call = client.calls.create(
                            twiml='<Response><Say>Hello Master You have new alert Check it ASAP!</Say></Response>',
                            to=to,
                            from_=from_
                        )
    logger.debug(f"Making Phone Call From {from_} to {to}\n\tSid: {call.sid}")
