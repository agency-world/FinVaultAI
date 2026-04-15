/**
 * FinVault AI — Marketing Deck Generator
 * Creates a 10-slide professional PPTX presentation
 */
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const DOCS_DIR = path.join(__dirname, "..", "docs");
const SCREENSHOTS_DIR = path.join(DOCS_DIR, "screenshots");
const OUTPUT = path.join(DOCS_DIR, "FinVault_AI_Marketing_Deck.pptx");

// ── Color Palette (Midnight Indigo) ──
const C = {
  bg:        "0F1117",
  bgCard:    "1A1C2E",
  bgCard2:   "1E1B4B",
  indigo:    "6366F1",
  indigoLt:  "A5B4FC",
  indigoXlt: "C7D2FE",
  green:     "4ADE80",
  greenDk:   "22C55E",
  amber:     "FBBF24",
  red:       "F87171",
  white:     "E2E8F0",
  muted:     "94A3B8",
  dimmed:    "64748B",
  dark:      "0F1117",
  accent:    "4F46E5",
};

// ── Helper: fresh shadow factory ──
const makeShadow = () => ({
  type: "outer", color: "000000", blur: 8, offset: 3, angle: 135, opacity: 0.25
});

// ── Shape references (set after pres is created) ──
let SHAPES = null;

// ── Helper: add a full-bleed background rectangle ──
function addBg(slide, color) {
  slide.background = { color: color || C.bg };
}

// ── Helper: add slide title ──
function addTitle(slide, text, opts = {}) {
  slide.addText(text, {
    x: 0.7, y: 0.35, w: 8.6, h: 0.6,
    fontSize: 28, fontFace: "Arial", bold: true,
    color: C.indigoXlt, margin: 0,
    ...opts,
  });
}

// ── Helper: add a subtle top accent bar ──
function addAccentBar(slide) {
  slide.addShape(SHAPES.rect, {
    x: 0.7, y: 0.28, w: 1.2, h: 0.06,
    fill: { color: C.indigo },
  });
}

// ── Helper: add page number ──
function addPageNum(slide, num) {
  slide.addText(String(num), {
    x: 9.2, y: 5.2, w: 0.5, h: 0.3,
    fontSize: 9, color: C.dimmed, align: "right",
  });
}

// ── SLIDE 1: Title ──
function slide1(pres) {
  const s = pres.addSlide();
  addBg(s, C.bgCard2);

  // Decorative circle
  s.addShape(SHAPES.ellipse, {
    x: 7.5, y: -1.5, w: 5, h: 5,
    fill: { color: C.indigo, transparency: 88 },
  });
  s.addShape(SHAPES.ellipse, {
    x: -2, y: 3, w: 4, h: 4,
    fill: { color: C.indigo, transparency: 92 },
  });

  // Title
  s.addText("FinVault AI", {
    x: 0.7, y: 1.2, w: 8.6, h: 1.2,
    fontSize: 52, fontFace: "Arial", bold: true,
    color: C.indigoXlt, margin: 0,
  });

  // Subtitle
  s.addText("On-Device Financial Intelligence. Private by Design.", {
    x: 0.7, y: 2.4, w: 8.6, h: 0.6,
    fontSize: 20, fontFace: "Arial",
    color: C.muted, margin: 0,
  });

  // Accent line
  s.addShape(SHAPES.rect, {
    x: 0.7, y: 3.15, w: 2, h: 0.05,
    fill: { color: C.indigo },
  });

  // Badge row
  const badges = [
    { text: "Air-Gapped", color: C.greenDk },
    { text: "Gemma 4 Powered", color: C.indigo },
    { text: "Zero Cloud", color: C.amber },
  ];
  badges.forEach((b, i) => {
    s.addShape(SHAPES.rect, {
      x: 0.7 + i * 2.2, y: 3.5, w: 1.9, h: 0.38,
      fill: { color: b.color, transparency: 85 },
      line: { color: b.color, width: 0.75, transparency: 60 },
      rectRadius: 0.05,
    });
    s.addText(b.text, {
      x: 0.7 + i * 2.2, y: 3.5, w: 1.9, h: 0.38,
      fontSize: 10, fontFace: "Arial", bold: true,
      color: b.color, align: "center", valign: "middle", margin: 0,
    });
  });

  // Bottom
  s.addText("Confidential  |  April 2026", {
    x: 0.7, y: 5.0, w: 8.6, h: 0.35,
    fontSize: 10, color: C.dimmed, margin: 0,
  });
}

