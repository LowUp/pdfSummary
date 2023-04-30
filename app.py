# importing required modules
from PyPDF2 import PdfReader
import openai
from dotenv import dotenv_values
import glob

#List all pdf files located in the pdf folder + let the user choose which file to process
def getPdf():

    try:
        pdfFiles = [f for f in glob.glob("./pdfFiles/*.pdf")]
        
        for count, file in enumerate(pdfFiles, 1):
            print(f"{count} - {file}\n\n")

        choice = int(input(f"Choisis le fichier PDF à traiter : "))

        if choice <= 0:
            raise Exception('die')

        return pdfFiles[choice - 1]

    except Exception as error:
        print(f"Error : {error}")


pdf = getPdf()
reader = PdfReader(pdf)
pages = reader.pages
config = dotenv_values(".env")
openai.api_key = config['GPT_API_KEY']


# Take text a make paragraph of 450 words
def makeParagraphs(text: str):

    text = text.strip()

    words = text.split()
    
    numLines = len(text.split())

    delimiter = ' '
    
    iterations = 1

    while numLines > 550:
        words.insert((550 * iterations),  "\n\n") # Add a break lines at position 550 * n of an array
        numLines -= 550
        iterations+=1
            
    # print(delimiter.join(words))
    return delimiter.join(words)

# separates each paragraphs and place it in a list
def retrieveParagraph(paragraphs: str):
    paragraph = paragraphs.split('\n\n')
    # print(paragraph)
    return paragraph

# Uses that open ai API to summarize text 
def gpt3(allPrompt: list):
    
    #Prompt ideas
    #Peut tu résumer brièvement le paragraphe suivant en listant les points importants à retenir de ce paragraphe
    #Peut tu résumer brièvement le paragraphe suivant en insistant sur les points importants à retenir

    with open(f'./result/summary - ({pdf[11:]}).txt', 'w', encoding="utf-8") as sumFile:
        for count, prompt in enumerate(allPrompt, 1):
            for text in prompt:
                if text:
                    response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt= "Peut tu résumer brièvement le paragraphe suivant en insistant sur les points importants à retenir. :\n" 
                        + text,
                        max_tokens=300,
                        temperature=0,
                        top_p=1,
                        n=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        # stop="\n",
                    )
                    print(f"\n\nSummary Paragraph {count} :\n{response.choices[0].text.strip()}")
                    # print(response)
                    summary = response.choices[0].text.strip()

                    sumFile.write(f"\n\nSum Page N°{count}\n\n")
                    sumFile.write(summary)
                    # if count > 1:
                    #     raise Exception('die')

# Main process
def process():

    allParagraphs = []

    try:
        with open(f'./result/original - ({pdf[11:]}).txt', 'w', encoding="utf-8") as file:

            for count, page in enumerate(pages, 1):

                file.write(f"\n\nPage N°{count}\n\n")
                print(f"\n\nExtract Page N°{count} ...\n\n")

                # extracting text from page
                text = page.extract_text()

                paragraphs = makeParagraphs(text)
                file.write(paragraphs)
                # allParagraphs.append()
                paragraphs = retrieveParagraph(paragraphs)
                allParagraphs.append(paragraphs)
                
                # if count > 2:
                #     raise Exception('die')

        gpt3(allParagraphs)

    except Exception as e:
        print(f"Error : {e}")
            


if __name__ == "__main__":
    process()
