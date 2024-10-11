# mini-archon
Archon with just chat completions

## Usage
Create an api_keys.json of this format:
```
{
    "OPENAI_API_KEY": [],
    "TOGETHER_API_KEY": [],
    "ANTHROPIC_API_KEY": [],
    "GROQ_API_KEY": [],
    "GOOGLE_API_KEY": [],
    "EXAMPLE_API_KEY": []
}
```

Pass this into your archon class along with an Archon config
Example:
```
archon = Archon(archon_config, api_key_file='api_keys.json', query_saves=False)
```
archon_config should be a valid Archon config json

# TODO:
- Update this readme
- Create completion formats similar to openai
