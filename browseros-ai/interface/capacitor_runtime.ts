export type RuntimeEnvironment = "web" | "ios" | "android";

export type RuntimeConfig = {
  environment: RuntimeEnvironment;
  isCapacitor: boolean;
  platform: RuntimeEnvironment;
};

export function detectRuntime(): RuntimeConfig {
  const globalAny = globalThis as typeof globalThis & {
    Capacitor?: { isNativePlatform: () => boolean; getPlatform: () => RuntimeEnvironment };
  };

  const capacitor = globalAny.Capacitor;
  if (capacitor && capacitor.isNativePlatform()) {
    const platform = capacitor.getPlatform();
    return {
      environment: platform,
      isCapacitor: true,
      platform,
    };
  }

  return {
    environment: "web",
    isCapacitor: false,
    platform: "web",
  };
}

export function ensureBrowserUIRuntime(): RuntimeConfig {
  const runtime = detectRuntime();

  if (runtime.isCapacitor) {
    console.info(`[capacitor-runtime] Browser UI running in ${runtime.platform}`);
  } else {
    console.info("[capacitor-runtime] Browser UI running in standard web/PWA mode");
  }

  return runtime;
}
