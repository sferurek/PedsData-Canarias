import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "maplibre-gl/dist/maplibre-gl.css";
import "./globals.css";
import { SiteHeader } from "@/components/SiteHeader";

const geist = Geist({ subsets: ["latin"], variable: "--font-geist" });

export const metadata: Metadata = {
  title: { default: "PedsData Canarias", template: "%s · PedsData Canarias" },
  description: "Accesibilidad geográfica potencial a Pediatría AP en las siete islas Canarias.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="es"><body className={geist.variable}>
    <SiteHeader /><main>{children}</main>
    <footer><div><strong>PedsData Canarias · RC1</strong><p>Datos públicos, método reproducible y limitaciones visibles.</p></div><p>Sin perfiles ZBS hasta disponer de geometría oficial vigente.</p></footer>
  </body></html>;
}
