import { Router, Request, Response } from 'express';
import { pool } from '../db';
import crypto from 'crypto';
import { User } from '../types';

const router = Router();

// Helper function to hash password
const hashPassword = (password: string): string => {
  return crypto.createHash('sha256').update(password).digest('hex');
};

// Register
router.post('/register', async (req: Request, res: Response): Promise<void> => {
  try {
    const { username, password } = req.body;
    const hashedPassword = hashPassword(password);

    const result = await pool.query<User>(
      'INSERT INTO users (username, password) VALUES ($1, $2) RETURNING id',
      [username, hashedPassword]
    );

    const userId = result.rows[0].id;

    // Generate random transactions for the new user
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 30); // Start from 30 days ago

    for (let i = 0; i < 20; i++) {
      const randomDate = new Date(startDate.getTime() + Math.random() * (new Date().getTime() - startDate.getTime()));
      const randomAmount = parseFloat((Math.random() * 1000 - 500).toFixed(2)); // Random amount between -500 and 500
      const descriptions = ['Groceries', 'Rent', 'Salary', 'Entertainment', 'Shopping', 'Utilities', 'Transport'];
      const randomDescription = descriptions[Math.floor(Math.random() * descriptions.length)];

      await pool.query(
        'INSERT INTO transactions (user_id, amount, description, transaction_date) VALUES ($1, $2, $3, $4)',
        [userId, randomAmount, randomDescription, randomDate]
      );
    }

    req.session.userId = userId;
    res.json({ success: true });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Login
router.post('/login', async (req: Request, res: Response): Promise<void> => {
  try {
    const { username, password } = req.body;
    const hashedPassword = hashPassword(password);

    const result = await pool.query<User>(
      'SELECT id FROM users WHERE username = $1 AND password = $2',
      [username, hashedPassword]
    );

    if (result.rows.length === 0) {
      res.status(401).json({ error: 'Invalid credentials' });
      return;
    }

    req.session.userId = result.rows[0].id;
    res.json({ success: true });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Logout
router.post('/logout', (req: Request, res: Response): void => {
  req.session.destroy((err) => {
    if (err) {
      console.error(err);
      res.status(500).json({ error: 'Internal server error' });
      return;
    }
    res.json({ success: true });
  });
});

// Check auth status
router.get('/status', (req: Request, res: Response): void => {
  res.json({ isAuthenticated: !!req.session.userId });
});

export default router; 