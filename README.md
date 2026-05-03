# Analytxia - Marketing Data Automation Platform 🚀

Analytxia is a custom SaaS platform designed to automate marketing data reporting, transform raw API data into actionable dashboards, and ensure high-integrity metrics for business decision-making.

## 📌 Project Overview
Built as an end-to-end data pipeline, this application connects directly with marketing APIs (Meta/Google Ads), processes the data using Python, and serves it through a clean, scalable Flask-based REST architecture.

## 🛠️ Technology Stack
*   **Backend Framework:** Python / Flask
*   **Database:** SQLite / PostgreSQL (configured via `database.py`)
*   **Data Processing:** Pandas (for metric validation and logic refinement)
*   **External APIs:** Meta Ads API / Google Ads API Integration
*   **Frontend Rendering:** Jinja2 Templates (HTML/CSS/JS)
*   **Architecture:** MVC (Model-View-Controller)

## 📁 Project Structure
*   `core/` - Handles external API integrations and data processing logic.
*   `static/` - Static assets (CSS, JS).
*   `templates/` - HTML templates for the UI dashboards.
*   `app.py` - Main application entry point and routing.
*   `database.py` - Database connection and ORM setup.
*   `requirements.txt` - Project dependencies.

## 🚀 Key Features
1.  **Automated Reporting:** Reduces processing time by standardizing data extraction workflows.
2.  **API Integration:** Securely fetches campaign metrics directly from advertising platforms.
3.  **Data Integrity:** Implements logical validation to detect outliers and ensure metric accuracy.
4.  **Scalable Architecture:** Designed with clear separation of concerns (Core logic vs. UI rendering).

## ⚙️ Local Setup
To run this project locally:

1.  Clone the repository:
    ```bash
    git clone [https://github.com/Juan-Araujo-C/analytxia-backend.git](https://github.com/Juan-Araujo-C/analytxia-backend.git)
    cd analytxia-backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Set up your environment variables (Create a `.env` file for your API keys).
5.  Run the application:
    ```bash
    python app.py
    ```

---
*Developed by **Juan Ignacio Araujo** - Backend Engineer | Data Systems Specialist*
