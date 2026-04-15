#!/usr/bin/perl
use strict;
use warnings;
use File::Basename;
use File::Path qw(make_path remove_tree);
use File::Copy;
use Cwd 'abs_path';
use MIME::Base64;
use POSIX qw(ceil);

# --- Config ---
my $base_dir = dirname(abs_path($0));
my $screenshots_dir = "$base_dir/screenshots";
my $output_file = "$base_dir/FinVault_AI_Technical_Guide.docx";
my $tmp_dir = "$base_dir/_docx_tmp";

# Clean and create tmp structure
remove_tree($tmp_dir) if -d $tmp_dir;
make_path("$tmp_dir/word/media");
make_path("$tmp_dir/word/_rels");
make_path("$tmp_dir/_rels");
make_path("$tmp_dir/docProps");

# --- Screenshot files ---
my @screenshots = (
    "01_dashboard_report.png",
    "02_data_query.png",
    "03_ocr_processing.png",
    "04_admin_panel.png",
    "05_architecture.png",
    "06_roadmap.png",
);

# Copy screenshots to media dir and get dimensions
my %img_rels;
my $img_idx = 1;
for my $img (@screenshots) {
    my $src = "$screenshots_dir/$img";
    if (-f $src) {
        my $dest = "$tmp_dir/word/media/image${img_idx}.png";
        copy($src, $dest) or warn "Cannot copy $img: $!";
        $img_rels{$img} = "rId" . (10 + $img_idx);
        $img_idx++;
    }
}

# --- [Content_Types].xml ---
my $content_types = <<'XML';
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Default Extension="jpg" ContentType="image/jpeg"/>
  <Default Extension="jpeg" ContentType="image/jpeg"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
  <Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
  <Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
XML
write_file("$tmp_dir/[Content_Types].xml", $content_types);

# --- _rels/.rels ---
my $root_rels = <<'XML';
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
XML
write_file("$tmp_dir/_rels/.rels", $root_rels);

# --- word/_rels/document.xml.rels ---
my $doc_rels = <<'XML';
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
  <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>
  <Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>
XML

