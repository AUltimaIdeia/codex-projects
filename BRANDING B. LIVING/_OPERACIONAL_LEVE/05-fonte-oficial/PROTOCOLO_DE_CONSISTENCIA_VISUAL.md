# Protocolo De Consistencia Visual - B. Living

Este protocolo existe para impedir que uma nova peca pareca uma interpretacao generica do brandbook.

## Regra central

Nao validar consistencia visual da B. Living com imagem gerada livremente por prompt.

Para materiais importantes, a validacao deve nascer de layout controlado: HTML/CSS, Figma, Canva ou ferramenta equivalente, usando tokens oficiais, logo real e diretrizes escritas.

## Por que

Prompts visuais tendem a capturar palavras como "premium", "azul", "imobiliaria", "brandbook" e "landing page", mas podem inventar:

- fonte;
- logo;
- paleta;
- data;
- versao;
- grid;
- mockup;
- clima de marca.

Isso cria uma estetica paralela. Bonita, mas perigosa.

## Ordem segura

1. Ler `FONTE_OFICIAL_PRODUCAO_B_LIVING.md`.
2. Ler `DIRETRIZES_PARA_NOVOS_MATERIAIS.md`.
3. Usar `../01-estrategia/DESIGN.json` como tokens.
4. Usar logos reais apontados em `referencias-textuais/README-LOGOS.md`.
5. Criar a peca em layout editavel.
6. Renderizar uma imagem somente depois do layout estar construido.
7. Rejeitar qualquer resultado que invente fonte, logo, paleta ou linguagem.

## Travas obrigatorias

- Fonte display oficial: Bodoni Moda, Bodoni 72, Didot, Bodoni MT, Georgia, Times New Roman, serif.
- Todo uso de fonte display/serifada em imagens, capas, headers, pranchas e testes visuais deve estar em CAIXA ALTA.
- Fonte de apoio oficial: Montserrat, Avenir Next, Helvetica Neue, Segoe UI, Arial, sans-serif.
- Paleta oficial: usar os tokens de `DESIGN.json` e `DESIGN.md`.
- Logo: usar SVG real do acervo, nao recriar assinatura por texto. Em fundo escuro, usar preferencialmente `B. LIVING LOGO - BEGE CLARO.svg`.
- Brass: detalhe fino, nunca bloco dominante.
- Imovel: consequencia da tese, nao vitrine inicial.
- Florianopolis: territorio estrategico, nao cartao-postal turistico.

## Criterios de rejeicao imediata

Rejeite a peca se ela:

- usa Playfair Display, Suisse Intl ou outra fonte inventada como oficial;
- usa fonte serifada/display em caixa baixa ou caixa mista em chamadas principais;
- apresenta paleta em hexadecimal inventada como se fosse oficial;
- recria o logo em texto em vez de usar o SVG real;
- omite a logo oficial quando a peca deveria validar identidade;
- parece prancha de "brandbook extension" generica;
- coloca mapa turistico como elemento principal sem estrategia;
- parece imobiliaria premium comum;
- usa dourado/brass como acabamento de luxo;
- adiciona versao, data ou assinatura que nao existe no brandbook.

## Teste seguro para landing page

Teste 01, prancha de consistencia:

`../06-testes-visuais/consistencia-landing-preview/index.html`

Teste 02, primeira dobra de landing real:

`../06-testes-visuais/teste-02-landing-home-real/index.html`

Os testes sao editaveis e nao sao pecas finais. O objetivo e provar que a identidade pode ser aplicada com controle antes de produzir a landing completa.