// ── SLIDE 2: The Problem ──
function slide2(pres) {
  const s = pres.addSlide();
  addBg(s, C.bg);
  addAccentBar(s);
  addTitle(s, "The Challenge: Financial Data at Risk");
  addPageNum(s, 2);

  const bullets = [
    "78% of financial firms cite data privacy as their #1 concern with AI adoption",
    "Cloud-based AI tools require sending sensitive accounting data to third-party servers",
    "Regulatory compliance (SOX, GDPR, CCPA) restricts data transfer to external APIs",
    "Manual report generation takes 4\u20138 hours per analyst per week",
    "Invoice processing backlogs average 12 days in mid-market firms",
    "No existing solution combines AI intelligence WITH complete data isolation",
  ];

  const items = bullets.map((b, i) => ({
    text: b,
    options: {
      bullet: true,
      breakLine: i < bullets.length - 1,
      color: C.white,
      fontSize: 14,
      fontFace: "Arial",
      paraSpaceAfter: 10,
    },
  }));

  s.addText(items, {
    x: 0.7, y: 1.15, w: 8.6, h: 4.0,
    valign: "top",
  });

  // Highlight box
  s.addShape(SHAPES.rect, {
    x: 0.7, y: 4.6, w: 8.6, h: 0.6,
    fill: { color: C.indigo, transparency: 88 },
    line: { color: C.indigo, width: 0.5, transparency: 70 },
  });
  s.addText("The gap: No AI tool delivers intelligence + total data isolation for finance teams.", {
    x: 0.9, y: 4.6, w: 8.2, h: 0.6,
    fontSize: 12, fontFace: "Arial", italic: true,
    color: C.indigoLt, valign: "middle", margin: 0,
  });
}

// ── SLIDE 3: Our Solution ──
function slide3(pres) {
  const s = pres.addSlide();
  addBg(s, C.bg);
  addAccentBar(s);
  addTitle(s, "FinVault AI: Intelligence Without Compromise");
  addPageNum(s, 3);

  const features = [
    {
      title: "Report Generator",
      desc: "AI-powered financial reports from your data. Executive summaries, expense breakdowns, trend analysis \u2014 generated in seconds, not hours.",
      icon: "\uD83D\uDCCA",
    },
    {
      title: "Data Query",
      desc: "Ask questions in plain English. Get precise answers with calculations. No SQL required. Your AI financial analyst, always available.",
      icon: "\uD83D\uDCAC",
    },
    {
      title: "Document OCR",
      desc: "Scan invoices, work-orders, receipts. Tesseract extracts text, AI parses structured fields. Digitize your paper trail instantly.",
      icon: "\uD83D\uDCC4",
    },
  ];

  features.forEach((f, i) => {
    const x = 0.5 + i * 3.1;
    // Card background
    s.addShape(SHAPES.rect, {
      x: x, y: 1.15, w: 2.9, h: 3.4,
      fill: { color: C.bgCard },
      line: { color: C.indigo, width: 0.5, transparency: 75 },
      shadow: makeShadow(),
    });
    // Icon
    s.addText(f.icon, {
      x: x, y: 1.3, w: 2.9, h: 0.5,
      fontSize: 28, align: "center", margin: 0,
    });
    // Feature title
    s.addText(f.title, {
      x: x + 0.2, y: 1.85, w: 2.5, h: 0.4,
      fontSize: 15, fontFace: "Arial", bold: true,
      color: C.indigoLt, align: "center", margin: 0,
    });
    // Description
    s.addText(f.desc, {
      x: x + 0.2, y: 2.3, w: 2.5, h: 2.0,
      fontSize: 11, fontFace: "Arial",
      color: C.muted, align: "center", valign: "top", margin: 0,
      lineSpacingMultiple: 1.3,
    });
  });

  // Bottom banner
  s.addShape(SHAPES.rect, {
    x: 0.5, y: 4.75, w: 9.0, h: 0.5,
    fill: { color: C.accent, transparency: 80 },
    line: { color: C.indigo, width: 0.5, transparency: 65 },
  });
  s.addText("100% Local   |   Zero Cloud   |   Air-Gapped Compatible", {
    x: 0.5, y: 4.75, w: 9.0, h: 0.5,
    fontSize: 12, fontFace: "Arial", bold: true,
    color: C.indigoLt, align: "center", valign: "middle", margin: 0,
  });
}

