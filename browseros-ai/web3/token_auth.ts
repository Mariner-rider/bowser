export type PermissionScope =
  | "agent:run"
  | "agent:pause"
  | "agent:stop"
  | "wallet:sign"
  | "automation:execute";

export type AuthToken = {
  sub: string;
  walletAddress: string;
  permissions: PermissionScope[];
  expiresAt: string;
};

export class TokenAuth {
  issueToken(sub: string, walletAddress: string, permissions: PermissionScope[], ttlSeconds: number): AuthToken {
    return {
      sub,
      walletAddress,
      permissions,
      expiresAt: new Date(Date.now() + ttlSeconds * 1000).toISOString(),
    };
  }

  isExpired(token: AuthToken): boolean {
    return new Date(token.expiresAt).getTime() <= Date.now();
  }

  authorize(token: AuthToken, required: PermissionScope): boolean {
    return !this.isExpired(token) && token.permissions.includes(required);
  }
}
