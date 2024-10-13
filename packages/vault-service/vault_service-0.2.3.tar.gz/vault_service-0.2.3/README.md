$ vault operator init --address=http://10.0.2.15:8200

WARNING! VAULT_ADDR and -address unset. Defaulting to https://127.0.0.1:8200.
Unseal Key 1: xxxxxxx
Unseal Key 2: xxxxxxx
Unseal Key 3: xxxxxxx
Unseal Key 4: xxxxxxx
Unseal Key 5: xxxxxxx

Initial Root Token: xxxxxxxx

Vault initialized with 5 key shares and a key threshold of 3. Please securely
distribute the key shares printed above. When the Vault is re-sealed,
restarted, or stopped, you must supply at least 3 of these keys to unseal it
before it can start servicing requests.

Vault does not store the generated root key. Without at least 3 keys to
reconstruct the root key, Vault will remain permanently sealed!

It is possible to generate new unseal keys, provided you have a quorum of
existing unseal keys shares. See "vault operator rekey" for more information
