import type { Pendencia } from "../types";
import type { UsuarioLogado } from "../contexts/AuthContext";

function esc(s: string | number | undefined | null): string {
  if (s == null) return "";
  const t = String(s);
  return t
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function formatNumero(numero: string | number | undefined | null): string {
  if (numero == null) return "";
  const raw = String(numero).trim();
  // Se for só dígitos, preenche à esquerda até 4 casas
  if (/^\d+$/.test(raw)) {
    return raw.padStart(4, "0");
  }
  return raw;
}

function formatData(data: string | undefined): string {
  if (!data) return "—";
  try {
    return new Date(data).toLocaleDateString("pt-BR");
  } catch {
    return data;
  }
}

function formatDataHora(data: string | undefined): string {
  if (!data) return "—";
  try {
    return new Date(data).toLocaleString("pt-BR");
  } catch {
    return data;
  }
}

function prazoFinal(dataCriacao: string | undefined, prazoResposta: number | undefined): string {
  if (!dataCriacao || prazoResposta == null) return "—";
  try {
    const d = new Date(dataCriacao);
    d.setDate(d.getDate() + prazoResposta);
    return d.toLocaleDateString("pt-BR");
  } catch {
    return "—";
  }
}

/**
 * Gera HTML do relatório de pendências ativas e abre a impressão em iframe (paisagem A4).
 * Pendências ativas = situacao !== "Finalizada".
 */
export function printRelatorioPendenciasAtivas(
  pendencias: Pendencia[],
  usuario: UsuarioLogado | null,
  setoresMap: Map<number, string>
): void {
  const agora = new Date();
  const dataHora = formatDataHora(agora.toISOString());
  const data = agora.toLocaleDateString("pt-BR");
  const hora = agora.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit", second: "2-digit" });

  const rows = pendencias
    .map(
      (p) => `
    <tr>
      <td>${esc(formatNumero(p.numero ?? p.id))}</td>
      <td>${formatData(p.data ?? p.dataCriacao)}</td>
      <td>${prazoFinal(p.dataCriacao, p.prazoResposta)}</td>
      <td>${esc(p.descricao ?? "")}</td>
      <td>${esc(p.situacao)}</td>
      <td>${esc(p.prioridade)}</td>
      <td>${p.idSetor != null ? esc(setoresMap.get(p.idSetor) ?? `Setor #${p.idSetor}`) : "—"}</td>
      <td>${p.atrasada ? "Atrasada" : "NO PRAZO"}</td>
    </tr>`
    )
    .join("");

  const setorUsuario =
    usuario?.idSetor != null
      ? setoresMap.get(usuario.idSetor) ?? `Setor #${usuario.idSetor}`
      : "—";

  const html = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>Relatório de Pendências Ativas</title>
  <style>
    @page { size: A4 landscape; margin: 12mm; }
    body {
      font-family: "Plus Jakarta Sans", -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 11px;
      padding: 0;
      margin: 0;
      color: #1a1a1a;
    }
    .header {
      margin-bottom: 14px;
      padding-bottom: 10px;
      border-bottom: 1px solid #ddd;
    }
    .title { font-size: 16px; font-weight: 700; margin: 0 0 10px 0; }
    .who-printed { background: #f8f9fa; padding: 10px 12px; margin-bottom: 10px; border-radius: 4px; border: 1px solid #eee; }
    .who-printed h2 { font-size: 12px; font-weight: 700; margin: 0 0 8px 0; color: #333; }
    .meta { color: #555; margin: 3px 0; }
    .meta strong { margin-right: 6px; min-width: 140px; display: inline-block; }
    table { width: 100%; border-collapse: collapse; }
    th, td { border: 1px solid #ccc; padding: 6px 8px; text-align: left; }
    th { background: #f5f5f5; font-weight: 600; font-size: 10px; }
    tr:nth-child(even) { background: #fafafa; }
  </style>
</head>
<body>
  <div class="header">
    <h1 class="title">Relatório de Pendências Ativas</h1>
    <div class="who-printed">
      <h2>Quem imprimiu</h2>
      <p class="meta"><strong>ID do usuário:</strong> ${usuario?.id != null ? esc(usuario.id) : "—"}</p>
      <p class="meta"><strong>Nome:</strong> ${esc(usuario?.nomeUsuario ?? "—")}</p>
      <p class="meta"><strong>E-mail:</strong> ${esc(usuario?.emailUsuario ?? "—")}</p>
      <p class="meta"><strong>Setor:</strong> ${esc(setorUsuario)}</p>
      <p class="meta"><strong>Cargo:</strong> ${esc(usuario?.cargoUsuario ?? "—")}</p>
      <p class="meta"><strong>Nível (acesso):</strong> ${usuario?.nivelUsuario != null ? esc(usuario.nivelUsuario) : "—"}</p>
    </div>
    <p class="meta"><strong>Data:</strong> ${data}</p>
    <p class="meta"><strong>Hora:</strong> ${hora}</p>
    <p class="meta"><strong>Data e hora completas:</strong> ${dataHora}</p>
    <p class="meta"><strong>Total de pendências ativas:</strong> ${pendencias.length}</p>
  </div>
  <table>
    <thead>
      <tr>
        <th>N°</th>
        <th>Data</th>
        <th>Prazo</th>
        <th>Descrição</th>
        <th>Situação</th>
        <th>Prioridade</th>
        <th>Setor atual</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      ${rows.length ? rows : "<tr><td colspan=\"8\" style=\"text-align:center\">Nenhuma pendência ativa</td></tr>"}
    </tbody>
  </table>
</body>
</html>`;

  const iframe = document.createElement("iframe");
  iframe.setAttribute("style", "position:absolute;width:0;height:0;border:0;visibility:hidden");
  document.body.appendChild(iframe);

  const doc = iframe.contentWindow?.document;
  if (!doc) {
    document.body.removeChild(iframe);
    return;
  }

  doc.open();
  doc.write(html);
  doc.close();

  iframe.contentWindow?.focus();
  iframe.contentWindow?.print();

  const removeIframe = () => {
    try {
      if (iframe.parentNode) document.body.removeChild(iframe);
    } catch {
      // ignore
    }
  };

  iframe.contentWindow?.addEventListener("afterprint", removeIframe);
  setTimeout(removeIframe, 1000);
}
