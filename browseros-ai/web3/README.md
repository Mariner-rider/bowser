# web3

Web3 identity and wallet abstractions.

## Responsibilities
- Wallet connection workflows.
- Signature and transaction authorization policies.
- DID/identity integration points.

## Framework Layout
- `wallet_manager.ts`: Ethereum-compatible wallet connection/session management and browser Web3 login option.
- `identity_manager.ts`: decentralized identity (`did:pkh`) creation from wallet address and chain.
- `blockchain_connector.ts`: chain queries and blockchain authentication challenge signing.
- `token_auth.ts`: token-based permission issuance and authorization checks.
