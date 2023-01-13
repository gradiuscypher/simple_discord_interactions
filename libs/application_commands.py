import logging
import traceback
from flask import jsonify, make_response


def demo():
    data = {
        "type": 4,
        "data": {
            "content": "This is a response to a demo string!"
        }
    }
    return make_response(data, 200)


def spawn_buttons():
    data = {
        "type": 4,
        "data": {
            "content": "Here's a message with three buttons.",
            "components": [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "Push Me!",
                            "style": 1,
                            "custom_id": "spawn_pushme"
                        },
                        {
                            "type": 2,
                            "style": 4,
                            "label": "Don't Push Me!",
                            "custom_id": "spawn_dontpush"
                        },
                        {
                            "type": 2,
                            "style": 2,
                            "label": "Disabled",
                            "custom_id": "spawn_disabled",
                        }
                    ]
                }
            ]
        }
    }
    return make_response(jsonify(data), 200)


def not_implemented():
    data = {
        "type": 4,
        "data": {
            "content": "This command doesn't seem to be implemented."
        }
    }
    return make_response(data, 200)


def parse(request):
    try:
        # ref: https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-types
        match request.json['data']['type']:
            # CHAT_INPUT
            case 1:
                match request.json['data']['name']:
                    case "demo": return spawn_buttons()
                    case other: return not_implemented()

            # USER
            case 2:
                logging.debug(f"USER not implemented: {request.json}")
                return make_response("", 500)

            # MESSAGE
            case 3:
                logging.debug(f"MESSAGE not implemented: {request.json}")
                return make_response("", 500)

            case other:
                logging.debug(f"ApplicationCommandType not implemented: {request.json}")
                return make_response("", 500)
    except:
        print(traceback.format_exc())
