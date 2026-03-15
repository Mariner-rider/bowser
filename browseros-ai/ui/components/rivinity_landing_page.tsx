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
  page: {
    fontFamily: "Inter,system-ui,sans-serif",
    color: "#0f172a",
    background: "linear-gradient(180deg,#f8fafc,#f1f5ff 42%,#f8fafc)",
  },
  section: { maxWidth: 1160, margin: "0 auto", padding: "0 20px" },
  pillBtn: {
    borderRadius: 999,
    border: "1px solid #d1d5db",
    padding: "10px 16px",
    background: "#fff",
    cursor: "pointer",
    fontWeight: 600,
  },
} as const;

export function RivinityLandingPage({
  routes = defaultRoutes,
  treesPlanted = 15234,
  metrics = defaultMetrics,
}: RivinityLandingPageProps) {
  const featureCards = [
    {
      title: "AI-powered browsing",
      body: "Research, code, automate and summarize from one command center with policy-aware routing.",
    },
    {
      title: "Local-first privacy",
      body: "Masking/unmasking, secure upload sealing, and guarded execution paths by default.",
    },
    {
      title: "Cross-platform",
      body: "Web, PWA, Android, iOS, extension, and desktop experiences with a shared brain.",
    },
    {
      title: "Marketplace ecosystem",
      body: "Install and publish community agents with app-store-like discoverability.",
    },
  ];

  const compareRows = [
    ["Secure upload masking + unsealing", "✅", "⚠️"],
    ["Local + cloud hybrid inference", "✅", "⚠️"],
    ["Agent marketplace publishing", "✅", "❌"],
    ["Cross-platform delivery", "✅", "⚠️"],
    ["Tree impact tracking", "✅", "❌"],
  ];

  const faqs = [
    {
      q: "Can I run Rivinity without cloning external browser repos?",
      a: "Yes. Rivinity includes a clean-room local runtime and end-to-end scripts for local execution.",
    },
    {
      q: "Do upload files remain secure?",
      a: "Yes. Uploads can be sealed/unsealed through protected APIs and metadata is masked before logging.",
    },
    {
      q: "Can public users publish agents?",
      a: "Yes. Marketplace supports public community submissions with publisher metadata and listing controls.",
    },
    {
      q: "How do I install Rivinity across devices?",
      a: "Use the direct platform download routes from this page for desktop, mobile, extension, or PWA.",
    },
  ];

  return (
    <main style={styles.page}>
      <section style={{ ...styles.section, paddingTop: 20, paddingBottom: 12 }}>
        <nav style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <strong style={{ fontSize: 20 }}>Rivinity Browser</strong>
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
            <a href="#features">Features</a>
            <a href="#security">Security</a>
            <a href="#pricing">Pricing</a>
            <a href="#downloads">Downloads</a>
          </div>
        </nav>
      </section>

      <section style={{ ...styles.section, paddingTop: 24, paddingBottom: 36 }}>
        <div
          style={{
            borderRadius: 30,
            background: "linear-gradient(135deg,#ffffff,#eef2ff 45%,#e0e7ff)",
            border: "1px solid #dbe4ff",
            padding: "56px 28px",
            textAlign: "center",
            boxShadow: "0 24px 55px rgba(17,24,39,.10)",
          }}
        >
          <div style={{ fontWeight: 700, color: "#4f46e5", marginBottom: 12 }}>Built for people who build fast</div>
          <h1 style={{ margin: 0, fontSize: 62, lineHeight: 1.04 }}>The AI browser built to outperform.</h1>
          <p style={{ maxWidth: 900, margin: "18px auto", color: "#475569", fontSize: 18 }}>
            Rivinity combines advanced automation, private local intelligence, secure workflows, and a public agent marketplace into one production-ready browser platform.
          </p>

          <div id="downloads" style={{ display: "flex", gap: 10, justifyContent: "center", flexWrap: "wrap", marginTop: 16 }}>
            <a href={routes.windows}><button style={styles.pillBtn}>Download for Windows</button></a>
            <a href={routes.mac}><button style={styles.pillBtn}>Download for macOS</button></a>
            <a href={routes.linux}><button style={styles.pillBtn}>Download for Linux</button></a>
            <a href={routes.extension}><button style={styles.pillBtn}>Add Browser Extension</button></a>
            <a href={routes.pwa}><button style={styles.pillBtn}>Launch PWA</button></a>
          </div>

          <div style={{ display: "flex", justifyContent: "center", gap: 12, marginTop: 14, flexWrap: "wrap" }}>
            <a href={routes.android}><button style={styles.pillBtn}>Get Android App</button></a>
            <a href={routes.ios}><button style={styles.pillBtn}>Get iOS App</button></a>
          </div>
        </div>
      </section>

      <section style={{ ...styles.section, paddingTop: 10, paddingBottom: 26 }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))", gap: 12 }}>
          {metrics.map((m) => (
            <article key={m.label} style={{ background: "#fff", border: "1px solid #e2e8f0", borderRadius: 14, padding: 16 }}>
              <div style={{ fontSize: 30, fontWeight: 800 }}>{m.value}</div>
              <div style={{ color: "#64748b" }}>{m.label}</div>
            </article>
          ))}
        </div>
      </section>

      <section id="features" style={{ ...styles.section, paddingTop: 14, paddingBottom: 30 }}>
        <h2 style={{ textAlign: "center", fontSize: 42, marginBottom: 16 }}>Built for performance, security, and scale</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))", gap: 12 }}>
          {featureCards.map((card) => (
            <article key={card.title} style={{ background: "#fff", borderRadius: 16, border: "1px solid #e2e8f0", padding: 18 }}>
              <h3 style={{ marginTop: 0 }}>{card.title}</h3>
              <p style={{ marginBottom: 0, color: "#475569" }}>{card.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="security" style={{ ...styles.section, paddingTop: 12, paddingBottom: 36 }}>
        <div style={{ background: "#fff", border: "1px solid #e2e8f0", borderRadius: 20, padding: 22 }}>
          <h2 style={{ marginTop: 0 }}>Security that protects users by design</h2>
          <p style={{ color: "#475569" }}>
            Rivinity uses secure masking and reversible protection primitives so sensitive operations are protected while still enabling authorized recovery.
          </p>

          <table style={{ width: "100%", borderCollapse: "collapse", marginTop: 10 }}>
            <thead>
              <tr style={{ textAlign: "left", borderBottom: "1px solid #e5e7eb" }}>
                <th style={{ padding: "10px 8px" }}>Capability</th>
                <th style={{ padding: "10px 8px" }}>Rivinity</th>
                <th style={{ padding: "10px 8px" }}>Typical Basic Browser</th>
              </tr>
            </thead>
            <tbody>
              {compareRows.map((row) => (
                <tr key={row[0]} style={{ borderBottom: "1px solid #f1f5f9" }}>
                  <td style={{ padding: "10px 8px" }}>{row[0]}</td>
                  <td style={{ padding: "10px 8px" }}>{row[1]}</td>
                  <td style={{ padding: "10px 8px" }}>{row[2]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section style={{ ...styles.section, paddingBottom: 26 }}>
        <div style={{ display: "grid", gridTemplateColumns: "1.2fr .8fr", gap: 14 }}>
          <article style={{ background: "#fff", border: "1px solid #e2e8f0", borderRadius: 18, padding: 20 }}>
            <h3 style={{ marginTop: 0 }}>Customer stories</h3>
            <p style={{ color: "#475569" }}>
              "Rivinity cut manual research time by 58% for our product team while improving reliability in high-stakes workflows."
            </p>
            <small>— Product Ops Lead, Growth Startup</small>
          </article>
          <article style={{ background: "#fff", border: "1px solid #e2e8f0", borderRadius: 18, padding: 20 }}>
            <h3 style={{ marginTop: 0 }}>Trusted by teams</h3>
            <p style={{ color: "#475569" }}>Adopted across engineering, research, ecommerce, and customer success operations.</p>
          </article>
        </div>
      </section>

      <section id="pricing" style={{ ...styles.section, paddingTop: 6, paddingBottom: 34 }}>
        <h2 style={{ textAlign: "center", fontSize: 36, marginBottom: 12 }}>Simple, transparent pricing</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))", gap: 12 }}>
          {[
            { tier: "Starter", price: "$0", items: ["Core browsing", "Basic agents", "Community support"] },
            { tier: "Growth", price: "$19", items: ["Automation workflows", "Marketplace publishing", "Secure upload workflows"] },
            { tier: "Scale", price: "$49", items: ["Advanced orchestration", "Priority support", "Enterprise policy controls"] },
          ].map((plan) => (
            <article key={plan.tier} style={{ background: "#fff", border: "1px solid #e2e8f0", borderRadius: 16, padding: 18 }}>
              <h3 style={{ marginTop: 0 }}>{plan.tier}</h3>
              <div style={{ fontSize: 34, fontWeight: 800 }}>{plan.price}</div>
              <ul>
                {plan.items.map((item) => <li key={item}>{item}</li>)}
              </ul>
              <button style={styles.pillBtn}>Choose {plan.tier}</button>
            </article>
          ))}
        </div>
      </section>

      <section style={{ ...styles.section, paddingTop: 4, paddingBottom: 24 }}>
        <h2 style={{ textAlign: "center" }}>Frequently asked questions</h2>
        <div style={{ display: "grid", gap: 10, maxWidth: 950, margin: "0 auto" }}>
          {faqs.map((faq) => (
            <details key={faq.q} style={{ background: "#fff", border: "1px solid #e2e8f0", borderRadius: 12, padding: "10px 14px" }}>
              <summary style={{ cursor: "pointer", fontWeight: 600 }}>{faq.q}</summary>
              <p style={{ color: "#475569", marginBottom: 4 }}>{faq.a}</p>
            </details>
          ))}
        </div>
      </section>

      <section style={{ ...styles.section, paddingTop: 10, paddingBottom: 56 }}>
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
            <a href="/impact"><button style={{ ...styles.pillBtn, background: "#fff" }}>View Impact Report</button></a>
          </div>
        </div>
      </section>

      <footer style={{ background: "#0f172a", color: "#e2e8f0", padding: "34px 20px" }}>
        <div style={{ ...styles.section, display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 12 }}>
          <div>
            <strong>Rivinity AI Browser</strong>
            <div style={{ fontSize: 12, opacity: 0.8 }}>Secure. Fast. Automated.</div>
          </div>
          <div style={{ display: "flex", gap: 14 }}>
            <a style={{ color: "#cbd5e1" }} href="/privacy">Privacy</a>
            <a style={{ color: "#cbd5e1" }} href="/terms">Terms</a>
            <a style={{ color: "#cbd5e1" }} href="/security">Security</a>
            <a style={{ color: "#cbd5e1" }} href="/docs">Docs</a>
          </div>
        </div>
      </footer>
    </main>
  );
}
