// 4/5 · Personalizar: lista compacta; um toque abre o campo para digitar o valor exato,
// dentro do limite do produto, com atalhos (mínimo, sugerido, máximo). Sem barra deslizante.
import { Feather } from "@expo/vector-icons";
import { router } from "expo-router";
import { useState } from "react";
import { Pressable, TextInput, View } from "react-native";
import Animated, { FadeIn, FadeOut, LinearTransition } from "react-native-reanimated";
import { ajustado, Estado, incluidas, opcionais, preco, sugeridoDe, useEstado } from "@/logica/estado";
import { SeloAjustado , Botao, Chave, Contador, Entra, haptic, Rotulo, T, Titulo, Toque } from "@/ui/base";
import { COB, Cob, FIXAS, PLANOS } from "@/logica/produto";
import { aprox, brl, brl2, ehApto, entre } from "@/logica/textos";
import { useAjuda } from "@/ui/ajuda";
import { Tela } from "@/ui/tela";
import { useFolha } from "@/ui/folha";
import { C, F, SOMBRA } from "@/ui/tema";

const REFLUXO = LinearTransition.duration(240);
const ABRE = FadeIn.duration(200).delay(60), FECHA = FadeOut.duration(120);

function dica(s: Estado, k: Cob) {
  const fx = s.faixa[k], v = s.valores[k];
  if (k === "incendio" && fx && v < fx[0]) return { t: `Abaixo de ${aprox(fx[0])}, um incêndio grande deixaria parte do prejuízo com você.`, alerta: true };
  if (fx && v < fx[0]) return { t: `Abaixo da faixa calculada para o seu imóvel (${entre(fx[0], fx[1])}). Num sinistro, parte pode ficar com você.`, alerta: true };
  if (fx && v > fx[1] * 1.25) return { t: "Acima do que calculamos para o seu imóvel. Você pagaria por uma proteção que talvez não use.", alerta: false };
  if (k === "incendio") return { t: `Reconstruir ${ehApto(s.f) ? "pisos, armários e acabamentos" : "a casa"} e repor os bens custa ${fx ? entre(fx[0], fx[1]) : "o valor do imóvel"}.`, alerta: false };
  return { t: fx ? "Dentro da faixa calculada para o seu imóvel." : COB[k].desc, alerta: false };
}

