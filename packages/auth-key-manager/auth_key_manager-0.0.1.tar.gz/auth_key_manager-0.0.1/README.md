# AuthKeyManager

**AuthKeyManager** is a class used to manage license keys, supporting both **MySQL and MongoDB databases**. With this class, you can generate, store, query, validate, and delete license keys for specific users.

# Features
- **Database Support**: MySQL and MongoDB
- **License Key Generation**: Generates random 12-character license keys in a custom format.
- **Record Creation**: Stores license keys associated with user IDs in the database.
- **Query**: Retrieves all license keys for a given user.
- **Validation**: Verifies if a license key is valid for a specific user.
- **Deletion**: Removes a specific license key for a user from the database.

# Installation
```bash
pip install auth_key_manager
```

# Usage

# 1. Initializing the Class

```python
from auth_key_manager import AuthKeyManager

# Initialize with MySQL
auth_manager = AuthKeyManager(
    db_type="mysql",
    connection_params={
        "host": "localhost", # Hostname
        # "port": 3306,  # Optional: Default MySQL port is 3306
        "user": "",
        "password": ""
    },
    db_name="", # Database name
    table_name="", # Table name 
    column_user_id="", # Column name for user ID
    column_license_key="", # Column name for license key
    column_created_at=""  # Column name for creation date
)

# Initialize with MongoDB
auth_manager = AuthKeyManager(
    db_type="mongodb",
    connection_params={
        "host": "localhost", # Hostname and 
        "port": 27017 # Optional: Default MongoDB port is 27017
        },
    db_name="", # Database name
    table_name="",  # Collection name 
    column_user_id="", # Field name for user ID
    column_license_key="", # Field name for license key
    column_created_at="" # Field name for creation date
)
```
# 2. Generating a License Key
```python
# Generate a license key for a user
user_id = "user123"
license_key = auth_manager.create_license_record(user_id)
print(f"Generated License Key: {license_key}")
# Output: Generated License Key: LICENSE-XXXX-XXXX-XXXX
```

# 3. Querying License Keys for a User
```python
# Query all license keys for a user
user_id = "user123"
license_keys = auth_manager.query_license_keys(user_id)
# Output: ['LICENSE-XXXX-XXXX-XXXX', 'LICENSE-XXXX-XXXX-XXXX', ...]
```
# 4. Validating a License Key
```python
# Validate a license key for a user
user_id = "user123"
license_key = "LICENSE-XXXX-XXXX-XXXX"
is_valid = auth_manager.validate_license_key(user_id, license_key)
print(f"Is Valid: {is_valid}")
# Output: Is Valid: True or False
```

# 5. Deleting a License Key
```python
# Delete a license key for a user
user_id = "user123"
license_key = "LICENSE-XXXX-XXXX-XXXX"
auth_manager.delete_license_key(user_id, license_key)
# Output: License key deleted successfully
```
# 6. Closing the Connection
```python
# Close the connection
auth_manager.close_connection()
```


# License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
