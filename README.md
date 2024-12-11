# cs411--BookSystemProject
CS411 Final Project - Personalized Book System

Application Description:

This Personalized Book System allows users to manage their book collections and track their reading progress. Users can create accounts and log in to access their personal library. They can search for books by title, author, or keyword using the Google Books API, and view detailed information about each book. Users can add books to their library and organize them with statuses like To read. They can also update the status of books as they progress through them. The system provides features for adding books to the library, viewing the collection, and updating the status of individual books. Additionally, it includes a health check route to ensure the system is working properly. This app is designed for anyone who wants an easy way to find books, organize their reading list, and track their progress.

Routes:

Route: / Request Type: GET Purpose: Home route for testing the API. Request Body: - Request Format: JSON Success Response Example: Code: 200 Content: {"message": "Welcome to the Personalized Book System API”} Example Request: { } Example Response: {"message": "Welcome to the Personalized Book System API! “status”: “200”}

Route: /create-account Request Type: POST Purpose: Creates a new user account with a username and password. Request Body: username (String): User’s chosen username. password (String): User’s chosen password. Request Format: JSON Success Response Example: Code: 201 Content: { "message": "Account created successfully!” } Example Request: { "username": "newuser123", "password": "securepassword" } Example Response: { "message": "Account created successfully”, "status": "201" }

Route: /login Request Type: POST Purpose: Allows user to login to their account after providing the username and password stored in the system. Request Body: username (String): User’s username. password (String): User’s password. Request Format: JSON Success Response Example: Code: 200 Content: { "message": "Login successful!”, “user_id”: user[0]} Example Request: { "username": "newuser123", "password": "securepassword" } Example Response: { "message": "Login successful!, “user_id”: 47382 "status": "200" }