function Linha({ k, opcional, aberta, onAbrir, ultima }: { k: Cob; opcional: boolean; aberta: boolean; onAbrir: () => void; ultima: boolean }) {
  const { s, set } = useEstado();
  const P = COB[k], fx = s.faixa[k], on = s.ligadas[k] !== false;
  const [texto, setTexto] = useState(s.valores[k].toLocaleString("pt-BR"));
  const [erro, setErro] = useState(false);
  const definir = (n: number) => {
    const v = Math.min(P.max, Math.max(P.min, Math.round(n / P.passo) * P.passo));
    setTexto(v.toLocaleString("pt-BR")); setErro(false);
    set((x) => ({ ...x, valores: { ...x.valores, [k]: v } }));
  };
  const digitar = (t: string) => {
    const n = +t.replace(/\D/g, "");
    setTexto(n ? n.toLocaleString("pt-BR") : "");
    const fora = n < P.min || n > P.max;
    setErro(fora);
    if (!fora) set((x) => ({ ...x, valores: { ...x.valores, [k]: n } }));
  };
  const d = erro ? { t: `Use um valor entre ${brl(P.min)} e ${brl(P.max)}.`, alerta: true } : dica(s, k);

  return (
    <Animated.View layout={REFLUXO} style={{ borderBottomWidth: ultima ? 0 : 1, borderBottomColor: "#EEF0F3" }}>
      <View style={{ flexDirection: "row", alignItems: "center", gap: 12, paddingHorizontal: 16, paddingVertical: 14 }}>
        {opcional ? <Chave on={on} onChange={() => set((x) => ({ ...x, ligadas: { ...x.ligadas, [k]: !x.ligadas[k] } }))} /> : null}
        <Pressable style={{ flex: 1 }} onPress={() => { haptic.toque(); onAbrir(); }}>
          <T s={{ fontFamily: F.b, fontSize: 15.5, color: on ? C.texto : C.suave }}>{P.curto}</T>
          <T s={{ fontSize: 12.5, color: C.suave }}>{fx ? "Para seu imóvel: " + entre(fx[0], fx[1]) : P.desc}</T>
        </Pressable>
        <Pressable onPress={() => { haptic.toque(); onAbrir(); }} style={{ flexDirection: "row", alignItems: "center", gap: 4 }} hitSlop={8}>
          <T s={{ fontFamily: F.x, fontSize: 15.5, color: on ? C.azulEscuro : "#A3A7AE", textDecorationLine: on ? "none" : "line-through" }}>{brl(s.valores[k])}</T>
          <Feather name={aberta ? "chevron-up" : "chevron-down"} size={18} color={C.azulEscuro} />
        </Pressable>
      </View>
      {aberta ? (
        <Animated.View entering={ABRE} exiting={FECHA} style={{ paddingHorizontal: 16, paddingBottom: 16 }}>
          <View style={{ flexDirection: "row", alignItems: "center", height: 52, borderRadius: 12, backgroundColor: C.fundo, borderWidth: 1.5, borderColor: erro ? C.vermelho : C.azul, paddingHorizontal: 14 }}>
            <T s={{ fontFamily: F.b, fontSize: 17, color: C.suave, marginRight: 6 }}>R$</T>
            <TextInput value={texto} onChangeText={digitar} onBlur={() => definir(+texto.replace(/\D/g, "") || s.valores[k])} onSubmitEditing={() => definir(+texto.replace(/\D/g, "") || s.valores[k])}
              keyboardType="number-pad" returnKeyType="done" autoFocus selectTextOnFocus style={{ flex: 1, fontFamily: F.x, fontSize: 20, color: C.texto, outlineStyle: "none" } as any} />
          </View>
          <View style={{ flexDirection: "row", justifyContent: "space-between", marginVertical: 8 }}>
            <T s={{ fontSize: 12.5, color: C.suave }}>mín. {brl(P.min)}</T><T s={{ fontSize: 12.5, color: C.suave }}>máx. {brl(P.max)}</T>
          </View>
          <View style={{ flexDirection: "row", gap: 8 }}>
            {[["Mínimo", P.min], ["Sugerido", sugeridoDe(s, k)], ["Máximo", P.max]].map(([n, v]) => (
              <Toque key={n as string} onPress={() => { haptic.toque(); definir(v as number); }} style={{ flex: 1, alignItems: "center", paddingVertical: 9, borderRadius: 10, backgroundColor: C.azulClaro }}>
                <T s={{ fontFamily: F.b, fontSize: 13.5, color: C.azulEscuro }}>{n as string}</T>
              </Toque>
            ))}
          </View>
          <T s={{ fontSize: 13, lineHeight: 18, color: d.alerta ? C.vermelho : C.suave, marginTop: 9 }}>{d.t}</T>
        </Animated.View>
      ) : null}
    </Animated.View>
  );
}

