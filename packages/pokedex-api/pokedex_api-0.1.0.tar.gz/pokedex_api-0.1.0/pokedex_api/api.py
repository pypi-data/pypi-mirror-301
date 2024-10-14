import requests

class PokedexAPI:
    BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

    def get_pokemon(self, name):
        """Retrieve information about a Pokémon by name."""
        response = requests.get(f"{self.BASE_URL}{name.lower()}")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError("Pokémon not found")

    def get_pokemon_image(self, pokemon):
        """Get the image URL of the Pokémon."""
        return pokemon['sprites']['front_default']

    def get_stats(self, pokemon):
        """Get the stats of the Pokémon."""
        return {stat['stat']['name']: stat['base_stat'] for stat in pokemon['stats']}
