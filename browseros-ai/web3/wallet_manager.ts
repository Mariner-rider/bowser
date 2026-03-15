export type EIP1193Provider = {
  request: (args: { method: string; params?: unknown[] | Record<string, unknown> }) => Promise<unknown>;
};

export type SupportedWallet = "metamask" | "walletconnect" | "injected";

export type WalletSession = {
  wallet: SupportedWallet;
  chainId: string;
  address: string;
  connectedAt: string;
};

export type BrowserLoginOption = {
  id: "web3_wallet";
  label: string;
  description: string;
  enabled: boolean;
};

export class WalletManager {
  private session: WalletSession | null = null;

  async connectEthereumWallet(
    provider: EIP1193Provider,
    wallet: SupportedWallet,
    chainIdHex: string,
  ): Promise<WalletSession> {
    await provider.request({
      method: "wallet_switchEthereumChain",
      params: [{ chainId: chainIdHex }],
    });

    const accounts = (await provider.request({ method: "eth_requestAccounts" })) as string[];
    if (!accounts || accounts.length === 0) {
      throw new Error("No wallet accounts returned from provider");
    }

    this.session = {
      wallet,
      chainId: chainIdHex,
      address: accounts[0],
      connectedAt: new Date().toISOString(),
    };
    return this.session;
  }

  getSession(): WalletSession | null {
    return this.session;
  }

  disconnect(): void {
    this.session = null;
  }

  getBrowserLoginOption(): BrowserLoginOption {
    return {
      id: "web3_wallet",
      label: "Login with Web3 Wallet",
      description: "Authenticate with an Ethereum-compatible wallet",
      enabled: true,
    };
  }
}
