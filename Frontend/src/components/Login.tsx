import { useState } from "react";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Alert from "@mui/material/Alert";
import CircularProgress from "@mui/material/CircularProgress";
import { useAuth } from "../contexts/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const [nomeUsuario, setNomeUsuario] = useState("");
  const [senha, setSenha] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const doLogin = async () => {
    setError(null);
    setLoading(true);
    try {
      await login(nomeUsuario, senha);
    } catch (e: any) {
      setError(e?.message ?? "Falha no login");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", p: 2 }}>
      <Paper sx={{ width: 420, p: 4 }}>
        <Typography variant="h5" sx={{ mb: 2, fontWeight: 700 }}>
          Entrar — Nexus
        </Typography>
        {error ? (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        ) : null}

        <TextField label="Nome de usuário" value={nomeUsuario} onChange={(e) => setNomeUsuario(e.target.value)} fullWidth sx={{ mb: 2 }} />
        <TextField label="Senha" type="password" value={senha} onChange={(e) => setSenha(e.target.value)} fullWidth sx={{ mb: 2 }} />

        <Box sx={{ display: "flex", gap: 1 }}>
          <Button variant="contained" onClick={doLogin} disabled={loading} fullWidth>
            {loading ? <CircularProgress size={20} color="inherit" /> : "Entrar"}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
}
