# Voka-Vokka

Voka-Vokka is a vocabulary learning application that helps users learn Korean words through groups, quizzes, and AI-generated hints.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

-   [MySQL Workbench 8.0 CE](https://dev.mysql.com/downloads/workbench/)
-   [Python 3.10+](https://www.python.org/downloads/)
-   [Node.js 18+](https://nodejs.org/)

## Setup Instructions

### 1. Database Setup

Since we are not using Docker, you need to manually set up the MySQL database using MySQL Workbench.

1.  **Install MySQL Workbench**: Download and install MySQL Workbench 8.0 CE.
2.  **Start MySQL Server**: Ensure your local MySQL server is running (often installed alongside Workbench or separately).
3.  **Create Database and User**:
    Open MySQL Workbench and connect to your local instance. 
    Open a new query tab and run the `db_init.sql` script to create the necessary tables.
4.  **Insert Test Data**:
    Open a new query tab and run the `test_data.sql` script to insert test data into the database.

### 2. Backend Setup

The backend is built with FastAPI.

1.  Navigate to the `app` directory:

    ```bash
    cd app
    ```

2.  Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3.  Activate the virtual environment:

    -   **Windows:**
        ```bash
        venv\Scripts\activate
        ```
    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5.  Configure environment variables:

    -   Copy `.env.example` to a new file named `.env`.
    -   Open `.env` and fill in your configuration.
        -   **Database**: Update `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE` (e.g., `voka`), etc., to match your local setup.
        -   **AI**: You must provide a valid `GEMINI_API_KEY` for the AI hint generation features.

6.  Run the backend server:

    ```bash
    uvicorn main:app --reload
    ```

    The backend will be available at `http://localhost:8000`. You can verify it's running by visiting `http://localhost:8000/health`.

    You can also use the API documentation at `http://localhost:8000/docs`.

### 3. Frontend Setup

The frontend is built with React and Vite.

1.  Open a new terminal and navigate to the `frontend` directory:

    ```bash
    cd frontend
    ```

2.  Install dependencies:

    ```bash
    npm install
    ```

3.  Run the development server:

    ```bash
    npm run dev
    ```

    The frontend will be available at `http://localhost:5173` (or the port shown in the terminal).

## Usage

1.  Ensure the Database, Backend, and Frontend are all running.
2.  Open your browser and go to the frontend URL (e.g., `http://localhost:5173`).
3.  Browse vocabulary groups and take quizzes!
