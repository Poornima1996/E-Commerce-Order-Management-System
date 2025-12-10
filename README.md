# E-Commerce Order Management System

A modern, full-stack order management application built with **React.js**, **Python (FastAPI)**, and **PostgreSQL**, fully containerized with **Docker** for seamless deployment.

## Overview

This application provides a complete solution for managing customer orders and products. It features a clean, intuitive interface for creating orders, selecting products, and tracking order history. The system is built with modern technologies and follows best practices for scalability, maintainability, and ease of deployment.

## Features

- **Order Management**: Create, read, update, and delete orders
- **Product Selection**: Select multiple products for each order
- **Product Count Display**: Shows the number of unique products per order
- **Search Functionality**: Filter orders by ID or description
- **Responsive Design**: Clean, modern UI that works on all devices
- **RESTful API**: Well-structured backend with proper error handling
- **Real-time Updates**: Instant feedback on all operations
- **Docker Support**: Fully containerized for easy deployment

---

## Tech Stack

### Frontend
- **React.js** (v19.2.0) - UI library
- **Vite** (v7.2.4) - Build tool and dev server
- **Axios** - HTTP client for API calls
- **CSS3** - Modern styling with flexbox and grid
- **Nginx** - Production web server

### Backend
- **Python** (3.11+)
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Database
- **PostgreSQL** (v15) - Relational database

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

---

## Prerequisites

### Required Software
- **Docker Desktop** (v20.10+) - [Download here](https://www.docker.com/products/docker-desktop)
- **Docker Compose** (v2.0+) - Included with Docker Desktop
- **Git** - For cloning the repository


### Step 1: Clone the Repository
```bash
git clone https://github.com/Poornima1996/E-Commerce-Order-Management-System.git
cd E-Commerce-Order-Management-System
```
### Step 2: Start All Services
```bash
docker-compose up -d
```

**That's it!**

### Access the Application

Open your browser and navigate to:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3001 | Main application interface |
| **Backend API** | http://localhost:8000 | REST API endpoints |
| **API Docs (Swagger)** | http://localhost:8000/api/docs | Interactive API documentation |


## Step-by-Step Implementation Guide

### Phase 1: Understanding the Project Structure

```
Ecomerce/
├── docker-compose.yml          # Orchestrates all containers
├── backend/
│   ├── Dockerfile              # Backend container configuration
│   ├── requirements.txt        # Python dependencies
│   └── app/
│       ├── main.py             # FastAPI application entry point
│       ├── database.py         # Database connection setup
│       ├── models.py           # SQLAlchemy database models
│       ├── schemas.py          # Pydantic validation schemas
│       ├── crud.py             # Database CRUD operations
│       ├── routes.py           # API endpoint definitions
│       ├── init_db.py          # Database initialization script
│       └── config.py           # Configuration management
└── frontend/
    ├── Dockerfile              # Frontend container configuration
    ├── nginx.conf              # Nginx web server configuration
    ├── package.json            # Node.js dependencies
    ├── vite.config.js          # Vite build configuration
    └── src/
        ├── App.jsx             # Main React component
        ├── services/
        │   └── api.js          # API client (Axios)
        └── components/
            ├── OrderList.jsx   # Order list view
            └── OrderForm.jsx   # Order creation/edit form
```

### Phase 2: Backend Implementation Details

#### 2.1 Database Models (`backend/app/models.py`)
Three main tables with relationships:
- **Products**: Stores product information
- **Orders**: Stores order information
- **OrderProductMap**: Many-to-many relationship between orders and products

#### 2.2 API Endpoints (`backend/app/routes.py`)
- `GET /api/orders` - Retrieve all orders with products
- `GET /api/orders/{id}` - Retrieve specific order
- `POST /api/orders` - Create new order
- `PUT /api/orders/{id}` - Update existing order
- `DELETE /api/orders/{id}` - Delete order
- `GET /api/products` - Retrieve all products

#### 2.3 Database Initialization (`backend/app/init_db.py`)
Automatically creates tables and seeds 4 products on first run:
1. HP laptop
2. Lenovo laptop
3. Car
4. Bike

### Phase 3: Frontend Implementation Details

#### 3.1 Main Components
- **OrderList.jsx**: Displays orders in a table with search, edit, and delete functionality
- **OrderForm.jsx**: Form for creating/editing orders with product selection
- **api.js**: Centralized API client using Axios

#### 3.2 Key Features
- Real-time search filtering
- Product count display (shows number of unique products per order)
- Responsive design with modern CSS
- Error handling and user feedback

### Phase 4: Docker Configuration

#### 4.1 Services Defined in `docker-compose.yml`
1. **db** (PostgreSQL)
   - Port: 5432
   - Database: ecommerce_db
   - User: postgres
   - Password: postgres

2. **backend** (FastAPI)
   - Port: 8000
   - Depends on: db
   - Auto-initializes database on startup

3. **frontend** (React + Nginx)
   - Port: 3001
   - Depends on: backend
   - Serves production-optimized build

#### 4.2 Container Communication
- Frontend → Backend: `http://backend:8000`
- Backend → Database: `postgresql://postgres:postgres@db:5432/ecommerce_db`
- External access via mapped ports

## Project Structure

### Backend File Descriptions

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app initialization, CORS setup, route registration |
| `database.py` | SQLAlchemy engine and session management |
| `models.py` | Database table definitions (Product, Order, OrderProductMap) |
| `schemas.py` | Pydantic models for request/response validation |
| `crud.py` | Database operations (create, read, update, delete) |
| `routes.py` | API endpoint handlers |
| `init_db.py` | Database initialization and product seeding |
| `config.py` | Environment variable configuration |

### Frontend File Descriptions

| File | Purpose |
|------|---------|
| `App.jsx` | Main component with routing logic |
| `OrderList.jsx` | Order table display with search and actions |
| `OrderForm.jsx` | Order creation/editing form |
| `api.js` | Axios HTTP client for API calls |
| `nginx.conf` | Production web server configuration |

