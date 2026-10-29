// Estado da demonstração: o caso escolhido (ficha do motor) e as escolhas do cliente.
import { createContext, ReactNode, useContext, useState } from "react";
import { FICHAS } from "../dados/contrato";
import { ACIMA_DO_PADRAO, BASE, COB, Cob, DESCONTO, FIXAS, PACOTE, PLANOS, Plano } from "./produto";
import { cobFicha, OPCOES, temAdicional } from "./textos";

const FD: any = FICHAS;
export type Pagamento = "DEBITO" | "CARTAO" | "PIX";
type Valores = Record<Cob, number>;
type Ligadas = Record<Cob, boolean>;
export type CampoEditavel = "tipo" | "uso" | "endereco" | "vinculo" | "bens";
/** Valor que veio do banco para cada campo editável do Passo 1. */
export const DO_BANCO: Record<CampoEditavel, (f: any) => string> = { tipo: (f) => f.campos.tipo.valor, uso: (f) => f.campos.uso.valor, endereco: () => "BANCO", vinculo: (f) => f.campos.vinculo.valor, bens: () => "FAIXA" };

export type Estado = {
  caso: string; f: any; plano: Plano; rec: Plano;
  valores: Valores; ligadas: Ligadas; faixa: Record<Cob, [number, number] | null>;
  resp: Record<string, string>; edicoes: Partial<Record<CampoEditavel, string>>; vig: number; entend: [boolean, boolean]; ajustada: boolean; pagamento: Pagamento;
};

function sugerido(k: Cob, fx: [number, number] | null) {
  // valor sugerido: meio da faixa do motor (o mínimo deixa subseguro), no passo e dentro do limite do produto
  const P = COB[k], meio = fx ? (fx[0] + fx[1]) / 2 : P.padrao;
  return Math.min(P.max, Math.max(P.min, Math.round(meio / P.passo) * P.passo));
}

export function estadoDoCaso(caso: string): Estado {
  const f = FD.fichas[FD.casos[caso]];
  const faixa = {} as Estado["faixa"], valores = {} as Valores, ligadas = {} as Ligadas;
  (Object.keys(COB) as Cob[]).forEach((k) => {
    const c = cobFicha(f, k);
    faixa[k] = c ? [c.min, c.max] : null;
    valores[k] = sugerido(k, faixa[k]);
    ligadas[k] = true;
  });
  ligadas.rc = f.plano === "TOTAL" || temAdicional(f, "rc");
  return { caso, f, plano: f.plano, rec: f.plano, valores, ligadas, faixa, resp: {}, edicoes: {}, vig: 1, entend: [false, false], ajustada: false, pagamento: "DEBITO" };
}

/** Tipo e uso valem o que o cliente escolheu; o resto vem do banco. */
export const tipoAtual = (s: Estado) => s.edicoes.tipo || s.f.campos.tipo.valor;
export const usoAtual = (s: Estado) => s.edicoes.uso || s.f.campos.uso.valor;
/** Quantos dados do banco o cliente trocou (cada um baixa a confiança da análise). */
export const mudancas = (s: Estado) => (Object.keys(s.edicoes) as CampoEditavel[]).filter((k) => s.edicoes[k] && s.edicoes[k] !== DO_BANCO[k](s.f)).length;
/** Perguntas que continuam na tela: as que repetem um campo editável ou pedem a área (que o cliente não sabe de cabeça) saem. */
export const perguntasDaTela = (f: any) => f.perguntas.filter((p: any) => !["BENS", "AREA", "USO", "VINCULO", "TIPO"].includes(p.codigo));

export const sugeridoDe = (s: Estado, k: Cob) => sugerido(k, s.faixa[k]);

export function incluidas(s: Estado, plano: Plano = s.plano): Cob[] {
  const l = [...FIXAS, ...PLANOS[plano].extras];
  if (plano !== "TOTAL" && s.ligadas.rc && !l.includes("rc")) l.push("rc");
  return l;
}
export function preco(s: Estado, plano: Plano = s.plano, valores: Valores = s.valores, ligadas: Ligadas = s.ligadas) {
  const custo = (k: Cob) => (COB[k].taxa * (Math.min(valores[k], COB[k].padrao) + ACIMA_DO_PADRAO * Math.max(0, valores[k] - COB[k].padrao))) / 1000;
  const p = PLANOS[plano];
  let v = BASE + p.pacotes * PACOTE;
  FIXAS.forEach((k) => (v += custo(k)));
  p.extras.forEach((k) => { if (ligadas[k]) v += custo(k); });
  if (plano !== "TOTAL" && ligadas.rc) v += custo("rc");
  return v;
}
/** Coberturas que o cliente pode ligar e desligar no plano: ficam na lista mesmo desligadas. */
export function opcionais(s: Estado, plano: Plano = s.plano): Cob[] {
  const l = [...PLANOS[plano].extras];
  if (plano !== "TOTAL" && temAdicional(s.f, "rc")) l.push("rc");
  return l;
}
/** O cliente mexeu no plano (valor diferente do sugerido ou cobertura desligada)? */
/** Quem ajustou: o gerente (proposta revisada) ou o próprio cliente (Personalizar). */
export const quemAjustou = (s: Estado): "gerente" | "cliente" | null => (s.ajustada ? "gerente" : ajustado(s) ? "cliente" : null);

export function ajustado(s: Estado): boolean {
  if (s.ajustada) return true;
  const rcPadrao = s.plano === "TOTAL" || temAdicional(s.f, "rc");
  if (opcionais(s).some((k) => (k === "rc" ? s.ligadas.rc !== rcPadrao : s.ligadas[k] === false))) return true;
  return [...FIXAS, ...opcionais(s)].some((k) => s.ligadas[k] !== false && s.valores[k] !== sugeridoDe(s, k));
}
export const precoFinal = (s: Estado) => preco(s) * (1 - DESCONTO[s.vig]);

/** O que o gerente ajusta: confirma as estimativas e sobe vidros e roubo para o máximo da faixa do motor. */
export function comAjusteDoGerente(s: Estado): Estado {
  if (s.ajustada) return s;
  const resp = { ...s.resp }, valores = { ...s.valores };
  s.f.perguntas.forEach((p: any) => { if (!resp[p.codigo]) resp[p.codigo] = (OPCOES[p.codigo] || ["Sim"])[0]; });
  (["vidros", "roubo"] as Cob[]).forEach((k) => {
    const fx = s.faixa[k];
    if (fx && incluidas(s).includes(k)) valores[k] = Math.min(COB[k].max, Math.round(fx[1] / COB[k].passo) * COB[k].passo);
  });
  return { ...s, resp, valores, ajustada: true };
}

const Ctx = createContext<{ s: Estado; set: (fn: (s: Estado) => Estado) => void; casos: Record<string, string> } | null>(null);

export function ProvedorEstado({ children }: { children: ReactNode }) {
  const [s, setS] = useState(() => estadoDoCaso("perfil_A_apto_urbano"));
  return <Ctx.Provider value={{ s, set: (fn) => setS(fn), casos: FD.casos }}>{children}</Ctx.Provider>;
}
export function useEstado() {
  const c = useContext(Ctx);
  if (!c) throw new Error("ProvedorEstado ausente");
  return c;
}
