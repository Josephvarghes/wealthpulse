import React from 'react';
import { RuleRecommendation } from '../types';
import { ShieldAlert, Zap, ArrowRight } from 'lucide-react';

interface RuleRecommendationsProps {
  recommendations: RuleRecommendation[];
}

export const RuleRecommendations: React.FC<RuleRecommendationsProps> = ({ recommendations }) => {
  if (!recommendations || recommendations.length === 0) return null;

  return (
    <div className="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-6 mb-8">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Zap className="w-5 h-5 text-amber-400" />
          <h3 className="font-semibold text-slate-100 text-sm">Deterministic Rule Recommendations</h3>
        </div>
        <span className="text-xs text-slate-400">Rule-engine generated</span>
      </div>

      <div className="space-y-3">
        {recommendations.map((rec) => {
          const isHigh = rec.priority === 'high';
          const isMedium = rec.priority === 'medium';

          const priorityBadgeClass = isHigh
            ? 'bg-rose-500/10 text-rose-300 border-rose-500/30'
            : isMedium
            ? 'bg-amber-500/10 text-amber-300 border-amber-500/30'
            : 'bg-indigo-500/10 text-indigo-300 border-indigo-500/30';

          return (
            <div
              key={rec.id}
              className="p-4 rounded-xl border border-slate-700/80 bg-slate-800/80 hover:border-slate-600 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3"
            >
              <div className="space-y-1">
                <div className="flex items-center space-x-2">
                  <span className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full border ${priorityBadgeClass}`}>
                    {rec.priority} Priority
                  </span>
                  <span className="text-xs text-indigo-400 font-medium">{rec.category}</span>
                </div>
                <h4 className="text-xs font-semibold text-slate-100">{rec.title}</h4>
                <p className="text-xs text-slate-400 leading-relaxed">{rec.message}</p>
              </div>

              <div className="flex-shrink-0 self-start sm:self-center">
                <div className="p-2 rounded-lg bg-slate-700/50 text-slate-300">
                  <ArrowRight className="w-4 h-4" />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

