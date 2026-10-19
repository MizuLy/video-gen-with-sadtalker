"""Talking image web app. Put this file in the SadTalker folder, then: python app.py"""
import glob
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
import asyncio

import edge_tts

BASE = Path(__file__).parent.resolve()
JOBS = BASE / "jobs"
JOBS.mkdir(exist_ok=True)
FFMPEG = shutil.which("ffmpeg") or str(
    Path(sys.executable).parent / "ffmpeg.exe")

VOICES = {
    ("km", "female"): "km-KH-SreymomNeural",
    ("km", "male"): "km-KH-PisethNeural",
    ("en", "female"): "en-US-JennyNeural",
    ("en", "male"): "en-US-GuyNeural",
}

app = FastAPI()

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Talking Image</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Figtree:wght@400;500;600&family=Noto+Sans+Khmer:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#eceff7; --panel:#ffffff; --ink:#171b3a; --muted:#5e6485; --line:#d9ddee;
    --accent:#4f46f5; --accent-ink:#ffffff; --accent-soft:#e8e7ff; --danger:#c0304a;
    --stage:#161a38;
    --display:"Bricolage Grotesque",system-ui,sans-serif;
    --body:"Figtree","Noto Sans Khmer",system-ui,sans-serif;
  }
  @media (prefers-color-scheme:dark){
    :root{--bg:#0f1226; --panel:#181c3a; --ink:#eceefc; --muted:#9aa0c8; --line:#2b3060;
      --accent:#8b84ff; --accent-ink:#0f1226; --accent-soft:#2a2c63; --danger:#ff7a93; --stage:#0b0d1d}
  }
  *{box-sizing:border-box}
  body{margin:0;min-height:100vh;background:var(--bg);color:var(--ink);font:16px/1.5 var(--body);
    background-image:radial-gradient(60rem 30rem at 85% -10%,var(--accent-soft),transparent 70%)}
  :focus-visible{outline:3px solid var(--accent);outline-offset:2px}
  main{max-width:1040px;margin:0 auto;padding:48px 20px 64px}
  header{margin-bottom:32px}
  h1{font:700 clamp(32px,5vw,52px)/1.02 var(--display);letter-spacing:-.025em;margin:0 0 10px}
  header p{margin:0;color:var(--muted);max-width:46ch}
  .grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,420px);gap:24px;align-items:start}
  @media (max-width:820px){.grid{grid-template-columns:1fr}.stage-wrap{order:-1}}

  .panel{background:var(--panel);border:1px solid var(--line);border-radius:20px;padding:24px;
    box-shadow:0 1px 2px rgba(23,27,58,.04),0 12px 32px -16px rgba(23,27,58,.18)}
  .field+.field{margin-top:22px}
  .field>label,.field>.lbl{display:block;font-weight:600;font-size:14px;margin-bottom:8px}
  .hint{font-weight:400;color:var(--muted)}

  .drop{display:flex;align-items:center;gap:14px;padding:16px;border:1.5px dashed var(--line);border-radius:14px;
    cursor:pointer;transition:border-color .15s,background .15s}
  .drop:hover,.drop.over{border-color:var(--accent);background:var(--accent-soft)}
  .drop input{position:absolute;opacity:0;width:1px;height:1px}
  .drop:focus-within{outline:3px solid var(--accent);outline-offset:2px}
  .drop svg{flex:none;width:36px;height:36px;color:var(--accent)}
  .drop b{display:block;font-size:15px}
  .drop span{font-size:13px;color:var(--muted)}

  textarea{width:100%;min-height:140px;padding:14px;border:1px solid var(--line);border-radius:14px;resize:vertical;
    background:transparent;color:var(--ink);font:17px/1.6 var(--body)}
  textarea::placeholder{color:var(--muted)}
  textarea:focus{outline:3px solid var(--accent);outline-offset:0;border-color:transparent}

  .seg{display:inline-grid;grid-auto-flow:column;gap:4px;padding:4px;border-radius:12px;background:var(--bg);border:1px solid var(--line)}
  .seg label{margin:0}
  .seg input{position:absolute;opacity:0;width:1px;height:1px}
  .seg span{display:block;padding:8px 18px;border-radius:9px;font-weight:600;font-size:14px;cursor:pointer;color:var(--muted)}
  .seg input:checked+span{background:var(--panel);color:var(--ink);box-shadow:0 1px 3px rgba(23,27,58,.2)}
  .seg input:focus-visible+span{outline:3px solid var(--accent)}

  .toggle{display:flex;align-items:center;gap:12px;cursor:pointer;font-size:15px}
  .toggle input{position:absolute;opacity:0;width:1px;height:1px}
  .track{flex:none;width:42px;height:24px;border-radius:99px;background:var(--line);position:relative;transition:background .15s}
  .track::after{content:"";position:absolute;top:3px;left:3px;width:18px;height:18px;border-radius:50%;background:#fff;transition:transform .15s}
  .toggle input:checked+.track{background:var(--accent)}
  .toggle input:checked+.track::after{transform:translateX(18px)}
  .toggle input:focus-visible+.track{outline:3px solid var(--accent);outline-offset:2px}
  .toggle small{color:var(--muted)}

  button#go{margin-top:26px;width:100%;padding:15px;border:0;border-radius:14px;background:var(--accent);color:var(--accent-ink);
    font:600 17px var(--body);cursor:pointer;transition:transform .1s,filter .15s}
  button#go:hover{filter:brightness(1.08)}
  button#go:active{transform:scale(.99)}
  button#go:disabled{opacity:.55;cursor:wait}

  .stage-wrap{position:sticky;top:24px}
  .stage{position:relative;aspect-ratio:4/5;border-radius:24px;overflow:hidden;background:var(--stage);
    display:grid;place-items:center;box-shadow:0 24px 48px -24px rgba(23,27,58,.5)}
  .stage img,.stage video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;background:var(--stage)}
  .stage video{z-index:2}
  .empty{text-align:center;color:#9aa0c8;padding:24px;max-width:26ch;font-size:14px}
  .empty svg{width:56px;height:56px;margin-bottom:8px;opacity:.8}
  .stage.busy img{filter:saturate(.8) brightness(.7)}
  .rings{position:absolute;inset:0;z-index:1;display:none;place-items:center;pointer-events:none}
  .stage.busy .rings{display:grid}
  .rings i{position:absolute;width:90px;height:90px;border-radius:50%;border:2px solid #fff;opacity:0;animation:ring 2.4s ease-out infinite}
  .rings i:nth-child(2){animation-delay:.8s}.rings i:nth-child(3){animation-delay:1.6s}
  @keyframes ring{0%{transform:scale(.6);opacity:.8}100%{transform:scale(4);opacity:0}}
  @media (prefers-reduced-motion:reduce){.rings i{animation:none;opacity:.5}}

  #status{margin-top:14px;font-size:14px;color:var(--muted);min-height:21px}
  #status.err{color:var(--danger);font-weight:500}
  #status[hidden]{display:none}
  #dl{display:none;margin-top:10px;font-weight:600;color:var(--accent);text-decoration:none}
  #dl:hover{text-decoration:underline}
</style></head>
<body>
<main>
<header>
  <h1>Make a photo talk</h1>
  <p>Upload a front-facing face, type what it should say, and get a short speaking video.</p>
</header>
<div class="grid">
  <section class="panel" aria-label="Settings">
    <div class="field">
      <span class="lbl">Face photo</span>
      <label class="drop" id="drop">
        <input type="file" id="image" accept="image/*">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5M4 15v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/></svg>
        <div><b id="fname">Choose a photo</b><span>Drop an image here or browse. Front-facing works best.</span></div>
      </label>
    </div>
    <div class="field">
      <label for="text">What should it say?</label>
      <textarea id="text" placeholder="Type what the face should say..."></textarea>
    </div>
    <div class="field">
      <span class="lbl">Language</span>
      <div class="seg" role="radiogroup" aria-label="Language">
        <label><input type="radio" name="lang" value="km" checked><span>Khmer</span></label>
        <label><input type="radio" name="lang" value="en"><span>English</span></label>
      </div>
    </div>
    <div class="field">
      <span class="lbl">Voice</span>
      <div class="seg" role="radiogroup" aria-label="Voice">
        <label><input type="radio" name="voice" value="female" checked><span>Female</span></label>
        <label><input type="radio" name="voice" value="male"><span>Male</span></label>
      </div>
    </div>
    <div class="field">
      <label class="toggle"><input type="checkbox" id="enhance"><span class="track"></span>
        <span>Sharper face <small>(slower)</small></span></label>
    </div>
    <button id="go">Generate video</button>
    <div id="status" role="status" aria-live="polite" hidden></div>
  </section>

  <aside class="stage-wrap">
    <div class="stage" id="stage">
      <div class="empty" id="empty">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="9" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/></svg>
        <div>Your photo and the finished video appear here.</div>
      </div>
      <img id="preview" alt="Selected face" style="display:none">
      <div class="rings"><i></i><i></i><i></i></div>
      <video id="video" controls playsinline style="display:none"></video>
    </div>
    <a id="dl" download="talking-image.mp4">Download video</a>
  </aside>
</div>
</main>
<script>
const $ = id => document.getElementById(id);
const setStatus = (msg, err) => {
  $("status").hidden = !msg; $("status").textContent = msg || "";
  $("status").className = err ? "err" : "";
};
const showFile = f => {
  if (!f) return;
  $("preview").src = URL.createObjectURL(f);
  $("preview").style.display = "block";
  $("empty").style.display = "none";
  $("video").style.display = "none";
  $("dl").style.display = "none";
  $("fname").textContent = f.name;
};
$("image").onchange = e => showFile(e.target.files[0]);
const drop = $("drop");
["dragenter","dragover"].forEach(t => drop.addEventListener(t, e => { e.preventDefault(); drop.classList.add("over"); }));
["dragleave","drop"].forEach(t => drop.addEventListener(t, e => { e.preventDefault(); drop.classList.remove("over"); }));
drop.addEventListener("drop", e => {
  const f = e.dataTransfer.files[0];
  if (f && f.type.startsWith("image/")) { $("image").files = e.dataTransfer.files; showFile(f); }
});
$("go").onclick = async () => {
  const file = $("image").files[0], text = $("text").value.trim();
  if (!file || !text) { setStatus("Choose a photo and type some text first.", true); return; }
  const fd = new FormData();
  fd.append("image", file);
  fd.append("text", text);
  fd.append("lang", document.querySelector("input[name=lang]:checked").value);
  fd.append("voice", document.querySelector("input[name=voice]:checked").value);
  fd.append("enhance", $("enhance").checked ? "true" : "false");
  $("go").disabled = true;
  $("go").textContent = "Generating...";
  $("video").style.display = "none";
  $("dl").style.display = "none";
  $("stage").classList.add("busy");
  const t0 = Date.now();
  const tick = setInterval(() => {
    const s = Math.floor((Date.now() - t0) / 1000);
    setStatus("Generating for " + Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0") + ". This takes 1-3 minutes, so keep this tab open.");
  }, 500);
  try {
    const res = await fetch("/generate", { method: "POST", body: fd });
    if (!res.ok) throw new Error((await res.json()).detail || res.statusText);
    const url = URL.createObjectURL(await res.blob());
    $("video").src = url;
    $("video").style.display = "block";
    $("video").play();
    $("dl").href = url; $("dl").style.display = "inline-block";
    setStatus("Your video is ready.");
  } catch (err) {
    setStatus("Generation failed: " + err.message, true);
  }
  clearInterval(tick);
  $("stage").classList.remove("busy");
  $("go").disabled = false;
  $("go").textContent = "Generate video";
};
</script>
</body></html>"""


@app.get("/", response_class=HTMLResponse)
def index():
    return PAGE


@app.post("/generate")
def generate(
    image: UploadFile = File(...),
    text: str = Form(...),
    lang: str = Form("km"),
    voice: str = Form("female"),
    enhance: bool = Form(False),
):
    job = JOBS / uuid.uuid4().hex
    job.mkdir()
    img = job / ("face" + (Path(image.filename or "").suffix or ".png"))
    img.write_bytes(image.file.read())
    mp3, wav = job / "speech.mp3", job / "speech.wav"

    try:
        name = VOICES.get((lang, voice), VOICES[("km", "female")])
        asyncio.run(edge_tts.Communicate(text, name).save(str(mp3)))
    except Exception as e:
        raise HTTPException(500, f"TTS failed (needs internet): {e}")

    conv = subprocess.run([FFMPEG, "-y", "-i", str(mp3),
                          str(wav)], capture_output=True, text=True)
    if conv.returncode != 0:
        raise HTTPException(500, f"ffmpeg failed: {conv.stderr[-500:]}")

    cmd = [
        sys.executable, str(BASE / "inference.py"),
        "--driven_audio", str(wav),
        "--source_image", str(img),
        "--result_dir", str(job / "out"),
        "--still", "--preprocess", "full",
    ]
    if enhance:
        cmd += ["--enhancer", "gfpgan"]
    run = subprocess.run(cmd, cwd=BASE, capture_output=True, text=True)

    videos = sorted(glob.glob(str(job / "out" / "*.mp4")))
    if not videos:
        raise HTTPException(500, (run.stderr or run.stdout)[-800:])
    # SadTalker writes MPEG-4 Part 2, which browsers can't show (audio only). Re-encode to H.264.
    web = job / "web.mp4"
    enc = subprocess.run(
        [FFMPEG, "-y", "-i", videos[-1], "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-movflags", "+faststart", str(web)],
        capture_output=True, text=True,
    )
    if enc.returncode != 0:
        raise HTTPException(500, f"re-encode failed: {enc.stderr[-500:]}")
    return FileResponse(str(web), media_type="video/mp4")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

# To run
# cd C:\Users\USER\Desktop\SadTalker
# venv\Scripts\activate        # PowerShell; in Git Bash: source venv/Scripts/activate
# python app.py
