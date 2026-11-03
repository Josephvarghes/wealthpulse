import React, { useState } from 'react';
import { TimeAnalysis, Currency } from '../types';
import { formatCurrency } from '../utils/formatters';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';
import { LineChart as ChartIcon, Calendar } from 'lucide-react';

interface TrendsChartProps {
  timeAnalysis: TimeAnalysis;
  currency: Currency;
}

type PeriodType = 'daily' | 'weekly' | 'monthly';

export const TrendsChart: React.FC<TrendsChartProps> = ({ timeAnalysis, currency }) => {
  const [period, setPeriod] = useState<PeriodType>('daily');

  const currentData =
    period === 'daily'
      ? timeAnalysis.daily
      : period === 'weekly'
      ? timeAnalysis.weekly
      : timeAnalysis.monthly;

  return (
    <div className="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-6">
        <div className="flex items-center space-x-2">
          <ChartIcon className="w-5 h-5 text-indigo-400" />
          <h3 className="font-semibold text-slate-100 text-sm">Spending Timeline &amp; Cash Flow</h3>
        </div>

        {/* Period Switcher */}
        <div className="flex items-center bg-slate-800 rounded-lg p-0.5 border border-slate-700 text-xs">
          <button
            onClick={() => setPeriod('daily')}
            className={`px-3 py-1 rounded-md font-medium transition-all ${
              period === 'daily'
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Daily
          </button>
          <button
            onClick={() => setPeriod('weekly')}
            className={`px-3 py-1 rounded-md font-medium transition-all ${
              period === 'weekly'
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Weekly
          </button>
          <button
            onClick={() => setPeriod('monthly')}
            className={`px-3 py-1 rounded-md font-medium transition-all ${
              period === 'monthly'
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Monthly
          </button>
        </div>
      </div>

      <div className="h-64 w-full">
        {currentData.length === 0 ? (
          <div className="h-full flex items-center justify-center text-xs text-slate-400">
            No timeline data for selected period.
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={currentData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="expenseGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.35} />
                  <stop offset="95%" stopColor="#f43f5e" stopOpacity={0.0} />
                </linearGradient>
                <linearGradient id="incomeGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.35} />
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.5} />
              <XAxis
                dataKey="period"
                stroke="#64748b"
                fontSize={11}
                tickLine={false}
              />
              <YAxis
                stroke="#64748b"
                fontSize={11}
                tickLine={false}
                tickFormatter={(val) => `${val >= 1000 ? `${(val / 1000).toFixed(0)}k` : val}`}
              />
              <Tooltip
                content={({ active, payload, label }) => {
                  if (active && payload && payload.length) {
                    const exp = payload.find((p) => p.dataKey === 'expenses')?.value as number || 0;
                    const inc = payload.find((p) => p.dataKey === 'income')?.value as number || 0;
                    return (
                      <div className="bg-slate-900 border border-slate-700 p-3 rounded-xl shadow-xl text-xs space-y-1">
                        <div className="font-semibold text-slate-300 flex items-center space-x-1.5">
                          <Calendar className="w-3.5 h-3.5 text-indigo-400" />
                          <span>{label}</span>
                        </div>
                        <div className="text-rose-400 font-medium">
                          Expenses: {formatCurrency(exp, currency)}
                        </div>
                        {inc > 0 && (
                          <div className="text-emerald-400 font-medium">
                            Income: {formatCurrency(inc, currency)}
                          </div>
                        )}
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Area
                type="monotone"
                dataKey="expenses"
                stroke="#f43f5e"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#expenseGradient)"
                name="Expenses"
              />
              {currentData.some((d) => d.income > 0) && (
                <Area
                  type="monotone"
                  dataKey="income"
                  stroke="#10b981"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#incomeGradient)"
                  name="Income"
                />
              )}
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
};

