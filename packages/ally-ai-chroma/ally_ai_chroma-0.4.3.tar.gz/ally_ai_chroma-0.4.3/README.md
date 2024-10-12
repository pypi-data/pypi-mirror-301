# Ally AI Chroma

## How to use

### Config File

#### Use API

```yaml
chromadb:
  host: "<endpoint>"
  port: 8000
  ssl: False
```

#### Use Local
```yaml
chromadb:
  persist_directory: './chroma/chroma'
```


### Initialize

```python
from ally_ai_chroma import Chroma

chroma = Chroma()
```



