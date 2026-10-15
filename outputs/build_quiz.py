#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""读取题库 JSON，生成自包含、低认知负荷、支持极速/深度双模式的现代决策学前置自测 HTML。"""
import json, pathlib

BASE = pathlib.Path(__file__).resolve().parent
data = json.loads((BASE / "decision_science_prequiz.json").read_text(encoding="utf-8"))
payload = json.dumps(data, ensure_ascii=False)

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>现代决策学 · 前置自测系统</title>
<style>
  :root {
    --bg: #f8fafc;
    --panel: #ffffff;
    --panel-sub: #f1f5f9;
    --ink: #0f172a;
    --sub: #475569;
    --muted: #94a3b8;
    --line: #e2e8f0;
    --brand: #2563eb;
    --brand-hover: #1d4ed8;
    --brand-soft: #eff6ff;
    --brand-border: #bfdbfe;
    --ok: #059669;
    --ok-soft: #ecfdf5;
    --ok-border: #a7f3d0;
    --warn: #d97706;
    --warn-soft: #fffbeb;
    --warn-border: #fde68a;
    --err: #dc2626;
    --err-soft: #fef2f2;
    --skip: #64748b;
    --skip-soft: #f8fafc;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }
  .wrap {
    max-width: 920px;
    margin: 0 auto;
    padding: 24px 18px 120px;
  }

  /* 顶部横幅 */
  header.hero {
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 60%, #3b82f6 100%);
    color: #fff;
    border-radius: 20px;
    padding: 30px 28px;
    box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.25);
    margin-bottom: 20px;
  }
  .hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    background: rgba(255, 255, 255, 0.18);
    backdrop-filter: blur(8px);
    padding: 4px 12px;
    border-radius: 100px;
    margin-bottom: 12px;
  }
  header.hero h1 {
    margin: 0 0 8px;
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.3px;
  }
  header.hero p {
    margin: 0 0 16px;
    font-size: 14.5px;
    opacity: 0.92;
    max-width: 680px;
    line-height: 1.55;
  }
  .hero-stats {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    font-size: 12.5px;
  }
  .hero-pill {
    background: rgba(255, 255, 255, 0.16);
    padding: 4px 12px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  /* 模式选择器卡片 */
  .mode-card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 18px 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
  }
  .mode-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    flex-wrap: wrap;
    gap: 10px;
  }
  .mode-title {
    font-size: 14.5px;
    font-weight: 700;
    color: var(--ink);
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .mode-switch-group {
    display: flex;
    background: var(--panel-sub);
    padding: 4px;
    border-radius: 12px;
    gap: 4px;
  }
  .mode-btn {
    border: none;
    background: transparent;
    padding: 8px 16px;
    border-radius: 9px;
    font-size: 13px;
    font-weight: 600;
    color: var(--sub);
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .mode-btn.active {
    background: var(--panel);
    color: var(--brand);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
  }
  .mode-desc {
    font-size: 13px;
    color: var(--sub);
    background: var(--brand-soft);
    border: 1px solid var(--brand-border);
    border-radius: 10px;
    padding: 10px 14px;
    line-height: 1.5;
  }

  /* 顶部吸顶进度条 */
  .sticky-progress {
    position: sticky;
    top: 10px;
    z-index: 100;
    background: rgba(255, 255, 255, 0.94);
    backdrop-filter: blur(12px);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 10px 16px;
    margin-bottom: 20px;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .prog-label {
    font-size: 13px;
    font-weight: 600;
    color: var(--ink);
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .prog-track {
    flex: 1;
    height: 8px;
    background: #e2e8f0;
    border-radius: 99px;
    overflow: hidden;
    position: relative;
  }
  .prog-bar {
    height: 100%;
    background: linear-gradient(90deg, #3b82f6, #10b981);
    width: 0%;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 99px;
  }
  .prog-num {
    font-size: 12.5px;
    font-weight: 700;
    color: var(--brand);
    white-space: nowrap;
  }

  /* 模块分步标签 (Module Step Tabs) */
  .mod-tabs {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding-bottom: 6px;
    margin-bottom: 18px;
    scrollbar-width: none;
  }
  .mod-tabs::-webkit-scrollbar { display: none; }
  .mod-tab {
    flex-shrink: 0;
    background: var(--panel);
    border: 1px solid var(--line);
    padding: 8px 14px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 600;
    color: var(--sub);
    cursor: pointer;
    transition: all 0.15s ease;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .mod-tab:hover {
    border-color: var(--brand-border);
    color: var(--brand);
  }
  .mod-tab.active {
    background: var(--brand);
    border-color: var(--brand);
    color: #fff;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.22);
  }
  .mod-tab-badge {
    background: rgba(0, 0, 0, 0.08);
    font-size: 11px;
    padding: 1px 6px;
    border-radius: 20px;
  }
  .mod-tab.active .mod-tab-badge {
    background: rgba(255, 255, 255, 0.25);
  }

  /* 模块容器与单元卡片 */
  .mod-section {
    display: none;
  }
  .mod-section.active {
    display: block;
  }
  .mod-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 24px 0 12px;
    padding-left: 4px;
  }
  .mod-heading-text {
    font-size: 16px;
    font-weight: 700;
    color: var(--ink);
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .mod-heading-text::before {
    content: "";
    width: 4px;
    height: 18px;
    border-radius: 2px;
    background: var(--brand);
  }

  .unit-card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03);
    transition: all 0.2s ease;
  }
  .unit-card:hover {
    border-color: #cbd5e1;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
  }
  .unit-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 6px;
  }
  .unit-name {
    font-size: 15.5px;
    font-weight: 700;
    color: var(--ink);
  }
  .unit-tag {
    font-size: 11.5px;
    font-weight: 700;
    color: var(--brand);
    background: var(--brand-soft);
    padding: 3px 8px;
    border-radius: 6px;
    margin-right: 8px;
  }
  .unit-status-badge {
    font-size: 12px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 99px;
    background: var(--panel-sub);
    color: var(--sub);
  }
  .unit-status-badge.ok {
    background: var(--ok-soft);
    color: var(--ok);
  }
  .unit-status-badge.warn {
    background: var(--warn-soft);
    color: var(--warn);
  }

  .unit-meta {
    font-size: 12.5px;
    color: var(--muted);
    margin-bottom: 14px;
    display: flex;
    gap: 8px;
    align-items: center;
    flex-wrap: wrap;
  }

  /* 题目项 */
  .question-item {
    padding: 16px 0 12px;
    border-top: 1px dashed var(--line);
  }
  .question-item:first-of-type {
    border-top: none;
    padding-top: 4px;
  }
  .question-item.hidden-question {
    display: none;
  }

  .q-top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
    gap: 10px;
  }
  .q-sentinel-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: #fef3c7;
    color: #92400e;
    font-size: 11.5px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 6px;
  }
  .q-concept-tag {
    font-size: 12px;
    color: var(--sub);
  }

  .q-title {
    font-size: 14.5px;
    font-weight: 600;
    line-height: 1.55;
    margin-bottom: 12px;
    color: var(--ink);
  }
  .q-title i {
    font-style: normal;
    color: var(--brand);
    font-weight: 700;
    margin-right: 6px;
  }

  /* 选项列表 */
  .opt-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 10px;
  }
  .opt-row {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 10px 14px;
    cursor: pointer;
    font-size: 13.8px;
    line-height: 1.45;
    color: var(--ink);
    transition: all 0.15s ease;
  }
  .opt-row:hover {
    border-color: #93c5fd;
    background: #f8fafc;
  }
  .opt-row input[type="radio"] {
    margin-top: 3px;
    accent-color: var(--brand);
  }
  .opt-row.selected {
    border-color: var(--brand);
    background: var(--brand-soft);
    color: #1e3a8a;
    font-weight: 500;
  }
  .opt-row.is-correct {
    border-color: var(--ok);
    background: var(--ok-soft);
    color: #065f46;
  }
  .opt-row.is-wrong {
    border-color: var(--err);
    background: var(--err-soft);
    color: #991b1b;
  }
  .opt-letter {
    font-weight: 700;
    color: var(--sub);
    min-width: 18px;
  }
  .opt-row.selected .opt-letter {
    color: var(--brand);
  }

  /* 跳过按钮与反馈区域 */
  .q-actions {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 4px;
  }
  .btn-skip {
    background: transparent;
    border: 1px dashed #cbd5e1;
    color: var(--sub);
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s ease;
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }
  .btn-skip:hover {
    border-color: var(--skip);
    background: var(--panel-sub);
    color: var(--ink);
  }
  .btn-skip.skipped {
    background: #f1f5f9;
    border-color: #94a3b8;
    color: #334155;
    font-weight: 600;
  }

  .q-feedback {
    display: none;
    margin-top: 10px;
    font-size: 13px;
    border-radius: 10px;
    padding: 10px 14px;
    line-height: 1.5;
  }
  .q-feedback.show { display: block; }
  .q-feedback.ok {
    background: var(--ok-soft);
    border: 1px solid var(--ok-border);
    color: #065f46;
  }
  .q-feedback.err {
    background: var(--err-soft);
    border: 1px solid #fecaca;
    color: #991b1b;
  }

  /* 单元扩展加测展开按钮 */
  .unit-expand-trigger {
    margin-top: 12px;
    padding-top: 10px;
    border-top: 1px solid var(--line);
    display: flex;
    justify-content: center;
  }
  .btn-expand-unit {
    background: transparent;
    border: 1px solid var(--line);
    color: var(--brand);
    font-size: 12.5px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.15s;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .btn-expand-unit:hover {
    background: var(--brand-soft);
    border-color: var(--brand-border);
  }

  /* 底部固定操作栏 */
  .bottom-bar {
    position: sticky;
    bottom: 0;
    margin-top: 30px;
    background: linear-gradient(180deg, rgba(248, 250, 252, 0) 0%, rgba(248, 250, 252, 0.98) 30%);
    padding: 18px 0 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    z-index: 90;
  }
  .bottom-left, .bottom-right {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .btn-action {
    border: none;
    border-radius: 12px;
    padding: 12px 22px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .btn-primary {
    background: var(--brand);
    color: #fff;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
  }
  .btn-primary:hover {
    background: var(--brand-hover);
    transform: translateY(-1px);
  }
  .btn-secondary {
    background: #fff;
    color: var(--sub);
    border: 1px solid var(--line);
  }
  .btn-secondary:hover {
    border-color: #cbd5e1;
    color: var(--ink);
  }

  /* 诊断结果报告面板 */
  .result-panel {
    display: none;
    margin-top: 30px;
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 28px;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  }
  .result-panel.show { display: block; }
  .res-header {
    border-bottom: 1px solid var(--line);
    padding-bottom: 18px;
    margin-bottom: 20px;
  }
  .res-title {
    font-size: 20px;
    font-weight: 800;
    color: var(--ink);
    margin: 0 0 6px;
  }
  .res-stat {
    font-size: 14px;
    color: var(--sub);
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
  }
  .res-banner {
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 24px;
    font-size: 14.5px;
    line-height: 1.6;
    display: flex;
    gap: 12px;
    align-items: flex-start;
  }
  .res-banner.full { background: #fee2e2; color: #991b1b; }
  .res-banner.some { background: #fef3c7; color: #92400e; }
  .res-banner.few { background: #dbeafe; color: #1e40af; }
  .res-banner.pass { background: #d1fae5; color: #065f46; }
  .res-banner-icon { font-size: 22px; flex-shrink: 0; }

  .res-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 24px;
  }
  @media (max-width: 640px) {
    .res-grid { grid-template-columns: 1fr; }
  }
  .res-card {
    border-radius: 12px;
    padding: 14px;
    border: 1px solid var(--line);
    background: #f8fafc;
  }
  .res-card.pass {
    border-color: var(--ok-border);
    background: var(--ok-soft);
  }
  .res-card.need {
    border-color: var(--warn-border);
    background: var(--warn-soft);
  }
  .res-card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
  }
  .res-card-title {
    font-size: 13.5px;
    font-weight: 700;
    color: var(--ink);
  }
  .res-card-badge {
    font-size: 11.5px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 6px;
  }
  .res-card.pass .res-card-badge { background: #a7f3d0; color: #065f46; }
  .res-card.need .res-card-badge { background: #fde68a; color: #92400e; }
  .res-card-concepts {
    font-size: 12px;
    color: var(--sub);
    line-height: 1.4;
  }

  .res-actions {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: flex-end;
    border-top: 1px solid var(--line);
    padding-top: 18px;
  }

  .toast {
    position: fixed;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%) translateY(100px);
    background: #0f172a;
    color: #fff;
    padding: 10px 20px;
    border-radius: 100px;
    font-size: 13px;
    font-weight: 500;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    opacity: 0;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    z-index: 999;
  }
  .toast.show {
    transform: translateX(-50%) translateY(0);
    opacity: 1;
  }
</style>
</head>
<body>
<div class="wrap">
  <!-- 头部介绍 -->
  <header class="hero">
    <div class="hero-tag">⚡ 智能分流与免修评估</div>
    <h1>现代决策学 · 前置自测</h1>
    <p>为每单元核心认知模型设计的快速诊断。若已掌握即可直接跳过，帮助你精准聚焦认知盲区，大幅节省学习时间。</p>
    <div class="hero-stats">
      <div class="hero-pill">🎯 5 个认知模块</div>
      <div class="hero-pill">📚 15 个决策单元</div>
      <div class="hero-pill">⚡ 极速诊断只需 5 分钟</div>
    </div>
  </header>

  <!-- 模式切换器 -->
  <div class="mode-card">
    <div class="mode-header">
      <div class="mode-title">
        <span>诊断模式选择</span>
      </div>
      <div class="mode-switch-group">
        <button class="mode-btn active" id="btn-mode-quick" data-mode="quick">
          <span>🌟 极速诊断 (15题)</span>
        </button>
        <button class="mode-btn" id="btn-mode-deep" data-mode="deep">
          <span>🔍 完整深度自测 (45题)</span>
        </button>
      </div>
    </div>
    <div class="mode-desc" id="mode-desc-text">
      <b>极速模式推荐：</b>每单元精选 1 道最具辨识度的核心“哨兵题”（共 15 题）。答对即判定可跳过；遇到不懂概念可一键跳过，约 5 分钟即可定位全部薄弱单元。
    </div>
  </div>

  <!-- 顶部吸顶进度条 -->
  <div class="sticky-progress">
    <div class="prog-label">
      <span>答题进度</span>
    </div>
    <div class="prog-track">
      <div class="prog-bar" id="prog-bar"></div>
    </div>
    <div class="prog-num" id="prog-num">0 / 15</div>
  </div>

  <!-- 模块导航 Tabs -->
  <div class="mod-tabs" id="mod-tabs"></div>

  <!-- 答题容器 -->
  <div id="quiz-container"></div>

  <!-- 底部操作栏 -->
  <div class="bottom-bar">
    <div class="bottom-left">
      <button class="btn-action btn-secondary" id="btn-prev-mod">上一模块</button>
      <button class="btn-action btn-secondary" id="btn-next-mod">下一模块</button>
    </div>
    <div class="bottom-right">
      <button class="btn-action btn-secondary" id="btn-reset">重置自测</button>
      <button class="btn-action btn-primary" id="btn-submit">提交并查看诊断报告</button>
    </div>
  </div>

  <!-- 诊断结果面板 -->
  <div class="result-panel" id="result-panel"></div>
</div>

<div class="toast" id="toast"></div>

<script>
const DATA = __PAYLOAD__;
let currentMode = "quick"; // 'quick' | 'deep'
let activeModIndex = 0;
const userAnswers = {}; // { qid: { choice: 'A'|'B'|'C'|'D'|'skip', isSkip: bool } }

const quizContainer = document.getElementById("quiz-container");
const modTabsContainer = document.getElementById("mod-tabs");
const progBar = document.getElementById("prog-bar");
const progNum = document.getElementById("prog-num");
const modeDescText = document.getElementById("mode-desc-text");

function showToast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2200);
}

// 初始化渲染
function initQuiz() {
  quizContainer.innerHTML = "";
  modTabsContainer.innerHTML = "";

  // 1. 渲染模块 Tabs
  DATA.模块.forEach((mod, idx) => {
    const tab = document.createElement("button");
    tab.className = "mod-tab" + (idx === 0 ? " active" : "");
    tab.dataset.modIdx = idx;
    tab.innerHTML = '<span>M' + (idx + 1) + ' ' + mod.模块名称.split("：")[0] + '</span><span class="mod-tab-badge" id="tab-badge-' + idx + '">0/' + getModuleQuestionCount(idx) + '</span>';
    tab.addEventListener("click", () => switchModule(idx));
    modTabsContainer.appendChild(tab);
  });

  // "全卷平铺" Tab
  const allTab = document.createElement("button");
  allTab.className = "mod-tab";
  allTab.dataset.modIdx = "all";
  allTab.innerHTML = '<span>📄 全卷平铺浏览</span>';
  allTab.addEventListener("click", () => switchModule("all"));
  modTabsContainer.appendChild(allTab);

  // 2. 渲染各模块内容
  DATA.模块.forEach((mod, modIdx) => {
    const modSec = document.createElement("div");
    modSec.className = "mod-section" + (modIdx === 0 ? " active" : "");
    modSec.dataset.modIdx = modIdx;

    const modHead = document.createElement("div");
    modHead.className = "mod-heading";
    modHead.innerHTML = '<div class="mod-heading-text">' + mod.模块编号 + '：' + mod.模块名称 + '</div>';
    modSec.appendChild(modHead);

    mod.单元.forEach(u => {
      const uCard = document.createElement("div");
      uCard.className = "unit-card";
      uCard.dataset.unit = u.编号;

      uCard.innerHTML =
        '<div class="unit-head">' +
          '<div class="unit-name"><span class="unit-tag">' + u.编号 + '</span>' + u.名称 + '</div>' +
          '<span class="unit-status-badge" data-unit-badge="' + u.编号 + '">未作答</span>' +
        '</div>' +
        '<div class="unit-meta">' +
          '<span>🎯 通过标准：' + (currentMode === "quick" ? "答对核心哨兵题即通过" : u.通过线) + '</span>' +
          '<span>· 重点：' + Array.from(new Set(u.题目.map(q => q.考察概念.split("、")[0]))).slice(0, 2).join("、") + '</span>' +
        '</div>' +
        '<div class="unit-questions" data-unit-q-container="' + u.编号 + '"></div>';

      const qContainer = uCard.querySelector('[data-unit-q-container="' + u.编号 + '"]');

      u.题目.forEach((q, qIndex) => {
        const qItem = document.createElement("div");
        qItem.className = "question-item";
        qItem.dataset.qid = q.id;
        qItem.dataset.isSentinel = q.is_sentinel ? "true" : "false";
        qItem.dataset.answer = q.答案;

        // 如果是极速模式且非哨兵题，默认隐藏
        if (currentMode === "quick" && !q.is_sentinel) {
          qItem.classList.add("hidden-question");
        }

        let optsHtml = '<div class="opt-list">';
        ["A", "B", "C", "D"].forEach(letter => {
          if (!q.选项[letter]) return;
          optsHtml +=
            '<label class="opt-row" data-letter="' + letter + '">' +
              '<input type="radio" name="' + q.id + '" value="' + letter + '">' +
              '<span class="opt-letter">' + letter + '.</span>' +
              '<span class="opt-text">' + q.选项[letter] + '</span>' +
            '</label>';
        });
        optsHtml += '</div>';

        qItem.innerHTML =
          '<div class="q-top-bar">' +
            '<div>' +
              (q.is_sentinel ? '<span class="q-sentinel-badge">🌟 核心哨兵题</span> ' : '') +
              '<span class="q-concept-tag">考察点：' + q.考察概念 + '</span>' +
            '</div>' +
          '</div>' +
          '<div class="q-title"><i>' + q.id + '</i>' + q.题干 + '</div>' +
          optsHtml +
          '<div class="q-actions">' +
            '<button type="button" class="btn-skip" data-skip-qid="' + q.id + '">⚡ 我不了解此概念（跳过）</button>' +
          '</div>' +
          '<div class="q-feedback" data-feedback-qid="' + q.id + '"></div>';

        qContainer.appendChild(qItem);
      });

      // 在极速模式下提供“展开剩余 2 题”按钮
      const expandDiv = document.createElement("div");
      expandDiv.className = "unit-expand-trigger";
      expandDiv.dataset.expandUnit = u.编号;
      expandDiv.style.display = currentMode === "quick" ? "flex" : "none";
      expandDiv.innerHTML = '<button class="btn-expand-unit" data-expand-btn="' + u.编号 + '">👇 展开本科剩余 2 题深度验证</button>';
      uCard.appendChild(expandDiv);

      modSec.appendChild(uCard);
    });

    quizContainer.appendChild(modSec);
  });

  bindEvents();
  updateProgress();
}

function getModuleQuestionCount(modIdx) {
  const mod = DATA.模块[modIdx];
  let count = 0;
  mod.单元.forEach(u => {
    u.题目.forEach(q => {
      if (currentMode === "deep" || q.is_sentinel) count++;
    });
  });
  return count;
}

function switchModule(target) {
  activeModIndex = target;
  document.querySelectorAll(".mod-tab").forEach(tab => {
    tab.classList.toggle("active", tab.dataset.modIdx == target);
  });

  document.querySelectorAll(".mod-section").forEach(sec => {
    if (target === "all") {
      sec.classList.add("active");
    } else {
      sec.classList.toggle("active", sec.dataset.modIdx == target);
    }
  });

  // 更新上一模块/下一模块按钮文字状态
  const prevBtn = document.getElementById("btn-prev-mod");
  const nextBtn = document.getElementById("btn-next-mod");
  if (target === "all") {
    prevBtn.style.display = "none";
    nextBtn.style.display = "none";
  } else {
    prevBtn.style.display = "inline-flex";
    nextBtn.style.display = "inline-flex";
    prevBtn.disabled = (target === 0);
    prevBtn.style.opacity = (target === 0 ? "0.5" : "1");
    nextBtn.textContent = (target === DATA.模块.length - 1 ? "完成浏览" : "下一模块 👉");
  }
}

function bindEvents() {
  // 选项点击事件代理
  quizContainer.addEventListener("change", e => {
    if (e.target.type !== "radio") return;
    const qid = e.target.name;
    const choice = e.target.value;
    const qItem = e.target.closest(".question-item");

    userAnswers[qid] = { choice, isSkip: false };

    qItem.querySelectorAll(".opt-row").forEach(r => r.classList.remove("selected"));
    e.target.closest(".opt-row").classList.add("selected");

    const skipBtn = qItem.querySelector('.btn-skip');
    if (skipBtn) skipBtn.classList.remove("skipped");

    updateUnitStatus(qItem.closest(".unit-card"));
    updateProgress();
  });

  // 点击“我不了解此概念（跳过）”按钮
  quizContainer.addEventListener("click", e => {
    const skipBtn = e.target.closest(".btn-skip");
    if (skipBtn) {
      const qid = skipBtn.dataset.skipQid;
      const qItem = skipBtn.closest(".question-item");
      const isAlreadySkipped = userAnswers[qid] && userAnswers[qid].isSkip;

      if (isAlreadySkipped) {
        // 取消跳过
        delete userAnswers[qid];
        skipBtn.classList.remove("skipped");
        skipBtn.textContent = "⚡ 我不了解此概念（跳过）";
      } else {
        // 设为跳过
        userAnswers[qid] = { choice: null, isSkip: true };
        qItem.querySelectorAll(".opt-row").forEach(r => {
          r.classList.remove("selected");
          const radio = r.querySelector("input");
          if (radio) radio.checked = false;
        });
        skipBtn.classList.add("skipped");
        skipBtn.textContent = "✓ 已标记跳过（未掌握）";
      }

      updateUnitStatus(qItem.closest(".unit-card"));
      updateProgress();
      return;
    }

    // 点击“展开本科剩余 2 题”
    const expandBtn = e.target.closest(".btn-expand-unit");
    if (expandBtn) {
      const uCard = expandBtn.closest(".unit-card");
      const hiddenQs = uCard.querySelectorAll(".question-item.hidden-question");
      const isExpanded = expandBtn.dataset.expanded === "true";

      if (isExpanded) {
        hiddenQs.forEach(q => q.style.display = "none");
        expandBtn.textContent = "👇 展开本科剩余 2 题深度验证";
        expandBtn.dataset.expanded = "false";
      } else {
        hiddenQs.forEach(q => q.style.display = "block");
        expandBtn.textContent = "👆 收起额外加测题目";
        expandBtn.dataset.expanded = "true";
      }
      updateProgress();
    }
  });

  // 模式切换
  document.getElementById("btn-mode-quick").addEventListener("click", () => switchMode("quick"));
  document.getElementById("btn-mode-deep").addEventListener("click", () => switchMode("deep"));

  // 模块导航
  document.getElementById("btn-prev-mod").addEventListener("click", () => {
    if (typeof activeModIndex === "number" && activeModIndex > 0) {
      switchModule(activeModIndex - 1);
      window.scrollTo({ top: 120, behavior: "smooth" });
    }
  });
  document.getElementById("btn-next-mod").addEventListener("click", () => {
    if (typeof activeModIndex === "number" && activeModIndex < DATA.模块.length - 1) {
      switchModule(activeModIndex + 1);
      window.scrollTo({ top: 120, behavior: "smooth" });
    } else {
      document.getElementById("btn-submit").scrollIntoView({ behavior: "smooth" });
    }
  });

  // 重置
  document.getElementById("btn-reset").addEventListener("click", () => {
    if (confirm("确定要清空当前所有答题记录吗？")) {
      location.reload();
    }
  });

  // 提交
  document.getElementById("btn-submit").addEventListener("click", handleSubmit);
}

function switchMode(newMode) {
  if (currentMode === newMode) return;
  currentMode = newMode;

  document.getElementById("btn-mode-quick").classList.toggle("active", newMode === "quick");
  document.getElementById("btn-mode-deep").classList.toggle("active", newMode === "deep");

  if (newMode === "quick") {
    modeDescText.innerHTML =
      '<b>极速模式（推荐）：</b>每单元精选 1 道最具辨识度的核心“哨兵题”（共 15 题）。答对即判定可跳过；遇到不懂概念可一键跳过，约 5 分钟即可定位全部薄弱单元。';
    document.querySelectorAll(".question-item").forEach(q => {
      if (q.dataset.isSentinel === "false") {
        q.classList.add("hidden-question");
        q.style.display = "none";
      } else {
        q.classList.remove("hidden-question");
        q.style.display = "block";
      }
    });
    document.querySelectorAll(".unit-expand-trigger").forEach(el => el.style.display = "flex");
  } else {
    modeDescText.innerHTML =
      '<b>深度自测模式：</b>开放全部 15 单元共 45 道题目（每单元 3 题）。单元答对率 ≥ 2/3 视为掌握，适合需要全面精确摸底的学员。';
    document.querySelectorAll(".question-item").forEach(q => {
      q.classList.remove("hidden-question");
      q.style.display = "block";
    });
    document.querySelectorAll(".unit-expand-trigger").forEach(el => el.style.display = "none");
  }

  // 刷新徽章总数
  DATA.模块.forEach((m, idx) => {
    const badge = document.getElementById("tab-badge-" + idx);
    if (badge) badge.textContent = "0/" + getModuleQuestionCount(idx);
  });

  document.querySelectorAll(".unit-card").forEach(u => updateUnitStatus(u));
  updateProgress();
  showToast(newMode === "quick" ? "已切换至 15 题极速诊断模式" : "已切换至 45 题完整深度自测模式");
}

function updateUnitStatus(uCard) {
  const qs = [...uCard.querySelectorAll(".question-item")].filter(q => q.style.display !== "none");
  const answered = qs.filter(q => userAnswers[q.dataset.qid]).length;
  const badge = uCard.querySelector("[data-unit-badge]");

  if (answered === 0) {
    badge.className = "unit-status-badge";
    badge.textContent = "未作答";
  } else if (answered < qs.length) {
    badge.className = "unit-status-badge";
    badge.textContent = answered + "/" + qs.length + " 作答中";
  } else {
    badge.className = "unit-status-badge ok";
    badge.textContent = "已完成本单元";
  }
}

function updateProgress() {
  // 计算当前可视题目的作答数
  const visibleQs = [...document.querySelectorAll(".question-item")].filter(q => q.style.display !== "none");
  const total = visibleQs.length;
  const answered = visibleQs.filter(q => userAnswers[q.dataset.qid]).length;

  const pct = total === 0 ? 0 : Math.round((answered / total) * 100);
  progBar.style.width = pct + "%";
  progNum.textContent = answered + " / " + total + " (" + pct + "%)";

  // 更新各模块 Tab 徽章
  DATA.模块.forEach((mod, idx) => {
    const sec = document.querySelector('.mod-section[data-mod-idx="' + idx + '"]');
    if (!sec) return;
    const modVisibleQs = [...sec.querySelectorAll(".question-item")].filter(q => q.style.display !== "none");
    const modAnswered = modVisibleQs.filter(q => userAnswers[q.dataset.qid]).length;
    const tabBadge = document.getElementById("tab-badge-" + idx);
    if (tabBadge) {
      tabBadge.textContent = modAnswered + "/" + modVisibleQs.length;
    }
  });
}

function handleSubmit() {
  const unitsResult = [];
  let totalScore = 0;
  let totalQuestionsCount = 0;

  document.querySelectorAll(".unit-card").forEach(uCard => {
    const unitId = uCard.dataset.unit;
    const unitTitle = uCard.querySelector(".unit-name").textContent.replace(unitId, "").trim();
    const qs = [...uCard.querySelectorAll(".question-item")].filter(q => q.style.display !== "none");

    let unitCorrect = 0;
    let sentinelCorrect = false;

    qs.forEach(qItem => {
      totalQuestionsCount++;
      const qid = qItem.dataset.qid;
      const ans = qItem.dataset.answer;
      const isSentinel = qItem.dataset.isSentinel === "true";
      const record = userAnswers[qid];
      const isSkip = record && record.isSkip;
      const userChoice = record ? record.choice : null;
      const isCorrect = userChoice === ans;

      if (isCorrect) {
        unitCorrect++;
        totalScore++;
        if (isSentinel) sentinelCorrect = true;
      }

      // 高亮选项
      qItem.querySelectorAll(".opt-row").forEach(row => {
        row.classList.remove("is-correct", "is-wrong");
        if (row.dataset.letter === ans) {
          row.classList.add("is-correct");
        } else if (row.dataset.letter === userChoice && !isCorrect) {
          row.classList.add("is-wrong");
        }
      });

      // 反馈信息
      const fb = qItem.querySelector("[data-feedback-qid]");
      const qData = DATA.模块.flatMap(m => m.单元).find(u => u.编号 === unitId).题目.find(x => x.id === qid);

      fb.className = "q-feedback show " + (isCorrect ? "ok" : "err");
      if (isCorrect) {
        fb.innerHTML = "✔ <b>正确！</b>考察重点：" + qData.考察概念;
      } else if (isSkip) {
        fb.innerHTML = "⚡ <b>已跳过。</b>标准答案是 <b>" + ans + "</b>（" + qData.选项[ans] + "）。<br><b>重点说明：</b>" + qData.答错说明;
      } else {
        fb.innerHTML = "✘ <b>有待提升。</b>标准答案是 <b>" + ans + "</b>。<br><b>解析说明：</b>" + qData.答错说明;
      }
    });

    // 单元达标判定
    let passed = false;
    if (currentMode === "quick") {
      // 极速模式：若只做 1 题看哨兵题；若展开做了多题，答对率 ≥ 2/3 亦可
      passed = (qs.length === 1) ? sentinelCorrect : (unitCorrect >= Math.ceil(qs.length * 2 / 3));
    } else {
      passed = unitCorrect >= Math.ceil(qs.length * 2 / 3);
    }

    const badge = uCard.querySelector("[data-unit-badge]");
    badge.className = "unit-status-badge " + (passed ? "ok" : "warn");
    badge.textContent = (passed ? "✅ 可跳过 " : "📘 建议学习 ") + unitCorrect + "/" + qs.length;

    // 抓取该单元考察概念
    const concepts = Array.from(new Set(
      DATA.模块.flatMap(m => m.单元).find(u => u.编号 === unitId).题目.map(q => q.考察概念)
    )).join("、");

    unitsResult.push({
      id: unitId,
      name: unitTitle,
      passed: passed,
      correct: unitCorrect,
      total: qs.length,
      concepts: concepts
    });
  });

  // 渲染诊断结果报告面板
  renderReport(unitsResult, totalScore, totalQuestionsCount);
}

function renderReport(units, totalScore, totalQ) {
  const needUnits = units.filter(u => !u.passed);
  const passUnits = units.filter(u => u.passed);
  const needCount = needUnits.length;

  let bannerClass, bannerIcon, bannerTitle, bannerDesc;
  if (needCount > 5) {
    bannerClass = "full";
    bannerIcon = "📘";
    bannerTitle = "建议系统、完整学习本课程";
    bannerDesc = "你有 <b>" + needCount + " 个核心决策单元</b> 存在认知盲区。现代决策学是一套互相关联的思考操作系统，建议从头按模块完整选修，彻底完成决策思维重构。";
  } else if (needCount >= 3) {
    bannerClass = "some";
    bannerIcon = "💡";
    bannerTitle = "建议按需重点补课";
    bannerDesc = "你已具备相当扎实的决策素养，但在 <b>" + needCount + " 个单元</b> 仍存在典型认知误区。建议针对下方标明的薄弱单元重点攻坚即可，其余单元可自主免修。";
  } else if (needCount >= 1) {
    bannerClass = "few";
    bannerIcon = "🎯";
    bannerTitle = "极高水准！仅需定向查漏补缺";
    bannerDesc = "仅有 <b>" + needCount + " 个单元</b> 建议查漏补缺，其余绝大部分课程你均已熟练掌握，完全可以直接跳过！";
  } else {
    bannerClass = "pass";
    bannerIcon = "🏆";
    bannerTitle = "恭喜通关！认知模型极其完备";
    bannerDesc = "全部 15 个决策单元均已达标！你对现代决策学的科学工具、实验机制与偏误防御具备极高敏锐度，<b>整门课程均可跳过</b>！";
  }

  const R = document.getElementById("result-panel");
  R.innerHTML =
    '<div class="res-header">' +
      '<h2 class="res-title">📊 个人决策认知能力诊断报告</h2>' +
      '<div class="res-stat">' +
        '<span>当前诊断模式：<b>' + (currentMode === "quick" ? "极速诊断（15题）" : "完整自测（45题）") + '</b></span>' +
        '<span>总体掌握得分：<b>' + totalScore + ' / ' + totalQ + ' (' + Math.round(totalScore / totalQ * 100) + '%)</b></span>' +
        '<span>达标可跳过：<b style="color:var(--ok);">' + passUnits.length + ' 单元</b></span>' +
        '<span>建议选修：<b style="color:var(--warn);">' + needUnits.length + ' 单元</b></span>' +
      '</div>' +
    '</div>' +
    '<div class="res-banner ' + bannerClass + '">' +
      '<div class="res-banner-icon">' + bannerIcon + '</div>' +
      '<div>' +
        '<div style="font-size:16px;font-weight:700;margin-bottom:4px;">' + bannerTitle + '</div>' +
        '<div>' + bannerDesc + '</div>' +
      '</div>' +
    '</div>' +
    '<h3 style="font-size:15px;margin:20px 0 10px;">📋 各单元诊断与选课清单：</h3>' +
    '<div class="res-grid">' +
      units.map(u =>
        '<div class="res-card ' + (u.passed ? "pass" : "need") + '">' +
          '<div class="res-card-top">' +
            '<span class="res-card-title">' + u.id + ' ' + u.name + '</span>' +
            '<span class="res-card-badge">' + (u.passed ? "✅ 可跳过 (" + u.correct + "/" + u.total + ")" : "📘 建议学习 (" + u.correct + "/" + u.total + ")") + '</span>' +
          '</div>' +
          '<div class="res-card-concepts">核心模型：' + u.concepts + '</div>' +
        '</div>'
      ).join("") +
    '</div>' +
    '<div class="res-actions">' +
      '<button class="btn-action btn-secondary" id="btn-copy-plan">📋 复制选课诊断清单</button>' +
      '<button class="btn-action btn-primary" onclick="window.scrollTo({top:0,behavior:\'smooth\'})">⬆ 回到顶部查看答题详情</button>' +
    '</div>';

  R.classList.add("show");
  R.scrollIntoView({ behavior: "smooth" });

  document.getElementById("btn-copy-plan").addEventListener("click", () => {
    let copyText = "【现代决策学 · 前置自测诊断清单】\\n";
    copyText += "评估结论：" + bannerTitle + "\\n";
    copyText += "达标单元：" + passUnits.map(u => u.id + " " + u.name).join("、") + "\\n";
    copyText += "建议选修：" + (needUnits.length ? needUnits.map(u => u.id + " " + u.name).join("、") : "无（全部达标）") + "\\n";
    navigator.clipboard.writeText(copyText).then(() => {
      showToast("已成功复制选课建议清单到剪贴板！");
    });
  });
}

// 启动初始化
initQuiz();
</script>
</body>
</html>
"""

out = HTML.replace("__PAYLOAD__", payload)
(BASE / "decision_science_prequiz.html").write_text(out, encoding="utf-8")
print("written:", BASE / "decision_science_prequiz.html")
