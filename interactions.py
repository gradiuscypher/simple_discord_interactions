#!/usr/bin/env python3

import traceback
import logging
from os import environ
from flask import Flask, request, abort, jsonify, make_response
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from libs import application_commands, message_components

app = Flask(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

try:
    PUBLIC_KEY = environ["DISCORD_PUBKEY"]
except KeyError:
    print(traceback.format_exc())
    exit(1)


@app.route("/interact", methods=['GET', 'POST'])
def interactions():
    # if signatures from API request failed to validate, abort with 401
    if not validate_signatures(request):
        abort(401, "invalid signature")

    try:
        # ref: https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-type
        match request.json['type']:
            # PING
            case 1:
                return make_response(jsonify({"type": 1}), 200)

            # APPLICATION_COMMAND
            case 2:
                return application_commands.parse(request)

            # MESSAGE_COMPONENT
            case 3:
                return message_components.parse(request)

            # APPLICATION_COMMAND_AUTOCOMPLETE
            case 4:
                logging.debug(f"Unhandled APPLICATION_COMMAND_AUTOCOMPLETE: {request.json}")
                return make_response("", 404)

            # MODAL_SUBMIT
            case 5:
                logging.debug(f"Unhandled MODAL_SUBMIT: {request.json}")
                return make_response("", 404)

            case other:
                logging.debug(f"Unhandled request type: {request.json}")
                return make_response("", 404)

    except:
        print(traceback.format_exc())


def validate_signatures(request: request) -> bool:
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

    signature = request.headers["X-Signature-Ed25519"]
    timestamp = request.headers["X-Signature-Timestamp"]
    body = request.data.decode("utf-8")

    try:
        verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
        return True
    except BadSignatureError:
        return False


if __name__ == "__main__":
    app.run(port=8080)
