import React from 'react';
import { BehaviorFinding } from '../types';
import { Compass, CheckCircle2, AlertTriangle, Info } from 'lucide-react';

interface BehaviorFindingsProps {
  findings: BehaviorFinding[];
}

export const BehaviorFindings: React.FC<BehaviorFindingsProps> = ({ findings }) => {
  if (!findings || findings.length === 0) return null;

  return (
    <div className="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-6 mb-8">
      <div className="flex items-center space-x-2 mb-4">
        <Compass className="w-5 h-5 text-indigo-400" />
        <h3 className="font-semibold text-slate-100 text-sm">Financial Behavior &amp; Spending Habits</h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {findings.map((item) => {
          const isPositive = item.severity === 'positive';
          const isWarning = item.severity === 'warning';

          const icon = isPositive ? (
            <CheckCircle2 className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
          ) : isWarning ? (
            <AlertTriangle className="w-4 h-4 text-amber-400 mt-0.5 flex-shrink-0" />
          ) : (
            <Info className="w-4 h-4 text-indigo-400 mt-0.5 flex-shrink-0" />
          );

          const borderColor = isPositive
            ? 'border-emerald-500/30 bg-emerald-950/20'
            : isWarning
            ? 'border-amber-500/30 bg-amber-950/20'
            : 'border-slate-700 bg-slate-800/80';

          return (
            <div
              key={item.id}
              className={`p-4 rounded-xl border ${borderColor} transition-all space-y-2 flex flex-col justify-between`}
            >
              <div className="flex items-start space-x-2.5">
                {icon}
                <div>
                  <h4 className="text-xs font-semibold text-slate-200">{item.title}</h4>
                  <p className="text-xs text-slate-400 mt-1 leading-relaxed">{item.description}</p>
                </div>
              </div>

              {item.metric && (
                <div className="pt-2 flex justify-end">
                  <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-slate-800 border border-slate-700 text-slate-300">
                    {item.metric}
                  </span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

