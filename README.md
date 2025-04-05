# SAP-AI-Dynamic-Pricing-Engine
AI-powered product recommendations and dynamic pricing for SAP e-commerce systems (Prototype)

Overview 

This project demonstrates how e-commerce companies can leverage SAP's Generative AI Hub and SAP AI Core to implement personalized product recommendations and dynamic pricing strategies. It showcases a simulated integration with existing CRM systems to deliver AI-enhanced customer experiences. 

Important Note: This is a demonstration project intended for portfolio purposes and not a production-ready application. It simulates SAP's GenAI capabilities rather than connecting to actual SAP services. 

Key Features 

Personalized Product Recommendations: AI-generated product suggestions based on customer behavior and preferences 

Dynamic Pricing Engine: Intelligent price calculations using multiple market and customer factors 

Simulated CRM Integration: Demonstrates how the solution connects with existing customer data 

Interactive Web Interface: User-friendly dashboard for exploring AI capabilities 

Technologies Demonstrated 

- SAP Business Technology Platform (BTP) 

- SAP Generative AI Hub 

- SAP AI Core 

- Python Flask 

- AI-based recommendation algorithms 

- Dynamic pricing models 

Pricing Factors Explained :

The dynamic pricing engine uses five key factors to calculate optimal pricing: 

Inventory Factor: Reflects how current stock levels influence pricing 

Value = 1: Neutral impact (optimal inventory levels) 

Value > 1: Low inventory suggesting higher prices due to scarcity 

Value < 1: High inventory suggesting discounts to increase sales velocity 

Market Position Factor: Indicates positioning relative to competitor pricing 

Value = 1: Aligned with market average pricing 

Value > 1: Premium positioning above market average 

Value < 1: Competitive positioning below market average 

Demand Factor: Measures current market demand for the product 

Value = 1: Average demand with no adjustment 

Value > 1: High demand supporting price increases (e.g., 1.21 = 21% increase) 

Value < 1: Low demand requiring price reductions 

Customer Factor: Adjusts pricing based on customer segment 

Value = 1: Standard pricing for typical customers 

Value > 1: Premium customers may see higher prices for exclusive offerings 

Value < 1: Budget segment customers receive discounts (e.g., 0.93 = 7% discount) 

Seasonal Factor: Accounts for seasonal demand variations 

Value = 1: No seasonal impact 

Value > 1: In-season products can command higher prices 

Value < 1: Off-season products require discounting 

Installation 

# Clone the repository 
git clone https://github.com/yourusername/SAP-GenAI-Commerce-Suite.git 
 
# Navigate to the project directory 
cd SAP-GenAI-Commerce-Suite 
 
# Install dependencies 
pip install -r requirements.txt 
 
# Run the application 
python app.py 
 

Usage 

After starting the application, navigate to http://localhost:5000 to access the dashboard. From there you can: 

Try the recommendation engine by selecting different customer profiles 

Experiment with dynamic pricing by selecting various products and customers 

See how the AI explains its decision-making process 


Limitations 

This project is a simulation for demonstration purposes and has several limitations: 

Uses simulated AI decision-making rather than actual SAP AI services 

Works with generated mock data instead of real customer/product data 

Not optimized for production deployment or large-scale use 

Development Process 

This project was developed as a portfolio demonstration of SAP GenAI implementation skills. AI assistance (primarily through large language models) was used in the development process to generate code, design the application structure, and create the user interface. This collaborative approach mirrors modern development practices where AI tools augment developer capabilities. 

License 

MIT License 

Forme 

This project is not affiliated with or endorsed by SAP SE. All SAP product names are trademarks or registered trademarks of SAP SE or its affiliates. 
