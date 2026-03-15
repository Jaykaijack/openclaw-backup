#!/usr/bin/env node
// Industry Report DOCX Generator
// Usage: NODE_PATH=$(npm root -g) node gen_report.js
// Reads DATA object below (or require as module and call generate(DATA))

const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, PageBreak, LevelFormat, TableOfContents
} = require("docx");

// ============================================================
// DEFAULT DATA — Replace this with your industry-specific data
// ============================================================
const DATA = {
  title: "示例行业",
  subtitle: "行业研究报告",
  date: new Date().toLocaleDateString("zh-CN", { year: "numeric", month: "long", day: "numeric" }),
  keywords: "关键词1 · 关键词2 · 关键词3",
  disclaimer: "本报告基于公开信息整理，仅供研究参考，不构成投资建议。",
  sources: "数据来源：Gartner、IDC、财联社",
  color: "2563EB", // blue
  sections: [
    { type: "summary", title: "执行摘要", points: [
      { label: "要点一：示例要点", text: "请替换为实际内容。" }
    ]},
  ]
};

// ============================================================
// GENERATOR ENGINE
// ============================================================
const PW = 9026; // A4 content width in DXA
const bdr = (c = "D1D5DB") => ({ style: BorderStyle.SINGLE, size: 1, color: c });
const borders = { top: bdr(), bottom: bdr(), left: bdr(), right: bdr() };
const cellMar = { top: 60, bottom: 60, left: 100, right: 100 };

function txt(text, o = {}) {
  return new TextRun({ text, font: o.font || "Microsoft YaHei", size: o.size || 22,
    bold: o.bold, color: o.color, italics: o.italics });
}
function mono(text, o = {}) {
  return new TextRun({ text, font: "Menlo", size: o.size || 20, color: o.color || "1F2937", bold: o.bold });
}
function para(children, o = {}) {
  return new Paragraph({ children: Array.isArray(children) ? children : [children],
    spacing: { before: o.before || 0, after: o.after || 100 }, alignment: o.align, ...o });
}
function hCell(text, w, bg = "1E3A5F") {
  return new TableCell({ borders, width: { size: w, type: WidthType.DXA },
    shading: { fill: bg, type: ShadingType.CLEAR }, margins: cellMar, verticalAlign: "center",
    children: [para([txt(text, { bold: true, color: "FFFFFF", size: 20 })], { align: AlignmentType.CENTER })] });
}
function dCell(text, w, o = {}) {
  const run = o.mono ? mono(text, { color: o.color, bold: o.bold }) : txt(text, { color: o.color || "1F2937", size: 20, bold: o.bold });
  return new TableCell({ borders, width: { size: w, type: WidthType.DXA },
    shading: o.bg ? { fill: o.bg, type: ShadingType.CLEAR } : undefined, margins: cellMar,
    children: [para([run], { align: o.mono ? AlignmentType.CENTER : AlignmentType.LEFT })] });
}

