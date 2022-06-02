from twilio.rest import Client


def make_phone_call(account_sid,auth_token, logger, from_, to):
    client = Client(account_sid, auth_token)

    call = client.calls.create(
                            twiml='<Response><Say>Hello Master You have new alert Check it ASAP!</Say></Response>',
                            to=to,
                            from_=from_
                        )
    logger.debug(f"Making Phone Call From {from_} to {to}\n\tSid: {call.sid}")
