export interface Transaction {
  id: string;
  amount: number;
  balance: number;
  category: string | null;
  date: string;
  description: string | null;
  is_deposit: boolean;
  is_recurring: boolean;
  transaction_id: string | null;
  type: 'Credit' | 'Debit';
}

export interface TransactionCreate {
  amount: number;
  balance: number;
  date: string;
  description?: string;
  category?: string;
  is_recurring?: boolean;
  transaction_id?: string;
}

export interface TransactionUpdate {
  amount?: number;
  balance?: number;
  date?: string;
  description?: string;
  category?: string;
  is_recurring?: boolean;
  transaction_id?: string;
}

export interface SummaryStats {
  total_spent: number;
  total_income: number;
  net: number;
  avg_transaction: number;
  transaction_count: number;
  category_count: number;
}

export interface SpendingTrend {
  date: string;
  total: number;
}

export interface CategoryBreakdown {
  [category: string]: number;
}
