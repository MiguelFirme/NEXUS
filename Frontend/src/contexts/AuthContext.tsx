import { createContext, useCallback, useContext, useEffect, useState } from "react";

export type UsuarioLogado = {
  id: number;
  nomeUsuario?: string;
  emailUsuario?: string;
  idSetor?: number;
  cargoUsuario?: string;
};

type AuthContextValue = {
  token: string | null;
  usuario: UsuarioLogado | null;
  login: (email: string, senha: string) => Promise<void>;
  definirSenha: (email: string, novaSenha: string) => Promise<void>;
  logout: () => void;
  isReady: boolean;
};

const STORAGE_TOKEN = "nexus_token";
const STORAGE_USUARIO = "nexus_usuario";

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [usuario, setUsuario] = useState<UsuarioLogado | null>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const t = localStorage.getItem(STORAGE_TOKEN);
    const u = localStorage.getItem(STORAGE_USUARIO);
    if (t && u) {
      try {
        setToken(t);
        setUsuario(JSON.parse(u) as UsuarioLogado);
      } catch {
        localStorage.removeItem(STORAGE_TOKEN);
        localStorage.removeItem(STORAGE_USUARIO);
      }
    }
    setIsReady(true);
  }, []);

  const login = useCallback(async (email: string, senha: string) => {
    const baseURL = import.meta.env.VITE_API_URL ?? "http://localhost:8080";
    const res = await fetch(`${baseURL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ emailUsuario: email.trim(), senha }),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.message ?? "Falha no login.");
    }
    const t = data.token as string;
    const u = data.usuario as UsuarioLogado;
    setToken(t);
    setUsuario(u);
    localStorage.setItem(STORAGE_TOKEN, t);
    localStorage.setItem(STORAGE_USUARIO, JSON.stringify(u));
  }, []);

  const definirSenha = useCallback(async (email: string, novaSenha: string) => {
    const baseURL = import.meta.env.VITE_API_URL ?? "http://localhost:8080";
    const res = await fetch(`${baseURL}/auth/definir-senha`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ emailUsuario: email.trim(), novaSenha }),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.message ?? "Falha ao definir senha.");
    }
    const t = data.token as string;
    const u = data.usuario as UsuarioLogado;
    setToken(t);
    setUsuario(u);
    localStorage.setItem(STORAGE_TOKEN, t);
    localStorage.setItem(STORAGE_USUARIO, JSON.stringify(u));
  }, []);

  const logout = useCallback(() => {
    setToken(null);
    setUsuario(null);
    localStorage.removeItem(STORAGE_TOKEN);
    localStorage.removeItem(STORAGE_USUARIO);
  }, []);

  return (
    <AuthContext.Provider value={{ token, usuario, login, definirSenha, logout, isReady }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth deve ser usado dentro de AuthProvider");
  return ctx;
}
