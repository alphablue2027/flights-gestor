# Flight Management System

A comprehensive desktop application for managing airlines, national flights, and international flights. Built with Python and PyQt5, this system provides an intuitive graphical interface for flight operations management, data persistence, and statistical analysis.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Data Models](#data-models)
- [Functionality](#functionality)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

## Features

### Airline Management

- Add and remove airlines with unique codes
- Track airline information (name, code, nationality, number of planes)
- Automatic validation of airline codes and names

### Flight Management

- **National Flights**: Manage domestic flights with origin and destination cities
- **International Flights**: Manage international flights with additional features:
  - Destination country tracking
  - Scale/layover support
  - Scale number tracking
- Add and remove flights with comprehensive validation
- Flight code validation (must start with airline code)
- PostgreSQL persistence: every change is saved immediately, with integrity enforced by the database (foreign keys, cascades and check constraints)

### Query and Analysis

- List all national or international flights
- Find outbound national flights by date
- Get airline information by flight code
- Calculate percentage of flights by aircraft mark for an airline
- Calculate average passenger capacity by destination
- Find international flight with most scales on a given date

### User Interface

- Modern PyQt5-based graphical interface
- Intuitive navigation with sidebar menu
- Form validation with user-friendly error messages
- Confirmation dialogs for critical operations
- Responsive window controls (minimize, maximize, close)

## Project Structure

```
flies-gestor/
├── controllers/          # Application controllers (MVC pattern)
│   ├── main_controller.py
│   ├── accept_controlers.py
│   ├── confirm_controllers.py
│   └── validators.py
├── models/              # Data models and business logic
│   ├── gestor.py        # Main flight and airline manager
│   ├── flights.py       # NationalFly and InternationalFly classes
│   ├── airline.py       # Airline model
│   ├── plane.py         # Aircraft model
│   └── link.py
├── views/               # UI components
│   ├── main_view.py
│   ├── accept_view.py
│   ├── confirm_view.py
│   └── ui/              # Qt Designer UI files
│       ├── main.ui
│       ├── accept.ui
│       └── confirm.ui
├── db/                  # PostgreSQL scripts
│   ├── schema.sql       # Tables, constraints and indexes
│   └── seed.sql         # Sample airlines and flights
├── diagrams/            # UML diagrams (PlantUML)
│   ├── business/
│   └── system/
├── icons/               # Application icons
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── link.qrc             # Qt resource file
├── LICENSE.md           # License information
└── README.md            # This file
```

## Requirements

- **Python**: 3.10 or higher
- **PostgreSQL**: 14 or higher
- **PyQt5**: For the graphical user interface
- **psycopg 3**: PostgreSQL driver

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd flies-gestor
   ```

2. **Install the dependencies** in a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Create the database** and load the schema (plus the optional sample data):

   ```bash
   createdb flights_gestor
   psql -d flights_gestor -f db/schema.sql -f db/seed.sql
   ```

   `schema.sql` drops and recreates the tables, so running it again resets all data.

4. **Configure the connection** (optional): the app reads `DATABASE_URL` and defaults to `postgresql:///flights_gestor` (local server, current OS user). For another server:

   ```bash
   export DATABASE_URL="postgresql://user:password@host:5432/flights_gestor"
   ```

## Usage

### Running the Application

```bash
python main.py
```

### Basic Workflow

1. **Add Airlines First**: Before adding flights, you must create at least one airline.
   - Click on "Add Airline" in the sidebar
   - Fill in the airline information:
     - Code: 2-character unique code (e.g., "CU")
     - Name: Airline name (no numbers)
     - Nationality: Country name (no numbers)
     - Number of Planes: Integer value

2. **Add Flights**:
   - Select flight type (National or International) from the dropdown
   - Click "Add Flight" in the sidebar
   - Fill in flight details:
     - Flight code: Must start with airline code + 3-4 digits
     - Origin and destination cities
     - Date and time
     - Aircraft information (mark, model, matriculation, capacity)
     - For international flights: destination country, scale information

3. **Query Flights**:
   - Use the sidebar options to:
     - List all flights (national or international)
     - Find outbound national flights by date
     - Get airline information by flight code
     - Calculate statistics and percentages

4. **Remove Items**:
   - Removing an airline will also remove all associated flights
   - A confirmation dialog will appear for airline deletion

### Data Persistence

Data lives in PostgreSQL across three tables:

- `airlines`: Airline information
- `flights`: Fields shared by every flight, including the aircraft
- `international_flights`: International-only fields (destination country, scales), linked one-to-one to `flights`

Every add or delete is written immediately; there is no save step on close. Deleting an airline removes its flights through `ON DELETE CASCADE`. If the database is unreachable at startup, the app shows an error dialog and exits.

## Architecture

The application follows the **Model-View-Controller (MVC)** architectural pattern:

- **Models** (`models/`): Business logic and data structures
  - `FlightsGestor`: Main manager class for flights and airlines
  - SQL queries through psycopg 3, mapping rows to model objects
  - Flight, airline and plane model classes

- **Views** (`views/`): User interface components
  - PyQt5-based windows and dialogs
  - UI files created with Qt Designer

- **Controllers** (`controllers/`):
  - `MainController`: Main application controller
  - Event handling and business logic coordination
  - Input validation

## Data Models

### Airline

- `name`: Airline name (string)
- `code`: Unique 2-character code (string)
- `nationality`: Country of origin (string)
- `planes_number`: Number of aircraft (integer)

### National Flight

- `code`: Flight code (string, must start with airline code)
- `inner`: Boolean indicating if it's an internal flight
- `airline`: Airline name (string)
- `init_city`: Origin city (string)
- `end_city`: Destination city (string)
- `datetime`: Flight date and time (datetime)
- `plane`: Aircraft information (Plane object)

### International Flight

Extends National Flight with:

- `destiny`: Destination country (string)
- `scale`: Boolean indicating if flight has layovers
- `scale_number`: Number of layovers (integer)

### Plane

- `mark`: Aircraft manufacturer (string)
- `model`: Aircraft model (string)
- `matricule`: Registration number (string)
- `capacity`: Passenger capacity (integer)

## Functionality

### Validation Rules

- **Airline Code**: Must be exactly 2 characters, unique
- **Airline Name**: Must be unique, cannot contain numbers
- **Flight Code**: Must start with airline code followed by 3-4 digits, must be unique
- **City Names**: Cannot be empty or contain numbers
- **Aircraft Information**: Model and matriculation cannot be empty or contain spaces

### Query Features

1. **List Outbound National Flights**: Filter national flights by date, sorted by time
2. **Get Airline by Flight Code**: Retrieve airline information associated with a flight
3. **Calculate Percentage**: Get percentage of flights by aircraft mark for a specific airline
4. **Average Capacity**: Calculate average passenger capacity for flights to a destination
5. **Most Scales Flight**: Find international flight with most layovers on a given date

## License

This project is distributed under the **PolyForm Perimeter License 1.0.0**.

### Key Terms

- **Permitted Use**: Only for non-commercial purposes
- **Restriction**: Prohibited for use in businesses that compete with the licensor
- **Commercial License**: Required for commercial use (contact the licensor)

For full license details, see [LICENSE.md](LICENSE.md).

### Permissions

- Forks, modifications, and non-commercial distribution are permitted

### Restrictions

- Commercial use is prohibited without express authorization
- Derivatives must maintain this same license

## Contributing

Contributions are welcome! However, please note that this project is licensed under the PolyForm Perimeter License, which restricts commercial use. When contributing:

1. Ensure your contributions align with the project's architecture
2. Follow the existing code style and patterns
3. Test your changes thoroughly
4. Update documentation as needed

## Contact

### Chrysal Core

- **Email**: [owner@chrysalcore.com](owner@chrysalcore.com)
- **Website**: [https://chrysalcore.com](https://chrysalcore.com)

---

Copyright (C) 2025 Ordnay Perez Hernandez

*Commercial use prohibited without permission!*
