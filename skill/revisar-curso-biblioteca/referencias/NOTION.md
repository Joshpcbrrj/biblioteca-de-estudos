# Notas técnicas do Notion

> Arquivo auxiliar da skill `revisar-curso-biblioteca`. Leia antes da primeira edição de página na sessão e sempre que uma chamada falhar.

- `update_content`: o `old_str` precisa ser texto exato e único, sem formatação cruzando o trecho. Para inserir algo no topo da página, **ancore no primeiro título/parágrafo** depois do breadcrumb (o `insert_content` com posição `start` coloca acima do breadcrumb).
- `insert_content` com posição `end` serve para o Resumo.
- Títulos de página: `update_properties` com `{"title": "texto limpo"}` (remove negrito herdado).
- Toggle heading: `heading="h3"` (não `"3"`).
- Em células de tabela, evite começar o texto com `+` (vira marcador). Escreva `<` e `>` diretamente; `&lt;` aparece literal em código.
- Para **mover uma página filha** no índice: num único `update_content`, apague a tag `<page url="...">Título</page>` de onde ela está e reinsira a mesma tag na posição desejada.
- Páginas novas não ganham breadcrumb pela API; avise o usuário que ele pode adicionar com `/breadcrumb`.
- Os arquivos anexados ao Notion não podem ser baixados direto da sessão (servidor bloqueado): para imagens existentes, use a exportação HTML descrita na Fase 6.
- Antes de mexer numa página, faça fetch; depois de várias edições, faça um fetch de conferência por amostragem.
- `+ ` logo depois de `</code>` ou no começo de uma célula vira marcador (`  •`). Escreva "e"/"com" no lugar; `<code>+</code>` sozinho funciona.
- Em `new_str`, sequências como `\u0000` são decodificadas e viram `�`. Evite escapes em texto (escreva por extenso, ex.: "caractere nulo"); quando a barra invertida for necessária (`%JAVA_HOME%\bin`), corrija depois com `update_content` em JSON, com a barra duplicada.
- Tags `<image source="notion-file-block://...">` não são encontradas pelo `update_content`, nem a tag inteira nem só o atributo `source` (a legenda dentro dela é encontrada, mas trocar a legenda não troca a imagem). Para trocar uma imagem existente: fetch da página, `notion-create-attachment` com o novo SVG e `replace_content` com o conteúdo completo da página trocando só a tag da imagem (mantenha breadcrumb, `<file>`, `<pdf>`, bookmarks e vídeos exatamente como vieram).
- Erro 502 no `replace_content`: faça fetch para ver se a página mudou e repita a chamada (o `file-upload://` continua válido até expirar).
- Bloco `<unknown url="...#id" />` sem `alt` que aponta para uma base de dados apagada (erro "Cannot create database reference" ou 500): o `replace_content` falha na página inteira. Reescreva a página por partes com vários `update_content` pequenos, sem incluir esse bloco em nenhum `old_str` (trechos que encostam nele também falham); ele fica invisível na página.
- `<details>`/`<summary>` no conteúdo enviado ao Notion são convertidos automaticamente em toggle; funciona, mas o Notion avisa. Nos títulos de toggle, escreva tipos genéricos com crase (`` `List<int>` ``): sem crase, `<int>` vira tag e quebra o XHTML do EPUB.
- O ícone `🖧` é recusado pela API ("Invalid page icon URL"); use emojis comuns.
- Para trocar muitas imagens, suba os SVGs por `source_url` com o link raw do GitHub fixado no hash do commit (`raw.githubusercontent.com/.../<hash>/...`): é mais leve que mandar o conteúdo. Faça uma página por vez (fetch → uploads → `replace_content`) e anote as páginas concluídas com `ferramentas/progresso.py`, para retomar depois de uma compactação de contexto sem refazer nada. Os links raw saem prontos de `ferramentas/raw_urls.py` (que também avisa se o commit ainda não foi enviado ao GitHub).
