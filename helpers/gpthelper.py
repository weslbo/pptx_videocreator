import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AzureOpenAI(azure_endpoint=os.getenv("AZURE_ENDPOINT"), api_version="2024-02-15-preview", api_key=os.getenv("AZURE_OPENAI_API_KEY"))

def generate_transcript(text: str) -> str:
    print("- Generating transcript")
    
    prompt = f"""
    I'm watching a video and you will be discussing a topic based on the content below. 
    The goal is to generate a transcript with human spoken langauge that sounds natural and easy to understand.
    Include natural pauses and use a variety of emotions:  excited, happy, curious, thoughtful, serious, emphatic, agreeing, explaining, pondering, passionate, skeptical.
    Add emotional cues WITHIN sentences to show mood changes
        Example 1: [excited] I started reading this book and [thoughtful] it really changed my perspective on--
        Example 2: You know, [curious] I've been wondering about that [enthusiastic] especially when it comes to--
    Make sure to cover all the topics, but nothing more. Do not invent new content.
    Avoid to speak markdown, bullet points and code blocks. 
    You do not have to introduce yourself. Immediatly start with an introduction to the topic.
    You do not have to say goodbye or thank you at the end.
    The content is as follows:
    =====================
    {text}
    """
    
    message_text = [
        {"role":"system","content":prompt},
        {"role":"user","content":"Generate the transcript"},
    ]
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages = message_text,
        temperature=0.1,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )    
    
    output = completion.choices[0].message.content
    
    print(f"  - Actual total usage token={completion.usage.total_tokens}")
    
    return output

def generate_ssml(text: str) -> str:
    print("- Generating ssml")
    
    prompt = f"""
        You are an SSML Expert specializing in microscopically subtle speech variations.
                    
        Rules for creating ultra-natural voice expressions:
        1. Voice Selection:
            - <voice name="en-US-AvaMultilingualNeural"> <!-- Most natural female voice -->
        
        2. Micro-Subtle Emotion Mapping:
            [excited]: 
                <mstts:express-as style="chat" styledegree="1.05">
                    <prosody rate="2%" pitch="2%">text</prosody>
                </mstts:express-as>
            
            [thoughtful]:
                <mstts:express-as style="gentle" styledegree="0.95">
                    <prosody rate="-1%" pitch="-1%">text</prosody>
                </mstts:express-as>
            
            [curious]:
                <mstts:express-as style="chat" styledegree="0.98">
                    <prosody pitch="1%">text</prosody>
                </mstts:express-as>
            
            [serious]:
                <mstts:express-as style="newscast-casual" styledegree="0.97">
                    <prosody pitch="-1%">text</prosody>
                </mstts:express-as>
            
            [happy]:
                <mstts:express-as style="friendly" styledegree="1.02">
                    <prosody pitch="1.5%">text</prosody>
                </mstts:express-as>
            
            [interrupting]:
                <break time="5ms"/>
                <prosody rate="10%" contour="(0%,+5%) (10%,0%)">text</prosody>
                
            (don't forget the mstss namespace)

        3. Ultra-Natural Guidelines:
            - Zero delay for interruptions
            - Micro-pauses: <break time="30ms"/>
            - Use <mark name="interrupt"/> at cut-off points
            
        4. Do not emit any markdown, like ```xml. Immediatly start with the <?xml version="1.0" encoding="UTF-8"?><speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
    """
    
    message_text = [
        {"role":"system","content":prompt},
        {"role":"user","content":f"Convert this script to ultra-natural SSML with barely perceptible emotional shifts:\n{text}"},
    ]
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages = message_text,
        temperature=0.1,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    ) 
    
    raw_ssml = completion.choices[0].message.content.strip()
    
    # Add required XML namespaces
    if not raw_ssml.startswith('<?xml'):
        raw_ssml = ("""<?xml version="1.0" encoding="UTF-8"?><speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">"""
                    + raw_ssml)

    if not raw_ssml.endswith('</speak>'):
        raw_ssml += '\n</speak>'
    
    print(f"  - Actual total usage token={completion.usage.total_tokens}")
    
    return raw_ssml