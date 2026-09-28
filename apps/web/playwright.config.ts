import { defineConfig, devices } from "@playwright/test";

const remoteBaseUrl = process.env.PLAYWRIGHT_BASE_URL;
const remoteStorageState = process.env.PLAYWRIGHT_STORAGE_STATE;

export default defineConfig({
  testDir: "./e2e",
  webServer: remoteBaseUrl ? undefined : {
    command: "pnpm build && pnpm start --port 3100",
    url: "http://localhost:3100",
    reuseExistingServer: true,
  },
  use: {
    baseURL: remoteBaseUrl ?? "http://localhost:3100",
    trace: "retain-on-failure",
    storageState: remoteStorageState || undefined,
  },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"] } },
    { name: "iphone", use: { ...devices["iPhone 13"], browserName: "chromium" } },
  ],
});
