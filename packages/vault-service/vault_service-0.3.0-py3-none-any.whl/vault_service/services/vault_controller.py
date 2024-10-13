import os
import logging
import hvac

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VaultController:
    DATA_PATH = 'secret/data/'  # Constant for the KV v2 path prefix

    def __init__(self):
        """
        Initialize the VaultController with configuration from a JSON file.
        
        :param config: Dictionary with Vault configuration details.
        """
        self.vault_addr = os.getenv('VAULT_ADDR')
        self.vault_token = os.getenv('VALUT_TOKEN')
        self.base_path = os.getenv('BASE_PATH')

        # Initialize Vault client
        self.client = hvac.Client(url=self.vault_addr, token=self.vault_token)

        # Check if the client is authenticated
        if not self.client.is_authenticated():
            raise ValueError("Failed to authenticate to Vault. Check your token and server configuration.")

        logger.info(f"Successfully authenticated to Vault with base path: {self.base_path}")

    def build_secret_path(self, tenant_id, secret_name):
        """
        Build the full secret path using tenant_id and secret_name.
        
        :param tenant_id: The tenant ID to append to the path.
        :param secret_name: The connector ID to append to the path.
        :return: The complete secret path.
        """
        return f"{self.base_path}/{tenant_id}/{secret_name}"

    def secret_exists(self, tenant_id, secret_name):
        """
        Check if a secret exists at the specified path.
        
        :param tenant_id: The tenant ID to check.
        :param secret_name: The connector ID to check.
        :return: True if the secret exists, False otherwise.
        """
        secret_path = self.build_secret_path(tenant_id, secret_name)
        try:
            self.client.secrets.kv.v2.read_secret_version(path=secret_path.split(self.DATA_PATH)[-1])
            return True
        except hvac.exceptions.InvalidRequest as e:
            if 'path' in str(e):
                logger.warning(f"Secret path not found at: {secret_path}. Check if tenant ID '{tenant_id}' and connector ID '{secret_name}' are correct.")
            return False

    def store_secret(self, tenant_id, secret_name, secret_data):
        """
        Store a new secret in HashiCorp Vault.
        
        :param tenant_id: Tenant ID to append to the secret path.
        :param secret_name: Connector ID to append to the secret path.
        :param secret_data: Dictionary containing the secret data to be stored.
        """
        secret_path = self.build_secret_path(tenant_id, secret_name)
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=secret_path.split(self.DATA_PATH)[-1],  # KV v2 path
                secret=secret_data
            )
            logger.info(f"Secret stored successfully at {secret_path}")
        except Exception as e:
            logger.error("Failed to store secret: %s", str(e))
            raise

    def get_secret(self, tenant_id, secret_name):
        """
        Retrieve a secret from HashiCorp Vault.
        
        :param tenant_id: Tenant ID to append to the secret path.
        :param secret_name: Connector ID to append to the secret path.
        :return: The retrieved secret data as a dictionary, or None if not found.
        """
        secret_path = self.build_secret_path(tenant_id, secret_name)
        if not self.secret_exists(tenant_id, secret_name):
            logger.info(f"No secret found for tenant ID '{tenant_id}' and connector ID '{secret_name}'.")
            return None

        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=secret_path.split(self.DATA_PATH)[-1]
            )
            secret_data = response['data']['data']
            logger.info(f"Secret retrieved successfully from {secret_path}")
            return secret_data
        except hvac.exceptions.VaultError as e:
            logger.error(f"Vault error occurred: {str(e)}")
            return None
        except hvac.exceptions.InvalidPath as e:
            # This exception is raised when the path doesn't exist
            logger.warning(f"No secrets found for tenant ID '{tenant_id}' and connector ID '{secret_name}'. Path does not exist: {str(e)}")
            return None
        except hvac.exceptions.InvalidRequest as e:
            logger.info(f"Invalid request for secret at {secret_path}: {str(e)}")
            return None
        except hvac.exceptions.Forbidden as e:
            logger.error(f"Permission denied when accessing secret for tenant ID '{tenant_id}' and connector ID '{secret_name}': {str(e)}")
            raise
        except Exception as e:
            logger.error("Failed to retrieve secret: %s", str(e))
            raise

    def update_secret(self, tenant_id, secret_name, updated_data):
        """
        Update an existing secret in HashiCorp Vault.
        
        :param tenant_id: Tenant ID to append to the secret path.
        :param secret_name: Connector ID to append to the secret path.
        :param updated_data: Dictionary containing the updated secret data.
        """
        secret_path = self.build_secret_path(tenant_id, secret_name)
        if not self.secret_exists(tenant_id, secret_name):
            logger.info(f"No secret found for tenant ID '{tenant_id}' and connector ID '{secret_name}' to update.")
            return {"status":"success", "message":f"No secret found for tenant ID '{tenant_id}' and connector ID '{secret_name}' to update."}

        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=secret_path.split(self.DATA_PATH)[-1],
                secret=updated_data
            )
            logger.info(f"Secret updated successfully at {secret_path}")
        except Exception as e:
            logger.error("Failed to update secret: %s", str(e))
            raise

    def delete_secret(self, tenant_id, secret_name):
        """
        Delete an existing secret in HashiCorp Vault.
        
        :param tenant_id: Tenant ID to append to the secret path.
        :param secret_name: Connector ID to append to the secret path.
        """
        secret_path = self.build_secret_path(tenant_id, secret_name)
        if not self.secret_exists(tenant_id, secret_name):
            logger.info(f"No secret found for tenant ID '{tenant_id}' and connector ID '{secret_name}' to delete.")
            return {"status":"success", "message":f"No secret found for tenant ID '{tenant_id}' and connector ID '{secret_name}' to update."}

        try:
            # Delete the secret at the specified path
            self.client.secrets.kv.v2.delete_metadata_and_all_versions(
                path=secret_path.split(self.DATA_PATH)[-1]
            )
            logger.info(f"Secret deleted successfully at {secret_path}")
        except Exception as e:
            logger.error("Failed to delete secret: %s", str(e))
            raise

    def get_all_secrets_for_tenant(self, tenant_id):
        """
        Retrieve all secrets for a tenant from HashiCorp Vault (KV v2).

        :param tenant_id: Tenant ID to fetch all secrets.
        :return: A list of all secrets for the tenant.
        """
        secrets = []
        secret_path = f"connector-service/{tenant_id}"  # Adjust path if necessary
        logger.info(f"Attempting to fetch secrets at path: {secret_path}")

        try:
            # List all secrets under the tenant path
            logger.info(f"Calling list_secrets with path: {secret_path}")
            secrets_list = self.client.secrets.kv.v2.list_secrets(path=secret_path)
            logger.info(f"Secrets fetched at path: {secret_path}")

            # Check if 'keys' is in the response data
            if 'keys' in secrets_list['data']:
                for secret_key in secrets_list['data']['keys']:
                    # Read each secret version
                    secret_data = self.client.secrets.kv.v2.read_secret_version(path=f"{secret_path}/{secret_key}")
                    secrets.append ({
                        'secret_name': secret_key,
                        'data': secret_data['data']['data']
                    })
            else:
                logger.warning(f"No secrets found at path: {secret_path}")

        except hvac.exceptions.InvalidPath as e:
            # This exception is raised when the path doesn't exist
            logger.warning(f"No secrets found for tenant ID '{tenant_id}'. Path does not exist: {str(e)}")
        except hvac.exceptions.InvalidRequest as e:
            logger.warning(f"No secrets found for tenant ID '{tenant_id}'. {str(e)}")
        except Exception as e:
            logger.error("Failed to retrieve all secrets for tenant: %s", str(e))

        return secrets


    def delete_all_secrets_for_tenant(self, tenant_id):
        """
        Delete all secrets for a specific tenant.

        :param tenant_id: The tenant ID to delete secrets for.
        """
        # Retrieve all secret keys for the tenant
        secret_keys = self.get_all_secrets_for_tenant(tenant_id)

        for key in secret_keys:
            secret_name = key.get('secret_name')
            logger.info(f"Deleting secret for tenant ID '{tenant_id}' and key '{secret_name}'")
            self.delete_secret(tenant_id, secret_name)

        logger.info(f"Deleted all secrets for tenant ID '{tenant_id}'")

