# Password Vault System
---
 An application that stores user accounts with passwords.

**Programming Language:**
- **Python (Interpreted)**
- Dart (Compiled)

## Current Progress
---
**Python** 
- Implemented an Auth System
	- account registration
	- password hashing
	- sessions
	- login 
	- logout
- Implemented Password Vault
	- Vaults are accessible by only by the vault owners
	- data encryption and decryption with keys
- Database Connection
	- All data is stored in a database
	- Database Connection (Local/ Online) needs to be setup for it to work

## Setup
---
### Dependencies

**Python 3.12**
- pymongo
- cryptography
- bson

#### Installation

In the terminal: 
```
pip install pymongo cryptography bson
```

#### Running the Program

*\*Current program cannot run properly without setting up a database connection. Create a MongoDB database first in [MongoDB Atlas](https://www.mongodb.com/docs/atlas/) or [Setup a local MongoDB database](https://www.mongodb.com/docs/manual/administration/install-community/#std-label-install-mdb-community-edition)*

To run the program:

Run **main.py**:
```
py main.py
```

Developer:
**KENT LORENZ V. DARIA**
*BSCS 4A AI*