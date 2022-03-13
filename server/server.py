import os
import stripe
import json
from flask import Flask, jsonify, request

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe.api_version = "2020-08-27;terminal_server_driven_beta=v1"
app = Flask(__name__, static_url_path='/static')


@app.route("/list-products", methods=['GET'])
def get_products():
    try:
        with open('db.json') as json_file:
            data = json.load(json_file)
            return jsonify({"product_list": data})
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


if __name__ == '__main__':
    app.run(port=4242, debug=True)
