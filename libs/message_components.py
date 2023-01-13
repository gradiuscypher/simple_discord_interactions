import logging
import traceback
from flask import jsonify, make_response


def split(request):
    action = request.json['data']['custom_id'].split("_")[1]

    data = {
        "type": 4,
        "data": {
            "content": f"You pushed the {action} button"
        }
    }
    return make_response(data, 200)


def parse(request):
    try:
        # ref: https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-types
        match request.json['data']['component_type']:
            # BUTTON_PRESS
            case 2:
                custom_id = request.json['data']['custom_id']

                match custom_id.split("_")[0]:
                    case "spawn": return split(request)
                    case other:
                        logging.debug(f"custom_id for button not implemented: {custom_id}")
                        return make_response("", 500)
            case other:
                logging.debug(f"MESSAGE_COMPONENT not implemented: {custom_id}")
                return make_response("", 500)

    except:
        print(traceback.format_exc())
