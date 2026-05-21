import React, { useState } from 'react';
import Navigation from './components/Navigation';
import TransactionsPage from './pages/TransactionsPage';
import DashboardPage from './pages/DashboardPage';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState<'transactions' | 'dashboard'>('transactions');

  return (
    <div className="app">
      <Navigation currentPage={currentPage} onPageChange={setCurrentPage} />
      
      <main className="app-content">
        {currentPage === 'transactions' && <TransactionsPage />}
        {currentPage === 'dashboard' && <DashboardPage />}
      </main>
    </div>
  );
}

export default App;
