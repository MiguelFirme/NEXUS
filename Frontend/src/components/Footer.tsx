import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

type Props = {
  version?: string;
  author?: string;
  releaseDate?: string;
};

export default function Footer({ version, author, releaseDate }: Props) {
  const ver = version ?? (import.meta.env.VITE_APP_VERSION ?? "0.1.2");
  const auth = author ?? (import.meta.env.VITE_APP_AUTHOR ?? "Miguel Firme & Pedro Luz");
  const date = releaseDate ?? (import.meta.env.VITE_APP_RELEASE_DATE ?? new Date().toLocaleDateString());

  return (
    <Box
      component="footer"
      sx={{
        mt: 2,
        py: 0.5,
        bgcolor: "transparent",
        borderTop: "1px solid",
        borderColor: "divider",
        opacity: 0.9,
      }}
    >
      <Box
        sx={{
          maxWidth: 1200,
          mx: "auto",
          px: 2,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: 2,
        }}
      >
        <Typography variant="body2" color="text.disabled" sx={{ fontSize: "0.75rem" }}>
          Versão: {ver}
        </Typography>
        <Typography variant="body2" color="text.disabled" sx={{ fontSize: "0.75rem" }}>
          Desenvolvido por: {auth}
        </Typography>
        <Typography variant="body2" color="text.disabled" sx={{ fontSize: "0.75rem" }}>
          Lançamento: {date}
        </Typography>
      </Box>
    </Box>
  );
}
