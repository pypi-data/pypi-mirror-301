# Dappier Python SDK

Python SDK for interacting with Dappier's API's.

## Overview

`dappier-py` provides a straightforward way to interact with Dappier's API's, which allows for real-time data search on the internet and other datamodels from the marketplace. The library is designed to be easy to use and integrate into existing Python projects.

## Installation

To install the package, run:

```bash
pip install dappier

```

Alternatively, you can clone the repository and install the dependencies:

```bash
git clone https://github.com/DappierAI/dappier-py
cd dappier-py
pip install -r requirements.txt
```

## Initialization

You can get your API key from your [Dappier account](https://platform.dappier.com).

```bash
from dappier.dappier import DappierApp

app = DappierApp(api_key='your_api_key')

```
## Real-Time Search

You can perform a real-time search by providing a query. This will search for real-time data related to your query.

```bash
result = app.realtime_search_api("When is the next election?")
print(result.response['response']["results"])

```

## AI Recommendations
The AI Recommendations feature allows you to query for articles and other content using a specific data model. 
You can pick a specific datamodel from [marketplace](https://marketplace.dappier.com/) 

### Default Options:

```python
ai_result = app.ai_recommendations(query="latest tech news", datamodel_id="dm_02hr75e8ate6adr15hjrf3ikol")
print(ai_result.results)
```

### Custom Options:
You can pass custom parameters such as `similarity_top_k`, `ref` and `num_articles_ref`:

```python
ai_custom_result = app.ai_recommendations(
    query="latest tech news", 
    datamodel_id="dm_02hr75e8ate6adr15hjrf3ikol", 
    similarity_top_k=5, 
    ref="techcrunch.com", 
    num_articles_ref=2
)
print(ai_custom_result.results)

```

## Search API
You can also perform a search using a specific datamodel_id. This method allows users to input custom queries and retrieve data based on the datamodel provided.
```python
search_result = app.search(
    query="Latest Microsoft News",
    datamodel_id="dm_01htjq2njgecvah7ncepm8v87y",
    similarity_top_k=6,
    ref="familyproof.com",
    num_articles_ref=3
)
print(search_result.results)

```


Checkout (example.py)[https://github.com/DappierAI/dappier-py] in this repository for a working example.