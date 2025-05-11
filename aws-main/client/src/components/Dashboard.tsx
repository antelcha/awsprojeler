import { useState, useEffect } from 'react';
import { auth, transactions } from '../services/api';
import type { Transaction } from '../types';
import TransactionForm from './TransactionForm';
import TransactionList from './TransactionList';

interface DashboardProps {
  setIsAuthenticated: (value: boolean) => void;
}

function Dashboard({ setIsAuthenticated }: DashboardProps) {
  const [timeRange, setTimeRange] = useState<'7days' | '30days'>('7days');
  const [transactionList, setTransactionList] = useState<Transaction[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  const fetchTransactions = async () => {
    try {
      const data = timeRange === '7days'
        ? await transactions.getLast7Days()
        : await transactions.getLast30Days();
      console.log('Fetched transactions:', data);
      setTransactionList(data);
    } catch (error) {
      console.error('Failed to fetch transactions:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, [timeRange]);

  const handleLogout = async () => {
    try {
      await auth.logout();
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const handleAddTransaction = () => {
    setShowForm(true);
  };

  const handleTransactionAdded = () => {
    setShowForm(false);
    fetchTransactions();
  };

  const handleDeleteTransaction = async (id: number) => {
    try {
      await transactions.delete(id);
      fetchTransactions();
    } catch (error) {
      console.error('Failed to delete transaction:', error);
    }
  };

  // Calculate summary statistics
  console.log('Transaction list before calculations:', transactionList);
  
  const positiveTransactions = transactionList.filter(t => t.amount > 0);
  console.log('Positive transactions:', positiveTransactions);
  
  const totalIncome = positiveTransactions.length > 0 
    ? positiveTransactions.reduce((sum, t) => sum + Number(t.amount), 0)
    : 0;

  const negativeTransactions = transactionList.filter(t => t.amount < 0);
  console.log('Negative transactions:', negativeTransactions);
  
  const totalExpenses = negativeTransactions.length > 0
    ? negativeTransactions.reduce((sum, t) => sum + Math.abs(Number(t.amount)), 0)
    : 0;

  const balance = totalIncome - totalExpenses;

  console.log('Calculated values:', { totalIncome, totalExpenses, balance });

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="nav">
        <div className="nav-container">
          <h1 className="nav-title">Budget Tracker</h1>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </nav>

      <main className="main">
        {/* Summary Cards */}
        <div className="summary-grid">
          <div className="summary-card">
            <h3 className="summary-label">Total Income</h3>
            <p className="summary-value income-value">${totalIncome.toFixed(2)}</p>
          </div>
          <div className="summary-card">
            <h3 className="summary-label">Total Expenses</h3>
            <p className="summary-value expense-value">${totalExpenses.toFixed(2)}</p>
          </div>
          <div className="summary-card">
            <h3 className="summary-label">Balance</h3>
            <p className={`summary-value balance-value ${balance < 0 ? 'negative' : ''}`}>
              ${balance.toFixed(2)}
            </p>
          </div>
        </div>

        {/* Main Content */}
        <div className="transaction-container">
          <div className="controls">
            <div className="time-range-btns">
              <button
                className={`time-btn ${timeRange === '7days' ? 'active' : ''}`}
                onClick={() => setTimeRange('7days')}
              >
                Last 7 Days
              </button>
              <button
                className={`time-btn ${timeRange === '30days' ? 'active' : ''}`}
                onClick={() => setTimeRange('30days')}
              >
                Last 30 Days
              </button>
            </div>
            <button onClick={handleAddTransaction} className="add-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
              Add Transaction
            </button>
          </div>

          {isLoading ? (
            <div className="loading-container">
              <div className="spinner" />
            </div>
          ) : (
            <TransactionList
              transactions={transactionList}
              onDelete={handleDeleteTransaction}
            />
          )}
        </div>
      </main>

      {/* Transaction Form Modal */}
      {showForm && (
        <div className="modal-overlay">
          <div className="modal-content">
            <TransactionForm
              onCancel={() => setShowForm(false)}
              onSuccess={handleTransactionAdded}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard; 