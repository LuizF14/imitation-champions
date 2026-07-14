PERSONA_GENERATOR_PROMPT = """
Gere {n} personas humanas fictícias, brasileiras, para um bot de teste de conversação estilo Turing Test.

Regras:
- Personas devem ser DIVERSAS entre si: idade, cidade, profissão, personalidade, forma de falar.
- Evite estereótipos repetidos (nem toda persona precisa ser "descolada" ou "extrovertida").
- Inclua personas de diferentes regiões do Brasil (não só São Paulo/BH/RJ).
- "forma_de_escrever" deve ser algo bem específico e usável para prompting depois,
  não genérico tipo "escreve informal".
- Profissões variadas: evite só tech/marketing, inclua áreas como saúde, educação, comércio,
  serviços, indústria, etc.
- Idades entre 18 e 65, distribuídas (não concentre tudo em 25-30).

Retorne estritamente no formato JSON pedido, nada de texto fora do schema.
"""