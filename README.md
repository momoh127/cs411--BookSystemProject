# cs411--BookSystemProject
CS411 Final Project - Personalized Book System

## Application Description:

This Personalized Book System allows users to manage their book collections and track their reading progress. Users can create accounts and log in to access their personal library. They can search for books by title, author, or keyword using the Google Books API, and view detailed information about each book. Users can add books to their library and organize them with statuses like **To read**. They can also update the status of books as they progress through them. 

The system provides features for:
- Adding books to the library
- Viewing the collection
- Updating the status of individual books

Additionally, it includes **health check** and **database check** routes to ensure the system is functioning correctly. This app is designed for anyone who wants an easy way to find books, organize their reading list, and track their progress.

---

## Routes:

### **Home Route**
- **Route:** `/`
- **Request Type:** `GET`
- **Purpose:** Home route for testing the API.
- **Request Body:** None
- **Success Response Example:**
  ```json
  {
    "message": "Welcome to the Personalized Book System API!"
  }

---

### **User Account Creation**
- **Route:** `/auth/create-account`
- **Request Type:** `POST`
- **Purpose:** Creates a new user account with a username and password.
- **Request Body:**
  - `username` (String): User’s chosen username.
  - `password` (String): User’s chosen password.
- **Success Response Example:**
  ```json
  {
    "message": "Account created successfully!"
  }
---

### **User Login**
- **Route:** `/auth/login`
- **Request Type:** `POST`
- **Purpose:** Allows users to log in to their account after providing their credentials.
- **Request Body:**
  - `username` (String): User’s username.
  - `password` (String): User’s password.
- **Success Response Example:**
  ```json
  {
    "message": "Login successful!",
    "user_id": 1
  }

---
### **Search for Books**
- **Route:** `/books/search`
- **Request Type:** `GET`
- **Purpose:** Search for books using the Google Books API.
- **Query Parameters:**
  - `q` (String): Book query (e.g., title, author, keyword).
- **Success Response Example:**
  ```json
  {
    "kind": "books#volumes",
    "items": [
      {
        "kind": "books#volume",
        "id": "string",
        "volumeInfo": {
          "title": "string",
          "authors": ["string"]
        }
      }
    ]
  }

---
### **Fetch Book Details**
- **Route:** `/books/details/<book_id>`
- **Request Type:** `GET`
- **Purpose:** Fetch details for a specific book using the Google Books API.
- **Path Parameter:**
  - `<book_id>`: The ID of the book to retrieve details for.
- **Success Response Example:**
  ```json
  {
    "volumeInfo": {
      "title": "string",
      "authors": ["string"],
      "publisher": "string",
      "publishedDate": "string"
    }
  }

---

### **Add Book to Library**
- **Route:** `/books/add-to-library`
- **Request Type:** `POST`
- **Purpose:** Adds a book to the user's library.
- **Request Body:**
  - `user_id` (Integer): User’s ID.
  - `book_id` (String): Book ID to add.
  - `status` (String, Optional): The status of the book (e.g., `To read`).
- **Success Response Example:**
  ```json
  {
    "message": "Book added to library successfully!"
  }

---
### **View User Library**
- **Route:** `/books/library/<int:user_id>`
- **Request Type:** `GET`
- **Purpose:** Retrieve the user's library with book details and statuses.
- **Path Parameter:**
  - `<user_id>`: The ID of the user whose library to retrieve.
- **Success Response Example:**
  ```json
  {
    "library": [
      {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "status": "To read"
      },
      {
        "title": "1984",
        "author": "George Orwell",
        "status": "Completed"
      }
    ]
  }

---

### **Update Book Status**
- **Route:** `/books/update-status`
- **Request Type:** `POST`
- **Purpose:** Update the status of a book in the user's library.
- **Request Body:**
  - `user_id` (Integer): User’s ID.
  - `book_id` (String): Book ID to update.
  - `status` (String): New status (e.g., `To read`, `Currently Reading`, `Completed`).
- **Success Response Example:**
  ```json
  {
    "message": "Book status updated successfully!"
  }

---

