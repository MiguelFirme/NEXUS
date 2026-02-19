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
import MenuItem from "@mui/material/MenuItem";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import AddIcon from "@mui/icons-material/Add";
import DragIndicatorIcon from "@mui/icons-material/DragIndicator";
import {
  getRoteiros,
  criarRoteiro,
  atualizarRoteiro,
  deletarRoteiro,
  getSetores,
  getUsuarios,
  type RoteiroDTO,
  type CreateRoteiroDTO,
  type PassoRoteiroCreate,
} from "../services/api";

type Props = {
  open: boolean;
  onClose: () => void;
};

type PassoForm = {
  tipo: "SETOR" | "USUARIO";
  idSetor?: number;
  idUsuario?: number;
  ordem: number;
  nomeSetor?: string;
  nomeUsuario?: string;
};

export default function RoteirosModal({ open, onClose }: Props) {
  const [roteiros, setRoteiros] = useState<RoteiroDTO[]>([]);
  const [setores, setSetores] = useState<{ id: number; nome_setor?: string }[]>([]);
  const [usuarios, setUsuarios] = useState<{ id: number; nomeUsuario?: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [formData, setFormData] = useState<{
    nome: string;
    descricao: string;
    ativo: boolean;
    passos: PassoForm[];
  }>({
    nome: "",
    descricao: "",
    ativo: true,
    passos: [],
  });

  const refreshRoteiros = () => {
    setLoading(true);
    getRoteiros()
      .then((r) => setRoteiros(r))
      .catch(() => setRoteiros([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    if (!open) return;
    refreshRoteiros();
    getSetores()
      .then(setSetores)
      .catch(() => setSetores([]));
    getUsuarios()
      .then((u) => setUsuarios(u || []))
      .catch(() => setUsuarios([]));
  }, [open]);

  const resetForm = () => {
    setEditingId(null);
    setFormData({
      nome: "",
      descricao: "",
      ativo: true,
      passos: [],
    });
  };

  const startEdit = (roteiro: RoteiroDTO) => {
    setEditingId(roteiro.id);
    setFormData({
      nome: roteiro.nome,
      descricao: roteiro.descricao || "",
      ativo: roteiro.ativo,
      passos:
        roteiro.passos?.map((p) => ({
          tipo: p.tipo,
          ordem: p.ordem,
          idSetor: p.idSetor,
          idUsuario: p.idUsuario,
          nomeSetor: p.nomeSetor,
          nomeUsuario: p.nomeUsuario,
        })) || [],
    });
  };

  const addPasso = (tipo: "SETOR" | "USUARIO") => {
    const novaOrdem = formData.passos.length > 0 ? Math.max(...formData.passos.map((p) => p.ordem)) + 1 : 1;
    const novo: PassoForm =
      tipo === "SETOR"
        ? { tipo: "SETOR", idSetor: setores[0]?.id ?? 0, ordem: novaOrdem }
        : { tipo: "USUARIO", idUsuario: usuarios[0]?.id ?? 0, ordem: novaOrdem };
    setFormData({ ...formData, passos: [...formData.passos, novo] });
  };

  const removePasso = (index: number) => {
    const novos = formData.passos.filter((_, i) => i !== index);
    novos.forEach((p, i) => {
      p.ordem = i + 1;
    });
    setFormData({ ...formData, passos: novos });
  };

  const updatePasso = (index: number, field: keyof PassoForm, value: any) => {
    const novos = [...formData.passos];
    novos[index] = { ...novos[index], [field]: value };
    setFormData({ ...formData, passos: novos });
  };

  const movePasso = (index: number, direction: "up" | "down") => {
    if (direction === "up" && index === 0) return;
    if (direction === "down" && index === formData.passos.length - 1) return;

    const novos = [...formData.passos];
    const temp = novos[index];
    const swapIndex = direction === "up" ? index - 1 : index + 1;
    novos[index] = novos[swapIndex];
    novos[swapIndex] = temp;
    novos.forEach((p, i) => {
      p.ordem = i + 1;
    });
    setFormData({ ...formData, passos: novos });
  };

  const handleSave = async () => {
    if (!formData.nome.trim()) {
      alert("Nome é obrigatório");
      return;
    }
    if (formData.passos.length === 0) {
      alert("Adicione pelo menos um passo (setor ou usuário) ao roteiro");
      return;
    }

    const passos: PassoRoteiroCreate[] = formData.passos.map((p, i) => ({
      tipo: p.tipo,
      ordem: i + 1,
      idSetor: p.tipo === "SETOR" ? p.idSetor : undefined,
      idUsuario: p.tipo === "USUARIO" ? p.idUsuario : undefined,
    }));

    const payload: CreateRoteiroDTO = {
      nome: formData.nome.trim(),
      descricao: formData.descricao.trim() || undefined,
      ativo: formData.ativo,
      passos,
    };

    try {
      setLoading(true);
      if (editingId) {
        await atualizarRoteiro(editingId, payload);
      } else {
        await criarRoteiro(payload);
      }
      resetForm();
      refreshRoteiros();
    } catch (e: any) {
      alert(e?.message ?? "Falha ao salvar roteiro");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Tem certeza que deseja excluir este roteiro?")) return;
    try {
      setLoading(true);
      await deletarRoteiro(id);
      refreshRoteiros();
    } catch (e: any) {
      alert(e?.message ?? "Falha ao excluir roteiro");
    } finally {
      setLoading(false);
    }
  };

  const isEditing = editingId !== null;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Gerenciar Roteiros</DialogTitle>
      <DialogContent>
        <Box sx={{ display: "flex", flexDirection: "column", gap: 3, mt: 1 }}>
          {/* Formulário de criação/edição */}
          <Box sx={{ p: 2, bgcolor: "background.default", borderRadius: 1 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              {isEditing ? "Editar Roteiro" : "Novo Roteiro"}
            </Typography>

            <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
              <TextField
                label="Nome do Roteiro"
                size="small"
                value={formData.nome}
                onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                fullWidth
              />
              <TextField
                label="Descrição (opcional)"
                size="small"
                multiline
                rows={2}
                value={formData.descricao}
                onChange={(e) => setFormData({ ...formData, descricao: e.target.value })}
                fullWidth
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.ativo}
                    onChange={(e) => setFormData({ ...formData, ativo: e.target.checked })}
                  />
                }
                label="Roteiro ativo"
              />

              <Box>
                <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 1 }}>
                  <Typography variant="subtitle2">Passos da rota (setores e/ou usuários na ordem desejada)</Typography>
                  <Box sx={{ display: "flex", gap: 0.5 }}>
                    <Button size="small" startIcon={<AddIcon />} onClick={() => addPasso("SETOR")}>
                      + Setor
                    </Button>
                    <Button size="small" startIcon={<AddIcon />} onClick={() => addPasso("USUARIO")}>
                      + Usuário
                    </Button>
                  </Box>
                </Box>

                {formData.passos.map((passo, index) => (
                  <Box
                    key={index}
                    sx={{
                      display: "flex",
                      gap: 1,
                      alignItems: "center",
                      mb: 1,
                      p: 1,
                      bgcolor: "background.paper",
                      borderRadius: 1,
                    }}
                  >
                    <DragIndicatorIcon sx={{ color: "text.secondary" }} />
                    <TextField
                      select
                      size="small"
                      value={passo.tipo}
                      onChange={(e) => {
                        const t = e.target.value as "SETOR" | "USUARIO";
                        updatePasso(index, "tipo", t);
                        if (t === "SETOR") updatePasso(index, "idUsuario", undefined);
                        else updatePasso(index, "idSetor", undefined);
                      }}
                      sx={{ minWidth: 100 }}
                    >
                      <MenuItem value="SETOR">Setor</MenuItem>
                      <MenuItem value="USUARIO">Usuário</MenuItem>
                    </TextField>
                    {passo.tipo === "SETOR" ? (
                      <TextField
                        select
                        size="small"
                        value={passo.idSetor ?? ""}
                        onChange={(e) => updatePasso(index, "idSetor", Number(e.target.value))}
                        sx={{ minWidth: 200 }}
                      >
                        {setores.map((s) => (
                          <MenuItem key={s.id} value={s.id}>
                            {s.nome_setor ?? `Setor #${s.id}`}
                          </MenuItem>
                        ))}
                      </TextField>
                    ) : (
                      <TextField
                        select
                        size="small"
                        value={passo.idUsuario ?? ""}
                        onChange={(e) => updatePasso(index, "idUsuario", Number(e.target.value))}
                        sx={{ minWidth: 200 }}
                      >
                        {usuarios.map((u) => (
                          <MenuItem key={u.id} value={u.id}>
                            {u.nomeUsuario ?? `Usuário #${u.id}`}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                    <Typography variant="body2" sx={{ minWidth: 50 }}>
                      #{passo.ordem}
                    </Typography>
                    <IconButton size="small" onClick={() => movePasso(index, "up")} disabled={index === 0}>
                      ↑
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => movePasso(index, "down")}
                      disabled={index === formData.passos.length - 1}
                    >
                      ↓
                    </IconButton>
                    <IconButton size="small" color="error" onClick={() => removePasso(index)}>
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                ))}
              </Box>

              <Box sx={{ display: "flex", gap: 1 }}>
                <Button variant="contained" onClick={handleSave} disabled={loading}>
                  {isEditing ? "Salvar Alterações" : "Criar Roteiro"}
                </Button>
                {isEditing && (
                  <Button onClick={resetForm} disabled={loading}>
                    Cancelar
                  </Button>
                )}
              </Box>
            </Box>
          </Box>

          {/* Lista de roteiros */}
          <Box>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Roteiros Existentes
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>ID</TableCell>
                    <TableCell>Nome</TableCell>
                    <TableCell>Descrição</TableCell>
                    <TableCell>Ativo</TableCell>
                    <TableCell>Rota (passos)</TableCell>
                    <TableCell>Ações</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {roteiros.map((r) => (
                    <TableRow key={r.id}>
                      <TableCell>{r.id}</TableCell>
                      <TableCell>{r.nome}</TableCell>
                      <TableCell>{r.descricao || "-"}</TableCell>
                      <TableCell>{r.ativo ? "Sim" : "Não"}</TableCell>
                      <TableCell>
                        {r.passos
                          ?.sort((a, b) => a.ordem - b.ordem)
                          .map((p) =>
                            p.tipo === "SETOR"
                              ? p.nomeSetor || `Setor #${p.idSetor}`
                              : p.nomeUsuario || `Usuário #${p.idUsuario}`
                          )
                          .join(" → ") || "-"}
                      </TableCell>
                      <TableCell>
                        <IconButton size="small" onClick={() => startEdit(r)}>
                          <EditIcon />
                        </IconButton>
                        <IconButton size="small" color="error" onClick={() => handleDelete(r.id)}>
                          <DeleteIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Fechar</Button>
      </DialogActions>
    </Dialog>
  );
}
