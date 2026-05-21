import React, { useState, useEffect } from 'react';
import Dashboard from '../components/Dashboard';
import './DashboardPage.css';

export default function DashboardPage() {
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');

  useEffect(() => {
    // Default to current month
    const today = new Date();
    const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
    const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0);

    setStartDate(firstDay.toISOString().split('T')[0]);
    setEndDate(lastDay.toISOString().split('T')[0]);
  }, []);

  return (
    <div className="dashboard-page">
      <div className="dashboard-controls">
        <div className="control-group">
          <label htmlFor="dashboard-start">From:</label>
          <input
            id="dashboard-start"
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="date-input"
          />
        </div>
        <div className="control-group">
          <label htmlFor="dashboard-end">To:</label>
          <input
            id="dashboard-end"
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="date-input"
          />
        </div>
      </div>

      {startDate && endDate && (
        <Dashboard startDate={startDate} endDate={endDate} />
      )}
    </div>
  );
}
