import type { EIP1193Provider } from "./wallet_manager";

export type SignedChallenge = {
  challenge: string;
  signature: string;
  address: string;
};

export class BlockchainConnector {
  constructor(private readonly provider: EIP1193Provider) {}

  async getChainId(): Promise<string> {
    const chainId = (await this.provider.request({ method: "eth_chainId" })) as string;
    if (!chainId) {
      throw new Error("Failed to fetch active chain id");
    }
    return chainId;
  }

  async signAuthenticationChallenge(address: string, challenge: string): Promise<SignedChallenge> {
    const signature = (await this.provider.request({
      method: "personal_sign",
      params: [challenge, address],
    })) as string;

    if (!signature) {
      throw new Error("Wallet failed to sign authentication challenge");
    }

    return { challenge, signature, address };
  }

  async verifyConnectedAddress(expectedAddress: string): Promise<boolean> {
    const accounts = (await this.provider.request({ method: "eth_accounts" })) as string[];
    return accounts.some((acct) => acct.toLowerCase() === expectedAddress.toLowerCase());
  }
}
