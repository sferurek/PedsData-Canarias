import type { NextConfig } from "next";

const legacyProductionHosts = [
  "web-sferureks-projects.vercel.app",
  "web-liart-ten-z4se3v7h05.vercel.app",
];

const nextConfig: NextConfig = {
  output: "standalone",
  poweredByHeader: false,
  async redirects() {
    return legacyProductionHosts.map((host) => ({
      source: "/:path*",
      has: [{ type: "host" as const, value: host }],
      destination: "https://pedsdata.pedscore.app/:path*",
      permanent: true,
    }));
  },
};

export default nextConfig;
