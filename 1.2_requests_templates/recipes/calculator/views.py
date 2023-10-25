from django.http import HttpResponse
from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }

def omlet(request):
    servings = request.GET.get('servings')
    if servings:
        res = DATA['omlet'].copy()
        for key in res:
            res[key] *= int(servings)
        context = {'recipe' : res}
    else:
        context = {'recipe' : DATA['omlet']}
    return render(request, 'calculator/index.html', context)

def pasta(request):
    servings = request.GET.get('servings')
    if servings:
        res = DATA['pasta'].copy()
        for key in res:
            res[key] *= int(servings)
        context = {'recipe' : res}
    else:
        context = {'recipe' : DATA['pasta']}
    return render(request, 'calculator/index.html', context)

def buter(request):
    servings = request.GET.get('servings')
    if servings:
        res = DATA['buter'].copy()
        for key in res:
            res[key] *= int(servings)
        context = {'recipe' : res}
    else:
        context = {'recipe' : DATA['buter']}
    return render(request, 'calculator/index.html', context)