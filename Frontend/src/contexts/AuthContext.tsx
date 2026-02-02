import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { login as apiLogin, definirSenha as apiDefinirSenha } from "../services/api";

export type UsuarioLogado = {
  id: number;
  nomeUsuario?: string;
  emailUsuario?: string;
  idSetor?: number;
  cargoUsuario?: string;
  nivelUsuario?: number;
};

type AuthContextValue = {
  token: string | null;
  usuario: UsuarioLogado | null;
  login: (nomeUsuario: string, senha: string) => Promise<void>;
  definirSenha: (nomeUsuario: string, novaSenha: string) => Promise<void>;
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

  const login = useCallback(async (nomeUsuario: string, senha: string) => {
    const data = await apiLogin(nomeUsuario, senha);
    const t = data.token as string;
    const u = data.usuario as UsuarioLogado;
    setToken(t);
    setUsuario(u);
    localStorage.setItem(STORAGE_TOKEN, t);
    localStorage.setItem(STORAGE_USUARIO, JSON.stringify(u));
  }, []);

  const definirSenha = useCallback(async (nomeUsuario: string, novaSenha: string) => {
    const data = await apiDefinirSenha(nomeUsuario, novaSenha);
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
