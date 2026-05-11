# Exemplo Rejeitado - Imagem 1 Gerada

Arquivo original analisado:

`C:\Users\vini1\OneDrive\Área de Trabalho\Imagem 1 gerada.png`

## Status

Rejeitado como referencia de consistencia visual.

## Motivo

A imagem capturou alguns sinais superficiais da B. Living, mas criou uma estetica paralela. Ela nao deve orientar landing page, post, apresentacao ou peca comercial.

## Problemas observados

- Usa "Playfair Display" e "Suisse Intl" como se fossem fontes oficiais. O sistema oficial usa didone editorial com Bodoni Moda/Bodoni/Didot como familia de display e Montserrat/Avenir/Helvetica/Segoe como apoio.
- Usa fonte serifada/display em caixa mista. A regra atual de producao exige que toda chamada serifada/display esteja em CAIXA ALTA.
- Apresenta uma paleta em hex como se fosse oficial. A fonte oficial esta em OKLCH no `DESIGN.md` e no `DESIGN.json`.
- Recria ou simula assinatura visual em vez de obrigar uso dos SVGs reais.
- Parece uma prancha generica de "brand book extension", nao uma aplicacao fiel do brandbook finalizado.
- Usa mapa e divisorias como estetica de luxo imobiliario, sem garantir a logica de decisao antes do imovel.
- O resultado e bonito, mas nao e confiavel como sistema de producao.

## Correcao

Para tranquilizar sobre consistencia, gerar uma imagem apenas a partir de um layout controlado em HTML/CSS ou Figma, usando:

- tokens reais;
- logo real;
- fonte oficial com chamadas serifadas/display em CAIXA ALTA;
- grid oficial;
- copy oficial;
- checklist de rejeicao.
