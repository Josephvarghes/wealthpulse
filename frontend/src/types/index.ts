export interface FinancialSummary {
  total_income: number;
  total_expenses: number;
  net_balance: number;
  savings: number;
  savings_rate: number;
  transaction_count: number;
  average_transaction: number;
  highest_transaction: number;
  lowest_transaction: number;
}

export interface CategoryItem {
  category: string;
  total_amount: number;
  transaction_count: number;
  percentage_of_total_expenses: number;
  average_transaction: number;
}

export interface TimeAnalysisItem {
  period: string;
  income: number;
  expenses: number;
  savings: number;
  transaction_count: number;
}

export interface TimeAnalysis {
  daily: TimeAnalysisItem[];
  weekly: TimeAnalysisItem[];
  monthly: TimeAnalysisItem[];
}

export interface TrendItem {
  category: string;
  current_period_amount: number;
  previous_period_amount: number;
  change_percent: number;
  trend_direction: 'increasing' | 'decreasing' | 'stable' | 'new';
}

export interface UnusualExpense {
  date: string;
  description: string;
  amount: number;
  category: string;
  reason: string;
}

export interface RecurringExpense {
  category: string;
  description: string;
  average_amount: number;
  occurrence_count: number;
  status: string;
}

export interface BehaviorFinding {
  id: string;
  title: string;
  description: string;
  severity: 'info' | 'positive' | 'warning';
  metric?: string;
}

export interface RuleRecommendation {
  id: string;
  category: string;
  title: string;
  message: string;
  priority: 'high' | 'medium' | 'low';
}

export interface AIRecommendation {
  ai_financial_summary: string;
  key_observation: string;
  positive_behavior: string;
  main_concern: string;
  practical_recommendation: string;
  short_term_action: string;
  provider_used: string;
  is_fallback: boolean;
}

export interface FullAnalysisResponse {
  summary: FinancialSummary;
  categories: CategoryItem[];
  time_analysis: TimeAnalysis;
  trends: TrendItem[];
  unusual_expenses: UnusualExpense[];
  recurring_expenses: RecurringExpense[];
  behavior_findings: BehaviorFinding[];
  rule_recommendations: RuleRecommendation[];
  ai_recommendations?: AIRecommendation;
  metadata: {
    filename?: string;
    row_count?: number;
    date_start?: string;
    date_end?: string;
  };
}

export type Currency = 'INR' | 'USD' | 'EUR';