function generate(data) {
  const C = data.color || "2563EB";
  const children = [];

  // === COVER ===
  children.push(para([txt("")], { before: 2000 }));
  children.push(para([txt(data.title, { size: 56, bold: true, color: C })], { align: AlignmentType.CENTER }));
  children.push(para([txt(data.subtitle || "行业研究报告", { size: 56, bold: true, color: "1F2937" })], { align: AlignmentType.CENTER }));
  children.push(new Paragraph({ children: [], border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: C, space: 1 } }, spacing: { before: 200, after: 200 } }));
  for (const line of [
    `报告类型：行业深度研究报告`, `发布日期：${data.date}`,
    `数据截止日期：${data.date.replace(/日$/, '')}`, `关键词：${data.keywords}`
  ]) children.push(para([txt(line, { size: 22, color: "6B7280" })], { align: AlignmentType.CENTER }));
  children.push(para([txt("")], { before: 600 }));
  children.push(para([txt(data.disclaimer || "", { size: 18, color: "6B7280" })], { align: AlignmentType.CENTER }));
  children.push(new Paragraph({ children: [new PageBreak()] }));

  // === TOC ===
  children.push(para([txt("目录", { size: 32, bold: true, color: C })], { heading: HeadingLevel.HEADING_1 }));
  children.push(new TableOfContents("目录", { hyperlink: true, headingStyleRange: "1-3" }));
  children.push(new Paragraph({ children: [new PageBreak()] }));

  // === SECTIONS ===
  let sectionNum = 1;
  for (const sec of data.sections) {
    const sTitle = sec.numbering !== false ? `${numCN(sectionNum)}、${sec.title}` : sec.title;

    switch (sec.type) {
      case "summary":
        children.push(para([txt(sTitle, { size: 32, bold: true, color: C })], { heading: HeadingLevel.HEADING_1, before: 360, after: 240 }));
        for (const p of sec.points) {
          children.push(para([txt(p.label, { bold: true, color: C, size: 22 }), txt(" " + p.text, { size: 21, color: "1F2937" })], { before: 120, after: 80 }));
        }
        break;

      case "kpi":
        children.push(para([txt(sTitle, { size: 32, bold: true, color: C })], { heading: HeadingLevel.HEADING_1, before: 360, after: 240 }));
        for (const row of (sec.rows || [])) {
          const colW = Math.floor(PW / row.length);
          children.push(new Table({
            width: { size: PW, type: WidthType.DXA },
            columnWidths: row.map((_, i) => i < row.length - 1 ? colW : PW - colW * (row.length - 1)),
            rows: [new TableRow({ children: row.map(k => {
              const w = colW;
              return new TableCell({
                borders: { top: { style: BorderStyle.SINGLE, size: 3, color: k.color || C }, bottom: bdr(), left: bdr(), right: bdr() },
                width: { size: w, type: WidthType.DXA },
                shading: { fill: k.bg || "DBEAFE", type: ShadingType.CLEAR },
                margins: { top: 100, bottom: 100, left: 120, right: 120 },
                children: [
                  para([txt(k.label, { size: 16, color: "6B7280" })], { align: AlignmentType.CENTER }),
                  para([txt(k.value, { size: 28, bold: true, color: k.color || C, font: "Menlo" })], { align: AlignmentType.CENTER }),
                  para([txt(k.sub || "", { size: 16, color: "6B7280" })], { align: AlignmentType.CENTER }),
                ]
              });
            })})]
          }));
          children.push(para([txt("")], { before: 60 }));
        }
        break;

      case "table":
      case "risk":
        children.push(para([txt(sTitle, { size: 32, bold: true, color: C })], { heading: HeadingLevel.HEADING_1, before: 360, after: 240 }));
        if (sec.description) children.push(para([txt(sec.description, { size: 21, color: "1F2937" })], { before: 80 }));
        const cols = sec.columns;
        const ws = cols.map(c => c.width);
        children.push(new Table({
          width: { size: PW, type: WidthType.DXA }, columnWidths: ws,
          rows: [
            new TableRow({ children: cols.map((c, i) => hCell(c.header, ws[i])) }),
            ...sec.rows.map(r => new TableRow({ children: r.map((cell, i) => {
              const col = cols[i];
              let color = undefined;
              if (col.colorMap && col.colorMap[cell]) color = col.colorMap[cell];
              return dCell(cell, ws[i], { mono: col.mono, color, bold: i === 0 });
            })}))
          ]
        }));
        if (sec.note) children.push(para([txt(sec.note, { size: 18, color: "6B7280" })], { before: 60 }));
        break;

      case "chain":
        children.push(para([txt(sTitle, { size: 32, bold: true, color: C })], { heading: HeadingLevel.HEADING_1, before: 360, after: 240 }));
        if (sec.description) children.push(para([txt(sec.description, { size: 21, color: "1F2937" })], { before: 80 }));
        const chainCols = [1600, 3200, PW - 4800];
        children.push(new Table({
          width: { size: PW, type: WidthType.DXA }, columnWidths: chainCols,
          rows: [
            new TableRow({ children: [hCell("产业环节", 1600), hCell("主要厂商", 3200), hCell("备注", PW - 4800)] }),
            ...sec.layers.flatMap(layer => layer.items.map((item, idx) => new TableRow({ children: [
              idx === 0
                ? new TableCell({ borders, width: { size: 1600, type: WidthType.DXA },
                    shading: { fill: layer.color, type: ShadingType.CLEAR }, margins: cellMar,
                    rowSpan: layer.items.length,
                    children: [para([txt(layer.name, { bold: true, color: "FFFFFF", size: 20 })])] })
                : undefined,
              dCell(item.label, 3200, { bold: true }),
              dCell(item.detail, PW - 4800),
            ].filter(Boolean) })))
          ]
        }));
        break;

      case "news":
        children.push(para([txt(sTitle, { size: 32, bold: true, color: C })], { heading: HeadingLevel.HEADING_1, before: 360, after: 240 }));
        for (const n of sec.items) {
          children.push(para([
            txt(`【${n.tag}】`, { bold: true, color: n.tagColor || C, size: 21 }),
            txt(n.headline, { bold: true, color: "1F2937", size: 21 }),
            txt(" " + (n.detail || ""), { size: 20, color: "6B7280" })
          ], { before: 80, after: 60 }));
        }
        break;

      case "strategy":
        children.push(para([txt(sTitle, { size: 32, bold: true, color: C })], { heading: HeadingLevel.HEADING_1, before: 360, after: 240 }));
        for (const s of sec.items) {
          children.push(para([txt(s.label, { bold: true, color: C, size: 22 }), txt(" " + s.text, { size: 21, color: "1F2937" })], { before: 120, after: 80 }));
        }
        break;

      case "text":
        children.push(para([txt(sTitle, { size: 32, bold: true, color: C })], { heading: HeadingLevel.HEADING_1, before: 360, after: 240 }));
        children.push(para([txt(sec.content, { size: 21, color: "1F2937" })], { before: 80 }));
        break;

      case "bullets":
        children.push(para([txt(sTitle, { size: 32, bold: true, color: C })], { heading: HeadingLevel.HEADING_1, before: 360, after: 240 }));
        for (const item of sec.items) {
          children.push(new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [txt(item, { size: 21, color: "1F2937" })],
            spacing: { before: 60, after: 60 }
          }));
        }
        break;

      default:
        children.push(para([txt(`[Unknown section type: ${sec.type}]`, { color: "DC2626" })]));
    }

    if (sec.pageBreak !== false && sec.type !== "text" && sec.type !== "bullets") {
      children.push(new Paragraph({ children: [new PageBreak()] }));
    }
    if (sec.numbering !== false) sectionNum++;
  }

  // === FOOTER ===
  children.push(new Paragraph({ children: [], border: { bottom: { style: BorderStyle.SINGLE, size: 3, color: C, space: 1 } }, spacing: { before: 200, after: 100 } }));
  children.push(para([txt(data.disclaimer || "", { size: 18, color: "6B7280" })], { align: AlignmentType.CENTER }));
  children.push(para([txt(data.sources || "", { size: 18, color: "6B7280" })], { align: AlignmentType.CENTER }));
  children.push(para([txt(`报告生成时间：${data.date}`, { size: 18, color: "6B7280" })], { align: AlignmentType.CENTER }));

  // === BUILD DOC ===
  const doc = new Document({
    styles: {
      default: { document: { run: { font: "Microsoft YaHei", size: 22 } } },
      paragraphStyles: [
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 32, bold: true, font: "Microsoft YaHei", color: C },
          paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 0 } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 28, bold: true, font: "Microsoft YaHei", color: "1F2937" },
          paragraph: { spacing: { before: 240, after: 180 }, outlineLevel: 1 } },
        { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 24, bold: true, font: "Microsoft YaHei", color: "1F2937" },
          paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
      ]
    },
    numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }] },
    sections: [{
      properties: {
        page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
      },
      headers: { default: new Header({ children: [new Paragraph({ children: [txt(`${data.title}${data.subtitle}`, { size: 18, color: "6B7280" })], alignment: AlignmentType.RIGHT, border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: C, space: 1 } } })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ children: [txt(`${data.date} · 行业深度研究`, { size: 16, color: "6B7280" }), new TextRun({ children: ["\t\t第 ", PageNumber.CURRENT, " 页"], font: "Microsoft YaHei", size: 16, color: "6B7280" })], tabStops: [{ type: "right", position: PW }] })] }) },
      children
    }]
  });

  return doc;
}

function numCN(n) {
  const map = ["","一","二","三","四","五","六","七","八","九","十","十一","十二","十三","十四","十五"];
  return map[n] || String(n);
}

// ============================================================
// CLI: generate with default DATA
// ============================================================
if (require.main === module) {
  const doc = generate(DATA);
  const outName = `${DATA.title}_report_${new Date().toISOString().slice(0,10).replace(/-/g,"")}.docx`;
  Packer.toBuffer(doc).then(buf => {
    fs.writeFileSync(outName, buf);
    console.log(`OK: ${outName} (${buf.length} bytes)`);
  }).catch(e => { console.error("ERR:", e.message || e); process.exit(1); });
}

module.exports = { generate, DATA };