export default function Ajuste() {
  const { s, set } = useEstado();
  const ajuda = useAjuda("ajuste");
  const folha = useFolha();
  const [aberta, setAberta] = useState<Cob | null>(null);
  const fixas = incluidas(s).filter((k) => FIXAS.includes(k)), extras = opcionais(s);
  const sugeridos = Object.fromEntries((Object.keys(COB) as Cob[]).map((k) => [k, sugeridoDe(s, k)])) as Estado["valores"];
  const dif = preco(s) - preco(s, s.plano, sugeridos, Object.fromEntries((Object.keys(COB) as Cob[]).map((k) => [k, true])) as Estado["ligadas"]);
  const vira = s.plano === "PRATICO" && !s.ligadas.roubo && !s.ligadas.vidros;
  const abrir = (k: Cob) => setAberta(aberta === k ? null : k);

  return (
    <Tela passo={4} rotulo="Personalizar" fala={`Ajuste do seu jeito. Plano ${PLANOS[s.plano].nome}, 12 vezes de ${brl2(preco(s))}. Toque num valor para mudar.`} onVoltar={() => router.back()} onFechar={() => router.dismissAll()} onAjuda={ajuda}
      rodape={<>
        <View style={{ flexDirection: "row", justifyContent: "space-between", alignItems: "center" }}>
          <View><View style={{ flexDirection: "row", alignItems: "center", gap: 6 }}><T s={{ fontSize: 13, color: C.suave }}>Plano {PLANOS[s.plano].nome} · 12x de</T>{ajustado(s) ? <SeloAjustado gerente={s.ajustada} /> : null}</View>
            <T s={{ fontSize: 12.5, fontFamily: F.b, color: Math.abs(dif) < 0.01 ? C.suave : dif > 0 ? C.azulEscuro : C.positivo }}>{Math.abs(dif) < 0.01 ? "valores sugeridos" : `${dif > 0 ? "+" : "−"}${brl2(Math.abs(dif))} do sugerido`}</T></View>
          <Contador valor={preco(s)} fmt={brl2} s={{ fontFamily: F.k, fontSize: 24, lineHeight: 30, color: C.azulEscuro }} />
        </View>
        <Botao titulo="Salvar e avançar" onPress={() => router.push("/conferir")} />
      </>}>
      <Titulo antes="Ajuste do " destaque="seu jeito" />
      <Entra i={1}><T s={{ color: C.suave, fontSize: 15.5, marginBottom: 4 }}>Toque num valor para mudar. Já sugerimos o meio da faixa calculada para o seu imóvel.</T></Entra>
      {vira ? (
        <Animated.View entering={FadeIn.duration(200)} exiting={FadeOut.duration(150)} layout={REFLUXO} style={{ flexDirection: "row", gap: 10, backgroundColor: C.ambarClaro, borderRadius: 14, padding: 14, marginTop: 12 }}>
          <Feather name="alert-triangle" size={18} color={C.ambar} />
          <T s={{ flex: 1, fontSize: 14, color: "#5f3e00" }}>Sem roubo e sem vidros, o Prático fica igual ao Essencial, que custa {brl2(preco(s) - preco(s, "ESSENCIAL"))} a menos por mês.</T>
          <Toque onPress={() => { set((x) => ({ ...x, plano: "ESSENCIAL", ligadas: { ...x.ligadas, roubo: true, vidros: true } })); folha.toast("Plano trocado para o Essencial"); }}>
            <T s={{ fontFamily: F.x, fontSize: 14, color: C.azulEscuro, textDecorationLine: "underline" }}>Trocar</T>
          </Toque>
        </Animated.View>
      ) : null}
      <Animated.View layout={REFLUXO}><Rotulo>Coberturas do plano · não saem</Rotulo></Animated.View>
      <Animated.View layout={REFLUXO} style={{ backgroundColor: C.branco, borderRadius: 16, ...SOMBRA }}>
        {fixas.map((k, i) => <Linha key={k + s.caso} k={k} opcional={false} aberta={aberta === k} onAbrir={() => abrir(k)} ultima={i === fixas.length - 1} />)}
      </Animated.View>
      {extras.length ? <>
        <Animated.View layout={REFLUXO}><Rotulo>Coberturas que você pode tirar</Rotulo></Animated.View>
        <Animated.View layout={REFLUXO} style={{ backgroundColor: C.branco, borderRadius: 16, ...SOMBRA }}>
          {extras.map((k, i) => <Linha key={k + s.caso} k={k} opcional aberta={aberta === k} onAbrir={() => abrir(k)} ultima={i === extras.length - 1} />)}
        </Animated.View>
      </> : null}
    </Tela>
  );
}
