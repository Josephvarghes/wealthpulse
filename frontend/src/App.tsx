import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { UploadSection } from './components/UploadSection';
import { SummaryCards } from './components/SummaryCards';
import { CategoryChart } from './charts/CategoryChart';
import { TrendsChart } from './charts/TrendsChart';
import { BehaviorFindings } from './components/BehaviorFindings';
import { RuleRecommendations } from './components/RuleRecommendations';
import { UnusualExpensesList } from './components/UnusualExpensesList';
import { AIRecommendationsCard } from './components/AIRecommendationsCard';
import { FullAnalysisResponse, Currency } from './types';
import { api } from './services/api';
import { Sparkles, Shield, BarChart3 } from 'lucide-react';

export const App: React.FC = () => {
  const [currency, setCurrency] = useState<Currency>('INR');
  const [analysisData, setAnalysisData] = useState<FullAnalysisResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Auto-load demo on initial mount for instant preview
  useEffect(() => {
    handleLoadDemo();
  }, []);

  const handleFileUpload = async (file: File) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await api.uploadFile(file);
      setAnalysisData(result);
    } catch (err: any) {
      setError(err?.message || 'Failed to process file. Please ensure it matches the required format.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoadDemo = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await api.loadDemoData();
      setAnalysisData(result);
    } catch (err: any) {
      setError(err?.message || 'Failed to load demo data. Please verify the backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Header
        currency={currency}
        onCurrencyChange={setCurrency}
        metadata={analysisData?.metadata}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Upload Zone with 1-click demo */}
        <UploadSection
          onFileUpload={handleFileUpload}
          onLoadDemo={handleLoadDemo}
          isLoading={isLoading}
          error={error}
        />

        {/* Dashboard Content */}
        {analysisData ? (
          <div className="space-y-8 animate-in fade-in duration-300">
            {/* Top Summary Metrics */}
            <SummaryCards summary={analysisData.summary} currency={currency} />

            {/* AI Recommendations Card */}
            <AIRecommendationsCard recommendation={analysisData.ai_recommendations} />

            {/* Visual Analytics Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              <CategoryChart categories={analysisData.categories} currency={currency} />
              <TrendsChart timeAnalysis={analysisData.time_analysis} currency={currency} />
            </div>

            {/* Behavioral Findings */}
            <BehaviorFindings findings={analysisData.behavior_findings} />

            {/* Unusual Expenses Outliers */}
            <UnusualExpensesList expenses={analysisData.unusual_expenses} currency={currency} />

            {/* Deterministic Rule Recommendations */}
            <RuleRecommendations recommendations={analysisData.rule_recommendations} />
          </div>
        ) : (
          !isLoading && (
            <div className="text-center py-16 px-4 bg-slate-900/40 border border-slate-800 rounded-3xl max-w-2xl mx-auto space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 mx-auto flex items-center justify-center">
                <BarChart3 className="w-6 h-6" />
              </div>
              <h3 className="text-base font-semibold text-slate-200">No Financial Records Loaded</h3>
              <p className="text-xs text-slate-400 max-w-md mx-auto">
                Upload your Google Sheets transaction export (CSV or Excel) above, or click "Load SDP Demo Dataset" to explore automatic calculations and behavior analysis.
              </p>
            </div>
          )
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>Personal Finance Intelligence &amp; Recommendation System</span>
          <div className="flex items-center space-x-2 text-slate-400">
            <Shield className="w-3.5 h-3.5 text-emerald-400" />
            <span>Strict privacy: Calculations performed locally; raw data never sent to AI</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;