for my $img (@screenshots) {
    if (exists $img_rels{$img}) {
        my $rid = $img_rels{$img};
        (my $num = $rid) =~ s/rId//;
        $doc_rels .= qq{  <Relationship Id="$rid" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image} . ($num - 10) . qq{.png"/>\n};
    }
}
$doc_rels .= "</Relationships>\n";
write_file("$tmp_dir/word/_rels/document.xml.rels", $doc_rels);

# --- docProps/core.xml ---
my $core_props = <<'XML';
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:dcterms="http://purl.org/dc/terms/"
  xmlns:dcmitype="http://purl.org/dc/dcmitype/"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>FinVault AI - Technical Guide</dc:title>
  <dc:subject>Product Design, Development &amp; Deployment Guide</dc:subject>
  <dc:creator>FinVault AI Team</dc:creator>
  <dc:description>Comprehensive technical documentation for FinVault AI v3.0</dc:description>
  <dcterms:created xsi:type="dcterms:W3CDTF">2026-04-12T00:00:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2026-04-12T00:00:00Z</dcterms:modified>
  <cp:revision>1</cp:revision>
</cp:coreProperties>
XML
write_file("$tmp_dir/docProps/core.xml", $core_props);

# --- docProps/app.xml ---
my $app_props = <<'XML';
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
  <Application>FinVault AI Document Generator</Application>
  <AppVersion>3.0</AppVersion>
  <Company>FinVault AI</Company>
</Properties>
XML
write_file("$tmp_dir/docProps/app.xml", $app_props);

# --- word/settings.xml ---
my $settings = <<'XML';
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:defaultTabStop w:val="720"/>
  <w:compat>
    <w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>
  </w:compat>
</w:settings>
XML
write_file("$tmp_dir/word/settings.xml", $settings);

# --- word/numbering.xml ---
my $numbering = <<'XML';
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:abstractNum w:abstractNumId="0">
    <w:lvl w:ilvl="0">
      <w:start w:val="1"/>
      <w:numFmt w:val="bullet"/>
      <w:lvlText w:val="&#x2022;"/>
      <w:lvlJc w:val="left"/>
      <w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>
      <w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default"/></w:rPr>
    </w:lvl>
    <w:lvl w:ilvl="1">
      <w:start w:val="1"/>
      <w:numFmt w:val="bullet"/>
      <w:lvlText w:val="&#x25E6;"/>
      <w:lvlJc w:val="left"/>
      <w:pPr><w:ind w:left="1440" w:hanging="360"/></w:pPr>
      <w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:hint="default"/></w:rPr>
    </w:lvl>
  </w:abstractNum>
  <w:abstractNum w:abstractNumId="1">
    <w:lvl w:ilvl="0">
      <w:start w:val="1"/>
      <w:numFmt w:val="decimal"/>
      <w:lvlText w:val="%1."/>
      <w:lvlJc w:val="left"/>
      <w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>
    </w:lvl>
  </w:abstractNum>
  <w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
  <w:num w:numId="2"><w:abstractNumId w:val="1"/></w:num>
</w:numbering>
XML
write_file("$tmp_dir/word/numbering.xml", $numbering);

# --- word/styles.xml ---
my $styles = <<'XML';
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri" w:eastAsia="Calibri"/>
        <w:sz w:val="21"/>
        <w:szCs w:val="21"/>
        <w:lang w:val="en-US"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="120" w:line="276" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:keepNext/>
      <w:keepLines/>
      <w:spacing w:before="360" w:after="160"/>
      <w:outlineLvl w:val="0"/>
      <w:pBdr><w:bottom w:val="single" w:sz="8" w:space="4" w:color="6366F1"/></w:pBdr>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      <w:b/>
      <w:color w:val="312E81"/>
      <w:sz w:val="44"/>
      <w:szCs w:val="44"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:keepNext/>
      <w:keepLines/>
      <w:spacing w:before="280" w:after="120"/>
      <w:outlineLvl w:val="1"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      <w:b/>
      <w:color w:val="312E81"/>
      <w:sz w:val="32"/>
      <w:szCs w:val="32"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:keepNext/>
      <w:keepLines/>
      <w:spacing w:before="200" w:after="80"/>
      <w:outlineLvl w:val="2"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      <w:b/>
      <w:color w:val="6366F1"/>
      <w:sz w:val="26"/>
      <w:szCs w:val="26"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="60"/></w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      <w:b/>
      <w:color w:val="1E1B4B"/>
      <w:sz w:val="84"/>
      <w:szCs w:val="84"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Subtitle">
    <w:name w:val="Subtitle"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="60"/></w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      <w:i/>
      <w:color w:val="6366F1"/>
      <w:sz w:val="32"/>
      <w:szCs w:val="32"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ListBullet">
    <w:name w:val="List Bullet"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:numPr><w:numId w:val="1"/></w:numPr>
      <w:spacing w:after="60"/>
    </w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Caption">
    <w:name w:val="Caption"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="200"/></w:pPr>
    <w:rPr>
      <w:i/>
      <w:color w:val="6B7280"/>
      <w:sz w:val="18"/>
      <w:szCs w:val="18"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="CodeBlock">
    <w:name w:val="Code Block"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:shd w:val="clear" w:color="auto" w:fill="F1F5F9"/>
      <w:spacing w:before="120" w:after="120" w:line="240" w:lineRule="auto"/>
      <w:ind w:left="288"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>
      <w:color w:val="374151"/>
      <w:sz w:val="18"/>
      <w:szCs w:val="18"/>
    </w:rPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:basedOn w:val="TableNormal"/>
    <w:tblPr>
      <w:tblBorders>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="C7D2FE"/>
        <w:left w:val="single" w:sz="4" w:space="0" w:color="C7D2FE"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="C7D2FE"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="C7D2FE"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="C7D2FE"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="C7D2FE"/>
      </w:tblBorders>
    </w:tblPr>
  </w:style>
  <w:style w:type="table" w:default="1" w:styleId="TableNormal">
    <w:name w:val="Normal Table"/>
    <w:tblPr>
      <w:tblInd w:w="0" w:type="dxa"/>
      <w:tblCellMar>
        <w:top w:w="0" w:type="dxa"/>
        <w:left w:w="108" w:type="dxa"/>
        <w:bottom w:w="0" w:type="dxa"/>
        <w:right w:w="108" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
  </w:style>
</w:styles>
XML
write_file("$tmp_dir/word/styles.xml", $styles);

# --- word/header1.xml ---
my $header = <<'XML';
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:jc w:val="right"/>
      <w:pBdr><w:bottom w:val="single" w:sz="4" w:space="4" w:color="C7D2FE"/></w:pBdr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
        <w:sz w:val="16"/>
        <w:color w:val="6B7280"/>
      </w:rPr>
      <w:t>FinVault AI  |  Technical Guide v3.0</w:t>
    </w:r>
  </w:p>
</w:hdr>
XML
write_file("$tmp_dir/word/header1.xml", $header);

# --- word/footer1.xml ---
my $footer = <<'XML';
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr><w:jc w:val="center"/></w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
        <w:sz w:val="16"/>
        <w:color w:val="6B7280"/>
      </w:rPr>
      <w:t xml:space="preserve">Confidential &#x2014; Internal Use Only    |    Page </w:t>
    </w:r>
    <w:r>
      <w:fldChar w:fldCharType="begin"/>
    </w:r>
    <w:r>
      <w:instrText xml:space="preserve"> PAGE </w:instrText>
    </w:r>
    <w:r>
      <w:fldChar w:fldCharType="end"/>
    </w:r>
  </w:p>
</w:ftr>
XML
write_file("$tmp_dir/word/footer1.xml", $footer);

# =========================================================================
# BUILD DOCUMENT BODY
# =========================================================================

my @body_parts;

# Section properties with header/footer refs
my $sect_props = <<'XML';
<w:sectPr>
  <w:headerReference w:type="default" r:id="rId4" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>
  <w:footerReference w:type="default" r:id="rId5" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>
  <w:pgSz w:w="12240" w:h="15840"/>
  <w:pgMar w:top="1152" w:right="1440" w:bottom="1152" w:left="1440" w:header="720" w:footer="720"/>
</w:sectPr>
XML

# ===== COVER PAGE =====
# Spacing
for (1..7) { push @body_parts, para("", {after => 0}); }

# Accent line
push @body_parts, accent_line();

# Title
push @body_parts, styled_para("FinVault AI", "Title");

# Subtitle
push @body_parts, styled_para("Product Design, Development &amp; Deployment Guide", "Subtitle");

# Accent line
push @body_parts, accent_line();

# Version/date
push @body_parts, para_centered("Version 3.0  |  April 2026", {size => 22, color => "6B7280", before => 400});

# Tagline
push @body_parts, para_centered("On-device financial intelligence. Private by design.", {size => 24, color => "6366F1", italic => 1, before => 600});

# Spacing
for (1..5) { push @body_parts, para("", {after => 0}); }

# Confidential notice
push @body_parts, para_centered("CONFIDENTIAL &#x2014; INTERNAL USE ONLY", {size => 18, color => "6B7280", bold => 1, caps => 1});

push @body_parts, page_break();

# ===== TABLE OF CONTENTS =====
push @body_parts, heading(1, "Table of Contents");
push @body_parts, para("", {after => 60});

my @toc = (
    [1, "1.", "Executive Overview"],
    [1, "2.", "Product Design"],
    [2, "", "2.1  Design Philosophy"],
    [2, "", "2.2  User Personas"],
    [2, "", "2.3  Feature Set"],
    [2, "", "2.4  UX Design Decisions"],
    [1, "3.", "System Architecture"],
    [2, "", "3.1  High-Level Architecture"],
    [2, "", "3.2  Component Breakdown"],
    [2, "", "3.3  Data Flow Diagram"],
    [1, "4.", "Agent Engineering &amp; LLM Configuration"],
    [2, "", "4.1  Secure LLM Usage"],
    [2, "", "4.2  Prompt Engineering Best Practices"],
    [2, "", "4.3  Configuration Parameters"],
    [2, "", "4.4  Multi-Modal Capabilities"],
    [1, "5.", "Development Technical Guide"],
    [2, "", "5.1  Project Structure"],
    [2, "", "5.2  Technology Stack"],
    [2, "", "5.3  Development Setup"],
    [2, "", "5.4  Code Quality Best Practices"],
    [1, "6.", "Deployment Process"],
    [2, "", "6.1  Local Deployment"],
    [2, "", "6.2  Docker Deployment"],
    [2, "", "6.3  Enterprise Deployment"],
    [1, "7.", "User Demo Guide"],
    [2, "", "7.1  Report Generation Demo"],
    [2, "", "7.2  Natural Language Query Demo"],
    [2, "", "7.3  OCR Document Processing Demo"],
    [1, "8.", "Roadmap &#x2014; Future Enhancements"],
    [2, "", "8.1  Phase 2 &#x2014; Intelligence (Q3 2026)"],
    [2, "", "8.2  Phase 3 &#x2014; Enterprise (Q4 2026)"],
    [2, "", "8.3  Phase 4 &#x2014; Scale (Q1 2027)"],
    [2, "", "8.4  Security Enhancements"],
    [2, "", "8.5  Optimization"],
    [1, "9.", "Appendix"],
    [2, "", "9.1  System Prompts Reference"],
    [2, "", "9.2  Supported File Types"],
    [2, "", "9.3  Sample Data Files"],
);

for my $entry (@toc) {
    my ($lvl, $num, $title) = @$entry;
    my $is_main = $lvl == 1;
    my $indent = $is_main ? 0 : 576;
    my $sz = $is_main ? 22 : 20;
    my $color = $is_main ? "312E81" : "374151";
    my $bold = $is_main ? 1 : 0;
    my $before_sp = $is_main ? 120 : 40;

    my $runs = "";
    if ($num) {
        $runs .= run($num . "  ", {size => $sz, color => "6366F1", bold => 1});
    }
    $runs .= run($title, {size => $sz, color => $color, bold => $bold});

    push @body_parts, <<XML;
<w:p>
  <w:pPr>
    <w:spacing w:before="$before_sp" w:after="40"/>
    <w:ind w:left="$indent"/>
  </w:pPr>
  $runs
</w:p>
XML
}

push @body_parts, page_break();

# ===== 1. EXECUTIVE OVERVIEW =====
push @body_parts, heading(1, "1. Executive Overview");

push @body_parts, para("FinVault AI is a secure, 100% local financial intelligence platform designed to bring the power of modern large language models to financial professionals without compromising data privacy or security. Built on a zero-cloud, air-gapped architecture, the application processes all data on-device using Google Gemma 4 running through LM Studio&#x2019;s local inference server.");

push @body_parts, para("The platform eliminates the fundamental tension between AI capability and data security that plagues cloud-based solutions. No financial data, prompts, or inference results ever leave the user&#x2019;s machine. This makes FinVault AI suitable for environments with the strictest regulatory and compliance requirements, including SOX-governed organizations, auditing firms, and financial institutions.");

push @body_parts, heading(3, "Target Users");
push @body_parts, bullet("Financial professionals (CFOs, Controllers, Financial Analysts)");
push @body_parts, bullet("Accountants and bookkeepers managing ledger data");
push @body_parts, bullet("Auditors requiring secure document analysis");
push @body_parts, bullet("Accounts Payable / Accounts Receivable clerks processing invoices and receipts");

push @body_parts, heading(3, "Core Capabilities");

push @body_parts, table_xml(
    ["Capability", "Description"],
    [
        ["Report Generation", "AI-generated financial reports from CSV/Excel data &#x2014; 7 report types including Executive Summary, Ledger Analysis, Expense Breakdown, and more"],
        ["Natural Language Query", "Chat-style data analysis: ask questions about your financial data in plain English and receive data-grounded answers with step-by-step calculations"],
        ["Document OCR", "Extract and parse structured data from invoices, work orders, receipts, and purchase orders using Tesseract OCR + Gemma AI parsing"],
        ["Admin Panel", "Configure model parameters, monitor system health, and manage inference settings in real time"],
    ],
    [2600, 6760]
);

push @body_parts, heading(3, "Key Differentiator");
push @body_parts, para("FinVault AI&#x2019;s core differentiator is its zero-cloud, air-gapped architecture. The entire AI inference pipeline runs locally on the user&#x2019;s hardware. There are no API keys to manage, no cloud endpoints to secure, and no data egress to monitor. The application can operate on a completely disconnected network, making it ideal for sensitive financial environments.");

push @body_parts, page_break();

# ===== 2. PRODUCT DESIGN =====
push @body_parts, heading(1, "2. Product Design");

push @body_parts, heading(2, "2.1 Design Philosophy");
push @body_parts, para("FinVault AI is built on three foundational design principles that guide every architectural and UX decision:");
push @body_parts, bold_bullet("Privacy-First: ", "All data processing occurs locally. No information is transmitted to external servers. The application requires no internet connectivity to function after initial setup.");
push @body_parts, bold_bullet("Local-First: ", "The complete AI inference pipeline runs on the user&#x2019;s hardware via LM Studio. This eliminates latency from network round-trips and ensures availability regardless of cloud service status.");
push @body_parts, bold_bullet("Modular Architecture: ", "The codebase follows strict separation of concerns &#x2014; UI components, core logic, configuration, and utilities are independently maintained modules that can be extended or replaced without affecting the rest of the system.");

push @body_parts, heading(2, "2.2 User Personas");
push @body_parts, table_xml(
    ["Persona", "Role", "Primary Use Case", "Key Need"],
    [
        ["CFO / Controller", "Executive oversight", "Executive summaries, trend analysis, variance reports", "Quick, accurate financial insights"],
        ["Staff Accountant", "Day-to-day accounting", "Ledger analysis, data queries, expense tracking", "Efficient data exploration"],
        ["Auditor", "Compliance review", "Document verification, cross-referencing, anomaly detection", "Secure document processing"],
        ["AP/AR Clerk", "Transaction processing", "Invoice OCR, receipt parsing, PO extraction", "Fast, accurate data extraction"],
    ],
    [1800, 1800, 2900, 2860]
);

push @body_parts, heading(2, "2.3 Feature Set");

push @body_parts, heading(3, "Report Generator");
push @body_parts, para("The Report Generator produces AI-authored financial reports from uploaded CSV or Excel data. Seven report types are available:");
for my $rt ("Executive Summary", "Detailed Ledger Analysis", "Expense Breakdown", "Revenue vs. Expense Comparison", "Cash Flow Summary", "Monthly Trend Analysis", "Budget Variance Report") {
    push @body_parts, bullet($rt);
}
push @body_parts, para("Each report includes automated statistical pre-computation (totals, means, category breakdowns) that is injected into the LLM prompt alongside the raw data, ensuring reports are grounded in actual figures.");

push @body_parts, heading(3, "Natural Language Query");
push @body_parts, para("The Data Query module enables conversational interaction with financial data. Users type questions in plain English (e.g., &#x201C;What is the total revenue for Q1 2026?&#x201D;) and receive data-grounded answers with step-by-step calculations. Chat history is maintained via Streamlit session state, allowing multi-turn conversations with context carryover.");

push @body_parts, heading(3, "Document OCR");
push @body_parts, para("The OCR pipeline processes financial documents in two stages: (1) Tesseract OCR extracts raw text from images with confidence scoring, and (2) Gemma AI parses the extracted text into structured fields using document-type-specific templates. Supported document types include Invoices, Work Orders, Receipts, Purchase Orders, and General Documents. When Tesseract is unavailable, the system falls back to Gemma 4&#x2019;s vision capabilities for direct image-to-text extraction.");

push @body_parts, heading(3, "Admin Panel");
push @body_parts, para("The Admin Panel provides real-time control over the AI inference pipeline. Users can adjust model temperature, maximum tokens, Top-P sampling, and other parameters. The panel also displays system health information including LM Studio connection status, loaded model details, and resource utilization.");

push @body_parts, heading(2, "2.4 UX Design Decisions");
push @body_parts, bold_bullet("Dark Theme: ", "Optimized for extended professional sessions. Reduces eye strain during prolonged financial analysis work.");
push @body_parts, bold_bullet("Tab-Based Navigation: ", "Primary features (Reports, Query, OCR) are organized as tabs for quick switching without page reloads.");
push @body_parts, bold_bullet("Progressive Disclosure: ", "Advanced options and detailed results are housed within Streamlit expanders, keeping the default view clean and focused.");
push @body_parts, bold_bullet("Responsive Layout: ", "The interface adapts to different screen sizes using Streamlit&#x2019;s column system, ensuring usability on both large monitors and laptops.");
push @body_parts, bold_bullet("Real-Time Feedback: ", "Spinners and status messages provide immediate feedback during AI inference, OCR processing, and data loading operations.");

push @body_parts, image_para("01_dashboard_report.png", "Figure 1: Report Generator &#x2014; data preview, metrics, and chart visualization");

push @body_parts, page_break();

# ===== 3. SYSTEM ARCHITECTURE =====
push @body_parts, heading(1, "3. System Architecture");

push @body_parts, heading(2, "3.1 High-Level Architecture");
push @body_parts, para("FinVault AI follows a strictly local client-server architecture where all components run on the user&#x2019;s machine within an air-gapped boundary:");

push @body_parts, code_block("User Browser\n    |\n    v\nStreamlit Web App (localhost:8501)\n    |                    |\n    v                    v\nLM Studio API           Tesseract OCR\n(localhost:1234)         (local binary)\n    |\n    v\nGoogle Gemma 4\n(on-device model)");

push @body_parts, para("The Streamlit application serves as the central orchestrator. It receives user input through the browser, routes requests to either the LM Studio API (for LLM inference) or Tesseract (for OCR), and renders results back to the user. All communication occurs over localhost &#x2014; no external network requests are made.");

push @body_parts, heading(2, "3.2 Component Breakdown");
push @body_parts, table_xml(
    ["File / Module", "Purpose"],
    [
        ["app.py", "Entry point. Page configuration, global CSS injection, tab routing, session state initialization."],
        ["config/settings.py", "Centralized constants: app identity, LM Studio defaults, LLM parameters, system prompts, OCR config, templates."],
        ["core/llm_client.py", "OpenAI-compatible client for LM Studio. Handles text completion and vision API calls with error handling."],
        ["core/ocr_engine.py", "Tesseract wrapper with image preprocessing. Extracts text with confidence scoring, handles fallback to vision API."],
        ["core/report_generator.py", "Prompt engineering module for financial reports. Builds context-rich prompts with data + statistics."],
        ["core/data_query.py", "Natural language question-to-answer pipeline. Injects CSV data + summary into prompts, manages chat context."],
        ["ui/sidebar.py", "Sidebar component: data upload, sample data toggle, file type selection, data preview."],
        ["ui/tab_reports.py", "Report Generator tab: metrics display, chart visualization, report type selection, AI report generation."],
        ["ui/tab_query.py", "Data Query tab: chat interface, message history, query input, AI response rendering."],
        ["ui/tab_ocr.py", "Document OCR tab: image upload, document type selection, OCR extraction, AI parsing, download options."],
        ["utils/data_loader.py", "File loading utilities for CSV, XLSX, XLS formats with error handling and validation."],
        ["utils/formatters.py", "Output formatting helpers: monetary values, markdown rendering, data summarization."],
    ],
    [2600, 6760]
);

push @body_parts, heading(2, "3.3 Data Flow Diagram");
push @body_parts, para("The following diagram illustrates the complete system architecture, showing how all components interact within the local air-gapped boundary:");

push @body_parts, image_para("05_architecture.png", "Figure 2: System Architecture &#x2014; all components run locally within an air-gapped boundary");

push @body_parts, page_break();

# ===== 4. AGENT ENGINEERING =====
push @body_parts, heading(1, "4. Agent Engineering &amp; LLM Configuration");

push @body_parts, heading(2, "4.1 How the LLM is Used Securely");
push @body_parts, para("FinVault AI treats security as a non-negotiable architectural constraint. The LLM integration is designed to ensure that no financial data ever leaves the user&#x2019;s machine:");
push @body_parts, bold_bullet("Local Inference Only: ", "All LLM calls go to localhost:1234 via the OpenAI-compatible API provided by LM Studio. There is no fallback to cloud endpoints.");
push @body_parts, bold_bullet("No External API Keys: ", "The only API key used is the local placeholder &#x2018;lm-studio&#x2019;, which never leaves the machine. No external service credentials are required.");
push @body_parts, bold_bullet("In-Memory Data Processing: ", "Financial data exists only in Streamlit session state during the active session. No data is persisted to disk by the application.");
push @body_parts, bold_bullet("Zero Telemetry: ", "No usage analytics, error reporting, or telemetry data is collected or transmitted. The application operates in complete isolation.");
push @body_parts, bold_bullet("User-Owned Hardware: ", "The Gemma 4 model runs on the user&#x2019;s own GPU or CPU. Model weights are stored locally and managed through LM Studio.");

push @body_parts, heading(2, "4.2 Prompt Engineering Best Practices");
push @body_parts, para("FinVault AI employs several prompt engineering techniques to ensure accurate, reliable financial analysis:");

push @body_parts, heading(3, "Expert Persona System Prompts");
push @body_parts, para("Each module uses a specialized system prompt that defines the AI&#x2019;s role and behavioral constraints. The Report Generator uses a CPA/financial analyst persona, the Data Query module uses a financial data analyst persona, and the OCR module uses a document parser persona.");

push @body_parts, heading(3, "Context Injection Strategy");
push @body_parts, para("Prompts are enriched with comprehensive context to ground the model&#x2019;s responses in actual data:");
push @body_parts, bullet("Full CSV data (up to 8,000 characters) is injected directly into the prompt");
push @body_parts, bullet("Pre-computed statistical summaries (totals, means, counts, category breakdowns) are included");
push @body_parts, bullet("Aggregated metrics are calculated before prompt construction to reduce hallucination risk");

push @body_parts, heading(3, "Structured Output Instructions");
push @body_parts, para("System prompts specify exact output formatting requirements:");
push @body_parts, bullet("Markdown tables for tabular data presentation");
push @body_parts, bullet("Defined report sections (Executive Summary, Key Metrics, Analysis, Risks, Recommendations)");
push @body_parts, bullet("Monetary value formatting (\$X,XXX.XX with commas and two decimal places)");
push @body_parts, bullet("Step-by-step calculation display for query responses");

push @body_parts, heading(3, "Temperature and Guard Rails");
push @body_parts, bold_bullet("Temperature: ", "Set to 0.15 by default for financial work, prioritizing deterministic, consistent outputs over creative variation. Adjustable via the Admin Panel.");
push @body_parts, bold_bullet("Data Grounding: ", "Prompts include explicit instructions to &#x2018;answer ONLY from data provided&#x2019; and to return &#x2018;N/A&#x2019; when information is not available in the dataset.");
push @body_parts, bold_bullet("Anomaly Flagging: ", "The query prompt instructs the model to proactively flag suspicious or inconsistent values encountered during analysis.");

push @body_parts, heading(2, "4.3 Configuration Parameters");
push @body_parts, para("The following inference parameters are configurable through the Admin Panel:");

push @body_parts, table_xml(
    ["Parameter", "Range", "Default", "Purpose"],
    [
        ["Temperature", "0.0 &#x2013; 1.0", "0.15", "Controls output randomness. Lower = more deterministic."],
        ["Max Tokens", "256 &#x2013; 4,096", "2,048 (reports: 3,072)", "Maximum length of generated response."],
        ["Top-P", "0.0 &#x2013; 1.0", "0.95", "Nucleus sampling threshold for token diversity."],
        ["Frequency Penalty", "0.0 &#x2013; 2.0", "0.0", "Penalizes repeated tokens to reduce redundancy."],
        ["Presence Penalty", "0.0 &#x2013; 2.0", "0.0", "Encourages the model to discuss new topics."],
        ["Model", "Any loaded model", "Gemma 4", "Supports any model loaded in LM Studio."],
        ["Endpoint URL", "Any localhost URL", "http://localhost:1234/v1", "LM Studio API endpoint."],
    ],
    [1900, 1600, 2200, 3660]
);

push @body_parts, heading(2, "4.4 Multi-Modal Capabilities");
push @body_parts, para("FinVault AI leverages Gemma 4&#x2019;s vision capabilities as a fallback mechanism for OCR processing. When Tesseract is unavailable or produces low-confidence results, the application encodes document images as Base64 and sends them to the vision-capable endpoint of the LM Studio API. This enables direct image-to-text extraction without external OCR dependencies.");
push @body_parts, para("The vision pipeline uses the same OpenAI-compatible API format, sending images as base64-encoded data URLs within the message content array. This approach maintains the zero-cloud architecture while providing robust document processing capabilities.");

push @body_parts, image_para("04_admin_panel.png", "Figure 3: Admin Panel &#x2014; model, inference settings, and system health monitoring");

push @body_parts, page_break();

# ===== 5. DEVELOPMENT TECHNICAL GUIDE =====
push @body_parts, heading(1, "5. Development Technical Guide");

push @body_parts, heading(2, "5.1 Project Structure");
push @body_parts, para("The application follows a modular directory structure with clear separation of concerns:");

push @body_parts, code_block("LocalGemmaApp/\n+-- app.py                     # Entry point, page config, tab routing\n+-- requirements.txt            # Python dependencies\n+-- .streamlit/\n|   +-- config.toml            # Streamlit server and theme config\n+-- config/\n|   +-- settings.py            # All constants, prompts, templates\n+-- core/\n|   +-- __init__.py\n|   +-- llm_client.py          # OpenAI-compatible LM Studio client\n|   +-- ocr_engine.py          # Tesseract wrapper + preprocessing\n|   +-- report_generator.py    # Prompt engineering for reports\n|   +-- data_query.py          # NL question to data answer\n+-- ui/\n|   +-- __init__.py\n|   +-- sidebar.py             # Data upload and preview sidebar\n|   +-- tab_reports.py         # Report Generator tab\n|   +-- tab_query.py           # Data Query chat tab\n|   +-- tab_ocr.py             # Document OCR tab\n+-- utils/\n|   +-- __init__.py\n|   +-- data_loader.py         # CSV/XLSX/XLS file loading\n|   +-- formatters.py          # Output formatting helpers\n+-- sample_data/\n|   +-- sample_accounts.csv\n|   +-- sample_accounts_payable.csv\n|   +-- sample_invoice.png\n|   +-- sample_invoice.pdf\n|   +-- sample_purchase_order.pdf\n|   +-- sample_receipt.png\n|   +-- sample_workorder.png\n+-- scripts/\n|   +-- generate_samples.py    # Synthetic test data generator\n|   +-- generate_screenshots.py\n|   +-- launcher.py            # Application launcher script\n+-- assets/                    # Static assets (icons, CSS)\n+-- docs/\n    +-- screenshots/           # Application screenshots\n    +-- FinVault_AI_Technical_Guide.docx");

push @body_parts, heading(2, "5.2 Technology Stack");
push @body_parts, table_xml(
    ["Technology", "Version", "Purpose"],
    [
        ["Python", "3.9+", "Core runtime"],
        ["Streamlit", "1.30+", "Web UI framework &#x2014; reactive, Python-native"],
        ["OpenAI SDK", "1.10+", "Client for OpenAI-compatible API (LM Studio)"],
        ["Pandas", "2.0+", "Data loading, manipulation, and statistical computation"],
        ["Plotly", "5.18+", "Interactive chart visualization"],
        ["Pillow", "10.0+", "Image processing and format handling"],
        ["pytesseract", "0.3.10+", "Python wrapper for Tesseract OCR engine"],
        ["openpyxl", "3.1+", "Excel file (.xlsx) reading support"],
        ["LM Studio", "Latest", "Local LLM inference server with OpenAI-compatible API"],
        ["Google Gemma 4", "Latest", "On-device large language model (text + vision)"],
        ["Tesseract OCR", "5.5+", "Open-source OCR engine (Homebrew / apt)"],
    ],
    [2200, 1400, 5760]
);

push @body_parts, heading(2, "5.3 Development Setup");
push @body_parts, para("Follow these steps to set up a local development environment:");

push @body_parts, heading(3, "Step 1: Clone the Repository");
push @body_parts, code_block("git clone &lt;repository-url&gt;\ncd LocalGemmaApp");

push @body_parts, heading(3, "Step 2: Install Python Dependencies");
push @body_parts, code_block("pip install -r requirements.txt");
push @body_parts, para("This installs: streamlit, openai, pandas, openpyxl, Pillow, pytesseract, plotly");

push @body_parts, heading(3, "Step 3: Install Tesseract OCR");
push @body_parts, code_block("# macOS (Homebrew)\nbrew install tesseract\n\n# Ubuntu / Debian\nsudo apt-get install tesseract-ocr\n\n# Verify installation\ntesseract --version");

push @body_parts, heading(3, "Step 4: Configure LM Studio");
push @body_parts, bullet("Download and install LM Studio from https://lmstudio.ai");
push @body_parts, bullet("Download Google Gemma 4 model (or any compatible model)");
push @body_parts, bullet("Start the local server (default: localhost:1234)");
push @body_parts, bullet("Ensure the server is running before launching FinVault AI");

push @body_parts, heading(3, "Step 5: Launch the Application");
push @body_parts, code_block("streamlit run app.py");
push @body_parts, para("The application will be available at http://localhost:8501 in your browser.");

push @body_parts, heading(2, "5.4 Code Quality Best Practices");
push @body_parts, bold_bullet("Modular Architecture: ", "Strict separation of UI components (ui/), core logic (core/), configuration (config/), and utilities (utils/). Each module has a single responsibility.");
push @body_parts, bold_bullet("Type Hints: ", "Python type annotations are used throughout the codebase to improve readability and enable static analysis.");
push @body_parts, bold_bullet("Centralized Configuration: ", "All constants, prompts, templates, and default values live in config/settings.py &#x2014; the single source of truth.");
push @body_parts, bold_bullet("Error Handling: ", "Graceful degradation throughout. OCR falls back to vision API when Tesseract is unavailable. LLM connection failures display informative error messages.");
push @body_parts, bold_bullet("Session State Management: ", "Streamlit session state is used to persist chat history, loaded data, and user preferences across reruns without server-side storage.");

push @body_parts, page_break();

# ===== 6. DEPLOYMENT PROCESS =====
push @body_parts, heading(1, "6. Deployment Process");

push @body_parts, heading(2, "6.1 Local Deployment (Recommended)");
push @body_parts, para("Local deployment is the recommended approach for FinVault AI, as it preserves the security guarantees of the air-gapped architecture. All components run directly on the user&#x2019;s machine.");

push @body_parts, heading(3, "Prerequisites");
push @body_parts, table_xml(
    ["Requirement", "Minimum", "Recommended"],
    [
        ["Python", "3.9", "3.11+"],
        ["RAM", "16 GB", "32 GB"],
        ["GPU", "Not required (CPU mode)", "8 GB+ VRAM (NVIDIA/Apple Silicon)"],
        ["Storage", "10 GB (model + app)", "20 GB (multiple models)"],
        ["LM Studio", "Latest stable", "Latest stable"],
        ["Tesseract", "5.0+", "5.5+"],
        ["OS", "macOS 12+ / Ubuntu 20.04+ / Win 10+", "macOS 14+ / Ubuntu 22.04+"],
    ],
    [2000, 3700, 3660]
);

push @body_parts, heading(3, "Deployment Steps");

push @body_parts, para_bold("1. Install Dependencies");
push @body_parts, code_block("pip install -r requirements.txt\nbrew install tesseract  # macOS");

push @body_parts, para_bold("2. Configure Streamlit");
push @body_parts, para("The .streamlit/config.toml file controls server settings and theme. Default configuration is provided.");

push @body_parts, para_bold("3. Start LM Studio");
push @body_parts, bullet("Launch LM Studio application");
push @body_parts, bullet("Load Google Gemma 4 (or preferred model)");
push @body_parts, bullet("Start the local server on port 1234");

push @body_parts, para_bold("4. Launch FinVault AI");
push @body_parts, code_block("streamlit run app.py");

push @body_parts, para_bold("5. Verify Connection");
push @body_parts, para("Navigate to the Admin Panel tab and confirm that LM Studio is connected and the model is loaded.");

push @body_parts, heading(3, "Deployment Process Flow");
push @body_parts, code_block("Install Dependencies -> Configure Streamlit -> Start LM Studio -> Launch App -> Verify Connection");

push @body_parts, heading(2, "6.2 Docker Deployment (Optional)");
push @body_parts, para("For containerized environments, FinVault AI can be deployed using Docker:");

push @body_parts, heading(3, "Dockerfile Pattern");
push @body_parts, code_block("FROM python:3.11-slim\n\n# Install Tesseract OCR\nRUN apt-get update &amp;&amp; apt-get install -y \\\\\n    tesseract-ocr \\\\\n    &amp;&amp; rm -rf /var/lib/apt/lists/*\n\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n\nCOPY . .\n\nEXPOSE 8501\nCMD [\"streamlit\", \"run\", \"app.py\", \"--server.port=8501\"]");

push @body_parts, heading(3, "Docker Compose");
push @body_parts, para("For a complete setup, use Docker Compose to orchestrate the Streamlit application alongside a separate LM Studio container. The LM Studio container manages GPU access and model loading, while the application container handles the web UI and OCR processing.");

push @body_parts, heading(2, "6.3 Enterprise Deployment Considerations");
push @body_parts, bold_bullet("Network Isolation: ", "FinVault AI requires no egress rules. The application communicates only over localhost. Firewall rules can block all outbound traffic without affecting functionality.");
push @body_parts, bold_bullet("GPU Allocation: ", "For optimal performance, dedicate GPU resources to the LM Studio process. On shared systems, use GPU isolation features (NVIDIA MPS, CUDA_VISIBLE_DEVICES) to prevent contention.");
push @body_parts, bold_bullet("Multi-User Access: ", "Deploy behind a reverse proxy (Nginx, Caddy) to enable multiple users to access the same instance. Streamlit supports concurrent sessions natively.");
push @body_parts, bold_bullet("Health Checks: ", "The Admin Panel provides real-time system health monitoring. For automated monitoring, implement health check endpoints that verify LM Studio connectivity and model availability.");

push @body_parts, page_break();

# ===== 7. USER DEMO GUIDE =====
push @body_parts, heading(1, "7. User Demo Guide");

push @body_parts, heading(2, "7.1 Report Generation Demo");
push @body_parts, para("Follow these steps to demonstrate the AI-powered report generation workflow:");

push @body_parts, para_bold("Step 1: Load Sample Data");
push @body_parts, para("In the sidebar, check the &#x2018;Use sample data&#x2019; checkbox. The application loads sample_accounts.csv, which contains synthetic Q1 2026 accounting data with revenue, expense, and transfer transactions.");

push @body_parts, para_bold("Step 2: Review Data Preview");
push @body_parts, para("The data table displays all loaded records. Key metrics are computed automatically &#x2014; the sample data includes approximately \$401K in total credits and \$349K in total debits across multiple account categories.");

push @body_parts, para_bold("Step 3: Select Report Type");
push @body_parts, para("Choose &#x2018;Executive Summary&#x2019; from the report type dropdown. This generates a comprehensive overview suitable for management review.");

push @body_parts, para_bold("Step 4: Generate Report");
push @body_parts, para("Click &#x2018;Generate Report&#x2019;. Gemma produces a full Q1 2026 financial report with Executive Summary, Key Metrics, Detailed Analysis, Anomalies &amp; Risks, and Recommendations sections. The report references specific numbers from the dataset.");

push @body_parts, image_para("01_dashboard_report.png", "Figure 4: Report Generator with sample data loaded");

push @body_parts, heading(2, "7.2 Natural Language Query Demo");
push @body_parts, para("Demonstrate conversational data analysis with these steps:");

push @body_parts, para_bold("Step 1: Navigate to Data Query");
push @body_parts, para("Switch to the Data Query tab. Ensure sample data is loaded from the sidebar.");

push @body_parts, para_bold("Step 2: Ask a Question");
push @body_parts, para("Type: &#x201C;What is the total revenue for Q1 2026?&#x201D; The query is sent to Gemma along with the full CSV data and pre-computed statistical summary.");

push @body_parts, para_bold("Step 3: Review the Response");
push @body_parts, para("Gemma returns the answer (\$401,200) with a step-by-step calculation showing how the total was derived from the data. Monetary values are formatted with proper notation.");

push @body_parts, para_bold("Step 4: Follow-Up Questions");
push @body_parts, para("Ask follow-up questions such as &#x201C;Break that down by category&#x201D; or &#x201C;Which account had the highest expenses?&#x201D; Chat history is maintained, allowing the model to reference previous context.");

push @body_parts, image_para("02_data_query.png", "Figure 5: Natural Language Query with AI-powered analysis");

push @body_parts, heading(2, "7.3 OCR Document Processing Demo");
push @body_parts, para("Walk through the complete OCR pipeline:");

push @body_parts, para_bold("Step 1: Navigate to Document OCR");
push @body_parts, para("Switch to the Document OCR tab and select &#x2018;Invoice&#x2019; as the document type.");

push @body_parts, para_bold("Step 2: Load Sample Document");
push @body_parts, para("Check &#x2018;Use sample docs&#x2019; to load sample_invoice.png. Alternatively, upload your own invoice image in PNG, JPG, TIFF, BMP, or WEBP format.");

push @body_parts, para_bold("Step 3: Extract and Parse");
push @body_parts, para("Click &#x2018;Extract &amp; Parse&#x2019;. The pipeline first runs Tesseract OCR to extract raw text (typically achieving 85&#x2013;95% confidence), then sends the extracted text to Gemma for structured parsing.");

push @body_parts, para_bold("Step 4: Review Results");
push @body_parts, para("The results display in two sections: (1) Raw OCR text with confidence score, and (2) Structured parsed data with labeled fields including Invoice Number, Date, Vendor, Line Items, Subtotal, Tax, and Total Amount Due.");

push @body_parts, para_bold("Step 5: Download Results");
push @body_parts, para("Download the raw extracted text or the structured parsed data for further processing. Results can be used for data entry, reconciliation, or audit documentation.");

push @body_parts, image_para("03_ocr_processing.png", "Figure 6: OCR Pipeline &#x2014; Tesseract extraction + AI parsing");

push @body_parts, page_break();

# ===== 8. ROADMAP =====
push @body_parts, heading(1, "8. Roadmap &#x2014; Future Enhancements");

push @body_parts, heading(2, "8.1 Phase 2 &#x2014; Intelligence (Q3 2026)");
push @body_parts, bold_bullet("RAG Pipeline: ", "Integrate a local vector store (ChromaDB or FAISS) for document retrieval-augmented generation, enabling the system to reference a library of historical documents.");
push @body_parts, bold_bullet("Multi-Document Analysis: ", "Cross-reference invoices with ledger entries, matching line items to accounting records for automated reconciliation.");
push @body_parts, bold_bullet("Anomaly Detection: ", "Automated flagging of unusual transactions based on statistical outlier detection combined with LLM-based pattern analysis.");
push @body_parts, bold_bullet("Auto-Categorization: ", "Use embedding similarity to automatically categorize expenses, reducing manual classification work.");

push @body_parts, heading(2, "8.2 Phase 3 &#x2014; Enterprise (Q4 2026)");
push @body_parts, bold_bullet("Role-Based Access Control (RBAC): ", "Define user roles (Admin, Analyst, Viewer) with permission-based access to features and data.");
push @body_parts, bold_bullet("Audit Logging: ", "Comprehensive logging of all user actions, queries, and AI-generated outputs for compliance and audit trail requirements.");
push @body_parts, bold_bullet("Export Formats: ", "Export reports and parsed documents to PDF and XLSX formats for distribution and archival.");
push @body_parts, bold_bullet("Batch Processing: ", "Process multiple documents in a queue, enabling bulk invoice processing and batch report generation.");
push @body_parts, bold_bullet("Custom Prompt Templates: ", "Allow organizations to define their own system prompts and report templates tailored to their specific financial reporting requirements.");

push @body_parts, heading(2, "8.3 Phase 4 &#x2014; Scale (Q1 2027)");
push @body_parts, bold_bullet("Multi-Model Support: ", "Seamlessly swap between Gemma, Llama, Mistral, and other models loaded in LM Studio without code changes.");
push @body_parts, bold_bullet("Observability Dashboard: ", "Real-time monitoring of token usage, inference latency, error rates, and system resource utilization.");
push @body_parts, bold_bullet("Plugin Architecture: ", "Extensible plugin system for custom data sources, report types, and processing pipelines.");
push @body_parts, bold_bullet("CI/CD Pipeline: ", "Automated testing, linting, and deployment pipeline for development teams.");
push @body_parts, bold_bullet("Performance Profiling: ", "Built-in profiling tools to identify bottlenecks in data processing, prompt construction, and inference workflows.");

push @body_parts, heading(2, "8.4 Security Enhancements");
push @body_parts, bold_bullet("End-to-End Encryption: ", "Encrypt file uploads in transit and at rest during session processing, even though all data remains local.");
push @body_parts, bold_bullet("Secure Session Management: ", "Implement token rotation and session expiration policies to prevent unauthorized access to active sessions.");
push @body_parts, bold_bullet("Prompt Injection Defense: ", "Input sanitization layer to detect and prevent prompt injection attacks in user queries and uploaded documents.");
push @body_parts, bold_bullet("Model Output Filtering: ", "Post-processing layer to validate and sanitize model outputs before rendering to the user interface.");

push @body_parts, heading(2, "8.5 Optimization");
push @body_parts, bold_bullet("Prompt Caching: ", "Cache repeated queries and their results to reduce redundant inference calls and improve response times.");
push @body_parts, bold_bullet("Streaming Responses: ", "Implement token-by-token streaming for LLM responses, providing real-time feedback during long report generation.");
push @body_parts, bold_bullet("Lazy Loading: ", "Defer loading of heavy UI components until they are needed, improving initial page load performance.");
push @body_parts, bold_bullet("Quantized Model Support: ", "Native support for GGUF quantized models, enabling deployment on machines with limited GPU memory.");

push @body_parts, image_para("06_roadmap.png", "Figure 7: Product Roadmap &#x2014; Q2 2026 through Q1 2027");

push @body_parts, page_break();

# ===== 9. APPENDIX =====
push @body_parts, heading(1, "9. Appendix");

push @body_parts, heading(2, "9.1 System Prompts Reference");
push @body_parts, para("FinVault AI uses four specialized system prompts, each defined in config/settings.py. These prompts establish the AI&#x2019;s persona, behavioral constraints, and output format requirements for each module.");

push @body_parts, heading(3, "Report Generation Prompt (SYSTEM_PROMPT_REPORT)");
push @body_parts, code_block("You are an expert Certified Public Accountant (CPA) and financial analyst. You generate precise, professional internal financial reports. Use proper accounting terminology (GAAP/IFRS). Structure reports with clear sections: Executive Summary, Key Metrics, Detailed Analysis, Anomalies &amp; Risks, and Recommendations. Always reference specific numbers from the data. Format monetary values with \$ signs, commas, and two decimal places.");

push @body_parts, heading(3, "Data Query Prompt (SYSTEM_PROMPT_QUERY)");
push @body_parts, code_block("You are a financial data analyst AI. You have access to accounting data provided as CSV. Answer the user's question accurately using ONLY the data provided. Show your calculations step-by-step. Format monetary values as \$X,XXX.XX. If the question cannot be answered from the data, say so clearly. If you spot anomalies or risks while answering, mention them briefly.");

push @body_parts, heading(3, "OCR Document Parsing Prompt (SYSTEM_PROMPT_OCR_PARSE)");
push @body_parts, code_block("You are a financial document parser with expertise in invoices, work orders, purchase orders, and receipts. Extract structured data from OCR text accurately. Be precise with numbers, dates, and amounts. Return data in a clean, structured format with clear field labels. If a field is not found in the text, mark it as 'N/A'. Flag any suspicious or inconsistent values.");

push @body_parts, heading(3, "OCR Vision Prompt (SYSTEM_PROMPT_OCR_VISION)");
push @body_parts, code_block("You are an OCR assistant. Extract ALL text visible in this document image exactly as it appears. Preserve the layout, alignment, and structure as much as possible. Include every number, date, and text element.");

push @body_parts, heading(2, "9.2 Supported File Types");

push @body_parts, heading(3, "Data Files (Report Generator &amp; Data Query)");
push @body_parts, table_xml(
    ["Format", "Extension", "Library"],
    [
        ["Comma-Separated Values", ".csv", "pandas (built-in)"],
        ["Excel Workbook", ".xlsx", "pandas + openpyxl"],
        ["Legacy Excel", ".xls", "pandas + openpyxl"],
    ],
    [3600, 2200, 3560]
);

push @body_parts, heading(3, "Image Files (Document OCR)");
push @body_parts, table_xml(
    ["Format", "Extension", "Notes"],
    [
        ["PNG", ".png", "Recommended for document scans"],
        ["JPEG", ".jpg, .jpeg", "Good for photographs of documents"],
        ["TIFF", ".tiff", "Common in enterprise scanning workflows"],
        ["BMP", ".bmp", "Legacy format, full support"],
        ["WebP", ".webp", "Modern format, good compression"],
    ],
    [2200, 2200, 4960]
);

push @body_parts, heading(2, "9.3 Sample Data Files");
push @body_parts, para("The sample_data/ directory contains seven synthetic test files for demonstrating all application features without requiring real financial data:");

push @body_parts, table_xml(
    ["File", "Type", "Description"],
    [
        ["sample_accounts.csv", "CSV", "Q1 2026 general ledger with revenue, expense, and transfer entries"],
        ["sample_accounts_payable.csv", "CSV", "Accounts payable aging report with vendor balances"],
        ["sample_invoice.png", "Image", "Synthetic invoice image for OCR demonstration"],
        ["sample_invoice.pdf", "PDF", "Synthetic invoice document (PDF version)"],
        ["sample_purchase_order.pdf", "PDF", "Synthetic purchase order for OCR testing"],
        ["sample_receipt.png", "Image", "Synthetic receipt image for OCR demonstration"],
        ["sample_workorder.png", "Image", "Synthetic work order image for OCR testing"],
    ],
    [3400, 1200, 4760]
);

# End of document
push @body_parts, accent_line();
push @body_parts, para_centered("End of Document", {size => 20, color => "6B7280", italic => 1, before => 240});
push @body_parts, para_centered("FinVault AI v3.0  |  April 2026  |  Confidential", {size => 18, color => "A5B4FC"});


# =========================================================================
# ASSEMBLE DOCUMENT XML
# =========================================================================
my $body_content = join("\n", @body_parts);

my $document_xml = <<XML;
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
  xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
  xmlns:o="urn:schemas-microsoft-com:office:office"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
  xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
  xmlns:v="urn:schemas-microsoft-com:vml"
  xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
  xmlns:w10="urn:schemas-microsoft-com:office:word"
  xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
  xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
  xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
  xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"
  xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing">
  <w:body>
$body_content
$sect_props
  </w:body>
</w:document>
XML

write_file("$tmp_dir/word/document.xml", $document_xml);

# =========================================================================
# ZIP INTO .docx
# =========================================================================
# Use system zip command
unlink $output_file if -f $output_file;
my $prev_dir = `pwd`;
chomp $prev_dir;
chdir $tmp_dir;
system("zip -r -q '$output_file' . -x '.*'") == 0
    or die "Failed to create zip: $!";
chdir $prev_dir;

# Cleanup
remove_tree($tmp_dir);

print "Document saved to: $output_file\n";

# =========================================================================
# HELPER SUBROUTINES
# =========================================================================

sub write_file {
    my ($path, $content) = @_;
    open my $fh, '>:utf8', $path or die "Cannot write $path: $!";
    print $fh $content;
    close $fh;
}

sub esc {
    my $t = shift;
    # Already XML-escaped content should not be double-escaped
    return $t;
}

sub run {
    my ($text, $opts) = @_;
    $opts //= {};
    my $rpr = "";
    my @rpr_parts;
    push @rpr_parts, "<w:b/>" if $opts->{bold};
    push @rpr_parts, "<w:i/>" if $opts->{italic};
    push @rpr_parts, "<w:caps/>" if $opts->{caps};
    push @rpr_parts, qq{<w:sz w:val="$opts->{size}"/>} if $opts->{size};
    push @rpr_parts, qq{<w:szCs w:val="$opts->{size}"/>} if $opts->{size};
    push @rpr_parts, qq{<w:color w:val="$opts->{color}"/>} if $opts->{color};
    push @rpr_parts, qq{<w:rFonts w:ascii="$opts->{font}" w:hAnsi="$opts->{font}" w:cs="$opts->{font}"/>} if $opts->{font};
    $rpr = "<w:rPr>" . join("", @rpr_parts) . "</w:rPr>" if @rpr_parts;

    my $preserve = ($text =~ /^\s|\s$/) ? ' xml:space="preserve"' : '';
    return qq{<w:r>$rpr<w:t$preserve>$text</w:t></w:r>};
}

sub para {
    my ($text, $opts) = @_;
    $opts //= {};
    my @ppr;
    push @ppr, qq{<w:spacing w:after="$opts->{after}"/>} if defined $opts->{after};
    push @ppr, qq{<w:spacing w:before="$opts->{before}"/>} if defined $opts->{before};
    push @ppr, qq{<w:jc w:val="center"/>} if $opts->{center};
    my $ppr_str = @ppr ? "<w:pPr>" . join("", @ppr) . "</w:pPr>" : "";

    return qq{<w:p>$ppr_str} . run($text) . "</w:p>";
}

sub para_centered {
    my ($text, $opts) = @_;
    $opts //= {};
    my @ppr;
    push @ppr, "<w:jc w:val=\"center\"/>";
    push @ppr, qq{<w:spacing w:before="$opts->{before}"/>} if $opts->{before};
    push @ppr, qq{<w:spacing w:after="$opts->{after}"/>} if $opts->{after};
    my $ppr_str = "<w:pPr>" . join("", @ppr) . "</w:pPr>";
    return qq{<w:p>$ppr_str} . run($text, $opts) . "</w:p>";
}

sub para_bold {
    my ($text) = @_;
    return qq{<w:p><w:pPr><w:spacing w:before="120" w:after="60"/></w:pPr>} . run($text, {bold => 1}) . "</w:p>";
}

sub heading {
    my ($level, $text) = @_;
    return qq{<w:p><w:pPr><w:pStyle w:val="Heading${level}"/></w:pPr>} . run($text) . "</w:p>";
}

sub styled_para {
    my ($text, $style) = @_;
    return qq{<w:p><w:pPr><w:pStyle w:val="$style"/></w:pPr>} . run($text) . "</w:p>";
}

sub bullet {
    my ($text) = @_;
    return <<XML;
<w:p>
  <w:pPr>
    <w:pStyle w:val="ListBullet"/>
    <w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>
    <w:spacing w:after="60"/>
  </w:pPr>
  @{[ run($text) ]}
</w:p>
XML
}

sub bold_bullet {
    my ($bold_text, $normal_text) = @_;
    return <<XML;
<w:p>
  <w:pPr>
    <w:pStyle w:val="ListBullet"/>
    <w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>
    <w:spacing w:after="80"/>
  </w:pPr>
  @{[ run($bold_text, {bold => 1}) ]}@{[ run($normal_text) ]}
</w:p>
XML
}

sub code_block {
    my ($text) = @_;
    # Split text into lines and create separate paragraphs for each line
    my @lines = split /\n/, $text;
    my $result = "";
    for my $line (@lines) {
        $result .= <<XML;
<w:p>
  <w:pPr>
    <w:pStyle w:val="CodeBlock"/>
    <w:spacing w:after="0" w:line="240" w:lineRule="auto"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>
      <w:sz w:val="18"/>
      <w:szCs w:val="18"/>
      <w:color w:val="374151"/>
    </w:rPr>
    <w:t xml:space="preserve">$line</w:t>
  </w:r>
</w:p>
XML
    }
    return $result;
}

sub accent_line {
    return <<'XML';
<w:p>
  <w:pPr>
    <w:spacing w:before="40" w:after="40"/>
    <w:pBdr><w:bottom w:val="single" w:sz="8" w:space="1" w:color="6366F1"/></w:pBdr>
  </w:pPr>
</w:p>
XML
}

sub page_break {
    return <<'XML';
<w:p>
  <w:r><w:br w:type="page"/></w:r>
</w:p>
XML
}

sub image_para {
    my ($filename, $caption) = @_;
    my $rid = $img_rels{$filename};
    return para("[$caption]", {center => 1}) unless $rid; # fallback if image missing

    # Image dimensions: ~5.5 inches wide, proportional height
    # EMUs: 1 inch = 914400 EMU
    my $width_emu = 5040000;  # ~5.5 inches
    my $height_emu = 3200000; # ~3.5 inches (will be constrained by aspect ratio in Word)

    my $img_xml = <<XML;
<w:p>
  <w:pPr><w:jc w:val="center"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="$width_emu" cy="$height_emu"/>
        <wp:docPr id="@{[int(rand(99999))+1]}" name="$filename"/>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="$filename"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="$rid"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm>
                  <a:off x="0" y="0"/>
                  <a:ext cx="$width_emu" cy="$height_emu"/>
                </a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>
<w:p>
  <w:pPr><w:pStyle w:val="Caption"/></w:pPr>
  @{[ run($caption, {italic => 1, size => 18, color => "6B7280"}) ]}
</w:p>
XML
    return $img_xml;
}

sub table_xml {
    my ($headers, $rows, $col_widths) = @_;
    my $num_cols = scalar @$headers;
    my $total_width = 9360; # page width minus margins in DXA

    # Default equal widths if not specified
    if (!$col_widths) {
        my $w = int($total_width / $num_cols);
        $col_widths = [($w) x $num_cols];
    }

    my $grid = "";
    for my $w (@$col_widths) {
        $grid .= qq{<w:gridCol w:w="$w"/>};
    }

    # Header row
    my $hdr_cells = "";
    for my $i (0..$#$headers) {
        my $w = $col_widths->[$i];
        $hdr_cells .= <<XML;
<w:tc>
  <w:tcPr>
    <w:tcW w:w="$w" w:type="dxa"/>
    <w:shd w:val="clear" w:color="auto" w:fill="4F46E5"/>
    <w:tcMar><w:top w:w="60" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/><w:left w:w="120" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tcMar>
  </w:tcPr>
  <w:p>
    <w:pPr><w:spacing w:after="0"/></w:pPr>
    @{[ run($headers->[$i], {bold => 1, size => 19, color => "FFFFFF"}) ]}
  </w:p>
</w:tc>
XML
    }

    # Data rows
    my $data_rows = "";
    for my $r_idx (0..$#$rows) {
        my $bg = ($r_idx % 2 == 0) ? "F5F3FF" : "FFFFFF";
        my $cells = "";
        for my $c_idx (0..$#{$rows->[$r_idx]}) {
            my $w = $col_widths->[$c_idx];
            $cells .= <<XML;
<w:tc>
  <w:tcPr>
    <w:tcW w:w="$w" w:type="dxa"/>
    <w:shd w:val="clear" w:color="auto" w:fill="$bg"/>
    <w:tcMar><w:top w:w="50" w:type="dxa"/><w:bottom w:w="50" w:type="dxa"/><w:left w:w="120" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tcMar>
  </w:tcPr>
  <w:p>
    <w:pPr><w:spacing w:after="0"/></w:pPr>
    @{[ run($rows->[$r_idx][$c_idx], {size => 19}) ]}
  </w:p>
</w:tc>
XML
        }
        $data_rows .= "<w:tr>$cells</w:tr>\n";
    }

    return <<XML;
<w:tbl>
  <w:tblPr>
    <w:tblStyle w:val="TableGrid"/>
    <w:tblW w:w="$total_width" w:type="dxa"/>
    <w:tblBorders>
      <w:top w:val="single" w:sz="4" w:space="0" w:color="C7D2FE"/>
      <w:left w:val="single" w:sz="4" w:space="0" w:color="C7D2FE"/>
      <w:bottom w:val="single" w:sz="4" w:space="0" w:color="C7D2FE"/>
      <w:right w:val="single" w:sz="4" w:space="0" w:color="C7D2FE"/>
      <w:insideH w:val="single" w:sz="4" w:space="0" w:color="C7D2FE"/>
      <w:insideV w:val="single" w:sz="4" w:space="0" w:color="C7D2FE"/>
    </w:tblBorders>
  </w:tblPr>
  <w:tblGrid>$grid</w:tblGrid>
  <w:tr>$hdr_cells</w:tr>
  $data_rows
</w:tbl>
<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>
XML
}
