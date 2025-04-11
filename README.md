# 🌾 KRISHIBAZAAR

**KRISHIBAZAAR** is a smart, multilingual web application designed to bridge the gap between **farmers** and **buyers** by removing middlemen and enabling direct transactions. Built with **Django**, it features crop listings, live bidding, multilingual crop recommendations, buyer demands, and more — making agriculture more accessible, profitable, and efficient.

---

## 🔥 Key Features

- 👨‍🌾 **Farmer & Buyer Portals** – Separate dashboards with role-based access  
- 🧠 **Crop Recommendation System** – Predicts suitable crops based on soil and climate data  
- 🌐 **Multilingual Interface** – Farmers can use the app in their preferred language  
- 📦 **Crop Listings (CRUD)** – Farmers can upload, edit, and delete crop listings  
- 📢 **Buyer Demand Notifications** – Buyers can post demands, farmers get alerts  
- 💰 **Live Bidding System** – Real-time bidding for crops  
- 📈 **Soil Testing Input** – Farmers can enter soil parameters to get recommendations  
- 🎨 Fully responsive UI using **Tailwind CSS**

---

## 🛠️ Tech Stack

- **Backend**: Python, Django, SQLite  
- **Frontend**: HTML5, Tailwind CSS, JavaScript (AJAX)  
- **Machine Learning**: Scikit-learn, joblib (crop recommendation model)  
- **Multilingual Support**: Django’s `i18n` and translation files  
- **Database**: SQLite (easily upgradeable to PostgreSQL or MySQL)

---

## 📁 Folder Structure

```
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
```

---

## 🚀 Getting Started

```bash
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
```

Open your browser and go to:  
👉 `http://127.0.0.1:8000/`

---

## 📸 Screenshots

| Farmer Dashboard | Buyer Dashboard | Crop Recommendation |
|------------------|------------------|-----------------------|
| ![farmer](https://via.placeholder.com/300x180.png?text=Farmer+Dashboard) | ![buyer](https://via.placeholder.com/300x180.png?text=Buyer+Dashboard) | ![recommend](https://via.placeholder.com/300x180.png?text=Crop+Recommendation) |

*(Replace these placeholders with your own screenshots for better presentation)*

---

## 🤖 Crop Recommendation API

**POST** `/get_crop/`  
**Input Parameters:**

```json
{
  "N": 80,
  "P": 40,
  "K": 35,
  "temperature": 28.0,
  "humidity": 75.0,
  "ph": 6.5,
  "rainfall": 100.0
}
```

**Response:**

```json
{
  "crop": "rice"
}
```

---

## 🌍 Languages Supported

- English  
- Hindi  
- Marathi  
- Bengali  
*(More languages can be added easily)*

Users can change the language via a dropdown on the dashboard.

---

## 🔐 Role-Based Access

### 🧑‍🌾 Farmers Can:

- Add, edit, and delete crop listings  
- View buyer demands  
- Participate in live bidding  
- Use the crop recommendation tool

### 🧑‍💼 Buyers Can:

- View available crops  
- Post crop demands  
- Participate in live bidding

---

## 🚧 Future Scope

- Integration with real-time weather and soil APIs  
- Payment gateway integration  
- Real-time chat between farmers and buyers  
- Mobile app using Flutter or React Native  
- Admin dashboard for analytics and moderation

---

## 🙏 Acknowledgements

- Crop dataset from [Kaggle](https://www.kaggle.com/)  
- Django Documentation  
- Tailwind CSS  
- OpenWeatherMap API (optional)

---

## 👨‍💻 Author

**Your Name** – [CREATOR-X]

If you found this project useful, don’t forget to ⭐ the repo and share it with others!

---
