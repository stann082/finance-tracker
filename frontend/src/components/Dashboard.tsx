import React, { useState, useEffect } from 'react';
import { statsApi, transactionApi } from '../api/endpoints';
import { PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import type { SummaryStats, SpendingTrend, CategoryBreakdown } from '../types';
import './Dashboard.css';

interface DashboardProps {
  startDate: string;
  endDate: string;
  loading?: boolean;
}

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b', '#fa709a', '#feca57'];

export default function Dashboard({ startDate, endDate, loading = false }: DashboardProps) {
  const [summary, setSummary] = useState<SummaryStats | null>(null);
  const [breakdown, setBreakdown] = useState<CategoryBreakdown>({});
  const [trend, setTrend] = useState<SpendingTrend[]>([]);
  const [graphLoading, setGraphLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        setGraphLoading(true);
        const [summaryRes, breakdownRes, trendRes] = await Promise.all([
          statsApi.getSummary(startDate, endDate),
          statsApi.getCategoryBreakdown(startDate, endDate),
          statsApi.getSpendingTrend(startDate, endDate, 'daily'),
        ]);

        setSummary(summaryRes.data);
        setBreakdown(breakdownRes.data);
        setTrend(trendRes.data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load dashboard');
      } finally {
        setGraphLoading(false);
      }
    };

    fetchDashboard();
  }, [startDate, endDate]);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const breakdownData = Object.entries(breakdown).map(([category, amount]) => ({
    name: category,
    value: parseFloat(amount.toFixed(2)),
  }));

  if (graphLoading) {
    return <div className="dashboard loading">Loading dashboard...</div>;
  }

  if (error) {
    return <div className="dashboard error">Error: {error}</div>;
  }

  return (
    <div className="dashboard">
      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="card">
          <h3>Total Income</h3>
          <p className="amount income">{summary?.total_income ? formatCurrency(summary.total_income) : '-'}</p>
        </div>
        <div className="card">
          <h3>Total Spent</h3>
          <p className="amount expense">{summary?.total_spent ? formatCurrency(summary.total_spent) : '-'}</p>
        </div>
        <div className="card">
          <h3>Net</h3>
          <p className={`amount ${(summary?.net ?? 0) >= 0 ? 'income' : 'expense'}`}>
            {summary?.net !== undefined ? formatCurrency(summary.net) : '-'}
          </p>
        </div>
        <div className="card">
          <h3>Avg Transaction</h3>
          <p className="amount">{summary?.avg_transaction ? formatCurrency(summary.avg_transaction) : '-'}</p>
        </div>
      </div>

      {/* Charts */}
      <div className="charts-container">
        {/* Spending Trend */}
        {trend.length > 0 && (
          <div className="chart-card full-width">
            <h2>Spending Trend</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip formatter={(value) => formatCurrency(value as number)} />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="total"
                  stroke="#667eea"
                  strokeWidth={2}
                  dot={{ fill: '#667eea', r: 4 }}
                  name="Daily Spending"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Category Breakdown */}
        {breakdownData.length > 0 && (
          <div className="chart-card">
            <h2>Spending by Category</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={breakdownData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {breakdownData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => formatCurrency(value as number)} />
              </PieChart>
            </ResponsiveContainer>
            <div className="category-legend">
              {breakdownData.map((item, idx) => (
                <div key={item.name} className="legend-item">
                  <span
                    className="legend-color"
                    style={{ backgroundColor: COLORS[idx % COLORS.length] }}
                  ></span>
                  <span className="legend-text">{item.name}</span>
                  <span className="legend-amount">{formatCurrency(item.value)}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Stats */}
      <div className="stats-section">
        <div className="stat-item">
          <span className="stat-label">Total Transactions:</span>
          <span className="stat-value">{summary?.transaction_count}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Categories:</span>
          <span className="stat-value">{summary?.category_count}</span>
        </div>
      </div>
    </div>
  );
}
