# Detector Inspector Engineering Challenge

This project reads tables from a Wikipedia URL, extracts relevant data, and generates bar plots. It includes tests for key functions and can be run locally or in a Docker container.


## Requirements

- Python 3.10 or higher
- Packages listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd DETECTOR
2. Create a virtual environment:
    python3 -m venv venv

3. Activate the virtual environment:
    + On Windows: venv\Scripts\activate
    + On macOS and Linux: source venv/bin/activate

4. Install packages:
    pip install -r requirements.txt

5. Running the Program
    python main.py

6. Running Tests
    python -m unittest test.py