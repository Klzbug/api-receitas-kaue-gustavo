from fastapi import FastAPI

app = FastAPI()

receitas = [
    {
        'nome': 'Brownie',
        'ingredientes': [
            '3 ovos',
            '6 colheres de açúcar',
            '1/2 xícara (chá) de chocolate em pó',
            '100g de manteiga',
            '1 xícara (chá) de farinha de trigo'
        ],
        'utensílios': [
            'Tigela',
            'Forma',
            'Colher de pau',
            'Forno'
        ],
        'modo_de_preparo': 'Misture todos os ingredientes em uma tigela, coloque a massa em uma forma untada e leve ao forno pré-aquecido a 180°C por cerca de 30 minutos.'
    },
    {
        'nome': 'Torta',
        'ingredientes': [
            '3 ovos',
            '6 colheres de açúcar',
            '1/2 xícara (chá) de chocolate em pó',
            '2 xícaras (chá) de farinha de trigo',
            '1 xícara (chá) de leite',
            '1 colher (sopa) de fermento em pó'
        ],
        'utensílios': [
            'Tigela',
            'Forma',
            'Batedeira ou fouet',
            'Forno'
        ],
        'modo_de_preparo': 'Bata os ovos com o açúcar, adicione os demais ingredientes e misture bem. Coloque em uma forma untada e leve ao forno a 180°C por cerca de 40 minutos.'
    },
    {
        'nome': 'cuscuz',
        'ingredientes' : ['2 xícaras de flocão de milho', '1 xícara de água', '1/2 colher de chá de sal', '1 colher de sopa de manteiga (opcional)'],
        'utensílios' : ['tigela', 'colher', 'cuscuzera', 'panela'],
        'modo de preparo' : [
            'Em uma tigela, misture o flocão de milho com o sal.',
            'Acrescente a água aos poucos, mexendo até que toda a farinha esteja úmida.',
            'Deixe descansar por 10 minutos para hidratar bem.',
            'Coloque a massa hidratada na cuscuzera sem apertar muito.',
            'Leve ao fogo médio por cerca de 10 minutos ou até sentir o cheiro de milho cozido.',
            'Desenforme com cuidado, coloque manteiga por cima e sirva quente.'
        ]
    },
    {
         'nome': 'Feijoada',
        'ingredientes': [
            '500g de feijão preto',
            '300g de carne-seca',
            '200g de costelinha de porco',
            '200g de linguiça calabresa',
            '150g de paio',
            '1 cebola picada',
            '3 dentes de alho amassados',
            '2 folhas de louro',
            'Sal e pimenta a gosto',
            'Cheiro-verde a gosto'
        ],
        'utensílios': [
            'Panela de pressão',
            'Faca',
            'Tábua de corte',
            'Colher de pau'
        ],
        'modo_de_preparo': 'Deixe a carne-seca de molho de um dia para o outro, trocando a água algumas vezes. Cozinhe o feijão preto em uma panela de pressão com as folhas de louro. Em outra panela, refogue as carnes com a cebola e o alho até dourar. Junte tudo ao feijão cozido e deixe apurar em fogo baixo até o caldo engrossar. Finalize com cheiro-verde e sirva acompanhado de arroz branco, couve refogada e farofa.'
    },
    {
        'nome': 'Salada de fruta',
        'ingredientes' : ['maçã', 'banana', 'uva', '...'],
        'utensílios' : ['tigela'],
        'modo de preparo' : ['Fatiar bem todas as frutas e misturá-las.']
    },
    {
        'nome': 'cuscuz',
        'ingredientes' : ['2 xícaras de flocão de milho', '1 xícara de água', '1/2 colher de chá de sal', '1 colher de sopa de manteiga (opcional)'],
        'utensílios' : ['tigela', 'colher', 'cuscuzera', 'panela'],
        'modo de preparo' : [
            'Em uma tigela, misture o flocão de milho com o sal.',
            'Acrescente a água aos poucos, mexendo até que toda a farinha esteja úmida.',
            'Deixe descansar por 10 minutos para hidratar bem.',
            'Coloque a massa hidratada na cuscuzera sem apertar muito.',
            'Leve ao fogo médio por cerca de 10 minutos ou até sentir o cheiro de milho cozido.',
            'Desenforme com cuidado, coloque manteiga por cima e sirva quente.'
        ]
    },
    {
        'nome': 'Pastel',
        'ingredientes': ['2 xícaras de farinha de trigo', '1 colher de sopa de óleo', '1 pitada de sal', '1/2 xícara de água morna', 'óleo para fritar', 'recheio a gosto (carne, queijo, frango, etc.)'],
        'utensílios': ['tigela', 'rolo de macarrão', 'faca ou cortador', 'garfo', 'panela funda', 'escumadeira'],
        'modo de preparo': [
            'Misture a farinha, o sal e o óleo, adicionando a água aos poucos até obter uma massa homogênea.',
            'Deixe a massa descansar por 20 minutos.',
            'Abra a massa fina com um rolo em superfície enfarinhada.',
            'Corte em retângulos, recheie, dobre e feche com um garfo.',
            'Frite em óleo quente até dourar.',
            'Escorra em papel-toalha e sirva quente.'
        ]
    },
    {
        'nome': 'Croissant Tradicional',
        'ingredientes': ['500g de farinha de trigo', '10g de sal', '50g de açúcar', '10g de fermento biológico seco', '300ml de leite morno', '300g de manteiga sem sal gelada', '1 ovo para pincelar'],
        'utensílios': ['tigela grande', 'rolo de massa', 'plástico filme', 'pincel culinário', 'assadeira', 'forno'],
        'modo de preparo': [
            'Misture farinha, sal, açúcar e fermento em uma tigela.',
            'Adicione o leite morno aos poucos até obter uma massa homogênea.',
            'Sove a massa, cubra com plástico filme e deixe descansar por 1 hora.',
            'Abra a massa em formato retangular e coloque a manteiga gelada no centro.',
            'Dobre a massa em camadas, leve à geladeira por 30 minutos e repita o processo de dobrar e gelar 3 vezes.',
            'Abra a massa, corte em triângulos e enrole formando croissants.',
            'Coloque os croissants em uma assadeira, deixe crescer por 1 hora.',
            'Pincele com ovo batido e asse em forno preaquecido a 200°C por cerca de 20 minutos ou até dourar.'
        ]
    }
]

@app.get("/receitas")
def listar_receitas():
    return receitas


@app.get("/receitas/{nome}")
def buscar_receita(nome: str):
    for receita in receitas:
        if receita['nome'].lower() == nome.lower():
            return receita
    return {"erro": "Receita não encontrada"}
