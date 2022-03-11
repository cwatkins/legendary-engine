import os
import stripe
import json
from flask import Flask, jsonify, request

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe.api_version = "2020-08-27;terminal_server_driven_beta=v1"
app = Flask(__name__, static_url_path='/static')

READERS = {}


@app.route("/list-products", methods=['GET'])
def get_products():
    try:
        with open('db.json') as json_file:
            data = json.load(json_file)
            return jsonify({"product_list": data})
    except Exception as e:
        return jsonify({"error": {"message": str(e)}})


@app.route("/create-location", methods=['POST'])
def create_location():
    try:
        request_json = request.json
        display_name = request_json.get("display_name")
        address = request_json.get("address")
        new_location = stripe.terminal.Location.create(
            display_name=display_name,
            address={
                "line1": address.get("line1"),
                "line2": address.get("line2"),
                "city": address.get("city"),
                "state": address.get("state"),
                "country": address.get("country"),
                "postal_code": address.get("postal_code"),
            }
        )
        return jsonify({"location": new_location})
    except stripe.error.StripeError as e:
        return jsonify({"error": {"message": str(e)}}), 400
    except Exception as e:
        return jsonify({"error": {"message": str(e)}}), 400


@app.route("/list-terminal-locations", methods=['GET'])
def list_locations():
    try:
        limit = request.args.get("limit")
        locations = stripe.terminal.Location.list(limit=limit)
        return jsonify({"locations": locations})
    except stripe.error.StripeError as e:
        return jsonify({"error": {"message": str(e)}})
    except Exception as e:
        return jsonify({"error": {"message": str(e)}})


@app.route("/retrieve-terminal-reader", methods=['GET'])
def retrieve_reader():
    try:
        reader_id = request.args.get("reader_id")
        reader_state = stripe.terminal.Reader.retrieve(reader_id)
        return jsonify({"reader_state": reader_state})
    except stripe.error.StripeError as e:
        return jsonify({"error": {"message": str(e)}})
    except Exception as e:
        return jsonify({"error": {"message": str(e)}})


@app.route("/register-terminal-reader", methods=['POST'])
def register_reader():
    try:
        request_json = request.json
        registration_code = request_json.get('registration_code')
        label = request_json.get('label')
        location = request_json.get('location')
        new_reader = stripe.terminal.Reader.create(
            registration_code=registration_code,
            label=label,
            location=location
        )
        return jsonify({"reader": new_reader})
    except stripe.error.StripeError as e:
        return jsonify({'error': {'message': str(e)}}), 400
    except Exception as e:
        return jsonify({'error': {'mesage': str(e)}}), 400


@app.route("/list-terminal-readers", methods=['GET'])
def list_terminal_readers():
    try:
        readers_list = stripe.terminal.Reader.list(limit=3)
        return jsonify({"readers": readers_list.data})
    except stripe.error.StripeError as e:
        return jsonify({'error': {'message': str(e)}}), 400
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


@app.route("/process-payment-intent", methods=['POST'])
def process_payment_intent():
    try:
        request_json = request.get_json()
        payment_intent_id, reader = request_json.get(
            'payment_intent_id'), request_json.get('reader_id')
        reader_state = stripe.terminal.Reader.process_payment_intent(
            reader,
            payment_intent=payment_intent_id,
        )
        return jsonify({'reader_state': reader_state})
    except stripe.error.StripeError as e:
        return jsonify({'error': {'message': str(e)}}), 400
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


@app.route("/cancel-terminal-action", methods=['POST'])
def cancel_terminal_action():
    try:
        request_json = request.get_json()
        reader = request_json.get('reader_id')
        reader_state = stripe.terminal.Reader.cancel_action(
            reader
        )
        return jsonify({'reader_state': reader_state})
    except stripe.error.StripeError as e:
        return jsonify({'error': {'message': str(e)}}), 400
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


@app.route("/create-payment-intent", methods=['POST'])
def create_payment_intent():
    try:
        amount = request.get_json().get('amount')
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            payment_method_types=["card_present"],
            capture_method="manual"
        )
        return jsonify({'payment_intent_id': payment_intent.id})
    except stripe.error.StripeError as e:
        return jsonify({'error': {'message': str(e)}}), 400
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


@app.route("/simulate-terminal-payment", methods=['POST'])
def simulate_terminal_payment():
    try:
        reader_id = request.get_json().get('reader_id')
        reader = stripe.test_helpers.SimulatedReader.simulate_payment(
            reader_id)
        return jsonify({'reader_state': reader})
    except stripe.error.StripeError as e:
        return jsonify({'error': {'message': str(e)}}), 400
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


@app.route("/capture-payment-intent", methods=['POST'])
def capture_payment_intent():
    try:
        payment_intent_id = request.get_json().get('payment_intent_id')
        payment_intent = stripe.PaymentIntent.capture(payment_intent_id)
        return jsonify({'payment_intent': payment_intent.id})
    except stripe.error.StripeError as e:
        return jsonify({'error': {'message': str(e)}}), 400
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


@app.route("/stream", methods=['GET'])
def stream():
    # While True send events for the reader
    return


if __name__ == '__main__':
    app.run(port=4242, debug=True)
