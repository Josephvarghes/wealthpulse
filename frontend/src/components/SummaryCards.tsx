import React from 'react';
import { FinancialSummary, Currency } from '../types';
import { formatCurrency } from '../utils/formatters';
import { TrendingUp, TrendingDown, Wallet, Percent, ArrowUpRight, Activity } from 'lucide-react';

interface SummaryCardsProps {
  summary: FinancialSummary;
  currency: Currency;
}

export const SummaryCards: React.FC<SummaryCardsProps> = ({ summary, currency }) => {
  const isPositiveSavings = summary.savings >= 0;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      {/* Total Income */}
      <div className="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-5 hover:border-slate-600 transition-all">
        <div className="flex items-center justify-between text-slate-400 mb-2">
          <span className="text-xs font-medium uppercase tracking-wider">Total Income</span>
          <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
            <TrendingUp className="w-4 h-4" />
          </div>
        </div>
        <div className="text-2xl font-bold text-white tracking-tight">
          {formatCurrency(summary.total_income, currency)}
        </div>
        <div className="mt-2 text-xs text-slate-400 flex items-center">
          <span className="text-emerald-400 font-medium">Inflows recorded</span>
        </div>
      </div>

      {/* Total Expenses */}
      <div className="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-5 hover:border-slate-600 transition-all">
        <div className="flex items-center justify-between text-slate-400 mb-2">
          <span className="text-xs font-medium uppercase tracking-wider">Total Expenses</span>
          <div className="w-8 h-8 rounded-lg bg-rose-500/10 text-rose-400 flex items-center justify-center">
            <TrendingDown className="w-4 h-4" />
          </div>
        </div>
        <div className="text-2xl font-bold text-white tracking-tight">
          {formatCurrency(summary.total_expenses, currency)}
        </div>
        <div className="mt-2 text-xs text-slate-400 flex items-center justify-between">
          <span>Avg: {formatCurrency(summary.average_transaction, currency)}/tx</span>
          <span>Max: {formatCurrency(summary.highest_transaction, currency)}</span>
        </div>
      </div>

      {/* Net Balance / Savings */}
      <div className="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-5 hover:border-slate-600 transition-all">
        <div className="flex items-center justify-between text-slate-400 mb-2">
          <span className="text-xs font-medium uppercase tracking-wider">Net Savings</span>
          <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
            isPositiveSavings ? 'bg-indigo-500/10 text-indigo-400' : 'bg-amber-500/10 text-amber-400'
          }`}>
            <Wallet className="w-4 h-4" />
          </div>
        </div>
        <div className={`text-2xl font-bold tracking-tight ${
          isPositiveSavings ? 'text-indigo-300' : 'text-amber-400'
        }`}>
          {formatCurrency(summary.savings, currency)}
        </div>
        <div className="mt-2 text-xs text-slate-400">
          <span>{summary.transaction_count} total transactions analyzed</span>
        </div>
      </div>

      {/* Savings Rate */}
      <div className="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-5 hover:border-slate-600 transition-all">
        <div className="flex items-center justify-between text-slate-400 mb-2">
          <span className="text-xs font-medium uppercase tracking-wider">Savings Rate</span>
          <div className="w-8 h-8 rounded-lg bg-violet-500/10 text-violet-400 flex items-center justify-center">
            <Percent className="w-4 h-4" />
          </div>
        </div>
        <div className="flex items-baseline space-x-2">
          <span className="text-2xl font-bold text-white tracking-tight">
            {summary.savings_rate.toFixed(1)}%
          </span>
          <span className="text-xs text-slate-400">
            {summary.total_income > 0 ? (summary.savings_rate >= 20 ? 'Optimal' : 'Low') : 'No income logged'}
          </span>
        </div>
        {/* Progress bar */}
        <div className="mt-3 w-full bg-slate-700/60 rounded-full h-1.5 overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-500 ${
              summary.savings_rate >= 20
                ? 'bg-gradient-to-r from-emerald-500 to-indigo-500'
                : 'bg-amber-500'
            }`}
            style={{ width: `${Math.min(Math.max(summary.savings_rate, 0), 100)}%` }}
          />
        </div>
      </div>
    </div>
  );
};

