// Ilustrações finais em PNG, geradas pelo time com assets/ilustracoes/PROMPT_ChatGPT.md.
// Enquanto um arquivo não existe, a tela usa o desenho em SVG de ilustracoes.tsx (nada quebra).
// Para ligar uma imagem: salve o PNG em assets/ilustracoes/ com o nome da tabela do prompt
// e descomente a linha dela abaixo. O require precisa ser literal (o Metro empacota na hora).

export type NomeImagem =
  | "heroi_entrada" | "casa_protegida" | "gerente_ricardo" | "gerente_painel"
  | "cena_agua" | "cena_raio" | "cena_vizinho_apto" | "cena_vizinho_casa" | "cena_roubo" | "cena_vidros"
  | "cena_vento_apto" | "cena_vento_casa" | "cena_fogo" | "cena_impacto" | "cena_aluguel" | "cena_despesas";

// require() de um PNG devolve um número (o id do recurso empacotado)
export const IMAGENS: Partial<Record<NomeImagem, number>> = {
  // heroi_entrada: require("../../assets/ilustracoes/heroi_entrada.png"),
  // casa_protegida: require("../../assets/ilustracoes/casa_protegida.png"),
  // gerente_ricardo: require("../../assets/ilustracoes/gerente_ricardo.png"),
  // gerente_painel: require("../../assets/ilustracoes/gerente_painel.png"),
  // cena_agua: require("../../assets/ilustracoes/cena_agua.png"),
  // cena_raio: require("../../assets/ilustracoes/cena_raio.png"),
  // cena_vizinho_apto: require("../../assets/ilustracoes/cena_vizinho_apto.png"),
  // cena_vizinho_casa: require("../../assets/ilustracoes/cena_vizinho_casa.png"),
  // cena_roubo: require("../../assets/ilustracoes/cena_roubo.png"),
  // cena_vidros: require("../../assets/ilustracoes/cena_vidros.png"),
  // cena_vento_apto: require("../../assets/ilustracoes/cena_vento_apto.png"),
  // cena_vento_casa: require("../../assets/ilustracoes/cena_vento_casa.png"),
  // cena_fogo: require("../../assets/ilustracoes/cena_fogo.png"),
  // cena_impacto: require("../../assets/ilustracoes/cena_impacto.png"),
  // cena_aluguel: require("../../assets/ilustracoes/cena_aluguel.png"),
  // cena_despesas: require("../../assets/ilustracoes/cena_despesas.png"),
};

/** Nome da imagem da situação do Passo 2 (vizinho e vento mudam entre apê e casa). */
export const imagemDaCena = (id: string, predio: boolean): NomeImagem =>
  (id === "vizinho" || id === "vento" ? `cena_${id}_${predio ? "apto" : "casa"}` : `cena_${id}`) as NomeImagem;
