SPLIT_PROMPT = """
Você recebe uma resposta de texto e deve reescrevê-la como uma sequência de mensagens de WhatsApp,
do jeito que uma pessoa real digitaria — várias mensagens curtas, não um parágrafo só.

Regras:
- Quebre por unidade de pensamento, não por frase gramatical.
- Máximo 4 mensagens. Não force quebra se a resposta já for curta.
- NÃO adicione conteúdo novo, só reorganize/quebre o que já está aqui.
- NÃO adicione pontuação final artificial nem emojis.

Resposta original:
{answer}
"""