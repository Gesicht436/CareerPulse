import React from 'react';
import { ShieldCheck, Upload, LineChart, BrainCircuit } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      {/* --- Navbar --- */}
      <nav className="bg-white border-b border-slate-200 px-6 py-4 flex justify-between items-center sticky top-0 z-50">
        <div className="flex items-center gap-2">
          <div className="bg-indigo-600 p-2 rounded-lg">
            <BrainCircuit className="text-white w-6 h-6" />
          </div>
          <span className="text-xl font-bold tracking-tight">CareerPulse</span>
        </div>
        <div className="flex gap-6 text-sm font-medium text-slate-600">
          <a href="#" className="hover:text-indigo-600 transition-colors">Dashboard</a>
          <a href="#" className="hover:text-indigo-600 transition-colors">Skill Gap</a>
          <a href="#" className="hover:text-indigo-600 transition-colors">Security Audit</a>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-12">
        {/* --- Hero Section --- */}
        <section className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-extrabold mb-4 tracking-tight">
            Adversarial-Robust <span className="text-indigo-600">ATS Simulator</span>
          </h1>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Bridge the gap between your skills and market demand with security-first AI matching and privacy-protected analysis.
          </p>
        </section>

        {/* --- Quick Action Cards --- */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow group">
            <div className="bg-indigo-50 w-12 h-12 rounded-xl flex items-center justify-center mb-6 group-hover:bg-indigo-100 transition-colors">
              <Upload className="text-indigo-600 w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold mb-2">Secure Upload</h3>
            <p className="text-slate-500 text-sm leading-relaxed">
              Upload your resume with local PII redaction. Your data stays private before it ever hits our servers.
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow group">
            <div className="bg-emerald-50 w-12 h-12 rounded-xl flex items-center justify-center mb-6 group-hover:bg-emerald-100 transition-colors">
              <ShieldCheck className="text-emerald-600 w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold mb-2">Adversarial Defense</h3>
            <p className="text-slate-500 text-sm leading-relaxed">
              We detect "Resume Smuggling," white-on-white text, and prompt injection to ensure fair matching.
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow group">
            <div className="bg-amber-50 w-12 h-12 rounded-xl flex items-center justify-center mb-6 group-hover:bg-amber-100 transition-colors">
              <LineChart className="text-amber-600 w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold mb-2">Skill Analysis</h3>
            <p className="text-slate-500 text-sm leading-relaxed">
              Get an explainable breakdown of your readiness score and actionable paths to fill your skill gaps.
            </p>
          </div>
        </div>

        {/* --- Placeholder for Main Feature --- */}
        <div className="bg-indigo-600 rounded-3xl p-12 text-center text-white relative overflow-hidden shadow-xl">
          <div className="relative z-10">
            <h2 className="text-3xl font-bold mb-6">Ready to check your Career Pulse?</h2>
            <button className="bg-white text-indigo-600 px-8 py-3 rounded-full font-bold hover:bg-slate-50 transition-colors shadow-lg">
              Get Started Now
            </button>
          </div>
          {/* Decorative background circle */}
          <div className="absolute -top-24 -right-24 w-64 h-64 bg-indigo-500 rounded-full opacity-20 blur-3xl"></div>
          <div className="absolute -bottom-24 -left-24 w-64 h-64 bg-indigo-500 rounded-full opacity-20 blur-3xl"></div>
        </div>
      </main>

      <footer className="border-t border-slate-200 py-8 text-center text-slate-400 text-sm">
        <p>&copy; 2026 CareerPulse - Capstone Project IIT Patna</p>
      </footer>
    </div>
  );
}
