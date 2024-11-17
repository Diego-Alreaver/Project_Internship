# BarkGIF
## 🐾 About BarkGIF

BarkGIF is a fun and interactive RESTful API where you can search through different dog breeds! Use filters to find a breed that matches the characteristics you're looking for, then dive deeper by querying the breed to get its traits and a fun GIF showing that breed in action! Whether you're a dog lover or just curious, BarkGIF brings you closer to discovering the perfect pup with a bit of playful flair! 🐕🎉

**Enough of advertising, now the serious part:**  
**BarkGIF** is a RESTful API designed to showcase my backend development skills, implementing best practices while meeting project requirements. This project combines external API integrations, authentication, caching, and deployment, with a basic frontend integration for testing purposes.

---

## 🌟 Features

- **RESTful API**:
  - **GET `/breeds`**: Retrieves dog breeds from *The Dog API*. Includes optional filters by characteristics such as "loyal" or "friendly". Utilizes caching to optimize performance, with data stored for 24 hours.
  - **POST `/breeds/details/`**: Fetches details about a specific breed from *The Dog API* and includes a GIF from *Giphy API*. The response is serialized.
  - **GET `/search-history`**: A protected endpoint (JWT) that allows the admin to access the user search history.
  - **DELETE `/search-history`**: A protected endpoint allowing the admin to delete the entire search history.

- **Authentication and Authorization**:
  - Uses JWT for access token management.
  - Admin-only access to sensitive endpoints.

- **Interactive Documentation**:
  - Swagger-powered API documentation for easy exploration and testing.

- **Unit Testing**:
  - Automated tests to ensure the functionality of the API (`tests.py`).

---

## 🎯 Goals

1. Showcase backend development skills through a RESTful API.  
2. Efficiently integrate external APIs (*The Dog API* and *Giphy API*).  
3. Implement JWT-based authentication and authorization.  
4. Optimize performance using caching.  
5. Deploy a fully functional application using *Railway*.  
6. Utilize Swagger for clear and interactive API documentation.

---

## 💻 Tech Stack

- **Backend**: Django, Django REST Framework.  
- **Frontend**: HTML, CSS.
- **Authentication**: JWT.
- **External APIs**: 
  - [The Dog API](https://thedogapi.com).  
  - [Giphy API](https://developers.giphy.com).  
- **Caching**: Django Core Cache.
- **Documentation**: Swagger.  
- **Testing**: Django APITestCase.  
- **Deployment**: Railway.  

---

## 🌐 Deployment

The project is deployed on **Railway** and accessible at:  
[https://projectinternship-production.up.railway.app](https://projectinternship-production.up.railway.app)

### Important Notes for Testing:
- Upon opening the website, you will be automatically redirected to the **Swagger** documentation for easy testing of the API endpoints.
- To test the **search-history** endpoint, you will need an **admin token**. For convenience, a superuser admin has been created. Put these credentials on /token/:
   - **Username**: `admin`
   - **Password**: `admin`
   
   Using the these login credentials you can obtain the access token. The token can be found under the **access** field. 
   - To use the token, click on **Authorize** in the Swagger UI and enter the token in the following format:  
     `Bearer <your-token-here>` (Example: `Bearer LO68qqaW`).

- The token is **necessary** to access the **search-history** endpoint as it is protected by JWT authentication.
  
### Optional Web Interface for POST Endpoint:
- If you prefer testing the **POST** endpoint `breeds/details/` through a graphical interface, you can visit:  
  [https://projectinternship-production.up.railway.app/api/webpage](https://projectinternship-production.up.railway.app/api/webpage)
**Note**: Please be aware that the interface is quite simple, as frontend is not my strong suit.

---

## 🚀 How to Run (locally)

### Prerequisites
- Python 3.10+
- Pipenv for dependency management.

### Steps
1. Clone the repository:
   git clone https://github.com/Diego-Alreaver/](https://github.com/Diego-Alreaver/Project_Internship.git
   
3. Set up a virtual environment with pipenv:
   pipenv install
   pipenv shell
   
4. Configure environment variables:
   In a .env inside the root of the project add this:
       GIPHY_API_KEY= yourgiphykey
       Django_KEY= "yourdjangokey"
       DJANGO_DEVELOPMENT=True
      
5. Run migrations and start the server:
   python manage.py migrate
   python manage.py runserver

6. Access Swagger documentation:
   Visit http://127.0.0.1:8000/swagger/

Next steps are optional:
Run unit tests: python manage.py test
Access frontend webpage: http://127.0.0.1:8000/api/webpage/

---

### Images
**Swagger documentation**
![image](https://github.com/user-attachments/assets/94a703d7-2d73-499c-a3f6-eb3585d80004)

**Endpoint response**
![image](https://github.com/user-attachments/assets/917368d9-ce26-4b5d-9caa-a7283afefbdd)

**Response using filters**
![image](https://github.com/user-attachments/assets/632c8548-2574-4c8b-8a8a-5cc70960d0ef)

**Testing on GUI**
![image](https://github.com/user-attachments/assets/e38468c1-d260-4220-abb1-ca1a3114fcf1)

