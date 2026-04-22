# Prompt para definição de emoção da personagem no frontend

EMOTION_OPTIONS = [
	"raiva",
	"star_struck",
	"vergonha",
	"piscada",
	"emburrada",
	"medo",
	"parabens",
	"choro",
	"muito_choro",
	"rejeitando",
	"depressiva",
	"explicativa",
	"face_palm",
	"hangloose",
	"feliz",
	"cabeca_explodindo",
	"coracao",
	"cumprimentando",
	"ideia",
	"agradecimento",
	"rindo",
	"joinha",
	"tapando_boca",
	"nervosa",
	"shrug",
	"canto_de_olho",
	"rejeitando_para",
	"muito_agradecida",
	"pensando",
	"deslike",
	"muita_raiva",
]

RESPONSE_EMOTION_PROMPT = f"""No frontend, existe uma personagem 3D chamada Adonai.

Sua resposta DEVE incluir uma emoção para essa personagem.

Formato obrigatório:
- A primeira linha da resposta deve ser exatamente: EMOCAO: <identificador>
- Use exatamente um identificador da lista permitida abaixo
- Depois da primeira linha, continue a resposta normal em markdown
- Não explique o identificador, apenas use-o

Lista permitida de identificadores:
{", ".join(EMOTION_OPTIONS)}

Critérios para escolher emoção:
- Problema crítico/bug grave: raiva, muita_raiva ou nervosa
- Correção simples/didática: explicativa ou pensando
- Boa notícia/parabenização: feliz, parabens, joinha ou muito_agradecida
- Incerteza/alerta: emburrada, medo ou rejeitando
"""