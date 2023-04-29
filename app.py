# importing required modules
from PyPDF2 import PdfReader

# creating a pdf reader object
reader = PdfReader('./pdfFiles/ACE+PNC+consolidé+Avril+2019.pdf')

# printing number of pages in pdf file
numberOfPages = len(reader.pages)
pages = reader.pages


# Take text a make paragraph of 450 words
def makeParagraphs(text: str):

    text = text.strip()

    words = text.split()
    
    numLines = len(text.split())

    delimiter = ' '
    
    iterations = 1

    while numLines > 450:
        words.insert((450 * iterations),  "\n\n") # Add a break lines at position 450 * n of an array
        numLines -= 450
        iterations+=1
            
    # print(delimiter.join(words))
    return delimiter.join(words)


# Main process
def process():
    try:
        with open('./result/text_2.txt', 'w', encoding="utf-8") as file:

            for count, page in enumerate(pages, 1):

                file.write(f"\n\nPage N°{count}\n\n")

                # extracting text from page
                text = page.extract_text()

                paragraphs = makeParagraphs(text)
                file.write(paragraphs)
                
                # makeParagraphs(reader.pages[31].extract_text())
                # raise Exception('die')
            
    except Exception as e:
        print(f"Error : {e}")
            


if __name__ == "__main__":
    process()
