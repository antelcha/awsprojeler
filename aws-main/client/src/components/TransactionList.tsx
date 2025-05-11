import type { Transaction } from '../types';

interface TransactionListProps {
  transactions: Transaction[];
  onDelete: (id: number) => void;
}

function TransactionList({ transactions, onDelete }: TransactionListProps) {
  if (transactions.length === 0) {
    return (
      <div className="empty-message">
        No transactions found for this period.
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  return (
    <div className="transaction-table-container">
      <table className="transaction-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Description</th>
            <th className="transaction-amount">Amount</th>
            <th className="transaction-amount">Actions</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.id}>
              <td>{formatDate(transaction.transaction_date)}</td>
              <td>{transaction.description}</td>
              <td className={`transaction-amount ${transaction.amount >= 0 ? 'positive' : 'negative'}`}>
                ${Math.abs(transaction.amount).toFixed(2)}
              </td>
              <td className="transaction-amount">
                <button
                  onClick={() => onDelete(transaction.id)}
                  className="delete-btn"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TransactionList; 