import numpy as np

import sympy as sp

from autora.theorist.rnn_sindy_rl import RNNSindy
from autora.theorist.rnn_sindy_rl.resources.bandits import AgentQ, EnvironmentBanditsDrift, create_dataset

rnnsindy = RNNSindy(n_actions=2)

synthetic_experiment = True

# setup of synthetic experiment
if synthetic_experiment:
    agent = AgentQ(
        alpha=0.25,
        beta=3,
        n_actions=2,
        forget_rate=0.,
        perseveration_bias=0.,
        correlated_reward=False,
    )
    env = EnvironmentBanditsDrift(
        sigma=0.25,
        n_actions=2,
    )
    n_trials_per_session, n_sessions = 100, 5
    training_data, experiment_list = create_dataset(agent, env, n_trials_per_session, n_sessions)
    conditions = np.expand_dims(np.stack([exp.rewards for exp in experiment_list]), -1)  # rewards with shape (session, trial, 1)
    observations = np.eye(2)[np.stack([exp.choices for exp in experiment_list])]  # one-hot encoding of actions with shape (session, trial, actions)
else:
    conditions = np.random.randint(0, 2, (1, 100, 1))  # rewards with shape (session, trial, 1)
    observations = np.eye(2)[np.random.randint(0, 2, (1, 100))]  # one-hot encoding of actions with shape (session, trial, actions)

rnnsindy = rnnsindy.fit(conditions, observations, epochs=10)


# parse the fitted equations into a usable format
threshold = 0.03
equations = rnnsindy.equation().split('\n')[:-1]

# remove [k+1] and [k] from equations
equations = [equation.replace('[k+1]', '').replace('[k]', '') for equation in equations] 

parsing_dict = {
    'Qr': 'Qa',
    'Qf': 'Qb',
    'Qc': 'Qb',
    'cr^2': 'cr',
}

# replace all xQr, xQf, xQc with either xQa (chosen) and xQb (not chosen) and replace cr**2 with cr because the reward is binary
for i, eq in enumerate(equations):
    for key, value in parsing_dict.items():
        eq = eq.replace(key, value)
    equations[i] = eq

# parse lhs and rhs of equations
eq_sep = ' = '

# get left hand sides of equations
lhs = [equation.split(eq_sep)[0] for equation in equations]

# get right hand sides of equations
rhs = [equation.split(eq_sep)[1] for equation in equations]

# check if any lhs is in rhs and replace it with the corresponding rhs
index_to_remove = []
for i, lhs_i in enumerate(lhs):
    for j, rhs_j in enumerate(rhs):
        if i != j and j not in index_to_remove:
            if lhs_i in rhs_j:
                rhs[j] = rhs_j.replace(lhs_i, '(' + rhs[i] + ')')
                # remove lhs_i from lhs and rhs
                index_to_remove.append(i)
for i in index_to_remove:
    lhs.pop(i)
    rhs.pop(i)

# create new equations with parsed rhs
equations = [lhs_i + eq_sep + rhs_i for lhs_i, rhs_i in zip(lhs, rhs)]

# simplify equations with sympy
def parse_equation_for_sympy(eq):
    # get all symbols of the equation by splitting the equation at ' ' and removing all elements which are not alphabetical
    symbols = set([s for s in eq.split(' ') if s.isalpha()])
    
    eq = eq.replace(' 1 ', '')
    eq = eq.replace(' = ', '=')
    eq = eq.replace(' + ', '+')
    eq = eq.replace(' - ', '-')
    eq = eq.replace(' * ', '*')
    eq = eq.replace(' / ', '/')
    eq = eq.replace('^', '**')
    eq = eq.replace('[k+1]', '')
    eq = eq.replace('[k]', '')
    
    # put a multiplication sign between numbers and variables or numbers and parentheses or variables and variables
    for i in range(len(eq)-2):
        if eq[i].isnumeric() and eq[i+1] == ' ' and (eq[i+2].isalpha() or eq[i+2] == '('):
            eq = eq[:i+1] + '*' + eq[i+2:]
        if eq[i] == ')' and eq[i+1] == ' ' and eq[i+2].isalpha():
            eq = eq[:i+1] + '*' + eq[i+2:]
        if eq[i] == ')' and eq[i+1] == ' ' and eq[i+2] == '(':
            eq = eq[:i+1] + '*' + eq[i+2:]
    
    # put a multiplication sign between two variables from the symbols set
    for symbol_i in symbols:
        for symbol_j in symbols:
                eq = eq.replace(symbol_i + ' ' + symbol_j, symbol_i + '*' + symbol_j) 
    
    # remove all remaining whitespaces
    eq = eq.replace(' ', '')
    
    return eq

for i, eq in enumerate(equations):    
    equations[i] = parse_equation_for_sympy(eq)

# simplify equations
def replace_small_coefficients(eq, round_to, threshold):
    """Replace coefficients smaller than the threshold with 0 in a SymPy equation."""    
    def replace_coeff(expr):
        terms = expr.as_ordered_terms()
        new_terms = []
        for term in terms:
            coeff, rest = term.as_coeff_Mul()
            coeff = round(coeff, round_to)
            if abs(coeff) < threshold:
                coeff = 0
            new_terms.append(coeff * rest)
        return sp.Add(*new_terms)
    
    new_eq = replace_coeff(eq)
    
    return new_eq

lhs = [eq.split('=')[0] for eq in equations]
rhs = [eq.split('=')[1] for eq in equations]
for i, eq in enumerate(rhs):
    eq = sp.expand(sp.simplify(eq))
    eq = sp.simplify(replace_small_coefficients(eq, 3, threshold))
    rhs[i] = str(eq)

# make latex-version of equations
for i, lhs_i in enumerate(lhs):
    rhs[i] = rhs[i].replace(lhs_i, lhs_i + '_{t}')
    lhs[i] = lhs_i + '_{t+1}'

# put together simplified equations
equations = [lhs_i + '=' + str(rhs_i) for lhs_i, rhs_i in zip(lhs, rhs)]

sindy_to_latex_dict = {
        ' 1 ': ' ',
        'cr': 'Reward',
        'cQr': '\frac{dQ_{chosen}}{dt}',
        'xQb': 'Q_{not chosen,}',
        'xQa': 'Q_{chosen,}',
        }

for i, eq in enumerate(equations):
    for key, value in sindy_to_latex_dict.items():
        equations[i] = equations[i].replace(key, value)
        
print('\nDisovered model:')
for eq in equations:
    print(eq)