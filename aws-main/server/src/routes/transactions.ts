import { Router, Request, Response, NextFunction } from 'express';
import { pool } from '../db';
import { Transaction } from '../types';

const router = Router();

// Middleware to check if user is authenticated
const isAuthenticated = (req: Request, res: Response, next: NextFunction): void => {
  if (!req.session.userId) {
    res.status(401).json({ error: 'Unauthorized' });
    return;
  }
  next();
};

// Get transactions for last 7 days
router.get('/last-7-days', isAuthenticated, async (req: Request, res: Response): Promise<void> => {
  try {
    const result = await pool.query<Transaction>(
      `SELECT * FROM transactions 
       WHERE user_id = $1 
       AND transaction_date >= NOW() - INTERVAL '7 days'
       ORDER BY transaction_date DESC`,
      [req.session.userId]
    );
    res.json(result.rows);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get transactions for last 30 days
router.get('/last-30-days', isAuthenticated, async (req: Request, res: Response): Promise<void> => {
  try {
    const result = await pool.query<Transaction>(
      `SELECT * FROM transactions 
       WHERE user_id = $1 
       AND transaction_date >= NOW() - INTERVAL '30 days'
       ORDER BY transaction_date DESC`,
      [req.session.userId]
    );
    res.json(result.rows);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Add new transaction
router.post('/', isAuthenticated, async (req: Request, res: Response): Promise<void> => {
  try {
    const { amount, description, transaction_date } = req.body;
    
    // Validate input
    if (typeof amount !== 'number' || isNaN(amount)) {
      res.status(400).json({ error: 'Invalid amount' });
      return;
    }

    if (!description || typeof description !== 'string') {
      res.status(400).json({ error: 'Invalid description' });
      return;
    }

    if (!transaction_date) {
      res.status(400).json({ error: 'Invalid transaction date' });
      return;
    }

    const result = await pool.query<Transaction>(
      'INSERT INTO transactions (user_id, amount, description, transaction_date) VALUES ($1, $2, $3, $4) RETURNING *',
      [req.session.userId, amount, description, transaction_date]
    );
    res.json(result.rows[0]);
  } catch (error) {
    console.error('Error creating transaction:', error);
    console.error('Request body:', req.body);
    res.status(500).json({ error: 'Internal server error', details: error instanceof Error ? error.message : 'Unknown error' });
  }
});

// Update transaction
router.put('/:id', isAuthenticated, async (req: Request, res: Response): Promise<void> => {
  try {
    const { id } = req.params;
    const { amount, description, transaction_date } = req.body;
    const result = await pool.query<Transaction>(
      `UPDATE transactions 
       SET amount = $1, description = $2, transaction_date = $3 
       WHERE id = $4 AND user_id = $5 
       RETURNING *`,
      [amount, description, transaction_date, id, req.session.userId]
    );
    
    if (result.rows.length === 0) {
      res.status(404).json({ error: 'Transaction not found' });
      return;
    }
    
    res.json(result.rows[0]);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Delete transaction
router.delete('/:id', isAuthenticated, async (req: Request, res: Response): Promise<void> => {
  try {
    const { id } = req.params;
    const result = await pool.query<Transaction>(
      'DELETE FROM transactions WHERE id = $1 AND user_id = $2 RETURNING *',
      [id, req.session.userId]
    );
    
    if (result.rows.length === 0) {
      res.status(404).json({ error: 'Transaction not found' });
      return;
    }
    
    res.json({ success: true });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

export default router; 