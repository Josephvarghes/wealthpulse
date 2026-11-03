import React from 'react';
import { UnusualExpense, Currency } from '../types';
import { formatCurrency } from '../utils/formatters';
import { AlertCircle, Calendar } from 'lucide-react';

interface UnusualExpensesListProps {
  expenses: UnusualExpense[];
  currency: Currency;
}

export const UnusualExpensesList: React.FC<UnusualExpensesListProps> = ({ expenses, currency }) => {
  if (!expenses || expenses.length === 0) return null;

  return (
    <div className="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-6 mb-8">
      <div className="flex items-center space-x-2 mb-4">
        <AlertCircle className="w-5 h-5 text-rose-400" />
        <h3 className="font-semibold text-slate-100 text-sm">Unusual Transactions &amp; Outliers Detected</h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {expenses.map((item, idx) => (
          <div
            key={idx}
            className="p-4 rounded-xl border border-rose-500/20 bg-rose-950/10 flex items-start justify-between gap-3"
          >
            <div className="space-y-1">
              <div className="flex items-center space-x-2 text-[11px] text-slate-400">
                <span className="flex items-center space-x-1">
                  <Calendar className="w-3 h-3 text-slate-500" />
                  <span>{item.date}</span>
                </span>
                <span>•</span>
                <span className="text-rose-400 font-medium">{item.category}</span>
              </div>
              <div className="font-semibold text-slate-200 text-xs">{item.description}</div>
              <p className="text-[11px] text-rose-300/80">{item.reason}</p>
            </div>

            <div className="text-right flex-shrink-0">
              <span className="text-sm font-bold text-rose-400">
                {formatCurrency(item.amount, currency)}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

