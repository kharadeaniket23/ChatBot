# 🛍️ E-commerce Sales Chatbot

A full-stack AI-powered chatbot system for product discovery and conversation history, featuring:

- Django REST Framework (Backend API)
- JWT Authentication (via SimpleJWT)
- React Frontend with secure token handling
- Chat interface with user-bot conversation history
- Product search and listing capabilities

---

## 📌 Features

- 🔐 User Registration & Login (JWT)
- 💬 AI Chatbot with basic intent detection
- 🛍️ Product search using name/description matching
- 🧠 Conversation logging per user (chat history)
- 🌐 Token-secured API endpoints
- 🎯 Postman-tested backend

---

## 📁 Project Structure

ecommerce-chatbot/
├── backend/
│ ├── manage.py
│ ├── chatbot/ # Django app with models, views, serializers
│ ├── users/ # Optional custom user app
│ └── ecommerce_api/ # Project settings
├── frontend/
│ ├── public/
│ └── src/
│ ├── App.jsx
│ ├── Login.jsx
│ ├── ChatbotInterface.jsx
│ └── ...

yaml
Copy
Edit

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ecommerce-chatbot.git
cd ecommerce-chatbot
2. Backend Setup
bash
Copy
Edit
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Start the server
python manage.py runserver
✅ Sample requirements.txt
txt
Copy
Edit
Django>=4.0
djangorestframework
djangorestframework-simplejwt
3. Frontend Setup (React)
bash
Copy
Edit
cd frontend
npm install
npm start
🔑 API Endpoints
Endpoint	Method	Description	Auth Required
/api/register/	POST	Register a new user	❌
/api/token/	POST	Get JWT token (login)	❌
/api/products/	GET	List all products	❌
/api/products/search/?q=	GET	Search products	❌
/api/chat/	POST	Send user message and get bot reply	✅
/api/conversation/	GET	Fetch user's chat history	✅

💻 Example Frontend: ChatbotInterface.jsx
jsx
Copy
Edit
useEffect(() => {
  axios.get("http://localhost:8000/api/conversation/", {
    headers: {
      Authorization: `Bearer ${user.token}`,
    }
  }).then(res => setMessages(res.data));
});

const handleSend = async () => {
  const res = await axios.post("http://localhost:8000/api/chat/", {
    message
  }, {
    headers: {
      Authorization: `Bearer ${user.token}`,
    }
  });

  setMessages([...messages, { sender: "user", message }, { sender: "bot", message: res.data.message }]);
};
🧪 Postman Testing
Register a new user:
POST http://localhost:8000/api/register/

Login to get token:
POST http://localhost:8000/api/token/

json
Copy
Edit
{
  "username": "testuser",
  "password": "testpass"
}
Add token to headers:
Authorization: Bearer <your-access-token>

🙋 Author
Developed by Aniket Kharade
🔗 LinkedIn
📧 kharadeaniket23@gmail.com
