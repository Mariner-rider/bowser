export type DecentralizedIdentity = {
  did: string;
  address: string;
  method: "did:pkh";
  createdAt: string;
};

export class IdentityManager {
  buildDidFromEthereumAddress(address: string, chainIdHex: string): DecentralizedIdentity {
    if (!address.startsWith("0x")) {
      throw new Error("Expected Ethereum-compatible wallet address");
    }

    const normalizedAddress = address.toLowerCase();
    const chainReference = parseInt(chainIdHex, 16).toString(10);
    const did = `did:pkh:eip155:${chainReference}:${normalizedAddress}`;

    return {
      did,
      address: normalizedAddress,
      method: "did:pkh",
      createdAt: new Date().toISOString(),
    };
  }
}
