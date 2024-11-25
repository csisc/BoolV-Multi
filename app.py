from llama_cpp import Llama
import pathlib
import pandas as pd
import math

#Choosing the language
lg = "afrikaans"
model = "Llama-3.2-3B-Instruct-Q8_0.gguf"

#Multilingual labels and prompts
true_first = {"afrikaans": "Antwoord met een woord: WAAR of ONWAAR.", 
              "german": "Antworten Sie mit einem Wort: WAHR oder FALSCH.",
	      "portuguese": "Responda com uma palavra: VERDADEIRO ou FALSO.",
              "spanish": "Responde con una palabra: VERDADERO o FALSO.",
              "polish": "Odpowiedz jednym słowem: PRAWDA lub FAŁSZ."}

false_first = {"afrikaans": "Antwoord met een woord: ONWAAR of WAAR.", 
              "german": "Antworten Sie mit einem Wort: FALSCH oder WAHR.",
	      "portuguese": "Responda com uma palavra: FALSO ou VERDADEIRO.",
              "spanish": "Responde con una palabra: FALSO o VERDADERO.",
              "polish": "Odpowiedz jednym słowem: FAŁSZ lub PRAWDA."}

if (model == "Llama-3.2-3B-Instruct-Q8_0.gguf"):
    true_f = {"afrikaans": " WA", 
          "german": " WA",
	  "portuguese": " VER",
          "spanish": " VER",
          "polish": " P"}
else:
    true_f = {"afrikaans": " W", 
          "german": " W",
	  "portuguese": " V",
          "spanish": " V",
          "polish": " P"}

if (model == "Llama-3.2-3B-Instruct-Q8_0.gguf"):
    false_f = {"afrikaans": " ON", 
           "german": " F",
	   "portuguese": " F",
           "spanish": " F",
           "polish": " FA"}
else:
    false_f = {"afrikaans": " ON", 
           "german": " F",
	   "portuguese": " F",
           "spanish": " F",
           "polish": " FA"}





#Defining models
MODEL_Q8_0 = Llama(
    model_path=model,
    n_ctx=128, n_gpu_layers=128, logits_all=True
)

#Defining function for getting a response
def query_with_logprobs(model, question, lg):
    prompt = f"Q: {question} A:"
    output = model(prompt=prompt, max_tokens=1, temperature=10000, logprobs=True)
    response = output["choices"][0]
    logprobs = response["logprobs"]["top_logprobs"][0]  # Get logprobs for first token
    # Extract logprobs for TRUE and FALSE
    logprob_true = math.exp(logprobs.get(true_f[lg], float("-inf")))
    if (logprob_true == 0): logprob_true = 1 - math.exp(logprobs.get(false_f[lg], float("-inf")))
    return logprob_true

#Resolve Wikidata IDs to English labels
df_verify = pd.read_excel("train.xlsx")

#Defining function to check a relation
def check_relation_with_llama(question, prompt, lg):
    logprob_true = query_with_logprobs(
        MODEL_Q8_0, f"{question}? {prompt}", lg
    )
    return logprob_true

df_verify[lg+"_true_first"] = ""  # Initialize a new column for LLAMA validity
df_verify[lg+"_false_first"] = ""

for index, row in df_verify.iterrows():
    question = row[lg]
    if (question[-1] == "?"): question = question[:-1]
    logprob_true = check_relation_with_llama(question, true_first[lg], lg)
    logprob_false = check_relation_with_llama(question, false_first[lg], lg)

    # Calculate normalized score as a confidence metric based on logprobs
    df_verify.at[index, lg+"_true_first"] = logprob_true
    df_verify.at[index, lg+"_false_first"] = logprob_false
    print(index)

df_verify.to_excel("train.xlsx", index=False)
