import re

import tellurium as te
import roadrunner
from libsbml import *

def algebraic2tellurium(model):
    """ Replaces the algebraic rules of our extended tellurium with a dummy
    syntax of original tellurium
    """
    # Regex expression to look for algebraic rules.
    exp = "((?!\d)\w+) \s*==\s*([^\\\r\n\f'#]*)"
    p = re.compile(exp)

    while True:
        # Search first ocurrence of a algebraic rule.
        m = p.search(model)

        if m == None: break

        # Create the dummy syntax for original tellurium.
        g = m.groups()
        string = f'species {g[0]}_algebraic_rule__ := {g[0]} - ({g[1]})'
        string += f'\nspecies {g[0]} = 0'

        # Replace algebraic rule with the dummy syntax.
        model = p.sub(string, model, count=1)

    return model

def tellurium2sbml(sbml):
    """ Get a tellurium-generated sbml model and adds the algebraic rules to
    the sbml.
    """
    reader = SBMLReader()
    document = readSBMLFromString(sbml)

    model = document.getModel()

    list_species = model.getListOfSpecies()

    # Find species that are algebraic rules.
    exp = '((?!\d)\w+)_algebraic_rule__'
    p = re.compile(exp)

    species_id = []
    for species in list_species:
        match = p.search(species.getId())
        if match:
            group = match.groups()
            species_id.append(group[0])

    for species in species_id:
        # Remove dummy species.
        model.removeSpecies(species + '_algebraic_rule__')

        # Add bounday condition.
        s = model.getSpecies(species)
        s.setBoundaryCondition(True)

        # Get dummy assigment rule.
        dummy_rule = model.getRule(species + '_algebraic_rule__')
        math = dummy_rule.getMath()

        # Create the algebraic rule.
        algebraic_rule = model.createAlgebraicRule()
        algebraic_rule.setMath(math)

        # Delete the dummy_rule.
        model.removeRule(species + '_algebraic_rule__')

    sbml = writeSBMLToString(document)

    return sbml

if __name__ == '__main__':
    model_test_str = """
    model test_model()
        k1_on = 100000
        k1_off = 100000
        k2 = 1
        
        P = 0
        S = 10
        E_tot = 1
        
        K_m := (k1_off + k2) / k1_on
        
        ES == E*S/K_m
        E == E_tot - ES
        
        P' = k2 * ES
    end
    A: test_model()
    """

    model_str = algebraic2tellurium(model_test_str)

    # print(model_test)
    # print('### CONVERTED INTO TELLURIUM ###')
    # print(model)

    r = te.loada(model_str)
    sbml = r.getSBML()

    sbml = tellurium2sbml(sbml)

    f = open('model.xml', 'w')
    f.write(sbml)
    f.close()