// ── SLIDES 4-6: Screenshots ──
function slideScreenshot(pres, num, title, imgFile, captions) {
  const s = pres.addSlide();
  addBg(s, C.bg);
  addAccentBar(s);
  addTitle(s, title);
  addPageNum(s, num);

  const imgPath = path.join(SCREENSHOTS_DIR, imgFile);
  if (fs.existsSync(imgPath)) {
    s.addImage({
      path: imgPath,
      x: 0.7, y: 1.1, w: 8.6, h: 3.0,
      sizing: { type: "contain", w: 8.6, h: 3.0 },
    });
  } else {
    s.addShape(SHAPES.rect, {
      x: 0.7, y: 1.1, w: 8.6, h: 3.0,
      fill: { color: C.bgCard },
      line: { color: C.indigo, width: 0.5, transparency: 70 },
    });
    s.addText("[Screenshot: " + imgFile + "]", {
      x: 0.7, y: 1.1, w: 8.6, h: 3.0,
      fontSize: 14, color: C.dimmed, align: "center", valign: "middle",
    });
  }

  // Caption bullets
  const items = captions.map((c, i) => ({
    text: c,
    options: {
      bullet: true,
      breakLine: i < captions.length - 1,
      color: C.muted,
      fontSize: 10,
      fontFace: "Arial",
      paraSpaceAfter: 4,
    },
  }));
  s.addText(items, {
    x: 0.7, y: 4.2, w: 8.6, h: 1.2,
    valign: "top",
  });
}

// ── SLIDE 7: Architecture ──
function slide7(pres) {
  const s = pres.addSlide();
  addBg(s, C.bg);
  addAccentBar(s);
  addTitle(s, "Secure Architecture: Nothing Leaves Your Machine");
  addPageNum(s, 7);

  const imgPath = path.join(SCREENSHOTS_DIR, "05_architecture.png");
  if (fs.existsSync(imgPath)) {
    s.addImage({
      path: imgPath,
      x: 0.7, y: 1.1, w: 8.6, h: 2.8,
      sizing: { type: "contain", w: 8.6, h: 2.8 },
    });
  }

  // Key callouts
  const callouts = [
    "Google Gemma 4 runs locally via LM Studio",
    "All API calls to localhost only",
    "No internet connection required",
    "Data exists only in browser session memory",
  ];

  callouts.forEach((c, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.7 + col * 4.4;
    const y = 4.1 + row * 0.55;

    s.addShape(SHAPES.rect, {
      x: x, y: y, w: 0.12, h: 0.35,
      fill: { color: C.greenDk },
    });
    s.addText(c, {
      x: x + 0.22, y: y, w: 4.0, h: 0.35,
      fontSize: 10, fontFace: "Arial", color: C.white,
      valign: "middle", margin: 0,
    });
  });
}

// ── SLIDE 8: Benefits / Impact ──
function slide8(pres) {
  const s = pres.addSlide();
  addBg(s, C.bg);
  addAccentBar(s);
  addTitle(s, "Measurable Impact");
  addPageNum(s, 8);

  const metrics = [
    { big: "85%", label: "faster", desc: "Report generation time vs. manual" },
    { big: "100%", label: "private", desc: "Zero data leaves your network" },
    { big: "12d \u2192 2h", label: "turnaround", desc: "Invoice processing turnaround" },
    { big: "$0", label: "cloud cost", desc: "No API fees, no subscriptions" },
    { big: "SOX/GDPR", label: "ready", desc: "Full regulatory compliance by design" },
    { big: "Air-gap", label: "compatible", desc: "Works in secure environments" },
  ];

  metrics.forEach((m, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.5 + col * 3.1;
    const y = 1.2 + row * 2.05;

    // Card
    s.addShape(SHAPES.rect, {
      x: x, y: y, w: 2.9, h: 1.8,
      fill: { color: C.bgCard },
      line: { color: C.indigo, width: 0.5, transparency: 75 },
      shadow: makeShadow(),
    });
    // Big number
    s.addText(m.big, {
      x: x, y: y + 0.2, w: 2.9, h: 0.65,
      fontSize: 30, fontFace: "Arial", bold: true,
      color: C.indigoLt, align: "center", margin: 0,
    });
    // Label
    s.addText(m.label, {
      x: x, y: y + 0.8, w: 2.9, h: 0.3,
      fontSize: 12, fontFace: "Arial", bold: true,
      color: C.green, align: "center", margin: 0,
      charSpacing: 2,
    });
    // Description
    s.addText(m.desc, {
      x: x + 0.2, y: y + 1.15, w: 2.5, h: 0.45,
      fontSize: 10, fontFace: "Arial",
      color: C.muted, align: "center", margin: 0,
    });
  });
}

