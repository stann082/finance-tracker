import React, { useState } from 'react';
import { BarChart3, Home } from 'lucide-react';
import './Navigation.css';

interface NavigationProps {
  currentPage: 'transactions' | 'dashboard';
  onPageChange: (page: 'transactions' | 'dashboard') => void;
}

export default function Navigation({ currentPage, onPageChange }: NavigationProps) {
  return (
    <nav className="navigation">
      <div className="nav-container">
        <h1 className="nav-title">💰 Finance Tracker</h1>
        
        <div className="nav-links">
          <button
            className={`nav-link ${currentPage === 'transactions' ? 'active' : ''}`}
            onClick={() => onPageChange('transactions')}
          >
            <Home size={20} />
            <span>Transactions</span>
          </button>
          
          <button
            className={`nav-link ${currentPage === 'dashboard' ? 'active' : ''}`}
            onClick={() => onPageChange('dashboard')}
          >
            <BarChart3 size={20} />
            <span>Dashboard</span>
          </button>
        </div>
      </div>
    </nav>
  );
}
