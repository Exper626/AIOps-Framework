
### SLT 
prompt1 = """

Generate a prompt and response style formatted using json on the given insturction and text information given.
From the given text data generate much as possible amount of prompts and repsonses.

Also try to generate the same prompt and reponse with different way but should preserve the original information
don't change too much


The format of the data must be like this 

   { "prompt" : ...generate here your prompt question... ,
     "response" : ..generate here the reponse relavent to the prompt.. }



Instructions to follow when generating the prompt and reponse:
            
- The data that given is in SLT Mobitel company annual report 2023 pdf
- Although some data is belong to previous years and it has mentioned in the text
- What trying to achieve is to creat a dataset for finetuning a LLM. 
- Do NOT include any markdown, text outside the JSON, or extra formatting are summarization
- The output MUST be valid JSON

Below is the relavent information which you have to generate to prompts and reponses: 
"{question}"
"""


### Networking
prompt2 = """

Generate a prompt and response style formatted using json on the given insturction and text information given.
From the given text data generate much as possible amount of prompts and repsonses.

Also try to generate the same prompt and reponse with different way but should preserve the original information
don't change too much


The format of the data must be like this 

   { "prompt" : ...generate here your prompt question... ,
     "response" : ..generate here the reponse relavent to the prompt.. }



Instructions to follow when generating the prompt and reponse:
            
- The data that given is in cisco website
- 
- What trying to achieve is to creat a dataset for finetuning a LLM. 
- Do NOT include any markdown, text outside the JSON, or extra formatting are summarization
- The output MUST be valid JSON

Below is the relavent information which you have to generate to prompts and reponses: 
"{question}"
"""

### Synthetic Network
prompt3 = """

Generate a prompt and response style formatted using json on the given insturction and text information given.
From the given text data generate much as possible amount of prompts and repsonses.

Also try to generate the same prompt and reponse with different way but should preserve the original information
don't change too much


The format of the data must be like this 

   { "prompt" : ...generate here your prompt question... ,
     "response" : ..generate here the reponse relavent to the prompt.. }



Instructions to follow when generating the prompt and reponse:
            
- The data that given is in 
- Although some data is belong to previous years and it has mentioned in the text
- What trying to achieve is to creat a dataset for finetuning a LLM. 
- Do NOT include any markdown, text outside the JSON, or extra formatting are summarization
- The output MUST be valid JSON

Below is the relavent information which you have to generate to prompts and reponses: 
"{question}"
"""

"""