### **Health Check**
- **Route:** `/api/health`
- **Request Type:** `GET`
- **Purpose:** Verifies the service is running.
- **Success Response Example:**
  ```json
  {
    "status": "healthy"
  }

---

### **Database Check**
- **Route:** `/api/db-check`
- **Request Type:** `GET`
- **Purpose:** Verifies the database connection and checks if required tables exist.
- **Success Response Example:**
  ```json
  {
    "database_status": "healthy"
  }

---

## Dockerfile:

Docker provides a way to package your application and its dependencies into a container. Containers ensure consistent and portable environments across development, testing, and production.

### Prerequisites:
- Docker installed on your machine.
- Clone this repository.

---

### Building and Running the Docker Image:

#### Build the Docker image:
```bash
docker buildx build booksystemdockerfile -t flask-app .

#### Run the container:
```bash
docker run -p 5000:5000 --env-file apikeys.env flask-app

#### Access the application:
Once the container is running, you can access the application at: [http://localhost:5000/](http://localhost:5000/).

### Common Issues:

#### Port Already in Use:
Ensure no other application is using port `5000` and change the mapping if needed:
```bash
docker run -p 8080:5000 --env-file apikeys.env flask-app

#### Database Not Persisting:
To ensure that the database persists across container restarts, mount a volume for the database:
```bash
docker run -v $(pwd)/databases:/app/databases -p 5000:5000 --env-file apikeys.env flask-app

### Additional Information:

#### Stopping the Docker Container:
To stop the Docker container, run the following command:
```bash
docker stop <container_id>

#### Viewing Docker Logs:
To view logs from the running container, use the following command:
```bash
docker logs <container_id>

#### Removing the Docker Container:
To remove the container after stopping it, run the following command:
```bash
docker rm <container_id>

#### Removing Docker Volumes:
If you want to remove the volumes associated with the container (for example, to delete the database data), run the following command:
```bash
docker volume prune

---

### **Smoketest Script**
To ensure the application is functioning correctly, a **smoketest.sh** script is included. This script tests core functionalities like health checks, database connectivity, and essential API routes.


#### **Usage:

1. **Make the script executable:**
   ```bash
   chmod +x smoketest.sh

2. **Run the smoketest:**
   ```bash
   ./smoketest.sh

3. **Optional Arguments:**
   The smoketest script supports the following optional arguments:
   - `--echo-json`: Prints the JSON responses of each API request to the console for debugging.

   Example usage:
   ```bash
   ./smoketest.sh --echo-json

4. **Expected Output:**
   When the smoketest runs successfully, you will see output similar to the following in the terminal:
   ```plaintext
   Starting smoketests for Personalized Book System...
   Checking health status...
   Service is healthy.
   Checking database connection...
   Database connection is healthy.
   Testing user account creation...
   User account created successfully.
   Testing user login...
   Login successful.
   Testing book search...
   Book search successful.
   Testing book details retrieval...
   Book details retrieved successfully.
   Testing adding a book to the library...
   Book added successfully.
   Testing retrieving user library...
   User library retrieved successfully.
   Testing updating book status...
   Book status updated successfully.
   Smoketests complete. All routes are functional.

5. **Error Handling:**
   If any test fails during the smoketest, the script will:
   - Output a clear error message indicating which test failed.
   - Stop execution to allow immediate debugging.
   - Log details of the failure in `smoketest.log`.

   Example failure output:
   ```plaintext
   Starting smoketests for Personalized Book System...
   Checking health status...
   Health check failed.

6. **Log File Management:**
   - The `smoketest.log` file will store the results of each smoketest run, including timestamps, inputs, outputs, and error messages.
   - To prevent the log file from growing indefinitely, consider truncating it periodically:
     ```bash
     > smoketest.log
     ```
   - Alternatively, use a log rotation tool like `logrotate` to manage the log file automatically.

7. **Debugging and Re-Running Tests:**
   - After fixing an issue, you can re-run the smoketest to ensure all routes and functionalities are working.
   - To focus on a specific section, comment out unrelated tests in the `smoketest.sh` script.

   Example:
   ```bash
   # Uncomment to test only database and health routes
   # check_health
   # check_db

---

## Conclusion:

This Personalized Book System allows users to efficiently manage their book collection, track their reading progress, and access detailed information about books from the Google Books API. With Docker integration, you can ensure consistent and portable environments for development, testing, and production. Additionally, the smoketest script ensures that the application functions as expected after deployment.
