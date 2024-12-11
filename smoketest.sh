#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000"

###############################################
#
# Health checks
#
###############################################

check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}

###############################################
#
# Authentication operations
#
###############################################

create_user() {
  echo "Creating a user..."
  response=$(curl -s -X POST "$BASE_URL/auth/create-account" \
    -H "Content-Type: application/json" \
    -d '{"username": "smoketestuser", "password": "password123"}')
  echo "$response" | grep -q '"message": "Account created successfully!"'
  if [ $? -eq 0 ]; then
    echo "User created successfully."
  else
    echo "User creation failed."
    exit 1
  fi
}

login_user() {
  echo "Logging in the user..."
  response=$(curl -s -X POST "$BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username": "smoketestuser", "password": "password123"}')
  echo "$response" | grep -q '"message": "Login successful!"'
  if [ $? -eq 0 ]; then
    echo "User logged in successfully."
  else
    echo "User login failed."
    exit 1
  fi
}

###############################################
#
# Book operations
#
###############################################

add_book_to_library() {
  echo "Adding a book to the library..."
  response=$(curl -s -X POST "$BASE_URL/books/add-to-library" \
    -H "Content-Type: application/json" \
    -d '{"user_id": 1, "book_id": "smoketestbook", "status": "To read"}')
  echo "$response" | grep -q '"message": "Book added to library successfully!"'
  if [ $? -eq 0 ]; then
    echo "Book added successfully."
  else
    echo "Failed to add book to library."
    exit 1
  fi
}

view_library() {
  echo "Viewing the library..."
  response=$(curl -s -X GET "$BASE_URL/books/library/1")
  echo "$response" | grep -q '"library":'
  if [ $? -eq 0 ]; then
    echo "Library viewed successfully."
  else
    echo "Failed to view library."
    exit 1
  fi
}

update_book_status() {
  echo "Updating the status of a book..."
  response=$(curl -s -X POST "$BASE_URL/books/update-status" \
    -H "Content-Type: application/json" \
    -d '{"user_id": 1, "book_id": "smoketestbook", "status": "Have read"}')
  echo "$response" | grep -q '"message": "Book status updated successfully!"'
  if [ $? -eq 0 ]; then
    echo "Book status updated successfully."
  else
    echo "Failed to update book status."
    exit 1
  fi
}

###############################################
#
# Run all smoketests
#
###############################################

echo "Starting smoketests for Personalized Book System..."

check_health
check_db
create_user
login_user
add_book_to_library
view_library
update_book_status

echo "Smoketests complete. All systems operational."