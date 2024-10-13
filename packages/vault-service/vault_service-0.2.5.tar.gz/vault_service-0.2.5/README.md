Here's a sample `README.md` for your Vault Service package, including descriptions for each method in your utilities file. You can customize it further based on your needs:

```markdown
# Vault Service

The **Vault Service** package provides a convenient interface for interacting with HashiCorp Vault. It offers various methods to manage secrets for different tenants and connectors. This package is designed for seamless integration into your applications.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Methods](#methods)
  - [store_secret](#store_secret)
  - [get_secret](#get_secret)
  - [update_secret](#update_secret)
  - [delete_secret](#delete_secret)
  - [get_all_secrets_for_tenant](#get_all_secrets_for_tenant)
  - [delete_all_secrets_for_tenant](#delete_all_secrets_for_tenant)
- [License](#license)

## Installation

You can install the Vault Service package using pip:

```bash
pip install vault-service
```

## Usage

To use the Vault Service, you need to initialize the `VaultController` and then call the utility functions. Make sure to set the required environment variables for Vault connection:

```bash
export VAULT_ADDR='https://your-vault-address'
export VAULT_TOKEN='your-vault-token'
export BASE_PATH='your-base-path'
```

## Methods

### `store_secret(tenant_id: str, connector_id: str, secret_data: SecretData)`

Stores a new secret in HashiCorp Vault under the specified tenant and connector ID. 

**Parameters:**
- `tenant_id`: The ID of the tenant.
- `connector_id`: The ID of the connector.
- `secret_data`: An instance of `SecretData`, containing the secret information to be stored.

**Returns:** A message indicating the success or failure of the operation.

---

### `get_secret(tenant_id: str, connector_id: str)`

Retrieves a secret from HashiCorp Vault for the specified tenant and connector ID.

**Parameters:**
- `tenant_id`: The ID of the tenant.
- `connector_id`: The ID of the connector.

**Returns:** The retrieved secret data as a dictionary, or an error message if not found.

---

### `update_secret(tenant_id: str, connector_id: str, secret_data: SecretData)`

Updates an existing secret in HashiCorp Vault for the specified tenant and connector ID.

**Parameters:**
- `tenant_id`: The ID of the tenant.
- `connector_id`: The ID of the connector.
- `secret_data`: An instance of `SecretData`, containing the updated secret information.

**Returns:** A message indicating the success or failure of the operation.

---

### `delete_secret(tenant_id: str, connector_id: str)`

Deletes a secret from HashiCorp Vault for the specified tenant and connector ID.

**Parameters:**
- `tenant_id`: The ID of the tenant.
- `connector_id`: The ID of the connector.

**Returns:** A message indicating the success or failure of the deletion.

---

### `get_all_secrets_for_tenant(tenant_id: str)`

Retrieves all secrets for a specific tenant from HashiCorp Vault.

**Parameters:**
- `tenant_id`: The ID of the tenant.

**Returns:** A list of all secrets associated with the tenant.

---

### `delete_all_secrets_for_tenant(tenant_id: str)`

Deletes all secrets associated with a specific tenant from HashiCorp Vault.

**Parameters:**
- `tenant_id`: The ID of the tenant.

**Returns:** A message indicating the success or failure of the deletion.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

### Additional Notes:
1. **Installation Instructions**: Modify the installation instructions if your package has specific dependencies or requires setup beyond `pip install`.
2. **Usage Section**: Include sample code snippets that demonstrate how to use your package effectively.
3. **Add Environment Variables**: Ensure users know they must set the environment variables needed for Vault connection.

Feel free to adjust the formatting and content as needed!