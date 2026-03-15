import type { CapacitorConfig } from "@capacitor/cli";

const config: CapacitorConfig = {
  appId: "ai.browseros.app",
  appName: "BrowserOS AI",
  webDir: "pwa/dist",
  bundledWebRuntime: false,
  server: {
    androidScheme: "https",
    iosScheme: "https"
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 1000
    }
  }
};

export default config;
