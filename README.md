# timepiece-traders

## Building the Application
### Architecture:

<img width="1009" alt="290250752-b9cce8c6-ade6-49b7-b980-f5114ab0c16a" src="https://github.com/ashkanray/luxuryauction/assets/49113488/84f56082-6f5a-4c02-a3da-9d0926d1bebe">

## Technology Stack:

### Frontend
Node.js for serving the website
Express.js for the API Gateway
ReactJS / HTML / CSS for website pages
Backend:

Python - Flask
RabbitMQ for microservice communication

### Databases
MySQL - hosted in separate Docker containers (accounts, items, notifications, auctions)
Redis - hosted in Docker container (bidding)
Running the Application
Download the repo and have Docker Desktop. In the root directory of this project locally, pip install microservices/requirements.txt
Run Docker Desktop App in your local machine
From a fresh terminal window, access the root directory of this project
Run: docker-compose build
Run: docker-compose up
Open a separate terminal and navigate to the same root directory
Run: bash start_application.sh
Acess a browser window, and search: "http://localhost:3000"

## Running the Application
0. Run Docker Desktop App in your local machine
1. From a fresh terminal window, access the sub-directory: timepiece-traders
2. Run: docker-compose build
3. Run: docker-compose up

4. Open a separate terminal 
5. In that window (from step 4) access the sub-directory: timepiece-traders as well
6. Run: bash start_application.sh
7. Acess a browser (chrome) window, access: "http://localhost:3000"
8. Boo-Yah!

## Project Description (Requirements)
(https://www.classes.cs.uchicago.edu/archive/2023/fall/51205-1/AuctionSiteRequirements.html)

## Specific Microservices
### Accounts

### Auction Platform

### Bidding

### Items

### Message Broker

### Notifications


