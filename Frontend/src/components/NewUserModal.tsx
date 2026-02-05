import { useState, useEffect } from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import MenuItem from "@mui/material/MenuItem";
import { criarUsuario, getSetores } from "../services/api";

type Props = {
  open: boolean;
  onClose: () => void;
  onCreated: () => void;
};

export default function NewUserModal({ open, onClose, onCreated }: Props) {
  const [formData, setFormData] = useState({
    id: "",
    nomeUsuario: "",
    emailUsuario: "",
    idSetor: "",
    nivelUsuario: 1,
    cargoUsuario: "",
    telefoneUsuario: "",
    computadorUsuario: "",
  });
  const [setores, setSetores] = useState<{ id: number; nome_setor?: string }[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (open) {
      getSetores().then(setSetores).catch(() => setSetores([]));
      setFormData({
        id: "",
        nomeUsuario: "",
        emailUsuario: "",
        idSetor: "",
        nivelUsuario: 1,
        cargoUsuario: "",
        telefoneUsuario: "",
        computadorUsuario: "",
      });
    }
  }, [open]);

  const handleSave = async () => {
    if (!formData.id || !formData.nomeUsuario) {
      alert("Código e Nome são obrigatórios");
      return;
    }
    setLoading(true);
    try {
      await criarUsuario({
        ...formData,
        id: Number(formData.id),
        idSetor: formData.idSetor ? Number(formData.idSetor) : null,
      });
      onCreated();
      onClose();
    } catch (e: any) {
      alert(e?.response?.data?.message ?? "Falha ao criar usuário");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Criar Novo Usuário</DialogTitle>
      <DialogContent>
        <Box sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}>
          <TextField
            label="Código (ID)"
            type="number"
            fullWidth
            value={formData.id}
            onChange={(e) => setFormData({ ...formData, id: e.target.value })}
          />
          <TextField
            label="Nome"
            fullWidth
            value={formData.nomeUsuario}
            onChange={(e) => setFormData({ ...formData, nomeUsuario: e.target.value })}
          />
          <TextField
            label="E-mail"
            fullWidth
            value={formData.emailUsuario}
            onChange={(e) => setFormData({ ...formData, emailUsuario: e.target.value })}
          />
          <TextField
            select
            label="Setor"
            fullWidth
            value={formData.idSetor}
            onChange={(e) => setFormData({ ...formData, idSetor: e.target.value })}
          >
            <MenuItem value="">Nenhum</MenuItem>
            {setores.map((s) => (
              <MenuItem key={s.id} value={s.id}>
                {s.nome_setor}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="Nível"
            fullWidth
            value={formData.nivelUsuario}
            onChange={(e) => setFormData({ ...formData, nivelUsuario: Number(e.target.value) })}
          >
            <MenuItem value={1}>1 - Operador</MenuItem>
            <MenuItem value={2}>2 - Supervisor</MenuItem>
            <MenuItem value={3}>3 - Gerente</MenuItem>
            <MenuItem value={4}>4 - Administrador</MenuItem>
          </TextField>
          <TextField
            label="Cargo"
            fullWidth
            value={formData.cargoUsuario}
            onChange={(e) => setFormData({ ...formData, cargoUsuario: e.target.value })}
          />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancelar</Button>
        <Button onClick={handleSave} variant="contained" disabled={loading}>
          Criar
        </Button>
      </DialogActions>
    </Dialog>
  );
}
