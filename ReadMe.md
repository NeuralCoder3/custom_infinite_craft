# SDXL+LLAMA Craft



## Features

- [x] Create high-quality words based on state-of-the-art LLMs (e.g. Mixtral)
- [x] Create fancy icons based on Stable-Diffusion
- [x] A website to play with the combinations
    - [ ] a tree/graph to keep track of your combinations
    - [ ] allow for subtractive combinations
- [ ] Export client-only website

## Explanation

Prompts, Models, and Explanation

## APIs

## Related

- Infinite Craft: https://neal.fun/infinite-craft/
- GPT Combination Guesser: https://github.com/YuraSuper2048/infinite-craft-gpt-server
- Infinite Craft Related Repos: https://github.com/search?q=infinite+craft&type=repositories (mostly bruteforcer or enumerators)
    - GPT-4 API + Dall-e (realistic images): https://github.com/sshh12/llm_alchemy
    - with oolama: https://github.com/Fus3n/infinite-sides?tab=readme-ov-file
    - docker+postgres: https://github.com/joeyagreco/infinite-craft-architecture
    - chatgpt 3.5: https://github.com/dekdao/infinite-craft-nextjs
    - mistral+website: https://github.com/bufferhead-code/opencraft


## Examples

Some example combinations from first testing:
```
fire + water = steam
fire + steam = vapor
steam + steam = pressure
water + water = ponds
steam + water = vapor
goblin + harry potter = snatcher
goblin + lord of the rings = orcish ruler
pond ecosystem + pond environment = pond habitat
vapor + vapor = evaporation
ponds + ponds = bodysofwater
bodysofwater + bodysofwater = large bodies of water
large bodies of water + water = oceanic masses
oceanic masses + water = marine volumes
oceanic masses + oceanic masses = vast oceanic expanse
oceanic masses + vast oceanic expanse = immense marine volumes
immense marine volumes + vast oceanic expanse = monumental aquatic dimensions
steam + vapor = water vapor
vapor + water vapor = atmospheric moisture
water + water vapor = moisture
moisture + water = dampness
comic + life = humor
comic + pokemon = pokémon-inspired comic
fire + pokemon = charizard
pokemon + water = squirtle
squirtle + time = moment
level + squirtle = tiered turtle
evolution + squirtle = evolved creature from squirtle
charizard + squirtle = firefighter squirrel
cannon + squirtle = watergun
charizard + flower = blossizard
flower + pokemon = petalbuddy
nature + pokemon = wilderness creatures
electricity + pokemon = pikachu
pokemon + rat = rattata
pikachu + pokemon = pikapokeball
evolution + pikachu = pikaevolution
pikachu + pikachu = two pikachus
blossizard + water = aquablossom
flower + pikachu = petal pokmon
```

<!-- find ./  -printf '![%f](examples/%f)\n' -->
<!-- 
find examples -type f -printf '<img src="examples/%f" width=50 height=50 />\n' 
-->
<p float="left">
<img src="examples/evolution.jpg" width=100 height=100 />
<img src="examples/firefighter_squirrel.jpg" width=100 height=100 />
<img src="examples/oceanic_masses.jpg" width=100 height=100 />
<img src="examples/pokemon.jpg" width=100 height=100 />
<img src="examples/rattata.jpg" width=100 height=100 />
<img src="examples/fire.jpg" width=100 height=100 />
<img src="examples/immense_marine_volumes.jpg" width=100 height=100 />
<img src="examples/pikaevolution.jpg" width=100 height=100 />
<img src="examples/orcish_ruler.jpg" width=100 height=100 />
<img src="examples/lord_of_the_rings.jpg" width=100 height=100 />
<img src="examples/large_bodies_of_water.jpg" width=100 height=100 />
<img src="examples/watergun.jpg" width=100 height=100 />
<img src="examples/steam.jpg" width=100 height=100 />
<img src="examples/monumental_aquatic_dimensions.jpg" width=100 height=100 />
<img src="examples/snatcher.jpg" width=100 height=100 />
<img src="examples/time.jpg" width=100 height=100 />
<img src="examples/pikapokeball.jpg" width=100 height=100 />
<img src="examples/rat.jpg" width=100 height=100 />
<img src="examples/flower.jpg" width=100 height=100 />
<img src="examples/humor.jpg" width=100 height=100 />
<img src="examples/level.jpg" width=100 height=100 />
<img src="examples/vast_oceanic_expanse.jpg" width=100 height=100 />
<img src="examples/comic.jpg" width=100 height=100 />
<img src="examples/petal_pokmon.jpg" width=100 height=100 />
<img src="examples/nature.jpg" width=100 height=100 />
<img src="examples/pond_environment.jpg" width=100 height=100 />
<img src="examples/charizard.jpg" width=100 height=100 />
<img src="examples/moment.jpg" width=100 height=100 />
<img src="examples/pikachu.jpg" width=100 height=100 />
<img src="examples/pond_ecosystem.jpg" width=100 height=100 />
<img src="examples/evaporation.jpg" width=100 height=100 />
<img src="examples/atmospheric_moisture.jpg" width=100 height=100 />
<img src="examples/ponds.jpg" width=100 height=100 />
<img src="examples/wilderness_creatures.jpg" width=100 height=100 />
<img src="examples/two_pikachus.jpg" width=100 height=100 />
<img src="examples/aquablossom.jpg" width=100 height=100 />
<img src="examples/pond_habitat.jpg" width=100 height=100 />
<img src="examples/evolved_creature_from_squirtle.jpg" width=100 height=100 />
<img src="examples/tiered_turtle.jpg" width=100 height=100 />
<img src="examples/vapor.jpg" width=100 height=100 />
<img src="examples/pok??mon-inspired_comic.jpg" width=100 height=100 />
<img src="examples/harry_potter.jpg" width=100 height=100 />
<img src="examples/goblin.jpg" width=100 height=100 />
<img src="examples/pressure.jpg" width=100 height=100 />
<img src="examples/water.jpg" width=100 height=100 />
<img src="examples/moisture.jpg" width=100 height=100 />
<img src="examples/electricity.jpg" width=100 height=100 />
<img src="examples/water_vapor.jpg" width=100 height=100 />
<img src="examples/cannon.jpg" width=100 height=100 />
<img src="examples/blossizard.jpg" width=100 height=100 />
<img src="examples/dampness.jpg" width=100 height=100 />
<img src="examples/petalbuddy.jpg" width=100 height=100 />
<img src="examples/marine_volumes.jpg" width=100 height=100 />
<img src="examples/life.jpg" width=100 height=100 />
<img src="examples/bodysofwater.jpg" width=100 height=100 />
<img src="examples/squirtle.jpg" width=100 height=100 />
</p>
