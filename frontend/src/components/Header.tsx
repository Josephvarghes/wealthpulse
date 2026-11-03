import React from 'react';
import { Currency } from '../types';
import { Sparkles, IndianRupee, DollarSign, Euro, ShieldCheck } from 'lucide-react';

interface HeaderProps {
  currency: Currency;
  onCurrencyChange: (c: Currency) => void;
  metadata?: {
    filename?: string;
    row_count?: number;
    date_start?: string;
    date_end?: string;
  };
}

export const Header: React.FC<HeaderProps> = ({ currency, onCurrencyChange, metadata }) => {
  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg text-white tracking-tight">FinPulse</span>
              <span className="text-xs bg-indigo-500/20 text-indigo-300 font-medium px-2 py-0.5 rounded-full border border-indigo-500/30">
                SDP Personal Intelligence
              </span>
            </div>
            <p className="text-xs text-slate-400">Google Sheets Financial Behavior & Intelligence Engine</p>
          </div>
        </div>

        {/* Right Actions */}
        <div className="flex items-center space-x-4">
          {metadata?.filename && (
            <div className="hidden md:flex items-center text-xs text-slate-400 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700/60">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400 mr-1.5" />
              <span>Loaded: <strong className="text-slate-200">{metadata.filename}</strong> ({metadata.row_count} txs)</span>
            </div>
          )}

          {/* Currency Toggle */}
          <div className="flex items-center bg-slate-800/90 rounded-lg p-0.5 border border-slate-700">
            <button
              onClick={() => onCurrencyChange('INR')}
              className={`flex items-center space-x-1 px-2.5 py-1 rounded-md text-xs font-medium transition-all ${
                currency === 'INR'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="Indian Rupee (₹)"
            >
              <IndianRupee className="w-3.5 h-3.5" />
              <span>INR</span>
            </button>
            <button
              onClick={() => onCurrencyChange('USD')}
              className={`flex items-center space-x-1 px-2.5 py-1 rounded-md text-xs font-medium transition-all ${
                currency === 'USD'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="US Dollar ($)"
            >
              <DollarSign className="w-3.5 h-3.5" />
              <span>USD</span>
            </button>
            <button
              onClick={() => onCurrencyChange('EUR')}
              className={`flex items-center space-x-1 px-2.5 py-1 rounded-md text-xs font-medium transition-all ${
                currency === 'EUR'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              title="Euro (€)"
            >
              <Euro className="w-3.5 h-3.5" />
              <span>EUR</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

