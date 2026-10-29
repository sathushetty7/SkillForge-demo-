"use client";

import { useEffect, useMemo, useState } from "react";
import {
  Activity, ArrowDownRight, ArrowRight, ArrowUpRight, BookOpen, BriefcaseBusiness,
  Check, ChevronDown, CircleHelp, Clock3, Code2, Compass, FileText, Flame,
  GraduationCap, LayoutDashboard, LoaderCircle, Menu, Plus, Rocket, Search,
  Settings2, ShieldCheck, Sparkles, Target, UploadCloud, X, Zap
} from "lucide-react";

type Role = { title: string; required_skills?: string[]; description?: string };
type RoadmapItem = {
  skill: string; estimated_hours?: number; week?: number; estimated_duration_weeks?: number;
  prerequisites?: string[]; resources?: (string | { title?: string; url?: string })[]; status?: string;
};
type Roadmap = {
  target_role?: string; current_skills?: string[]; weekly_hours?: number; total_estimated_hours?: number;
  estimated_total_weeks?: number; roadmap?: RoadmapItem[]; note?: string;
};
type GapResult = { gaps?: { skill?: string; status?: string; [key: string]: unknown }[]; [key: string]: unknown };

const starterSkills = ["Python", "SQL", "Excel"];
const fallbackRoles = ["Data Scientist", "Data Analyst", "Data Engineer", "Machine Learning Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "AI Engineer"];

export default function Home() {
  const [roles, setRoles] = useState<Role[]>([]);
  const [role, setRole] = useState("Data Scientist");
  const [skills, setSkills] = useState<string[]>(starterSkills);
  const [skillInput, setSkillInput] = useState("");
  const [hours, setHours] = useState(10);
  const [resumeName, setResumeName] = useState("");
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [gapResult, setGapResult] = useState<GapResult | null>(null);
  const [loading, setLoading] = useState<"resume" | "roadmap" | "roles" | "gaps" | null>(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [activeTab, setActiveTab] = useState("Overview");
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetch("/api/backend/api/job-roles")
      .then(async r => { if (!r.ok) throw new Error("API unavailable"); return r.json(); })
      .then(data => {
        const list: Role[] = Array.isArray(data) ? data : (data.job_roles || data.roles || []);
        setRoles(list);
        if (list.length && !list.some(x => x.title === role)) setRole(list[0].title);
      })
      .catch(() => setNotice("API is offline — start your FastAPI backend to load live job roles."));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const roleNames = useMemo(() => {
    const names = roles.map(r => r.title).filter(Boolean);
    return (names.length ? names : fallbackRoles).filter(n => n.toLowerCase().includes(search.toLowerCase()));
  }, [roles, search]);

  const addSkill = () => {
    const value = skillInput.trim();
    if (value && !skills.some(s => s.toLowerCase() === value.toLowerCase())) setSkills(old => [...old, value]);
    setSkillInput("");
  };

  async function uploadResume(file?: File) {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith(".pdf")) { setError("Please choose a PDF resume."); return; }
    setLoading("resume"); setError(""); setNotice("");
    const form = new FormData(); form.append("file", file);
    try {
      const response = await fetch("/api/backend/api/resume/parse", { method: "POST", body: form });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Resume parsing failed.");
      const found: string[] = data.detected_skills || [];
      setResumeName(file.name);
      if (found.length) setSkills(found);
      setNotice(found.length ? `Found ${found.length} skills in ${file.name}. Review them before generating your roadmap.` : "Resume uploaded, but no skills were detected. Add them manually below.");
    } catch (e) { setError(e instanceof Error ? e.message : "Could not parse resume."); }
    finally { setLoading(null); }
  }

  async function generateRoadmap() {
    if (!role) { setError("Choose a target role first."); return; }
    setLoading("roadmap"); setError(""); setNotice("");
    try {
      const response = await fetch("/api/backend/api/roadmap/generate", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target_role: role, current_skills: skills, weekly_hours: hours })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Roadmap generation failed.");
      setRoadmap(data); setActiveTab("Roadmap");
    } catch (e) { setError(e instanceof Error ? e.message : "Could not generate roadmap."); }
    finally { setLoading(null); }
  }

  async function analyzeGaps() {
    setLoading("gaps"); setError(""); setNotice("");
    try {
      const response = await fetch("/api/backend/api/skills/gaps", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          student: { name: "Student", education: null, skills: skills.map(name => ({ name, level: "beginner" })), projects: [], weekly_hours: hours },
          job: { title: role, requirements: (roles.find(r => r.title === role)?.required_skills || []).map(skill => ({ skill, importance: "required", required_level: "intermediate" })) }
        })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Skill-gap analysis failed.");
      setGapResult(data); setActiveTab("Skill gap");
    } catch (e) { setError(e instanceof Error ? e.message : "Could not analyze skills."); }
    finally { setLoading(null); }
  }

  const items = roadmap?.roadmap || [];
  const complete = items.filter(i => i.status?.toLowerCase() === "completed").length;
  const progress = items.length ? Math.round(complete / items.length * 100) : 0;

  return (
    <main className="shell">
      <aside className="sidebar">
        <a className="brand" href="#"><span className="brand-mark"><Sparkles size={19}/></span><span>skillforge<span className="brand-dot">.</span><small>CAREER INTELLIGENCE</small></span></a>
        <div className="workspace"><div className="workspace-icon">S</div><div><strong>Student workspace</strong><small>Personal learning space</small></div><ChevronDown size={15}/></div>
        <p className="nav-label">WORKSPACE</p>
        {[
          ["Overview", LayoutDashboard], ["Roadmap", Compass], ["Skill gap", Target], ["Resume", FileText]
        ].map(([label, Icon]) => {
          const I = Icon as typeof LayoutDashboard;
          return <button key={label as string} className={`nav-item ${activeTab === label ? "selected" : ""}`} onClick={() => setActiveTab(label as string)}><I size={17}/>{label as string}{label === "Roadmap" && roadmap && <span className="nav-count">{items.length}</span>}</button>;
        })}
        <p className="nav-label nav-spaced">YOUR PROGRESS</p>
        <div className="sidebar-progress"><div className="progress-row"><span>Learning journey</span><b>{progress}%</b></div><div className="progress-track"><span style={{ width: `${progress}%` }}/></div><small>{complete} of {items.length} milestones completed</small></div>
        <div className="sidebar-bottom"><button className="nav-item" onClick={() => setNotice("Settings are coming soon.")}><Settings2 size={17}/>Settings</button><button className="nav-item" onClick={() => setNotice("Need help? Check that your FastAPI server is running on port 8000.")}><CircleHelp size={17}/>Help & support</button><div className="profile"><div className="avatar">S</div><div><strong>Your profile</strong><small>Career explorer</small></div><ChevronDown size={15}/></div></div>
      </aside>

      <section className="main-area">
        <header className="topbar"><div className="breadcrumb">Workspace <span>/</span> <b>{activeTab}</b></div><div className="top-actions"><span className="api-status"><i/> API-connected UI</span><button className="icon-button" aria-label="Search" onClick={() => document.getElementById("role-search")?.focus()}><Search size={17}/></button><button className="avatar small-avatar" title="Profile">S</button><button className="mobile-menu" aria-label="Menu"><Menu size={20}/></button></div></header>
        <div className="content">
          <div className="welcome-row"><div><div className="eyebrow"><span className="eyebrow-dot"/> YOUR NEXT CHAPTER STARTS HERE</div><h1>Build skills. <span>Build your future.</span></h1><p className="subtitle">A learning path designed around where you are — and where you want to go.</p></div><div className="date-chip"><Sparkles size={15}/> Your career, in focus</div></div>
          {(error || notice) && <div className={`message ${error ? "error" : ""}`}><span>{error || notice}</span><button onClick={() => {setError("");setNotice("");}} aria-label="Dismiss"><X size={15}/></button></div>}

          <div className="hero-card"><div className="hero-copy"><div className="pill"><Zap size={13}/> PERSONALIZED CAREER PLAN</div><h2>Turn your ambition<br/>into a <em>clear direction.</em></h2><p>Tell us what you know, choose your target role, and get a structured roadmap you can actually follow.</p><button className="primary-button" onClick={() => document.getElementById("plan-builder")?.scrollIntoView({behavior:"smooth"})}>Build my roadmap <ArrowRight size={16}/></button><div className="hero-proof"><span><ShieldCheck size={14}/> Built around your skills</span><span><Clock3 size={14}/> Fits your schedule</span></div></div><div className="hero-art" aria-hidden="true"><div className="orbit orbit-one"/><div className="orbit orbit-two"/><div className="orbit orbit-three"/><div className="art-core"><Rocket size={42}/></div><div className="float-card float-one"><span className="float-icon green"><Check size={14}/></span><span><b>Clear milestones</b><small>One step at a time</small></span></div><div className="float-card float-two"><span className="float-icon purple"><Activity size={14}/></span><span><b>Skills that matter</b><small>Aligned to your goal</small></span></div><div className="art-spark spark-a">✦</div><div className="art-spark spark-b">✧</div></div></div>

          <div className="section-heading"><div><h2>Your learning overview</h2><p>Your starting point for a focused career journey.</p></div><span className="live-badge"><span/> LIVE WORKSPACE</span></div>
          <div className="stats-grid">
            <Stat icon={<Target size={18}/>} label="Target role" value={role || "Not selected"} note="Your next destination" tone="green"/>
            <Stat icon={<Code2 size={18}/>} label="Current skills" value={String(skills.length)} note="Skills in your profile" tone="purple"/>
            <Stat icon={<Clock3 size={18}/>} label="Weekly commitment" value={`${hours} hrs`} note="Time set aside to learn" tone="orange"/>
            <Stat icon={<Flame size={18}/>} label="Roadmap progress" value={`${progress}%`} note={roadmap ? `${items.length} learning milestones` : "Generate your first roadmap"} tone="blue"/>
          </div>

          <div className="builder-grid" id="plan-builder">
            <section className="panel plan-panel"><div className="panel-heading"><div className="panel-icon"><Compass size={18}/></div><div><h3>Build your learning plan</h3><p>Start with your career goal and current skills.</p></div><span className="step-tag">STEP 01</span></div>
              <label className="field-label" htmlFor="role-search">What role are you aiming for?</label><div className="role-search"><Search size={16}/><input id="role-search" value={search} onChange={e => setSearch(e.target.value)} placeholder="Search careers, e.g. Data Scientist"/></div>
              <div className="role-list">{roleNames.slice(0,6).map(name => <button key={name} onClick={() => setRole(name)} className={`role-option ${role === name ? "role-active" : ""}`}><span className="role-symbol"><BriefcaseBusiness size={16}/></span><span>{name}</span>{role === name ? <span className="radio-on"><Check size={12}/></span> : <span className="radio-off"/>}</button>)}</div>
              <div className="field-divider"/><div className="hours-row"><div><label className="field-label" htmlFor="hours">Time available each week</label><p>Make it realistic. Consistency wins.</p></div><div className="hours-value">{hours}<small> hrs/wk</small></div></div><input id="hours" className="range" type="range" min="2" max="30" step="1" value={hours} onChange={e => setHours(Number(e.target.value))}/><div className="range-labels"><span>2 hours</span><span>30 hours</span></div>
              <button className="primary-button full-button" onClick={generateRoadmap} disabled={loading !== null}>{loading === "roadmap" ? <><LoaderCircle className="spin" size={16}/> Building your roadmap…</> : <>Generate my roadmap <ArrowRight size={16}/></>}</button>
            </section>

            <section className="panel skills-panel"><div className="panel-heading"><div className="panel-icon purple-bg"><GraduationCap size={18}/></div><div><h3>Your current skills</h3><p>Start with what you already know.</p></div><span className="step-tag">STEP 02</span></div>
              <label className="upload-box" htmlFor="resume-file"><span className="upload-icon"><UploadCloud size={20}/></span><span><b>{loading === "resume" ? "Reading your resume…" : "Upload your resume"}</b><small>{resumeName || "PDF format · We’ll extract skills for you"}</small></span>{loading === "resume" ? <LoaderCircle className="spin" size={17}/> : <ArrowUpRight size={17}/>}<input id="resume-file" type="file" accept=".pdf,application/pdf" onChange={e => uploadResume(e.target.files?.[0])} hidden/></label>
              <div className="skills-subhead"><span>YOUR SKILL SET <b>{skills.length}</b></span><span className="editable">EDITABLE</span></div>
              <div className="skill-chips">{skills.map(skill => <span className="skill-chip" key={skill}>{skill}<button onClick={() => setSkills(old => old.filter(s => s !== skill))} aria-label={`Remove ${skill}`}><X size={12}/></button></span>)}</div>
              <form className="add-skill" onSubmit={e => {e.preventDefault();addSkill();}}><input value={skillInput} onChange={e => setSkillInput(e.target.value)} placeholder="Add a skill, e.g. Pandas"/><button type="submit" aria-label="Add skill"><Plus size={16}/></button></form>
              <div className="skills-tip"><Sparkles size={15}/><p><b>Make it yours.</b> Remove skills you’re unfamiliar with and add the ones you’ve practiced.</p></div>
              <button className="secondary-button full-button" onClick={analyzeGaps} disabled={loading !== null}>{loading === "gaps" ? <><LoaderCircle className="spin" size={16}/> Analyzing skills…</> : <>Analyze my skill gap <ArrowRight size={16}/></>}</button>
            </section>
          </div>

          <div className="bottom-grid">
            <section className="panel roadmap-panel"><div className="section-inline"><div><h3>{activeTab === "Skill gap" ? "Skill-gap analysis" : "Your learning roadmap"}</h3><p>{activeTab === "Skill gap" ? "See what to focus on for your target role." : "Your next milestones, organized into a clear path."}</p></div><span className="subtle-tag">{roadmap ? `${items.length} MILESTONES` : "READY WHEN YOU ARE"}</span></div>
              {activeTab === "Skill gap" && gapResult ? <pre className="gap-output">{JSON.stringify(gapResult, null, 2)}</pre> : roadmap && items.length ? <div className="timeline">{items.map((item, index) => <div className="timeline-item" key={`${item.skill}-${index}`}><div className={`timeline-node ${item.status?.toLowerCase() === "completed" ? "node-done" : ""}`}>{item.status?.toLowerCase() === "completed" ? <Check size={13}/> : String(index + 1).padStart(2,"0")}</div><div className="timeline-body"><div className="timeline-title"><b>{item.skill}</b><span>{item.estimated_hours ?? "—"} hrs</span></div><p>{item.prerequisites?.length ? `Build on: ${item.prerequisites.join(", ")}` : "Build a strong foundation and practice with a small project."}</p>{item.resources?.length ? <div className="resource-list">{item.resources.map((r, i) => {const title = typeof r === "string" ? r : r.title || r.url || "Learning resource";const url = typeof r === "string" ? "" : r.url || "";return url ? <a key={i} href={url} target="_blank" rel="noreferrer">{title} <ArrowUpRight size={12}/></a> : <span key={i}>{title}</span>;})}</div> : null}</div></div>)}</div> : <div className="empty-state"><span className="empty-icon"><BookOpen size={23}/></span><b>Your roadmap will appear here</b><p>Choose your target role, review your skills, then generate a plan tailored to your weekly schedule.</p><button className="text-button" onClick={generateRoadmap}>Create my first roadmap <ArrowRight size={14}/></button></div>}
              {roadmap?.note && <p className="roadmap-note">{roadmap.note}</p>}
            </section>
            <section className="panel focus-panel"><div className="section-inline"><div><h3>Learning snapshot</h3><p>A quick view of your plan.</p></div><span className="snapshot-icon"><Activity size={17}/></span></div><div className="snapshot-hero"><div className="snapshot-ring"><span>{progress}%</span></div><div><b>{roadmap ? "Your journey is mapped" : "Your journey starts here"}</b><p>{roadmap ? "Keep showing up, one milestone at a time." : "Generate a roadmap to see your learning progress."}</p></div></div><div className="snapshot-stat"><span><Clock3 size={15}/> Estimated learning time</span><b>{roadmap ? `${roadmap.total_estimated_hours ?? "—"} hrs` : "—"}</b></div><div className="snapshot-stat"><span><CalendarIcon/> Estimated duration</span><b>{roadmap ? `${roadmap.estimated_total_weeks ?? "—"} weeks` : "—"}</b></div><div className="snapshot-stat"><span><Check size={15}/> Milestones completed</span><b>{complete} / {items.length}</b></div><div className="focus-note"><Sparkles size={15}/><span>Small steps, steady progress. Your schedule is built around the time you choose.</span></div></section>
          </div>
          <footer><a className="footer-brand" href="#"><Sparkles size={14}/> skillforge.</a><span>Make your next move count.</span><span className="footer-right">Built for curious minds <span>✦</span></span></footer>
        </div>
      </section>
    </main>
  );
}

function Stat({icon,label,value,note,tone}:{icon:React.ReactNode;label:string;value:string;note:string;tone:string}) {
  return <div className="stat-card"><div className={`stat-icon ${tone}`}>{icon}</div><div className="stat-label">{label}</div><div className="stat-value">{value}</div><div className="stat-note">{note}</div></div>;
}
function CalendarIcon(){return <Clock3 size={15}/>;}