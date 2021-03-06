# -*- coding: utf-8 -*-
# authors: Ethosa
import asyncio

from mchains import AMarkovChains


async def main():
    mchains = AMarkovChains(use_regex=True, ignorecase=True)
    string = "Hello? bye! hELLO. bYE? hElLo bYe"
    await mchains.to_chains_marks(string)
    print(await mchains.genstr_normal(10))
    print(await mchains.genstr_normal(10))
    print(await mchains.genstr_normal(10))
    print(await mchains.genstr_normal(10))
    print(await mchains.genstr_normal(10))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
