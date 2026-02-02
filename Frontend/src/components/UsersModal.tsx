import { useEffect, useState } from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import TextField from "@mui/material/TextField";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import Box from "@mui/material/Box";
import { getUsuarios, atualizarNivelUsuario, atualizarSenhaUsuario } from "../services/api";

type Props = {
  open: boolean;
  onClose: () => void;
};

export default function UsersModal({ open, onClose }: Props) {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [editingNivel, setEditingNivel] = useState<Record<number, number>>({});
  const [editingPassword, setEditingPassword] = useState<Record<number, string>>({});

  useEffect(() => {
    if (!open) return;
    setLoading(true);
    getUsuarios()
      .then((u) => setUsers(u))
      .catch(() => setUsers([]))
      .finally(() => setLoading(false));
  }, [open]);

  const saveNivel = async (id: number) => {
    const novo = editingNivel[id];
    if (novo == null) return;
    try {
      await atualizarNivelUsuario(id, novo);
      setUsers((s) => s.map((x) => (x.id === id ? { ...x, nivelUsuario: novo } : x)));
    } catch (e: any) {
      alert(e?.message ?? "Falha ao atualizar nível");
    }
  };

  const saveSenha = async (id: number) => {
    const nova = editingPassword[id];
    if (!nova) return;
    try {
      await atualizarSenhaUsuario(id, nova);
      setEditingPassword((s) => ({ ...s, [id]: "" }));
      alert("Senha atualizada");
    } catch (e: any) {
      alert(e?.message ?? "Falha ao atualizar senha");
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="lg" fullWidth>
      <DialogTitle>Usuários</DialogTitle>
      <DialogContent>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Nome</TableCell>
                <TableCell>E-mail</TableCell>
                <TableCell>Setor</TableCell>
                <TableCell>Nível</TableCell>
                <TableCell>Nova senha</TableCell>
                <TableCell></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {users.map((u) => (
                <TableRow key={u.id}>
                  <TableCell>{u.nomeUsuario}</TableCell>
                  <TableCell>{u.emailUsuario}</TableCell>
                  <TableCell>{u.idSetor ?? "-"}</TableCell>
                  <TableCell>
                    <Select
                      value={editingNivel[u.id] ?? u.nivelUsuario ?? 1}
                      onChange={(e) => setEditingNivel((s) => ({ ...s, [u.id]: Number(e.target.value) }))}
                      size="small"
                    >
                      <MenuItem value={1}>1</MenuItem>
                      <MenuItem value={2}>2</MenuItem>
                      <MenuItem value={3}>3</MenuItem>
                      <MenuItem value={4}>4</MenuItem>
                    </Select>
                    <Button size="small" onClick={() => saveNivel(u.id)} sx={{ ml: 1 }}>Salvar</Button>
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: "flex", gap: 1 }}>
                      <TextField size="small" value={editingPassword[u.id] ?? ""} onChange={(e) => setEditingPassword((s) => ({ ...s, [u.id]: e.target.value }))} />
                      <Button size="small" onClick={() => saveSenha(u.id)}>Atualizar</Button>
                    </Box>
                  </TableCell>
                  <TableCell />
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Fechar</Button>
      </DialogActions>
    </Dialog>
  );
}