Route: /search Request Type: GET Purpose: Search for books using the Google Books API. Request Body: q (String): Book query (e.g., title, author, keyword). Request Format: JSON Success Response Example: Code: 200 Content: { "kind": "books#volumes", "items": [ { "kind": "books#volume", "id": "string", "etag": "string", "selfLink": "string", "volumeInfo": { "title": "string", "authors": [ "string" ], ... },

	 "totalItems": number
	}
Example Request: { "q": "Flowers" } Example Response: { "kind": "books#volumes", "items": [ { "kind": "books#volume", "id": "_ojXNuzgHRcC", "etag": "OTD2tB19qn4", "selfLink": "https:// www.googleapis.com/books/v1/volumes/_ojXNuzgHRcC", "volumeInfo": { "title": "Flowers", "authors": [ "Vijaya Khisty Bodach" ], ... }, { "kind": "books#volume", "id": "RJxWIQOvoZUC", "etag": "NsxMT6kCCVs", "selfLink": "https://www.googleapis.com/books/v1/volumes/RJxWIQOvoZUC", "volumeInfo": { "title": "Flowers", "authors": [ "Gail Saunders-Smith" ], ... }, "totalItems": 2

"status": "200"
}

Route: /api/health Request Type: GET Purpose: Health check route to verify the service is running. Request Body: - Request Format: JSON Success Response Example: Code: 200 Content: {'status': ‘healthy'} Example Request: { } Example Response: {'status': ‘healthy'}

Route: /details/<book_id> Request Type: GET Purpose: Fetch details for a specific book using the Google Books API. Request Body: - Request Format: JSON Success Response Example: Code: 200 Content: { "kind": "books#volume", "id": “string", "etag": "string/I", "selfLink": "string", "volumeInfo": { "title": "string", "authors": [ "string", "string" ], "publisher": "string", "publishedDate": "string", "description": ""string", "industryIdentifiers": [ { "type": "string", "identifier": "string" }, { "type": "string", "identifier": "string" } ], "pageCount": number, "dimensions": { "height": "string", "width": "string", "thickness": "string" }, "printType": "string", "mainCategory": "string", "categories": [ "string", ... ], "averageRating": number, "ratingsCount": number, "contentVersion": "string", "imageLinks": { "string", "string", … }, "language": "string", "infoLink": "string", "canonicalVolumeLink": "string" }, "saleInfo": { "country": "string", "saleability": "string", "isEbook": boolean, "listPrice": { "amount": number, "currencyCode": "string" }, "retailPrice": { "amount": number, "currencyCode": "string" }, "buyLink": "string" }, "accessInfo": { "country": "string", "viewability": "string", "embeddable": boolean, "publicDomain": boolean, "textToSpeechPermission": "string", "epub": { "isAvailable": boolean, "acsTokenLink": "string" }, "pdf": { "isAvailable": boolean }, "accessViewStatus": "string" } "status": "200" }

Example Request: { } Example Response: { "kind": "books#volume", "id": "zyTCAlFPjgYC", "etag": "f0zKg75Mx/I", "selfLink": "https://www.googleapis.com/books/v1/volumes/zyTCAlFPjgYC", "volumeInfo": { "title": "The Google story", "authors": [ "David A. Vise", "Mark Malseed" ], "publisher": "Random House Digital, Inc.", "publishedDate": "2005-11-15", "description": ""Here is the story behind one of the most remarkable Internet successes of our time. Based on scrupulous research and extraordinary access to Google, ...", "industryIdentifiers": [ { "type": "ISBN_10", "identifier": "055380457X" }, { "type": "ISBN_13", "identifier": "9780553804577" } ], "pageCount": 207, "dimensions": { "height": "24.00 cm", "width": "16.03 cm", "thickness": "2.74 cm" }, "printType": "BOOK", "mainCategory": "Business & Economics / Entrepreneurship", "categories": [ "Browsers (Computer programs)", ... ], "averageRating": 3.5, "ratingsCount": 136, "contentVersion": "1.1.0.0.preview.2", "imageLinks": { "smallThumbnail": "https://books.google.com/books?id=zyTCAlFPjgYC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api", "thumbnail": "https://books.google.com/books?id=zyTCAlFPjgYC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api", "small": "https://books.google.com/books?id=zyTCAlFPjgYC&printsec=frontcover&img=1&zoom=2&edge=curl&source=gbs_api", "medium": "https://books.google.com/books?id=zyTCAlFPjgYC&printsec=frontcover&img=1&zoom=3&edge=curl&source=gbs_api", "large": "https://books.google.com/books?id=zyTCAlFPjgYC&printsec=frontcover&img=1&zoom=4&edge=curl&source=gbs_api", "extraLarge": "https://books.google.com/books?id=zyTCAlFPjgYC&printsec=frontcover&img=1&zoom=6&edge=curl&source=gbs_api" }, "language": "en", "infoLink": "https://books.google.com/books?id=zyTCAlFPjgYC&ie=ISO-8859-1&source=gbs_api", "canonicalVolumeLink": "https://books.google.com/books/about/The_Google_story.html?id=zyTCAlFPjgYC" }, "saleInfo": { "country": "US", "saleability": "FOR_SALE", "isEbook": true, "listPrice": { "amount": 11.99, "currencyCode": "USD" }, "retailPrice": { "amount": 11.99, "currencyCode": "USD" }, "buyLink": "https://books.google.com/books?id=zyTCAlFPjgYC&ie=ISO-8859-1&buy=&source=gbs_api" }, "accessInfo": { "country": "US", "viewability": "PARTIAL", "embeddable": true, "publicDomain": false, "textToSpeechPermission": "ALLOWED_FOR_ACCESSIBILITY", "epub": { "isAvailable": true, "acsTokenLink": "https://books.google.com/books/download/The_Google_story-sample-epub.acsm?id=zyTCAlFPjgYC&format=epub&output=acs4_fulfillment_token&dl_type=sample&source=gbs_api" }, "pdf": { "isAvailable": false }, "accessViewStatus": "SAMPLE" } "status": "200" }

Route: /add-to-library

Request Type: POST Purpose: Adds a book to the user's library. Request Body: user_id (String): User’s chosen username. password (String): User’s chosen password. Status (String) Optional : Chosen bookshelf to add book in. Request Format: JSON Success Response Example: Code: 201 Content: {“message": “Book added to library successfully!”} Example Request: { “user_id” : “47382” “book_id” : “zyTCAlFPjgYC” “status” : “To read” } Example Response: {“message": “Book added to library successfully!” “status” : “201”}

Route: /library/int:user_id Request Type: GET Purpose: Retrieve the user's library with book details and statuses. Request Body: - Request Format: JSON Success Response Example: Code: 200 Content: {“library”: [{ "title": book[0], "author": book[1], "status": book[2] }] } Example Request: { } Example Response: { "library": [ { "title": "To Kill a Mockingbird”, "author": "Harper Lee", "status": "Reading" }, { "title": "1984", "author":"George Orwell", "status": "Completed" }, { "title": "The Catcher in the Rye", "author": "J.D. Salinger", "status": "Plan to Read" } ] “status” = “200” }

Route: /update-status Request Type: POST Purpose: Update the status of a book in the user's library. Request Body: user_id (String): User’s chosen username. password (String): User’s chosen password. Status (String) : Chosen status to mark book under. Request Format: JSON Success Response Example: Code: 200 Content: {"message": "Book status updated successfully!"} Example Request: { “user_id” : “47382” “book_id” : “zyTCAlFPjgYC” “status” : “To read” } Example Response: {"message": "Book status updated successfully!"}

Dockerfile:

Docker provides a way to package your application and its dependencies into a container. Containers ensure consistent and portable environments across development, testing, and production.

Prerequisites: docker installed on your machine. clone this repository

Building and Running the Docker Image:

Building docker image: docker buildx build booksystemdockerfile -t flask-app .

Running the container: docker run -p 5000:5000 --env-file apikeys.env flask-app

Once the container is running, you can access the application at: http://localhost:5000/

Common Issues:

Port Already in Use: Ensure no other application is using port 5000 and change the mapping if needed with: docker run -p 8080:5000 --env-file apikeys.env flask-app

Database Not Persisting: Mount a volume for the database to persist: docker run -v $(pwd)/databases:/app/databases -p 5000:5000 --env-file apikeys.env flask-app