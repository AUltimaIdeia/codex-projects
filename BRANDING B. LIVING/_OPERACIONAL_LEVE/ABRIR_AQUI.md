# B. Living - Workspace Operacional Leve

Use esta pasta como raiz do projeto no Codex quando quiser produzir novos materiais da B. Living sem travamentos.

Este workspace contem somente arquivos pequenos e operacionais. O acervo pesado continua preservado em:

`C:\Users\BRANDING B. LIVING`

## Ordem de abertura

1. `00-entrada/CONTINUAR_AQUI_B_LIVING.md`
2. `05-fonte-oficial/FONTE_OFICIAL_PRODUCAO_B_LIVING.md`
3. `05-fonte-oficial/DIRETRIZES_PARA_NOVOS_MATERIAIS.md`
4. `05-fonte-oficial/PROTOCOLO_DE_CONSISTENCIA_VISUAL.md`
5. `05-fonte-oficial/BRIEF_BASE_LANDING_PAGE.md`
6. `01-estrategia/PRODUCT.md`
7. `01-estrategia/DESIGN.md`
8. `03-brandbook/brandbook-b-living-editorial-copy.md`
9. `99-mapa-acervo/MAPA_DE_ATIVOS.md`

## Fase atual

O brandbook deve ser tratado como finalizado para fins de producao.

O foco agora e criar materiais derivados com o mesmo nivel de qualidade:

- landing page;
- paginas comerciais;
- apresentacoes;
- posts e campanhas;
- materiais institucionais;
- pecas para corretores.

Qualquer nova peca deve seguir a fonte oficial de producao em `05-fonte-oficial`.

Regra fixa para geracao e validacao de imagens:

- usar sempre a logo oficial em SVG, nunca uma assinatura digitada ou simulada;
- em fundo escuro, priorizar `B. LIVING LOGO - BEGE CLARO.svg`;
- toda chamada em fonte serifada/display deve estar em CAIXA ALTA;
- se a IA nao aplicar logo ou tipografia com fidelidade, gerar apenas a base visual e aplicar logo/tipo depois em HTML/CSS, Canva, Figma ou ferramenta equivalente.

Para validar consistencia visual, nao use imagem gerada por prompt como prova final. Use primeiro um layout renderizado em HTML/CSS com tokens e logo real. O teste inicial esta em:

`06-testes-visuais/consistencia-landing-preview/index.html`

O segundo teste, mais proximo de uma landing real, esta em:

`06-testes-visuais/teste-02-landing-home-real/index.html`

## Regra de uso

Nao abrir nem buscar em massa dentro de `brandbook-toolkit`, `paginas-curadas`, `06-Imagens`, `02-Logos` ou previews PNG. Quando precisar de visual, consulte primeiro `99-mapa-acervo/MAPA_DE_ATIVOS.md`.
