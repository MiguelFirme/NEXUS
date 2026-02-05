import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import AssignmentOutlined from "@mui/icons-material/AssignmentOutlined";
import Avatar from "@mui/material/Avatar";
import IconButton from "@mui/material/IconButton";
import PeopleRounded from "@mui/icons-material/PeopleRounded";
import ExitToAppRounded from "@mui/icons-material/ExitToAppRounded";
import { useState } from "react";
import UsersModal from "./UsersModal";
import { useAuth } from "../contexts/AuthContext";

export default function Header() {
  const { usuario, logout } = useAuth();
  const [openUsers, setOpenUsers] = useState(false);
  return (
    <AppBar
      position="static"
      elevation={0}
      sx={{
        background: "linear-gradient(135deg, #1e293b 0%, #334155 100%)",
        borderBottom: "1px solid rgba(255,255,255,0.08)",
      }}
    >
      <Toolbar sx={{ gap: 2, py: 1.5 }}>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1.5 }}>
          <Box
            sx={{
              width: 40,
              height: 40,
              borderRadius: 2,
              bgcolor: "rgba(255,255,255,0.12)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <AssignmentOutlined sx={{ color: "#fff", fontSize: 22 }} />
          </Box>
          <Typography variant="h6" fontWeight={700} sx={{ letterSpacing: "-0.02em" }}>
            Nexus
          </Typography>
          <Typography variant="body2" sx={{ color: "rgba(255,255,255,0.7)", fontWeight: 500 }}>
            Gestão de Pendências
          </Typography>
        </Box>
        <Box sx={{ flex: 1 }} />
        <Box sx={{ display: "flex", alignItems: "center", gap: 1.5 }}>
          <Typography variant="body2" sx={{ color: "rgba(255,255,255,0.85)", fontWeight: 500 }}>
            {usuario?.nomeUsuario ?? "Miguel Firme"}
          </Typography>
          <Typography variant="caption" sx={{ color: "rgba(255,255,255,0.6)" }}>
            {usuario?.cargoUsuario ?? "Desenvolvimento"}
          </Typography>
          <Avatar
            sx={{
              width: 36,
              height: 36,
              bgcolor: "primary.main",
              fontSize: "0.9rem",
            }}
          >
            MF
          </Avatar>
          {usuario?.nivelUsuario === 4 ? (
            <IconButton sx={{ ml: 1 }} onClick={() => setOpenUsers(true)} color="inherit">
              <PeopleRounded />
            </IconButton>
          ) : null}
          {usuario ? (
            <IconButton sx={{ ml: 1 }} onClick={() => { logout(); setOpenUsers(false); }} color="inherit">
              <ExitToAppRounded />
            </IconButton>
          ) : null}
        </Box>
      </Toolbar>
      <UsersModal open={openUsers} onClose={() => setOpenUsers(false)} currentUserLevel={usuario?.nivelUsuario} />
    </AppBar>
  );
}
