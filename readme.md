Mini Wallet :

Mini Wallet Exercise in Flask Python by Kaustubh Sharma.  
## Table of Contents
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Setup](#database-setup)
- [Running the App](#running-the-app)
- [API Endpoints](#api-endpoints)
- [Sql Versions](#Sql-versions)


## Getting Started

### Prerequisites
- Python 3.7 or higher
- Virtual environment (recommended)

### Installation
Clone this repository to your local machine:
   ```bash
   git clone https://github.com/RayStainerZ/mini-wallet.git
   ```
Navigate to the project directory:
```bash
cd mini-wallet
```
Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
Install the project dependencies:
```bash
pip install -r requirements.txt
```

### Running The App
Run the following command to start the Flask development server:
```bash
flask run
or 
python3 run.py
```
The app will be available on url : 
```commandline
http://127.0.0.1:5000
```
### API Endpoints
```commandline
/api/v1/wallet: Enable, view, and disable the wallet.
/api/v1/wallet/deposits: Add deposits to the wallet.
/api/v1/wallet/withdrawals: Make withdrawals from the wallet.
/api/v1/wallet/transactions: View transaction history.
```

### Sql Versions
Provided to keep local DB updated based on latest time stamp.



