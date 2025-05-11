import { useState } from 'react';
import { transactions } from '../services/api';
import type { TransactionFormData } from '../types';

interface TransactionFormProps {
  onSuccess: () => void;
  onCancel: () => void;
}

function TransactionForm({ onSuccess, onCancel }: TransactionFormProps) {
  const [formData, setFormData] = useState<TransactionFormData>({
    amount: 0,
    description: '',
    transaction_date: new Date().toISOString().split('T')[0],
  });
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await transactions.create(formData);
      onSuccess();
    } catch (error) {
      setError('Failed to create transaction. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="transaction-form">
      <div className="form-group">
        <label htmlFor="amount" className="form-label">
          Amount
        </label>
        <input
          type="number"
          step="0.01"
          id="amount"
          value={formData.amount}
          onChange={(e) => {
            const value = e.target.value;
            setFormData({ 
              ...formData, 
              amount: value === '' ? 0 : parseFloat(value) 
            });
          }}
          className="form-input"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="description" className="form-label">
          Description
        </label>
        <input
          type="text"
          id="description"
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          className="form-input"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="date" className="form-label">
          Date
        </label>
        <input
          type="date"
          id="date"
          value={formData.transaction_date}
          onChange={(e) => setFormData({ ...formData, transaction_date: e.target.value })}
          className="form-input"
          required
        />
      </div>

      {error && (
        <div className="form-error">{error}</div>
      )}

      <div className="form-buttons">
        <button
          type="button"
          onClick={onCancel}
          className="btn btn-secondary"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="btn btn-primary"
        >
          Add Transaction
        </button>
      </div>
    </form>
  );
}

export default TransactionForm; 