import React from 'react';
import { CategoryItem, Currency } from '../types';
import { formatCurrency } from '../utils/formatters';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts';
import { PieChart as PieIcon } from 'lucide-react';

interface CategoryChartProps {
  categories: CategoryItem[];
  currency: Currency;
}

const COLORS = [
  '#6366f1', // Indigo
  '#ec4899', // Pink
  '#10b981', // Emerald
  '#f59e0b', // Amber
  '#8b5cf6', // Violet
  '#06b6d4', // Cyan
  '#f43f5e', // Rose
  '#84cc16', // Lime
];

export const CategoryChart: React.FC<CategoryChartProps> = ({ categories, currency }) => {
  if (!categories || categories.length === 0) {
    return (
      <div className="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-6 text-center text-slate-400">
        No category data available.
      </div>
    );
  }

  const chartData = categories.map((cat, idx) => ({
    name: cat.category,
    value: cat.total_amount,
    pct: cat.percentage_of_total_expenses,
    color: COLORS[idx % COLORS.length],
  }));

  return (
    <div className="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <PieIcon className="w-5 h-5 text-indigo-400" />
          <h3 className="font-semibold text-slate-100 text-sm">Expenses by Category</h3>
        </div>
        <span className="text-xs text-slate-400">{categories.length} Categories</span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        {/* Donut Chart */}
        <div className="lg:col-span-5 h-56 relative flex items-center justify-center">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={85}
                paddingAngle={4}
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="bg-slate-900 border border-slate-700 p-2.5 rounded-xl shadow-xl text-xs">
                        <div className="font-semibold text-white">{data.name}</div>
                        <div className="text-indigo-400 font-medium mt-0.5">
                          {formatCurrency(data.value, currency)} ({data.pct}%)
                        </div>
                      </div>
                    );
                  }
                  return null;
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Categories List Breakdown */}
        <div className="lg:col-span-7 space-y-3">
          {categories.map((cat, idx) => {
            const color = COLORS[idx % COLORS.length];
            return (
              <div key={cat.category} className="space-y-1">
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center space-x-2">
                    <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: color }} />
                    <span className="font-medium text-slate-200">{cat.category}</span>
                    <span className="text-slate-500">({cat.transaction_count} txs)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="font-semibold text-slate-100">{formatCurrency(cat.total_amount, currency)}</span>
                    <span className="text-slate-400 w-12 text-right">{cat.percentage_of_total_expenses.toFixed(1)}%</span>
                  </div>
                </div>
                {/* Visual bar */}
                <div className="w-full bg-slate-700/40 rounded-full h-1.5 overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-300"
                    style={{
                      width: `${Math.min(cat.percentage_of_total_expenses, 100)}%`,
                      backgroundColor: color,
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

