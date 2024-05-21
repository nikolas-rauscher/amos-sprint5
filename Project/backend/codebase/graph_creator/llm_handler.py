import os

from groq import Groq


def extraxt_entities_and_relations_from_chunk(chunk):

    # system prompt to guide bahavior of llm
    SYS_PROMPT = (
        "Only answer in a JSON format. \n"
        "You are a network graph maker who extracts terms and their relations from a given context. "
        "You are provided with a context chunk (delimited by ```) Your task is to extract the ontology "
        "of terms mentioned in the given context. These terms should represent the key concepts as per the context. \n"
        "Thought 1: While traversing through each sentence, Think about the key terms mentioned in it.\n"
            "\tTerms may include object, entity, location, organization, person, \n"
            "\tcondition, acronym, documents, service, concept, etc.\n"
            "\tTerms should be as atomistic as possible\n\n"
        "Thought 2: Think about how these terms can have one on one relation with other terms.\n"
            "\tTerms that are mentioned in the same sentence or the same paragraph are typically related to each other.\n"
            "\tTerms can be related to many other terms\n\n"
        "Thought 3: Find out the relation between each such related pair of terms. \n\n"
        "Format your output as a list of JSON. Each element of the list contains a pair of terms"
        "and the relation between them, like the follwing: \n"
        "[\n"
        "   {\n"
        '       "node_1": "A concept from extracted ontology",\n'
        '       "node_2": "A related concept from extracted ontology",\n'
        '       "edge": "relationship between the two concepts, node_1 and node_2 in one or two sentences"\n'
        "   }, {...}\n"
        "]"
    )

    # input data for the llm to work on
    USER_PROMPT = f"context: ```{chunk}``` \n\n output: "

    # get api key from shell environment
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    # request to the llm with the prepared prompts
    chat_completion = client.chat.completions.create(
        messages=[

            {"role": "system", "content": SYS_PROMPT},
            {"role": "user", "content": USER_PROMPT}
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content