#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""读取题库 JSON，生成自包含的互动自测 HTML。"""
import json, pathlib

BASE = pathlib.Path(__file__).resolve().parent
data = json.loads((BASE / "decision_science_prequiz.json").read_text(encoding="utf-8"))
payload = json.dumps(data, ensure_ascii=False)

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>现代决策学 · 前置自测</title>
<style>
  :root{
    --bg:#f6f7f9; --panel:#ffffff; --ink:#1f2430; --sub:#5b6472; --line:#e6e9ef;
    --brand:#2f6fed; --brand-soft:#eaf1ff; --ok:#1a9e6a; --ok-soft:#e8f7f0;
    --warn:#d97706; --warn-soft:#fdf3e3; --err:#dc2626; --err-soft:#fdecec;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",system-ui,sans-serif;
    line-height:1.6;}
  .wrap{max-width:880px;margin:0 auto;padding:32px 20px 96px;}
  header.top{background:linear-gradient(135deg,#2f6fed,#5b8cf7);color:#fff;border-radius:18px;
    padding:28px 26px;box-shadow:0 8px 24px rgba(47,111,237,.18);}
  header.top h1{margin:0 0 6px;font-size:22px;letter-spacing:.5px}
  header.top p{margin:0;opacity:.92;font-size:13.5px}
  .legend{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px;font-size:12px}
  .legend span{background:rgba(255,255,255,.18);padding:3px 10px;border-radius:20px}
  .intro{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 18px;
    margin:18px 0 22px;font-size:13.5px;color:var(--sub)}
  .intro b{color:var(--ink)}
  .mod{margin:26px 0 10px;font-size:15px;font-weight:700;color:var(--ink);
    display:flex;align-items:center;gap:10px}
  .mod::before{content:"";width:4px;height:18px;border-radius:3px;background:var(--brand)}
  .unit{background:var(--panel);border:1px solid var(--line);border-radius:16px;
    padding:18px 20px;margin:14px 0;box-shadow:0 1px 3px rgba(20,30,60,.04)}
  .unit-h{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
  .unit-t{font-size:15px;font-weight:700}
  .unit-t small{font-weight:600;color:var(--brand);margin-right:8px;background:var(--brand-soft);
    padding:2px 8px;border-radius:8px;font-size:12px}
  .badge{font-size:12.5px;font-weight:600;padding:5px 12px;border-radius:20px;white-space:nowrap;
    background:#eef1f6;color:var(--sub)}
  .badge.ok{background:var(--ok-soft);color:var(--ok)}
  .badge.warn{background:var(--warn-soft);color:var(--warn)}
  .goal{font-size:12.5px;color:var(--sub);margin:8px 0 4px}
  .q{padding:14px 0;border-top:1px dashed var(--line);margin-top:12px}
  .q:first-of-type{border-top:none;margin-top:6px}
  .q-t{font-size:14px;font-weight:600;margin-bottom:10px}
  .q-t i{font-style:normal;color:var(--brand);font-weight:700;margin-right:6px}
  .opts{display:flex;flex-direction:column;gap:7px}
  .opt{display:flex;gap:10px;align-items:flex-start;border:1px solid var(--line);border-radius:10px;
    padding:9px 12px;cursor:pointer;font-size:13.5px;transition:.15s;background:#fff}
  .opt:hover{border-color:#c7d5f5;background:#fafbff}
  .opt input{margin-top:3px;accent-color:var(--brand)}
  .opt.sel{border-color:var(--brand);background:var(--brand-soft)}
  .opt.right{border-color:var(--ok);background:var(--ok-soft)}
  .opt.wrong{border-color:var(--err);background:var(--err-soft)}
  .opt .k{font-weight:700;color:var(--sub);min-width:14px}
  .fb{display:none;margin-top:10px;font-size:12.8px;border-radius:10px;padding:10px 12px}
  .fb.show{display:block}
  .fb.right{background:var(--ok-soft);color:#166a4b}
  .fb.wrong{background:var(--err-soft);color:#a12121}
  .fb b{color:inherit}
  .actions{position:sticky;bottom:0;margin-top:26px;background:linear-gradient(180deg,rgba(246,247,249,0),var(--bg) 30%);
    padding:18px 0 6px;display:flex;gap:12px;flex-wrap:wrap;align-items:center}
  button{border:none;border-radius:12px;padding:12px 22px;font-size:14.5px;font-weight:600;cursor:pointer;
    font-family:inherit;transition:.15s}
  .primary{background:var(--brand);color:#fff;box-shadow:0 6px 16px rgba(47,111,237,.28)}
  .primary:hover{background:#255fd6}
  .ghost{background:#fff;color:var(--sub);border:1px solid var(--line)}
  .ghost:hover{border-color:#c7d5f5;color:var(--brand)}
  .result{display:none;margin-top:22px;background:var(--panel);border:1px solid var(--line);
    border-radius:16px;padding:22px;box-shadow:0 8px 24px rgba(20,30,60,.08)}
  .result.show{display:block}
  .result h2{margin:0 0 6px;font-size:18px}
  .score-top{font-size:13.5px;color:var(--sub);margin-bottom:14px}
  .bar{height:10px;border-radius:6px;background:#eef1f6;overflow:hidden;margin:6px 0 14px}
  .bar>i{display:block;height:100%;background:linear-gradient(90deg,#2f6fed,#6aa0ff);width:0;transition:.6s}
  .advice{font-size:14px;background:var(--brand-soft);color:#1d4fa8;border-radius:12px;padding:12px 14px;margin-bottom:16px}
  .rlist{display:grid;grid-template-columns:1fr 1fr;gap:8px}
  .ritem{display:flex;justify-content:space-between;gap:8px;font-size:13px;padding:8px 11px;border-radius:10px;background:#f4f6fa}
  .ritem.ok{background:var(--ok-soft)}
  .ritem.warn{background:var(--warn-soft)}
  .ritem .n{color:var(--sub)}
  @media(max-width:560px){.rlist{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <h1>现代决策学 · 前置自测</h1>
    <p>答完每单元的选择题，系统自动判断你是否已掌握，并提示是否需要上这门课。</p>
    <div class="legend">
      <span>✅ 答对率 ≥ 2/3 → 可跳过</span>
      <span>📘 低于 2/3 → 建议学习</span>
    </div>
  </header>

  <div class="intro" id="intro"></div>

  <div id="quiz"></div>

  <div class="actions">
    <button class="primary" id="submit">提交并查看诊断结果</button>
    <button class="ghost" id="reset">重做</button>
  </div>

  <div class="result" id="result"></div>
</div>

<script>
const DATA = __PAYLOAD__;
const KEY = ["A","B","C","D"];

document.getElementById("intro").innerHTML =
  "<b>课程：</b>" + DATA["课程名称"] + "　|　<b>共 " + DATA.模块.length + " 个模块、" +
  DATA.模块.reduce((n,m)=>n+m.单元.length,0) + " 个单元</b><br>" +
  DATA.评分规则.单元判定;

const quiz = document.getElementById("quiz");
DATA.模块.forEach(mod=>{
  const h = document.createElement("div");
  h.className = "mod"; h.textContent = mod.模块编号 + "　" + mod.模块名称;
  quiz.appendChild(h);
  mod.单元.forEach(u=>{
    const box = document.createElement("div");
    box.className = "unit";
    box.dataset.unit = u.编号;
    box.innerHTML =
      '<div class="unit-h"><div class="unit-t"><small>'+u.编号+'</small>'+u.名称+'</div>'+
      '<span class="badge" data-badge>未作答</span></div>'+
      '<div class="goal">通过线：'+u.通过线+'　·　考察目标：'+(u.题目.map(q=>q.考察概念).filter((v,i,a)=>a.indexOf(v)===i).join("、"))+'</div>';
    u.题目.forEach((q,qi)=>{
      const qd = document.createElement("div");
      qd.className = "q";
      qd.dataset.qid = q.id;
      qd.dataset.answer = q.答案;
      let opts = '<div class="opts">';
      KEY.forEach(k=>{
        if(!(k in q.选项)) return;
        opts += '<label class="opt" data-k="'+k+'"><input type="radio" name="'+q.id+'" value="'+k+'">'+
                '<span class="k">'+k+'.</span><span>'+q.选项[k]+'</span></label>';
      });
      opts += '</div>';
      qd.innerHTML = '<div class="q-t"><i>Q'+(qi+1)+'</i>'+q.题干+'</div>'+opts+
        '<div class="fb" data-fb></div>';
      box.appendChild(qd);
    });
    quiz.appendChild(box);
  });
});

quiz.addEventListener("change", e=>{
  if(e.target.type!=="radio") return;
  const qd = e.target.closest(".q");
  qd.querySelectorAll(".opt").forEach(o=>o.classList.remove("sel"));
  e.target.closest(".opt").classList.add("sel");
  updateBadge(qd.closest(".unit"));
});

function updateBadge(unitBox){
  const qs = [...unitBox.querySelectorAll(".q")];
  const done = qs.filter(q=>q.querySelector("input:checked")).length;
  const badge = unitBox.querySelector("[data-badge]");
  if(done===0){ badge.className="badge"; badge.textContent="未作答"; }
  else if(done<qs.length){ badge.className="badge"; badge.textContent=done+"/"+qs.length+" 作答中"; }
  else { badge.className="badge"; badge.textContent="待提交"; }
}

document.getElementById("reset").addEventListener("click", ()=>location.reload());

document.getElementById("submit").addEventListener("click", ()=>{
  const units = [];
  let answeredAll = true;
  document.querySelectorAll(".unit").forEach(unitBox=>{
    const qs = [...unitBox.querySelectorAll(".q")];
    let correct=0, answered=0;
    qs.forEach(q=>{
      const sel = q.querySelector("input:checked");
      const ans = q.dataset.answer;
      const fb = q.querySelector("[data-fb]");
      q.querySelectorAll(".opt").forEach(o=>o.classList.remove("right","wrong"));
      if(sel){
        answered++;
        const chosen = sel.value;
        if(chosen===ans){ correct++; sel.closest(".opt").classList.add("right"); }
        else {
          sel.closest(".opt").classList.add("wrong");
          q.querySelector('.opt[data-k="'+ans+'"]').classList.add("right");
        }
      } else {
        q.querySelector('.opt[data-k="'+ans+'"]').classList.add("right");
      }
      const data = DATA.模块.flatMap(m=>m.单元).find(u=>u.编号===unitBox.dataset.unit)
                    .题目.find(x=>x.id===q.dataset.qid);
      const ok = sel && sel.value===ans;
      fb.className = "fb show " + (ok?"right":"wrong");
      fb.innerHTML = ok
        ? "✔ 回答正确。考察点：" + data.考察概念
        : "✘ 正确答案：" + ans + "。考察点：" + data.考察概念 + "<br>说明：" + data.答错说明;
    });
    if(answered<qs.length) answeredAll=false;
    const pass = correct >= Math.ceil(qs.length*2/3);
    const badge = unitBox.querySelector("[data-badge]");
    badge.className = "badge " + (pass?"ok":"warn");
    badge.textContent = (pass?"✅ 可跳过 ":"📘 建议学习 ") + correct+"/"+qs.length;
    units.push({编号:unitBox.dataset.unit,
      名称:unitBox.querySelector(".unit-t").textContent.replace(unitBox.dataset.unit,"").trim(),
      正确:correct,题数:qs.length,pass});
  });

  const need = units.filter(u=>!u.pass).length;
  let advice;
  if(need>5) advice = "你有 <b>"+need+"</b> 个单元未达标，建议<b>完整学习本课程</b>，从头建立决策操作系统。";
  else if(need>=3) advice = "你有 <b>"+need+"</b> 个单元未达标，建议<b>按需补课</b>，优先补齐下方标记为『建议学习』的单元。";
  else if(need>=1) advice = "仅 <b>"+need+"</b> 个单元未达标，可<b>定向学习</b>这几个薄弱单元，其余可跳过。";
  else advice = "🎉 全部单元均已达标，你已具备本课程的核心认知，<b>可整体跳过</b>，或仅做兴趣性浏览。";

  const R = document.getElementById("result");
  const total = units.reduce((s,u)=>s+u.正确,0);
  const totalQ = units.reduce((s,u)=>s+u.题数,0);
  R.innerHTML =
    '<h2>诊断结果</h2>'+
    '<div class="score-top">总正确率：'+total+' / '+totalQ+'　（'+Math.round(total/totalQ*100)+'%）'+
      (answeredAll?"":"　⚠️ 存在未作答题目，已按答错计")+'</div>'+
    '<div class="bar"><i style="width:'+(total/totalQ*100)+'%"></i></div>'+
    '<div class="advice">'+advice+'</div>'+
    '<div class="rlist">'+units.map(u=>
      '<div class="ritem '+(u.pass?"ok":"warn")+'"><span class="n">'+u.编号+" "+u.名称+
      '</span><b>'+(u.pass?"可跳过":"建议学习")+' '+u.正确+"/"+u.题数+'</b></div>').join("")+'</div>';
  R.classList.add("show");
  R.scrollIntoView({behavior:"smooth"});
});
</script>
</body>
</html>
"""

out = HTML.replace("__PAYLOAD__", payload)
(BASE / "decision_science_prequiz.html").write_text(out, encoding="utf-8")
print("written:", BASE / "decision_science_prequiz.html")
