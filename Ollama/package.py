import ollama

#initialize the Ollama client
client = ollama.Client()

#Define the model and input prompt
model = "llama3"
prompt = "What is python?"

#Send the query to the model
response = client.generate(model=model, prompt=prompt)

#Print the response from the model
print("Response from ollama:")
print(response.response)