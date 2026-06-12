import React, { useState, useEffect } from 'react';
import { transactionApi } from '../api/endpoints';
import type { Transaction } from '../types';
import { Search, Trash2, Edit2 } from 'lucide-react';
import './TransactionsList.css';

interface TransactionsListProps {
  transactions: Transaction[];
  onRefresh: () => void;
  loading?: boolean;
}

export default function TransactionsList({ transactions, onRefresh, loading = false }: TransactionsListProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredTransactions, setFilteredTransactions] = useState<Transaction[]>(transactions);

  useEffect(() => {
    if (searchQuery.trim() === '') {
      setFilteredTransactions(transactions);
    } else {
      const query = searchQuery.toLowerCase();
      setFilteredTransactions(
        transactions.filter(t =>
          (t.description?.toLowerCase().includes(query) ||
          t.category?.toLowerCase().includes(query) ||
          t.amount.toString().includes(query))
        )
      );
    }
  }, [searchQuery, transactions]);

  const handleDelete = async (id: string) => {
    if (window.confirm('Delete this transaction?')) {
      try {
        await transactionApi.delete(id);
        onRefresh();
      } catch (err) {
        alert('Failed to delete transaction');
      }
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  return (
    <div className="transactions-list">
      <div className="search-bar">
        <Search size={20} />
        <input
          type="text"
          placeholder="Search by description, category, or amount..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-input"
        />
      </div>

      {loading && <div className="loading">Loading transactions...</div>}

      {filteredTransactions.length === 0 ? (
        <div className="empty-state">
          <p>No transactions found</p>
        </div>
      ) : (
        <div className="table-container">
          <table className="transactions-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Description</th>
                <th>Category</th>
                <th className="amount-col">Amount</th>
                <th className="balance-col">Balance</th>
                <th className="actions-col">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredTransactions.map((txn) => (
                <tr key={txn.id} className={txn.is_deposit ? 'deposit' : 'expense'}>
                  <td className="date-col">{formatDate(txn.date)}</td>
                  <td className="description-col" title={txn.description || ''}>
                    {txn.description || 'N/A'}
                  </td>
                  <td className="category-col">{txn.category || 'Uncategorized'}</td>
                  <td className={`amount-col ${txn.is_deposit ? 'income' : 'expense'}`}>
                    {formatCurrency(txn.amount)}
                  </td>
                  <td className="balance-col">{formatCurrency(txn.balance)}</td>
                  <td className="actions-col">
                    <button className="action-btn edit-btn" title="Edit">
                      <Edit2 size={16} />
                    </button>
                    <button
                      className="action-btn delete-btn"
                      onClick={() => handleDelete(txn.id)}
                      title="Delete"
                    >
                      <Trash2 size={16} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
