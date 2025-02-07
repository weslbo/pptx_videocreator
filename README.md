# PowerPoint video helper

This projects aims to help with adding videos of an avatar reasoning over a PowerPoint presentation, just like a presenter would. The code takes as an input a PowerPoint file and outputs a new PowerPoint file with the videos added.


You can influence what the avatar is saying by adding a prompt to the notes section of the slide. The avatar will then discuss the slide content (so it doesn't take the notes as a script, but rather the result of the prompt you entered). 


To run the code, you need to have Python 3 installed. You can install the required packages by running `pip install -r requirements.txt`.


You will need to have a .env file with the following variables:


```txt
SPEECH_KEY=[yourkey]
SPEECH_ENDPOINT=https://[yourendpoint].api.cognitive.microsoft.com
AZURE_ENDPOINT=https://[yourendpoint].openai.azure.com/
AZURE_OPENAI_API_KEY=[yourkey]
```


ffmpeg -vcodec libvpx-vp9 -i 0b0370c5-f446-4f82-bee7-edf986955239.webm -vcodec png -pix_fmt rgba metadata:s:v:0 alpha_mode="1" 0b0370c5-f446-4f82-bee7-edf986955239.mov


