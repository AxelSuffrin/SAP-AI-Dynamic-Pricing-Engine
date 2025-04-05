# genai/pricing.py
import random
from datetime import datetime, timedelta

class DynamicPricingEngine:
    """
    Simulates a Generative AI pricing engine that would
    typically be implemented using SAP's Generative AI Hub
    """
    
    def __init__(self, mock_data_provider):
        self.mock_data = mock_data_provider
        # Generate simulated market conditions
        self._generate_market_conditions()
    
    def _generate_market_conditions(self):
        """Generate simulated market conditions for all products"""
        self.market_conditions = {}
        
        for product in self.mock_data.products:
            product_id = product['product_id']
            
            # Generate random market data
            self.market_conditions[product_id] = {
                "demand_index": random.uniform(0.7, 1.3),  # 1.0 is average
                "competitor_prices": [
                    round(product['base_price'] * random.uniform(0.85, 1.15), 2)
                    for _ in range(3)  # Simulate 3 competitors
                ],
                "seasonal_factor": random.uniform(0.9, 1.1),
                "trend": random.choice(["rising", "stable", "declining"]),
                "last_price_change": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
            }
    
    def generate_dynamic_price(self, product_id, customer_id):
        """
        Generate a dynamic price for a product based on market conditions
        and customer attributes. Simulates GenAI-based pricing logic.
        """
        # Find the product
        product = next((p for p in self.mock_data.products if p['product_id'] == product_id), None)
        if not product:
            return {"status": "error", "message": "Product not found"}
            
        # Find the customer
        customer = next((c for c in self.mock_data.customers if c['customer_id'] == customer_id), None)
        if not customer:
            return {"status": "error", "message": "Customer not found"}
        
        # Get base price and market conditions
        base_price = product['base_price']
        market = self.market_conditions.get(product_id)
        
        # Calculate pricing factors
        inventory_factor = 1.05 if product['current_stock'] < 20 else 0.95 if product['current_stock'] > 200 else 1.0
        
        avg_competitor_price = sum(market['competitor_prices']) / len(market['competitor_prices'])
        market_position_factor = (avg_competitor_price / base_price) * 0.5 + 0.5
        
        # Customer segment affects price sensitivity
        if customer['customer_segment'] == 'Premium':
            customer_factor = random.uniform(1.05, 1.1)  # Premium customers less price sensitive
        elif customer['customer_segment'] == 'Standard':
            customer_factor = random.uniform(0.95, 1.05)
        else:  # Budget
            customer_factor = random.uniform(0.9, 0.95)  # Budget customers more price sensitive
            
        demand_factor = market['demand_index']
        seasonal_factor = market['seasonal_factor']
        
        # Combine all factors
        pricing_factors = {
            "inventory_factor": round(inventory_factor, 2),
            "market_position_factor": round(market_position_factor, 2),
            "demand_factor": round(demand_factor, 2),
            "customer_factor": round(customer_factor, 2),
            "seasonal_factor": round(seasonal_factor, 2)
        }
        
        # Calculate raw price
        adjusted_price = base_price * inventory_factor * market_position_factor * demand_factor * customer_factor * seasonal_factor
        
        # Apply business rules - never go below 80% or above 120% of base price
        final_price = max(min(adjusted_price, base_price * 1.2), base_price * 0.8)
        
        # Generate explanation text using simulated GenAI
        price_change_pct = ((final_price / base_price) - 1) * 100
        direction = "increased" if price_change_pct > 0 else "decreased"
        
        explanation = f"The price for {product['name']} has been {direction} by {abs(price_change_pct):.1f}% "
        explanation += f"from the base price of ${base_price:.2f} to ${final_price:.2f}.\n\n"
        explanation += "This price takes into account several factors:\n"
        
        # Add factor explanations based on actual values
        if inventory_factor > 1:
            explanation += f"- Limited inventory (current stock: {product['current_stock']} units) suggests higher demand\n"
        elif inventory_factor < 1:
            explanation += f"- Abundant inventory (current stock: {product['current_stock']} units) suggests offering competitive pricing\n"
        
        # Add other explanations for each factor
        
        return {
            "product_id": product_id,
            "product_name": product['name'],
            "customer_id": customer_id,
            "customer_segment": customer['customer_segment'],
            "base_price": base_price,
            "dynamic_price": round(final_price, 2),
            "pricing_factors": pricing_factors,
            "competitor_prices": market['competitor_prices'],
            "explanation": explanation,
            "timestamp": datetime.now().isoformat(),
            "model_used": "GPT-4 (simulated)"
        }
