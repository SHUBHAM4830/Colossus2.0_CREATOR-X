🌾 KRISHIBAZAAR
KRISHIBAZAAR is a smart, multilingual web application designed to bridge the gap between farmers and buyers by removing middlemen and enabling direct transactions. Built with Django, it features crop listings, live bidding, multilingual crop recommendations, buyer demands, and more — making agriculture more accessible, profitable, and efficient.

🔥 Key Features
👨‍🌾 Farmer & Buyer Portals – Separate dashboards with role-based access

🧠 Crop Recommendation System – Predicts suitable crops based on soil and climate data

🌐 Multilingual Interface – Farmers can use the app in their preferred language

📦 Crop Listings (CRUD) – Farmers can upload, edit, and delete crop listings

📢 Buyer Demand Notifications – Buyers can post demands, farmers get alerts

💰 Live Bidding System – Real-time bidding for crops

📈 Soil Testing Input – Farmers can enter soil parameters to get recommendations

🎨 Fully responsive UI using Tailwind CSS

🛠️ Tech Stack
Backend: Python, Django, SQLite

Frontend: HTML5, Tailwind CSS, JavaScript (AJAX)

Machine Learning: Scikit-learn, joblib (crop recommendation model)

Multilingual Support: Django’s i18n and translation files

Database: SQLite (easily upgradeable to PostgreSQL or MySQL)

📁 Folder Structure
bash
Copy
Edit
krishibazaar/
├── crop_recommendation/
│   └── model.pkl  # Trained ML model
├── static/
│   └── (CSS, JS, Images)
├── templates/
│   ├── dashboard_farmer.html
│   ├── dashboard_buyer.html
│   └── crop_recommendation.html
├── users/
│   └── (User auth, roles)
├── manage.py
├── README.md
└── requirements.txt
🚀 Getting Started
bash
Copy
Edit
# Clone the repository
git clone https://github.com/yourusername/krishibazaar.git
cd krishibazaar

# Create and activate a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install the dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
Open your browser:
👉 http://127.0.0.1:8000/

📸 Screenshots
Farmer Dashboard	Buyer Dashboard	Crop Recommendation
🤖 Crop Recommendation API
POST /get_crop/
Input Parameters:

json
Copy
Edit
{
  "N": 80,
  "P": 40,
  "K": 35,
  "temperature": 28.0,
  "humidity": 75.0,
  "ph": 6.5,
  "rainfall": 100.0
}
Response:

json
Copy
Edit
{
  "crop": "rice"
}
🌍 Languages Supported
English

Hindi

Marathi

Bengali (add more as needed)

Farmers can switch language preferences via a simple dropdown on the dashboard.

🔐 Role-Based Access
Farmers can:

Add/Edit/Delete crops

View buyer demands

Participate in bidding

Use crop recommendation

Buyers can:

View listed crops

Post demands

Participate in live bidding

🚧 Future Scope
Integration with real-time weather/soil APIs

Payment gateway for secure transactions

Live chat between farmers and buyers

Mobile app (Flutter/React Native)

Admin dashboard for analytics & moderation

🙏 Acknowledgements
Crop dataset from Kaggle

Django Docs

Tailwind CSS

OpenWeatherMap API (optional integration)

👨‍💻 Author
Creator-X

If you like this project, ⭐ the repo and share it with your peers!