// ── SLIDE 9: Roadmap ──
function slide9(pres) {
  const s = pres.addSlide();
  addBg(s, C.bg);
  addAccentBar(s);
  addTitle(s, "Product Roadmap");
  addPageNum(s, 9);

  const imgPath = path.join(SCREENSHOTS_DIR, "06_roadmap.png");
  if (fs.existsSync(imgPath)) {
    s.addImage({
      path: imgPath,
      x: 0.7, y: 1.1, w: 8.6, h: 2.6,
      sizing: { type: "contain", w: 8.6, h: 2.6 },
    });
  }

  // Timeline
  const phases = [
    { q: "Q2 2026", label: "Current", desc: "Core platform — Reports, Query, OCR", color: C.greenDk },
    { q: "Q3 2026", label: "Next", desc: "RAG pipeline, anomaly detection", color: C.indigo },
    { q: "Q4 2026", label: "Scale", desc: "Enterprise features, multi-user", color: C.amber },
    { q: "Q1 2027", label: "Mature", desc: "Observability, advanced agents", color: C.indigoLt },
  ];

  // Timeline line
  s.addShape(SHAPES.line, {
    x: 1.2, y: 4.25, w: 7.6, h: 0,
    line: { color: C.indigo, width: 2, transparency: 50 },
  });

  phases.forEach((p, i) => {
    const x = 0.9 + i * 2.2;
    // Dot
    s.addShape(SHAPES.ellipse, {
      x: x + 0.7, y: 4.08, w: 0.3, h: 0.3,
      fill: { color: p.color },
    });
    // Quarter
    s.addText(p.q, {
      x: x, y: 3.6, w: 1.8, h: 0.35,
      fontSize: 11, fontFace: "Arial", bold: true,
      color: p.color, align: "center", margin: 0,
    });
    // Description
    s.addText(p.desc, {
      x: x, y: 4.5, w: 1.8, h: 0.7,
      fontSize: 9, fontFace: "Arial",
      color: C.muted, align: "center", margin: 0,
    });
  });
}

// ── SLIDE 10: Closing ──
function slide10(pres) {
  const s = pres.addSlide();
  addBg(s, C.bgCard2);

  // Decorative
  s.addShape(SHAPES.ellipse, {
    x: 6.5, y: -2, w: 6, h: 6,
    fill: { color: C.indigo, transparency: 90 },
  });

  s.addText("FinVault AI", {
    x: 0.7, y: 1.0, w: 8.6, h: 1.0,
    fontSize: 48, fontFace: "Arial", bold: true,
    color: C.indigoXlt, margin: 0, align: "center",
  });

  s.addText("Your data. Your AI. Your machine.", {
    x: 0.7, y: 2.1, w: 8.6, h: 0.6,
    fontSize: 22, fontFace: "Arial", italic: true,
    color: C.white, margin: 0, align: "center",
  });

  s.addShape(SHAPES.rect, {
    x: 3.5, y: 2.85, w: 3.0, h: 0.04,
    fill: { color: C.indigo },
  });

  s.addText("On-device financial intelligence. Private by design.", {
    x: 0.7, y: 3.1, w: 8.6, h: 0.5,
    fontSize: 14, fontFace: "Arial",
    color: C.muted, margin: 0, align: "center",
  });

  // CTA box
  s.addShape(SHAPES.rect, {
    x: 2.5, y: 3.9, w: 5, h: 1.0,
    fill: { color: C.indigo, transparency: 85 },
    line: { color: C.indigo, width: 0.5, transparency: 60 },
  });
  s.addText([
    { text: "Next Steps", options: { bold: true, fontSize: 14, color: C.indigoLt, breakLine: true } },
    { text: "Schedule a live demo  |  hello@finvault.ai", options: { fontSize: 11, color: C.muted } },
  ], {
    x: 2.5, y: 3.9, w: 5, h: 1.0,
    align: "center", valign: "middle", margin: 0,
  });

  addPageNum(s, 10);
}

// ── MAIN ──
async function main() {
  const pres = new pptxgen();
  SHAPES = pres.ShapeType;
  pres.layout = "LAYOUT_16x9";
  pres.author = "FinVault AI";
  pres.title = "FinVault AI — Marketing Deck";
  pres.subject = "On-Device Financial Intelligence";

  slide1(pres);
  slide2(pres);
  slide3(pres);

  slideScreenshot(pres, 4, "Intelligent Report Generation", "01_dashboard_report.png", [
    "Upload CSV/Excel accounting data",
    "7 report types including Executive Summary, Expense Breakdown",
    "Interactive charts and real-time metrics",
    "Download reports for internal distribution",
  ]);

  slideScreenshot(pres, 5, "Natural Language Financial Analysis", "02_data_query.png", [
    "Chat-style interface for intuitive interaction",
    "Step-by-step calculations with source data references",
    "Maintains conversation context for follow-up questions",
    'Example: "What is Q1 revenue?" yields $401,200 with full breakdown',
  ]);

  slideScreenshot(pres, 6, "Automated Document Processing", "03_ocr_processing.png", [
    "Tesseract OCR extracts text at 87%+ confidence",
    "AI parses structured fields: invoice number, amounts, line items",
    "Supports invoices, work orders, receipts, purchase orders",
    "Export raw text or parsed data",
  ]);

  slide7(pres);
  slide8(pres);
  slide9(pres);
  slide10(pres);

  await pres.writeFile({ fileName: OUTPUT });
  console.log("PPTX created:", OUTPUT);
}

main().catch(console.error);
