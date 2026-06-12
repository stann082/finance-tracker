import React, { useState, useEffect } from 'react';
import { transactionApi } from '../api/endpoints';
import type { Transaction } from '../types';
import TransactionsList from '../components/TransactionsList';
import { RefreshCw, Calendar } from 'lucide-react';
import './TransactionsPage.css';

export default function TransactionsPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [payPeriods, setPayPeriods] = useState<string[]>([]);
  const [selectedPeriod, setSelectedPeriod] = useState<string>('');
  const [usePayPeriod, setUsePayPeriod] = useState(true);
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchPayPeriods();
    fetchTransactions();
  }, []);

  const fetchPayPeriods = async () => {
    try {
      const response = await transactionApi.getPayPeriods(12);
      setPayPeriods(response.data);
      if (response.data.length > 0) {
        setSelectedPeriod(response.data[0]);
      }
    } catch (err) {
      console.error('Failed to fetch pay periods:', err);
    }
  };

  const fetchTransactions = async () => {
    setLoading(true);
    try {
      let response;
      if (usePayPeriod && selectedPeriod) {
        response = await transactionApi.getByPayPeriod(selectedPeriod);
      } else if (startDate && endDate) {
        response = await transactionApi.getByDateRange(startDate, endDate);
      } else {
        response = await transactionApi.getAll(1000);
      }
      setTransactions(response.data);
    } catch (err) {
      console.error('Failed to fetch transactions:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if ((usePayPeriod && selectedPeriod) || (!usePayPeriod && startDate && endDate)) {
      fetchTransactions();
    }
  }, [usePayPeriod, selectedPeriod, startDate, endDate]);

  const handleRefresh = () => {
    fetchTransactions();
  };

  return (
    <div className="transactions-page">
      <div className="controls-panel">
        <div className="control-group">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={usePayPeriod}
              onChange={(e) => setUsePayPeriod(e.target.checked)}
            />
            <span>Use Pay Period</span>
          </label>
        </div>

        {usePayPeriod ? (
          <div className="control-group">
            <label htmlFor="pay-period">Period:</label>
            <select
              id="pay-period"
              value={selectedPeriod}
              onChange={(e) => setSelectedPeriod(e.target.value)}
              className="select-input"
            >
              {payPeriods.map((period) => (
                <option key={period} value={period}>
                  {period}
                </option>
              ))}
            </select>
          </div>
        ) : (
          <>
            <div className="control-group">
              <label htmlFor="start-date">From:</label>
              <input
                id="start-date"
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="date-input"
              />
            </div>
            <div className="control-group">
              <label htmlFor="end-date">To:</label>
              <input
                id="end-date"
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="date-input"
              />
            </div>
          </>
        )}

        <button onClick={handleRefresh} className="refresh-btn" disabled={loading}>
          <RefreshCw size={18} />
          <span>Refresh</span>
        </button>
      </div>

      <TransactionsList
        transactions={transactions}
        onRefresh={handleRefresh}
        loading={loading}
      />
    </div>
  );
}
