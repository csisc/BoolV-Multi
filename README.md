# BoolV
A method to evaluate the response of lightweight LLMs to TRUE-FALSE questions across languages

# Supported Languages
The supported natural languages are the ones that have been featured as the [best performing](http://www.scholink.org/ojs/index.php/sll/article/view/2180) ones on Google Translation:
- English
- Afrikaans
- German
- Portuguese
- Spanish
- Polish

# Models
| Model         | Hyperparameters |
| ------------- | --------------- |
| [llama-3.2-3b-instruct-q8_0](https://huggingface.co/lmstudio-community/Llama-3.2-3B-Instruct-GGUF/blob/main/Llama-3.2-3B-Instruct-Q8_0.gguf) | 3.21 B |
| [Phi-3.5-mini-instruct.Q8_0](https://huggingface.co/MaziyarPanahi/Phi-3.5-mini-instruct-GGUF/blob/main/Phi-3.5-mini-instruct.Q8_0.gguf) | 3.82 B |

# Dataset
- https://github.com/google-research-datasets/boolean-questions
- Train dataset: 9427 labeled training examples.
- Dev dataset: 3270 labeled dev examples.

# Dependencies
- llama-cpp-python
- pathlib
- pandas
- math

# Funding
This research work has been done thanks to the [computer resources](https://wikimedia.ch/fr/news/swiss-server-helps-optimise-wikidata-in-the-field-of-medicine/) of [Wikimedia Switzerland](https://wikimedia.ch/).
