import React from "react";

type DownloadRoutes = {
  android: string;
  ios: string;
  windows: string;
  mac: string;
  linux: string;
  extension: string;
  pwa: string;
};

type Metric = { label: string; value: string };

type RivinityLandingPageProps = {
  routes?: DownloadRoutes;
  treesPlanted?: number;
  metrics?: Metric[];
};

const defaultRoutes: DownloadRoutes = {
  android: "/downloads/android",
  ios: "/downloads/ios",
  windows: "/downloads/windows",
  mac: "/downloads/mac",
  linux: "/downloads/linux",
  extension: "/downloads/extension",
  pwa: "/downloads/pwa",
};

const defaultMetrics: Metric[] = [
  { label: "Daily active users", value: "120K+" },
  { label: "Tasks automated", value: "9.4M+" },
  { label: "Agents in marketplace", value: "2,100+" },
  { label: "Countries reached", value: "78" },
];

const styles = {
  page: { fontFamily: "Inter,system-ui,sans-serif", color: "#0f172a", background: "#f8fafc" },
  section: { maxWidth: 1160, margin: "0 auto", padding: "0 20px" },
} as const;

export function RivinityLandingPage({
  routes = defaultRoutes,
  treesPlanted = 15234,
  metrics = defaultMetrics,
}: RivinityLandingPageProps) {
  const featureCards = [
    { title: "AI-powered browsing", body: "Research, code, automate and summarize from one command center." },
    { title: "Local-first privacy", body: "Masking/unmasking + secure upload sealing with policy-aware boundaries." },
    { title: "Cross-platform", body: "Web, PWA, Android, iOS, extension, and desktop experiences." },
    { title: "Marketplace ecosystem", body: "Install and publish community agents like an app store." },
  ];

  return (
    <main style={styles.page}>
      <section style={{ ...styles.section, paddingTop: 64, paddingBottom: 36 }}>
        <div
          style={{
            borderRadius: 28,
            background: "linear-gradient(135deg,#ffffff,#eef2ff 45%,#e0e7ff)",
            border: "1px solid #dbe4ff",
            padding: "52px 28px",
            textAlign: "center",
            boxShadow: "0 20px 45px rgba(17,24,39,.08)",
          }}
        >
          <div style={{ fontWeight: 700, color: "#4f46e5", marginBottom: 10 }}>Rivinity AI Browser</div>
          <h1 style={{ margin: 0, fontSize: 58, lineHeight: 1.06 }}>The browser built around your intelligence</h1>
          <p style={{ maxWidth: 860, margin: "18px auto", color: "#475569", fontSize: 18 }}>
            Faster workflows, secure automation, private local inference, and a unified agent marketplace — engineered to compete at world-class level.
          </p>

          <div style={{ display: "flex", gap: 10, justifyContent: "center", flexWrap: "wrap", marginTop: 14 }}>
            <a href={routes.windows}><button>Download for Windows</button></a>
            <a href={routes.mac}><button>Download for macOS</button></a>
            <a href={routes.linux}><button>Download for Linux</button></a>
            <a href={routes.extension}><button>Add Browser Extension</button></a>
            <a href={routes.pwa}><button>Launch PWA</button></a>
          </div>

          <div style={{ display: "flex", justifyContent: "center", gap: 12, marginTop: 14, flexWrap: "wrap" }}>
            <a href={routes.android}><button>Get Android App</button></a>
            <a href={routes.ios}><button>Get iOS App</button></a>
          </div>
        </div>
      </section>

      <section style={{ ...styles.section, paddingTop: 18, paddingBottom: 24 }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))", gap: 12 }}>
          {metrics.map((m) => (
            <article key={m.label} style={{ background: "#fff", border: "1px solid #e2e8f0", borderRadius: 14, padding: 16 }}>
              <div style={{ fontSize: 28, fontWeight: 800 }}>{m.value}</div>
              <div style={{ color: "#64748b" }}>{m.label}</div>
            </article>
          ))}
        </div>
      </section>

      <section style={{ ...styles.section, paddingTop: 10, paddingBottom: 28 }}>
        <h2 style={{ textAlign: "center", fontSize: 40, marginBottom: 16 }}>Built for performance, security, and scale</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))", gap: 12 }}>
          {featureCards.map((card) => (
            <article key={card.title} style={{ background: "#fff", borderRadius: 16, border: "1px solid #e2e8f0", padding: 18 }}>
              <h3 style={{ marginTop: 0 }}>{card.title}</h3>
              <p style={{ marginBottom: 0, color: "#475569" }}>{card.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section style={{ ...styles.section, paddingTop: 8, paddingBottom: 56 }}>
        <div
          style={{
            background: "linear-gradient(135deg,#111827,#4338ca)",
            borderRadius: 22,
            color: "#fff",
            padding: 26,
            display: "grid",
            gridTemplateColumns: "2fr 1fr",
            gap: 16,
            alignItems: "center",
          }}
        >
          <div>
            <h2 style={{ marginTop: 0 }}>Every download plants one tree 🌱</h2>
            <p style={{ opacity: 0.9, maxWidth: 620 }}>
              Rivinity contributes to verified restoration projects. Your installation helps reduce carbon impact while accelerating your digital productivity.
            </p>
            <div style={{ fontSize: 30, fontWeight: 900 }}>{treesPlanted.toLocaleString()} trees planted</div>
          </div>
          <div style={{ textAlign: "right" }}>
            <a href="/impact"><button>View Impact Report</button></a>
          </div>
        </div>
      </section>
    </main>
  );
}
