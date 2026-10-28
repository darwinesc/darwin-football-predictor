from scipy.stats import poisson

from scipy.stats import poisson

def get_goal_prob(lambda_home, lambda_away):
    lambda_home = float(lambda_home)
    lambda_away = float(lambda_away)
    lambda_total = lambda_home + lambda_away
    resultados = {}

    # Line of goals for match
    for linea in [0.5, 1.5, 2.5, 3.5, 4.5]:
        limite = int(linea)

        resultados[f"Over {linea}"] = (
            1 - poisson.cdf(limite, lambda_total)
        )
        resultados[f"Under {linea}"] = (
            poisson.cdf(limite, lambda_total)
        )

    return resultados