# genai/recommendation.py
import random
import numpy as np
from datetime import datetime

class RecommendationEngine:
    """
    Simulates a Generative AI recommendation engine that would
    typically be implemented using SAP's Generative AI Hub
    """
    
    def __init__(self, mock_data_provider):
        self.mock_data = mock_data_provider
        # Simulate a vector embedding space for products
        self.product_embeddings = {}
        self._generate_product_embeddings()
    
    def _generate_product_embeddings(self):
        """Create simulated vector embeddings for products"""
        for product in self.mock_data.products:
            # Generate a random 128-dimensional vector for each product
            # In a real system, these would be semantic embeddings from an LLM
            embedding = np.random.normal(0, 1, 128)
            # Normalize the vector
            embedding = embedding / np.linalg.norm(embedding)
            self.product_embeddings[product['product_id']] = embedding
    
    def _get_customer_profile_vector(self, customer_id):
        """Generate a customer profile vector based on purchase history"""
        # Find the customer
        customer = next((c for c in self.mock_data.customers if c['customer_id'] == customer_id), None)
        if not customer:
            return np.zeros(128)
        
        # Find transactions for this customer
        customer_transactions = [t for t in self.mock_data.transactions 
                                 if t['customer_id'] == customer_id]
        
        if not customer_transactions:
            # For customers with no transactions, generate a random profile
            profile_vector = np.random.normal(0, 0.5, 128)
            return profile_vector / np.linalg.norm(profile_vector)
        
        # Create a profile vector based on purchased products
        profile_vector = np.zeros(128)
        purchased_products = []
        
        for transaction in customer_transactions:
            for item in transaction['items']:
                purchased_products.append(item['product_id'])
        
        # Add the embeddings of all purchased products
        for product_id in purchased_products:
            if product_id in self.product_embeddings:
                profile_vector += self.product_embeddings[product_id]
        
        # Normalize if not zero
        if np.linalg.norm(profile_vector) > 0:
            profile_vector = profile_vector / np.linalg.norm(profile_vector)
            
        return profile_vector
    
    def generate_recommendations(self, customer_id, count=5):
        """Generate personalized product recommendations with explanations"""
        # Get customer profile vector
        profile_vector = self._get_customer_profile_vector(customer_id)
        
        # Find purchased products to exclude them 
        customer_transactions = [t for t in self.mock_data.transactions 
                                 if t['customer_id'] == customer_id]
        purchased_product_ids = set()
        
        for transaction in customer_transactions:
            for item in transaction['items']:
                purchased_product_ids.add(item['product_id'])
        
        # Calculate similarity scores for all products
        similarity_scores = []
        for product in self.mock_data.products:
            product_id = product['product_id']
            
            # Skip already purchased products
            if product_id in purchased_product_ids:
                continue
                
            if product_id in self.product_embeddings:
                similarity = np.dot(profile_vector, self.product_embeddings[product_id])
                # Add some randomness to make it more interesting
                adjusted_similarity = similarity * random.uniform(0.9, 1.1)
                
                similarity_scores.append((product, adjusted_similarity))
        
        # Sort by similarity and take top-N
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        top_products = [item[0] for item in similarity_scores[:count]]
        
        # Generate explanations for each recommendation
        recommendations = []
        for product in top_products:
            # Simulate GenAI-generated explanation
            category_reason = f"based on your interest in {product['category']} products"
            price_range = "premium" if product['base_price'] > 500 else "mid-range" if product['base_price'] > 100 else "budget-friendly"
            price_reason = f"this {price_range} item matches your typical spending patterns"
            
            random_reasons = [
                "the seasonal trends in your shopping history",
                "complementary products to your recent purchases",
                "popular items among customers with similar preferences",
                "your browsing activity for similar items"
            ]
            
            explanation = f"Recommended {product['name']} {category_reason} and {random.choice(random_reasons)}. Additionally, {price_reason}."
            
            recommendations.append({
                "product": product,
                "explanation": explanation,
                "relevance_score": round(random.uniform(0.7, 0.99), 2)
            })
            
        return {
            "customer_id": customer_id,
            "recommendations": recommendations,
            "generated_at": datetime.now().isoformat(),
            "model_used": "GPT-4 (simulated)",
            "recommendation_type": "personalized"
        }
