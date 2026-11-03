import React from 'react';
import { Calendar, Filter, ChevronDown, Check } from 'lucide-react';

interface DateRangeSelectorProps {
  availableMonths: string[];
  selectedMonth: string;
  onSelectMonth: (month: string) => void;
  isLoading: boolean;
  totalRows?: number;
  filteredRows?: number;
}

export const formatMonthLabel = (monthStr: string): string => {
  if (!monthStr || monthStr === 'all') return 'All Time';
  const parts = monthStr.split('-');
  if (parts.length === 2) {
    const year = parts[0];
    const month = parseInt(parts[1], 10);
    const date = new Date(parseInt(year, 10), month - 1, 1);
    if (!isNaN(date.getTime())) {
      return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
    }
  }
  return monthStr;
};

export const DateRangeSelector: React.FC<DateRangeSelectorProps> = ({
  availableMonths,
  selectedMonth,
  onSelectMonth,
  isLoading,
  totalRows,
  filteredRows,
}) => {
  if (!availableMonths || availableMonths.length === 0) {
    return null;
  }

  const isFiltered = selectedMonth !== 'all';

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 mb-8 shadow-lg shadow-black/20 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
      {/* Label and Status */}
      <div className="flex items-center space-x-3">
        <div className="w-9 h-9 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center">
          <Calendar className="w-4 h-4" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-semibold text-slate-200 uppercase tracking-wider">Analysis Period</span>
            {isFiltered ? (
              <span className="text-[10px] bg-amber-500/10 text-amber-300 font-medium px-2 py-0.5 rounded-full border border-amber-500/20 flex items-center space-x-1">
                <Filter className="w-2.5 h-2.5 mr-0.5" />
                <span>Filtered View</span>
              </span>
            ) : (
              <span className="text-[10px] bg-slate-800 text-slate-400 font-medium px-2 py-0.5 rounded-full border border-slate-700">
                Full Dataset
              </span>
            )}
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            {isFiltered
              ? `Displaying ${filteredRows ?? 0} transactions for ${formatMonthLabel(selectedMonth)} (of ${totalRows ?? 0} total)`
              : `Aggregating ${totalRows ?? 0} transactions across ${availableMonths.length} month${availableMonths.length > 1 ? 's' : ''}`}
          </p>
        </div>
      </div>

      {/* Month Pill / Button Options */}
      <div className="flex flex-wrap items-center gap-1.5 w-full md:w-auto">
        <button
          onClick={() => onSelectMonth('all')}
          disabled={isLoading}
          className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
            selectedMonth === 'all'
              ? 'bg-indigo-600 text-white shadow-sm shadow-indigo-600/30'
              : 'bg-slate-800/80 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-700/60'
          } ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
        >
          {selectedMonth === 'all' && <Check className="w-3.5 h-3.5" />}
          <span>All Time</span>
        </button>

        {availableMonths.map((m) => {
          const isSelected = selectedMonth === m;
          return (
            <button
              key={m}
              onClick={() => onSelectMonth(m)}
              disabled={isLoading}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                isSelected
                  ? 'bg-indigo-600 text-white shadow-sm shadow-indigo-600/30'
                  : 'bg-slate-800/80 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-700/60'
              } ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
            >
              {isSelected && <Check className="w-3.5 h-3.5" />}
              <span>{formatMonthLabel(m)}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};

