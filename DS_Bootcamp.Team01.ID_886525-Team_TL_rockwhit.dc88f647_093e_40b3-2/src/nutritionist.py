import recipes
import sys


def main(input_list):
    print('I. OUR FORECAST')
    pred = recipes.IngredientsPredict(input_list)
    pred.predict_for_list()

    print('II. NUTRITION FACTS')
    nutrients = recipes.NutritionFacts("../datasets/nutrients.csv")
    for i in input_list:
        nutrients.printNutrients(i)


    print('III. TOP-3 SIMILAR RECIPES:')
    finder = recipes.SimilarRecipes("../datasets/epi_r_clean_links.csv")
    l = list(map(lambda x: x.strip(" ,"), input_list))
    finder.findSimilar(l)

    print('BONUS:')
    menuMaker = recipes.MenuMaker("../datasets/epi_r_clean_links.csv")
    menuMaker.makeMenu(4)


if __name__ == '__main__':
    checker = recipes.InputCheсker()
    input_list = checker.preprocess(sys.argv[1:])
    try:
        checker.check(input_list)
    except Exception as e:
        print(e)
    else:
        main(input_list)

    

