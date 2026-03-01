# Sistema de Consulta de Livros para Biblioteca

Aplicação web **autocontida** em HTML + CSS + JavaScript puro para consulta de livros por **ISBN**, **EAN** ou **Título**.

## Recursos implementados

- Busca por ISBN/EAN/Título com abas de seleção
- Integração com:
  - Google Books API
  - Open Library API
- Combinação de dados entre APIs (fallback de campos)
- Lista em cards para busca por título
- Modal de detalhes com:
  - Título/subtítulo
  - Autores
  - Editora
  - Data
  - Páginas
  - ISBN-10/ISBN-13
  - Categorias
  - Idioma
  - Sinopse
  - Capa (ou placeholder estilizado)
  - Avaliação média
  - Link de prévia
- Loading spinner durante buscas
- Mensagens amigáveis para erros/sem resultados
- Histórico de buscas com `localStorage` + limpar histórico
- Botão copiar ISBN
- Botão imprimir ficha
- Busca por título com debounce de 500ms
- Scanner de código de barras com câmera (ZXing via CDN)
- Suporte offline-friendly após primeiro carregamento (Service Worker)

## Estrutura

- `index.html`: aplicação completa (UI + lógica)
- `sw.js`: cache para shell da aplicação

## Como usar

1. Abra `index.html` em um navegador moderno.
2. Escolha o tipo de busca (ISBN, EAN ou Título).
3. Digite o termo e clique em **Buscar** (ou use Enter).
4. Para título, escolha um card para abrir detalhes.
5. Use **Escanear** para ler código de barras pela câmera.

## Exemplos de teste

- `9788535902778`
- `9780141439518`
- `O Pequeno Príncipe`

## Observações

- O modo offline funciona para os arquivos estáticos após o primeiro carregamento.
- As consultas às APIs externas exigem internet.
- O scanner depende de permissão de câmera e HTTPS (ou `localhost`).
