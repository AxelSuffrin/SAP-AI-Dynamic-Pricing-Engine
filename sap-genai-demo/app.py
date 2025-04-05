# app.py
from flask import Flask, render_template, request, jsonify
import json
import os
from mock.sap_mock import SAPMockGenerator
from genai.recommendation import RecommendationEngine
from genai.pricing import DynamicPricingEngine

app = Flask(__name__)

# Initialize mock data
mock_data = SAPMockGenerator()
mock_data.generate_customer_data(100)
mock_data.generate_product_data(50)
mock_data.generate_transaction_data(1000)

# Save mock data to files
if not os.path.exists('data'):
    os.makedirs('data')
mock_data.export_to_json(filename_prefix="data/sap_mock_data")

# Initialize GenAI engines
recommendation_engine = RecommendationEngine(mock_data)
pricing_engine = DynamicPricingEngine(mock_data)

@app.route('/')
def index():
    """Main page showing the dashboard"""
    return render_template('index.html', 
                          customers=mock_data.customers[:10],
                          products=mock_data.products[:10])

@app.route('/api/recommendations/<customer_id>')
def api_recommendations(customer_id):
    """API endpoint to get personalized recommendations"""
    count = request.args.get('count', default=5, type=int)
    recommendations = recommendation_engine.generate_recommendations(customer_id, count)
    return jsonify(recommendations)

@app.route('/api/pricing/<product_id>/<customer_id>')
def api_dynamic_pricing(product_id, customer_id):
    """API endpoint to get dynamic pricing"""
    pricing = pricing_engine.generate_dynamic_price(product_id, customer_id)
    return jsonify(pricing)

@app.route('/recommendations')
def recommendations_page():
    """Page to display and test recommendations"""
    customer_id = request.args.get('customer_id', default=mock_data.customers[0]['customer_id'])
    return render_template('recommendations.html', 
                          customers=mock_data.customers,
                          current_customer_id=customer_id)

@app.route('/pricing')
def pricing_page():
    """Page to display and test dynamic pricing"""
    product_id = request.args.get('product_id', default=mock_data.products[0]['product_id'])
    customer_id = request.args.get('customer_id', default=mock_data.customers[0]['customer_id'])
    return render_template('pricing.html', 
                          products=mock_data.products,
                          customers=mock_data.customers,
                          current_product_id=product_id,
                          current_customer_id=customer_id)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
