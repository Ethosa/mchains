# -*- coding: utf-8 -*-
# authors: Ethosa

from mchains import MarkovChains

if __name__ == "__main__":
    markovchains = MarkovChains(True)
    markovchains.to_chains("snakecase camelcase SnakeCase CamelCase SnAkEcAsE cAmElCaSe")

    print(markovchains.genstr(70))
