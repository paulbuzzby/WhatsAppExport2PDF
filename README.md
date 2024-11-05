# WhatsAppExport2PDF

# The Idea

Thought it would be nice and simple. Export a WhatsApp chat. Parse the information and convert to a PDF so that it can be sent to a print service for printing.

# The reality

Some existing codebases do exist that used to do this. I tried at least 2 or 3. See later for more info. It seems that the updates in multiple software packages. Specific ReportLab, PIL and LaTeX. All mean that these legacy code bases don't run as simply as they used to. 

# The Big Problem

Multiple problems really. 

The biggest issue. Emoji's. I think these might be the new date time parsing issue for parsing text. There does not seem to be a simple or universal solution to move Emoji's around and more importantly have them render correctly within a PDF document. 
The solution I have used in this codebase uses the Symbola font. It is only OK. Doesn't cover all of even the "basic" emoji's that get used in WhatsApp all the time.
The repository I tried (linked below) had a good looking LaTeX solution but i couldn;t get it to work. There are a couple of Python modules for dealing with Emoji's 'Emoji' being one of them, and this has some great features which I used. Namley, detecting an emoji, so you could then do something. I suspect the correct way to do this is to somehow grab an image of the emoji being used and insert this into the PDF at the correct point. I am not sure how seamless ReportLab might handle this.

LaTeX is a great idea but for me who is just starting out trying to use it and gain experience. It feels like very specific things are needed in order for it to work. I have LaTeX on a Unix system and 2 LaTeX GUI's on my Windows machine. None of them would simply "work" with the generated LaTeX I could find on other code bases.
It reminds me of trying to debug CSS.

The final irritating problem is with different formats using different special characters. LaTeX has a bunch of reserved characters and ReportLab has a set as well. 
In development, I found that you need to care about <> and :. I am sure these can be escaped but for now i simply replace. 
The : is specificly annoying because the Emoji module uses this to wrap the text name of an emoji.

# The rest

This is a bit of a messy codebase. Thought it would be simpler / faster than it turned out to be.

Inspiration has been taken from [https://github.com/theveloped/WhatsBook] 
but this is an old respository. It looks like WhatsApp changed the formatting subtly when the export function is used. 
This can be quickly corrected so that the code generates the TEX file but then getting the TEX files to render is a massive main. I'm very new to LaTeX and just couldn't get the emoji stuff to work.

# Improvements

1. Make Emoji's work properly
2. Implement name substitution like in the Whatsbook system
    * You can do a simple Find / Replace in the _chat.txt but being able to control this would be nice
3. Make the code work via command line. Like Whatsbook
    * At present you need to potentially modify the WhatsAppExport2PDF.py before execution. Not clean
4. Give options for pictures and video
    * Currently pictures and video are ignored but the text is output do you can see that something was posted.
    * dont underesitmate how many addtional pages including images will create.
    * Perhaps something similar to the Monthly wordcloud. Have a set of images for a given time frame tiled onto a single page
    * Video could be handled by grabbing a single frame from the video and using that as an image
5. Allow for date ranges to be set.
    * This would make it easy to split out and create a PDF for a fixed timeframe instead of the whole chat
6. Make the PDF output a bit more configurable
    * The output is very fixed at the moment. Might not be what some people are after
7. Check it works for group chats
8. More testing to try and find other potential syntax issues

# How to use 

* Install the required modules 
```
pip install -r requirements.txt
```
* Export a WhatsApp chat and get the exported zip file onto your computer with this code
* Create a "data" directory as a sub directory to the WhatsappExportRender.py file.
* Extract your WhatsApp export into the data directory
```plaintext
chatExport.zip
    |--  _chat.txt
    |--  2017-04-13-PHOTO-00000001.jpg
    |--  2017-04-13-PHOTO-00000002.jpg
    |--  2017-04-13-AUDIO-00000003.aac
    |--  2017-04-13-AUDIO-00000004.opus
    |--  2017-04-13-VIDEO-00000005.mp4
```
should look similar to the above.
* Execute the WhatsappExportRender.py file
    * This will create a WhatsappExportRender.pdf file in the same folder location.

# What are these other files?

The other python files are test files. You can explore or ignore.