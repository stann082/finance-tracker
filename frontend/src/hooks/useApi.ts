import { useState, useEffect } from 'react';
import apiClient from '../api/client';
import type { Transaction } from '../types';

export function useTransactions(limit: number = 100, skip: number = 0) {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        setLoading(true);
        const response = await apiClient.get('/transactions', {
          params: { limit, skip },
        });
        setTransactions(response.data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch transactions');
        setTransactions([]);
      } finally {
        setLoading(false);
      }
    };

    fetchTransactions();
  }, [limit, skip]);

  return { transactions, loading, error };
}

export function usePayPeriods(monthsBack: number = 12) {
  const [periods, setPeriods] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPeriods = async () => {
      try {
        setLoading(true);
        const response = await apiClient.get('/pay-periods', {
          params: { months: monthsBack },
        });
        setPeriods(response.data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch pay periods');
        setPeriods([]);
      } finally {
        setLoading(false);
      }
    };

    fetchPeriods();
  }, [monthsBack]);

  return { periods, loading, error };
}

export function useCategories() {
  const [categories, setCategories] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setLoading(true);
        const response = await apiClient.get('/categories');
        setCategories(response.data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch categories');
        setCategories([]);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  return { categories, loading, error };
}
