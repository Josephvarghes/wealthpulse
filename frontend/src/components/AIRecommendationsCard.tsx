import React from 'react';
import { AIRecommendation } from '../types';
import { Bot, Lightbulb, CheckCircle2, AlertOctagon, Target, ArrowRightCircle } from 'lucide-react';

interface AIRecommendationsCardProps {
  recommendation?: AIRecommendation;
}

export const AIRecommendationsCard: React.FC<AIRecommendationsCardProps> = ({ recommendation }) => {
  if (!recommendation) return null;

  return (
    <div className="bg-gradient-to-br from-indigo-950/40 via-slate-800/80 to-purple-950/30 border border-indigo-500/30 rounded-2xl p-6 md:p-8 mb-8 shadow-xl shadow-indigo-950/30">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-6 pb-4 border-b border-indigo-500/20">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center text-white shadow-md shadow-indigo-500/30">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white tracking-tight">AI Financial Intelligence &amp; Advisory</h3>
            <p className="text-xs text-indigo-300">Explains calculated behavior without modifying numbers</p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <span className="text-[11px] px-2.5 py-1 rounded-full bg-indigo-500/20 text-indigo-300 font-medium border border-indigo-500/30 flex items-center space-x-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse" />
            <span>Engine: {recommendation.provider_used}</span>
          </span>
          {recommendation.is_fallback && (
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
              Offline Safeguard
            </span>
          )}
        </div>
      </div>

      {/* Summary Banner */}
      <div className="bg-slate-900/60 rounded-xl p-4 border border-indigo-500/20 mb-6">
        <p className="text-xs text-slate-300 leading-relaxed font-medium">
          "{recommendation.ai_financial_summary}"
        </p>
      </div>

      {/* Grid of 5 Insights */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Key Observation */}
        <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-700/60 space-y-1.5">
          <div className="flex items-center space-x-2 text-indigo-400">
            <Lightbulb className="w-4 h-4" />
            <span className="text-xs font-semibold uppercase tracking-wider">Key Observation</span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">{recommendation.key_observation}</p>
        </div>

        {/* Positive Behavior */}
        <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-700/60 space-y-1.5">
          <div className="flex items-center space-x-2 text-emerald-400">
            <CheckCircle2 className="w-4 h-4" />
            <span className="text-xs font-semibold uppercase tracking-wider">Positive Discipline</span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">{recommendation.positive_behavior}</p>
        </div>

        {/* Main Concern */}
        <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-700/60 space-y-1.5">
          <div className="flex items-center space-x-2 text-rose-400">
            <AlertOctagon className="w-4 h-4" />
            <span className="text-xs font-semibold uppercase tracking-wider">Primary Concern</span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">{recommendation.main_concern}</p>
        </div>

        {/* Practical Recommendation */}
        <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-700/60 space-y-1.5">
          <div className="flex items-center space-x-2 text-amber-400">
            <Target className="w-4 h-4" />
            <span className="text-xs font-semibold uppercase tracking-wider">Practical Advice</span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">{recommendation.practical_recommendation}</p>
        </div>
      </div>

      {/* Immediate Next Action Highlight */}
      <div className="mt-4 p-4 rounded-xl bg-gradient-to-r from-indigo-900/40 to-violet-900/40 border border-indigo-500/30 flex items-start space-x-3">
        <ArrowRightCircle className="w-5 h-5 text-indigo-400 mt-0.5 flex-shrink-0" />
        <div>
          <span className="text-xs font-bold text-indigo-200 uppercase tracking-wider">Recommended Next Action: </span>
          <span className="text-xs text-slate-200">{recommendation.short_term_action}</span>
        </div>
      </div>
    </div>
  );
};

