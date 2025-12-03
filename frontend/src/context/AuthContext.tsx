import React, { createContext, useContext, useState, useEffect } from 'react';

// Demo user credentials (hardcoded)
const DEMO_USERS = {
  admin: {
    password: '12345',
    role: 'admin',
    name: 'Admin User',
    email: 'admin@demo.com'
  },
  customer: {
    password: 'demo123',
    role: 'customer',
    name: 'Demo Customer',
    email: 'customer@demo.com'
  }
};

interface User {
  username: string;
  role: string;
  name: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => boolean;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  // Check if user is already logged in on mount
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (error) {
        console.error('Failed to parse stored user:', error);
        localStorage.removeItem('user');
      }
    }
  }, []);

  const login = (username: string, password: string): boolean => {
    const demoUser = DEMO_USERS[username as keyof typeof DEMO_USERS];
    
    if (demoUser && demoUser.password === password) {
      const userData: User = {
        username,
        role: demoUser.role,
        name: demoUser.name,
        email: demoUser.email
      };
      
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      return true;
    }
    
    return false;
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  const isAuthenticated = user !== null;

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
