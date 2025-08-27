from fastapi import FastAPI

receitas = [
    {
        'nome': 'brownie',
        'igredientes' : ['3 ovos', '6 colheres de açúcar','...'],
        'utensílios' : ['tijela', 'forma'],
        'modo de preparo' : '...'
    },
    {
        'nome': 'torta',
        'igredientes' : ['3 ovos', '6 colheres de açúcar','...'],
        'utensílios' : ['tijela', 'forma'],
        'modo de preparo' : '...'
    },
    {
        'nome': 'Salada de fruta',
        'igredientes' : ['maça', 'banana','uva','...'],
        'utensílios' : ['tijela'],
        'modo de preparo' : 'fatiar bem todas as frutas e misturalas'
    },
     {
        'nome': 'cuzcuz',
        'ingrediente' : ['2 xícaras de flocão de milho', '1 xícara de água', '1/2 colher de chá de sal', '1 colher de sopa de manteiga (opcional)'],
        'utensílios' : ['Tigela', 'Colher', 'Cuzcuzeira', 'Panela'],
        'modo de preparo' :'Em uma tigela, misture o flocão de milho com o sal; Acrescente a água aos poucos, mexendo até que toda a farinha esteja úmida. Deixe descansar por 10 minutos para hidratar bem; Coloque a massa hidratada na cuscuzeira sem apertar muito; Leve ao fogo médio por cerca de 10 minutos ou até sentir o cheiro de milho cozido; Desenforme com cuidado, coloque manteiga por cima e sirva quente.'
    },
    {
         "nome": "Pastel",
    "ingrediente": ["2 xícaras de farinha de trigo", "1 colher de sopa de óleo", "1 pitada de sal", "1/2 xícara de água morna", "óleo para fritar", "recheio a gosto (carne, queijo, frango, etc.)"],
    "utensílios": ["tigela", "rolo de macarrão", "faca ou cortador", "garfo", "panela funda", "escumadeira"],
    "modo de preparo": ["Misture a farinha, o sal e o óleo, adicionando a água aos poucos até obter uma massa homogênea.", "Deixe a massa descansar por 20 minutos.", "Abra a massa fina com um rolo em superfície enfarinhada.", "Corte em retângulos, recheie, dobre e feche com um garfo.", "Frite em óleo quente até dourar.", "Escorra em papel-toalha e sirva quente."]
    },
]