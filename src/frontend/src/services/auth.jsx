import { createContext, useContext, useMemo, useState } from "react";

const AuthContext = createContext(null);
const demoAccounts = [
  { email: "admin@gridguard.ai", password: "admin123", role: "admin", name: "Grid Operator" },
  { email: "user@gridguard.ai", password: "user123", role: "user", name: "GridGuard Customer" },
];

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const value = useMemo(() => ({
    user,
    login(email, password) {
      const account = demoAccounts.find((candidate) => candidate.email === email.trim().toLowerCase() && candidate.password === password);
      if (!account) return null;
      const authenticatedUser = { email: account.email, role: account.role, name: account.name };
      setUser(authenticatedUser);
      return authenticatedUser;
    },
    logout() { setUser(null); },
  }), [user]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// This module deliberately exposes the paired context hook with its provider.
// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within an AuthProvider.");
  return context;
}
