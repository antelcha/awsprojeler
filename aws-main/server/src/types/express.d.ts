import { Session } from 'express-session';

declare module 'express-session' {
  interface Session {
    userId: number;
  }
}

declare module 'express' {
  interface Request {
    session: Session & {
      userId: number;
    };
  }
} 