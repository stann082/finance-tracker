import apiClient from '../api/client';
import { SummaryStats, SpendingTrend, CategoryBreakdown } from '../types';

export const transactionApi = {
  getAll: (limit = 100, skip = 0) =>
    apiClient.get('/transactions', { params: { limit, skip } }),

  getById: (id: string) =>
    apiClient.get(`/transactions/${id}`),

  search: (query: string, limit = 100, skip = 0) =>
    apiClient.get('/transactions/search', { params: { query, limit, skip } }),

  getByDateRange: (start: string, end: string, limit = 1000) =>
    apiClient.get('/transactions/by-date', { params: { start, end, limit } }),

  getByPayPeriod: (month: string) =>
    apiClient.get('/transactions/by-pay-period', { params: { month } }),

  create: (data: any) =>
    apiClient.post('/transactions', data),

  update: (id: string, data: any) =>
    apiClient.put(`/transactions/${id}`, data),

  delete: (id: string) =>
    apiClient.delete(`/transactions/${id}`),

  getRecurring: () =>
    apiClient.get('/recurring'),

  getPayPeriods: (months = 12) =>
    apiClient.get('/pay-periods', { params: { months } }),

  getCategories: () =>
    apiClient.get('/categories'),
};

export const statsApi = {
  getSummary: (start: string, end: string): Promise<{ data: SummaryStats }> =>
    apiClient.get('/stats/summary', { params: { start, end } }),

  getCategoryBreakdown: (start: string, end: string): Promise<{ data: CategoryBreakdown }> =>
    apiClient.get('/stats/category-breakdown', { params: { start, end } }),

  getSpendingTrend: (start: string, end: string, granularity = 'daily'): Promise<{ data: SpendingTrend[] }> =>
    apiClient.get('/stats/spending-trend', { params: { start, end, granularity } }),
};

export const healthApi = {
  check: () =>
    apiClient.get('/health'),

  checkFull: () =>
    apiClient.get('/health'),
};
