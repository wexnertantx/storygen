from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline
import os
from flask_ngrok import run_with_ngrok
from flask import Flask, request
#import gpt_2_simple as gpt2_simple
import threading
import time
#import tensorflow as tf
import requests # For Pastebin API
#import language_tool_python
#tool = language_tool_python.LanguageTool('en-US')

#tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")

#model = GPT2LMHeadModel.from_pretrained("gpt2-medium")


story_gen = pipeline("text-generation", "pranavpsv/genre-story-generator-v2",max_length=400)

def listToString(li):  
    li2 = []
    for sublist in li:
        li2.extend(sublist)
    str1 = " " 

    return (str1.join(li2))  

#def grammar_check(my_story):
    matches = tool.check(my_story)
    length = len(matches)
    res=[]
    for i in range(0,length):
        lst = list(matches)
        res.append(str(lst[i]).split("\n")[1:])
        resu = listToString(res)
        resu = resu.replace("^","")
        resu = resu.replace('Message:','<br/><br/><i class="far fa-hand-point-right"></i>&nbsp;&nbsp;')
    return resu

app = Flask(__name__)
#run_with_ngrok(app)   #starts ngrok when the app is run

scary_result=None
scary_start_with=None
scary_word_limit=None

humour_result=None
humour_start_with=None
humour_word_limit=None

scifi_result=None
scifi_start_with=None
scifi_word_limit=None

global share
share=None
global grammatical_errors
grammatical_errors=None

def scary_generate_story():
    global scary_result
    #sess = gpt2_simple.start_tf_sess()
    #gpt2_simple.copy_checkpoint_from_gdrive(run_name='run1')
    #gpt2_simple.load_gpt2(sess)
    scary_result = story_gen("<BOS> <horror> "+scary_start_with+"Tell me what happens in the story and how the story ends.",max_length=scary_word_limit)[0]['generated_text'].replace("<BOS> <horror> ","") 
    #scary_result =story_gen(scary_result_first, max_length=scary_word_limit)[0]['generated_text'].replace("<BOS> <horror> ","")


def humour_generate_story():
    global humour_result
    #tf.reset_default_graph()  
    #sess = gpt2_simple.start_tf_sess()
    #gpt2_simple.copy_checkpoint_from_gdrive(run_name='run2')
    #gpt2_simple.load_gpt2(sess, run_name='comedy')
    #humour_result = str(gpt2_simple.generate(sess, run_name='comedy', length=humour_word_limit,temperature=0.7,top_k=96, prefix=humour_start_with,return_as_list=True)[0]).replace("\n","")
    humour_result= story_gen("<BOS> <drama> "+humour_start_with+ "Tell me what happens in the story and how the story ends.",max_length=humour_word_limit)[0]['generated_text'].replace("<BOS> <drama> ","")
    #humour_result =story_gen(humour_result_first, max_length=humour_word_limit)[0]['generated_text']

def scifi_generate_story():
    global scifi_result
    #tf.reset_default_graph()  
    #sess = gpt2_simple.start_tf_sess()
    #gpt2_simple.copy_checkpoint_from_gdrive(run_name='run3')
    #gpt2_simple.load_gpt2(sess, run_name='scifi')
    scifi_result = story_gen("<BOS> <sci_fi> "+scifi_start_with+"Tell me what happens in the story and how the story ends.",max_length=scifi_word_limit)[0]['generated_text']
    scifi_result=scifi_result.replace("<BOS> <sci_fi> ","")
    # scifi_result =story_gen(humour_result_first, max_length_word_limit)[0]['generated_text'].replace("<BOS><sci_fi>","")
########################################################################################################################
#                                                      HOME PAGE
########################################################################################################################

@app.route('/',methods=["GET","POST"])
def home_page():
    return '''
<html>
<head>
<title>GeneratorStory test</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://kit.fontawesome.com/5de545e21a.js" crossorigin="anonymous"></script>
<link rel="stylesheet" href="/static/css/homepage.css/">
<link rel="stylesheet" href="/static/css/polaroid.css/">
</head>
<body>
<div class="intro">
  <div class="black"></div>  
  <div class="white"></div>
  <div class="boxfather">
    <div class="box">
      <h1>GENERATE A STORY</h1>
      <button><i class="fab fa-get-pocket"></i> Start</button>
    </div>
  </div>
  
</div>


<div class="homepage">
  <h1> Tell <u>me</u> a Genre for your Story </h1>

<div class="wrapper">

  <div class="item">
  <a href="/scary">
    <div class="polaroid"><img src="https://cdn.pixabay.com/photo/2016/06/28/00/13/castle-1483681_960_720.jpg">
      <div class="caption">Scary</div>
    </div>
  </a>
  </div>

  <div class="item">
  <a href="/funny">
    <div class="polaroid"><img src="https://filmdaily.co/wp-content/uploads/2020/07/dirty-lede-1300x731.jpg">
      <div class="caption">Funny</div>
    </div>
  </a>
  </div>

  <div class="item">
  <a href="/scifi">
    <div class="polaroid"><img src="https://cdn.pixabay.com/photo/2020/05/12/20/01/spaceship-5164780_960_720.jpg">
      <div class="caption">Scifi </div>
    </div>
  </a>
  </div>


</div>


</div>

<script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
<script src='https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.11.2/jquery-ui.min.js'></script>
<script src="/static/js/homepage.js"></script>
</body>
</html>
'''.format()

################################################################################
#                                 SCARY STORIES
################################################################################

@app.route('/scary', methods=["GET", "POST"])
def adder_page_scary():
    global scary_result
    global scary_start_with
    global scary_word_limit
    global share
    global grammatical_errors
    errors = ""
    if request.method == "POST":
        try:
            scary_start_with = (request.form["start_of_story_post_request"])
        except:
            errors = "Something Unusual"
        try:
            scary_word_limit = int(request.form["word_limit"])
        except:
            errors = "Something Unusual"
        try:
            thread = threading.Thread(target=scary_generate_story)
            thread.start()
            thread.join()
            #share = pastebin_share(scary_result,"Scary")
            #grammatical_errors = grammar_check(scary_result)
        except:
            result="N/A"
        return '''

<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GENERATOR STORY</title>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
  <link rel="stylesheet" href="/static/css/style.css/">
  <link rel="stylesheet" href="/static/css/textbox-notebook-effect.css/">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Nanum+Gothic&display=swap" rel="stylesheet">
  <script src="/static/js/tts.js/"></script>

</head>
<body>

<div class="wrapper">
  <h1><h1><i class="fas fa-book-dead"></i>   We wrote you a Scary story</h1></h1>
</div>

    
	<textarea id="text-to-speech">
    {scary_result}
    </textarea>

        <div><button type="button" onclick="textToAudio()"><i class="fas fa-volume-up"></i>   Narrate</button>
        <button onclick="saveTextAsFile()"><i class="fas fa-download"></i>   Download The Story</button>
        <!-- Button trigger modal -->
        <!--<button type="button" data-toggle="modal" data-target="#exampleModalCenter"><i class="fas fa-share-alt"></i>    Share</button>-->
        <button type="button" data-toggle="modal" data-target="#exampleModalLong"><i class="fas fa-exclamation-circle"></i>    Grammatical Errors</button>
        <!--<button type="button" data-toggle="modal" data-target=".bd-example-modal-lg"><i class="fas fa-project-diagram"></i>    Add To Wall</button>-->

<div class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <iframe frameborder="0" style="height:500px;width:99%;border:none;" src='https://forms.zohopublic.in/maliciousyunk/form/Clientreview/formperma/rSA2h2eUY9ktKDEIlqXnvPUPMlE5uGuWe_EZ0bTfjDM'></iframe>
    </div>
  </div>
</div>





<!-- Modal for grammar check-->
<div class="modal fade" id="exampleModalLong" tabindex="-1" role="dialog" aria-labelledby="exampleModalLongTitle" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
      <font color="black">
        <h5 class="modal-title" id="exampleModalLongTitle">Possible Grammatical Errors</h5>
    </font>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <font color="black">


        {grammatical_errors}


        </font>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>


<script src="https://kit.fontawesome.com/5de545e21a.js" crossorigin="anonymous"></script>
<script src="/static/js/script.js/"></script>
<script src="/static/js/save_as.js/"></script>
<script src="/static/js/copy_function.js/"></script>
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

</body>
</html>

                       '''.format(scary_result=scary_result,share=share,grammatical_errors=grammatical_errors)

    
    return '''
<!DOCTYPE html>
<html lang="en" >
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GeneratorStory</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/meyer-reset/2.0/reset.min.css">
    <link rel="stylesheet" href="/static/css/style.css/">
    <link rel="stylesheet" href="/static/css/text-glitch-style.css/">
    <link rel="stylesheet" href="/static/css/glitching-granny-image-style.css">
</head>
<body>
    {errors}


        <div id="glitch-granny-text-container">
        <div class="glitch" data-text="G">Generator Story</div>
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
            <defs>
            <filter id="glitch" x="0" y="0">
                <feColorMatrix in="SourceGraphic" mode="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r" />
                    
                <feOffset in="r" result="r" dx="-5">
                <animate attributeName="dx" attributeType="XML" values="0; -2; 0; -18; -2; -4; 0 ;-1; 0" dur="1s" repeatCount="indefinite"/>
                </feOffset>
                <feColorMatrix in="SourceGraphic" mode="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0" result="g"/>
                <feOffset in="g" result="g" dx="-5" dy="1">
                <animate attributeName="dx" attributeType="XML" values="0; 0; 0; -3; 0; 8; 0 ;-1; 0" dur="2s" repeatCount="indefinite"/>
                </feOffset>
                <feColorMatrix in="SourceGraphic" mode="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" result="b"/>
                <feOffset in="b" result="b" dx="5" dy="2">
                <animate attributeName="dx" attributeType="XML" values="0; 3; -1; 4; 0; 2; 0 ;18; 0" dur="4s" repeatCount="indefinite"/>
                </feOffset>
                <feBlend in="r" in2="g" mode="screen" result="blend" />
                <feBlend in="blend" in2="b" mode="screen" result="blend" />
            </filter>
            </defs>
        </svg>
        </div>

    <h1 id="suggest">SUGGEST PROMPT TO START A STORY WITH</h1><br/>
    <form class="form" method="post" action="/scary">
    <div id="form-container">
        <div class="form-group">
            <!--<textarea name="number1" placeholder="Starting of story" rows="4" cols="50"></textarea>-->
            <textarea name="start_of_story_post_request" placeholder="Starting of story" class="form-control" id="formGroupExampleInput"></textarea></br>
            <div class="slidecontainer">
                <p>Word Limit (<span id="demo"></span> Words)</p><br>
                <input type="range" min="50" max="400" value="225" class="slider" id="myRange" name="word_limit" value="225">  
            </div>
        </div>
        <button type="submit" class="btn btn-primary">Tell me a story</button>
    </div>
    </form>


    <div id="loader" style="display:none">
    <img src="https://webstockreview.net/images/clipart-ghost-sticker-13.gif" height="150" width="150"/>
    <p><i class="fas fa-pencil-alt"></i>  Writing a Horror Story... </p>
    </div>

    <center>
    <div class="glitch-container">
	<img src="https://flyclipart.com/thumb2/face-halloween-scary-smiley-icon-273569.png" alt="" class="img-1">
	<img src="https://flyclipart.com/thumb2/face-halloween-scary-smiley-icon-273569.png" alt="" class="img-2">
	<img src="https://flyclipart.com/thumb2/face-halloween-scary-smiley-icon-273569.png" alt="" class="img-3">
	
	<div class="line">
		<img src="https://flyclipart.com/thumb2/face-halloween-scary-smiley-icon-273569.png" alt="" class="img-4">
	</div>
    </center>
		
</div>

<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
<script src='https://cdnjs.cloudflare.com/ajax/libs/dat-gui/0.5/dat.gui.min.js'></script>
<script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js'></script>
<script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
<script src="https://kit.fontawesome.com/5de545e21a.js" crossorigin="anonymous"></script>
<script src="/static/js/script.js/"></script>
</body>
</html>

    '''.format(errors=errors)


################################################################################
#                                    FUNNY STORIES
################################################################################



@app.route('/funny', methods=["GET", "POST"])
def adder_page_humour():
    global humour_result
    global humour_start_with
    global humour_word_limit
    global share
    global grammatical_errors
    errors= ""
    share=""
    if request.method == "POST":
        try:
            humour_start_with = (request.form["start_of_story_post_request"])
        except:
            errors = "Something Unusual"
        try:
            humour_word_limit = int(request.form["word_limit"])
        except:
            errors = "Something Unusual"
        try:
            thread = threading.Thread(target=humour_generate_story)
            thread.start()
            thread.join()
            #share = pastebin_share(humour_result,"Funny")
           # grammatical_errors = grammar_check(humour_result)
        except:
            result="N/A"
        return '''

<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GENERATORSTORY</title>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
  <link rel="stylesheet" href="/static/css/humour_style.css/">
  <link rel="stylesheet" href="/static/css/textbox-notebook-effect.css/">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Dancing+Script&display=swap" rel="stylesheet">
  <script src="/static/js/tts.js/"></script>

</head>
<body>

<div class="wrapper">
  <h1><h1><i class="fas fa-book-dead"></i>   We wrote you a Funny story</h1></h1>
</div>

    
	<textarea id="text-to-speech">
    {humour_result}
    </textarea>

        <div><button type="button" onclick="textToAudio()"><i class="fas fa-volume-up"></i>   Narrate</button>
        <button onclick="saveTextAsFile()"><i class="fas fa-download"></i>   Download The Story</button>
        <!-- Button trigger modal -->
        <button type="button" data-toggle="modal" data-target="#exampleModalCenter"><i class="fas fa-share-alt"></i>    Share</button>
         <button type="button" data-toggle="modal" data-target="#exampleModalLong"><i class="fas fa-exclamation-circle"></i>    Grammatical Errors</button>
        <button type="button" data-toggle="modal" data-target=".bd-example-modal-lg"><i class="fas fa-project-diagram"></i>    Add To Wall</button>

<div class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <iframe frameborder="0" style="height:500px;width:99%;border:none;" src='https://forms.zohopublic.in/maliciousyunk/form/Clientreview/formperma/rSA2h2eUY9ktKDEIlqXnvPUPMlE5uGuWe_EZ0bTfjDM'></iframe>
    </div>
  </div>
</div>

<!-- Modal -->
<div class="modal fade" id="exampleModalCenter" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLongTitle">Modal title</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
      <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={share}"><br/></br>
       <input type="text" value="{share}" id="url" size="30" readonly>
        <div id="share-buttons">
        <!-- Email -->
    <a href="mailto:?Subject=Simple Share Buttons&amp;Body=AI%20Generated%20SScary%20Story%20 {share}">
        <img src="https://simplesharebuttons.com/images/somacro/email.png" alt="Email" />
    </a>

        <!-- Facebook -->
    <a href="http://www.facebook.com/sharer.php?u={share}" target="_blank">
        <img src="https://simplesharebuttons.com/images/somacro/facebook.png" alt="Facebook" />
    </a>

        <!-- LinkedIn -->
    <a href="http://www.linkedin.com/shareArticle?mini=true&amp;url={share}" target="_blank">
        <img src="https://simplesharebuttons.com/images/somacro/linkedin.png" alt="LinkedIn" />
    </a>

        <!-- Print -->
    <a href="javascript:;" onclick="window.print()">
        <img src="https://simplesharebuttons.com/images/somacro/print.png" alt="Print" />
    </a>

        <!-- Reddit -->
    <a href="http://reddit.com/submit?url={share};title=GRANNY" target="_blank">
        <img src="https://simplesharebuttons.com/images/somacro/reddit.png" alt="Reddit" />
    </a>

        <!-- StumbleUpon-->
    <a href="http://www.stumbleupon.com/submit?url={share};title=GRANNY" target="_blank">
        <img src="https://simplesharebuttons.com/images/somacro/stumbleupon.png" alt="StumbleUpon" />
    </a>
    
    <!-- Tumblr-->
    <a href="http://www.tumblr.com/share/link?url={share};title=GRANNY" target="_blank">
        <img src="https://simplesharebuttons.com/images/somacro/tumblr.png" alt="Tumblr" />
    </a>
     
    <!-- Twitter -->
    <a href="https://twitter.com/share?url={share};text=AI%20Generated%20Story&amp;hashtags=granny" target="_blank">
        <img src="https://simplesharebuttons.com/images/somacro/twitter.png" alt="Twitter" />
    </a>


        </div>
        
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" onclick="copy_that()">Copy</button>
      </div>
    </div>
  </div>
</div>
</div>

        
        </div>

        <!-- Modal for grammar check-->
<div class="modal fade" id="exampleModalLong" tabindex="-1" role="dialog" aria-labelledby="exampleModalLongTitle" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
      <font color="black">
        <h5 class="modal-title" id="exampleModalLongTitle">Possible Grammatical Errors</h5>
    </font>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <font color="black">


        {grammatical_errors}


        </font>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
<script src="https://kit.fontawesome.com/5de545e21a.js" crossorigin="anonymous"></script>
<script src="/static/js/script.js/"></script>
<script src="/static/js/save_as.js/"></script>
</body>
</html>

            '''.format(humour_result=humour_result,share=False,grammatical_errors=grammatical_errors)
    return '''
<!DOCTYPE html>
<html lang="en" >
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GENERATOR STORY</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/meyer-reset/2.0/reset.min.css">
    <link rel="stylesheet" href="/static/css/humour_style.css/">
    <link rel="stylesheet" href="/static/css/text-glitch-style.css/">
    <link rel="stylesheet" href="/static/css/glitching-granny-image-style.css">
</head>
<body>
    {errors}


        <div id="glitch-granny-text-container">
        <div class="glitch" data-text="G" width="400">GENERATOR STORY</div>
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
            <defs>
            <filter id="glitch" x="0" y="0">
                <feColorMatrix in="SourceGraphic" mode="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r" />
                    
                <feOffset in="r" result="r" dx="-5">
                <animate attributeName="dx" attributeType="XML" values="0; -2; 0; -18; -2; -4; 0 ;-1; 0" dur="1s" repeatCount="indefinite"/>
                </feOffset>
                <feColorMatrix in="SourceGraphic" mode="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0" result="g"/>
                <feOffset in="g" result="g" dx="-5" dy="1">
                <animate attributeName="dx" attributeType="XML" values="0; 0; 0; -3; 0; 8; 0 ;-1; 0" dur="2s" repeatCount="indefinite"/>
                </feOffset>
                <feColorMatrix in="SourceGraphic" mode="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" result="b"/>
                <feOffset in="b" result="b" dx="5" dy="2">
                <animate attributeName="dx" attributeType="XML" values="0; 3; -1; 4; 0; 2; 0 ;18; 0" dur="4s" repeatCount="indefinite"/>
                </feOffset>
                <feBlend in="r" in2="g" mode="screen" result="blend" />
                <feBlend in="blend" in2="b" mode="screen" result="blend" />
            </filter>
            </defs>
        </svg>
        </div>


    <h1 id="suggest">SUGGEST A LINE TO START A STORY WITH</h1><br/>
    <form class="form" method="post" action="/funny">
    <div id="form-container">
        <div class="form-group">
            <!--<textarea name="number1" placeholder="Starting of story" rows="4" cols="50"></textarea>-->
            <textarea name="start_of_story_post_request" placeholder="Starting of story" class="form-control" id="formGroupExampleInput"></textarea></br>
            <div class="slidecontainer">
                <p>Word Limit (<span id="demo"></span> Words)</p><br>
                <input type="range" min="50" max="400" value="225" class="slider" id="myRange" name="word_limit" value="225">  
            </div>
        </div>
        <button type="submit" class="btn btn-primary">Tell me a story</button>
    </div>
    </form>


    <div id="loader" style="display:none">
    <img src="https://media1.giphy.com/media/1YcLOSW6JCNdsfSr5E/200w.gif" height="200" width="200"/>
    <p><i class="fas fa-pencil-alt"></i>  Writing a Funny Story... </p>
    </div>


<img src="https://c.tenor.com/h7xHyShRg3kAAAAi/laugh-emoji.gif"/>


    <center>
<img src=""/>
</center>

<!-- partial -->
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
<script src='https://cdnjs.cloudflare.com/ajax/libs/dat-gui/0.5/dat.gui.min.js'></script>
<script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js'></script>
<script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
<script src="https://kit.fontawesome.com/5de545e21a.js" crossorigin="anonymous"></script>
<script src="/static/js/script.js/"></script>
</body>
</html>

    '''.format(errors=errors)

################################################################################
#                              SCIFI STORIES
################################################################################

@app.route('/scifi', methods=["GET", "POST"])
def adder_page_scifi():
    global scifi_result
    global scifi_start_with
    global scifi_word_limit
    global share
    global grammatical_errors
    errors = ""
    if request.method == "POST":
        try:
            scifi_start_with = (request.form["start_of_story_post_request"])
        except:
            errors = "Something Unusual"
        try:
            scifi_word_limit = int(request.form["word_limit"])
        except:
            errors = "Something Unusual"
        try:
            thread = threading.Thread(target=scifi_generate_story)
            thread.start()
            thread.join()
            #share = pastebin_share(scifi_result,"Scifi")
            #grammatical_errors = grammar_check(scifi_result)
        except:
            result="N/A"
        return '''

<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GENERATOR STORY</title>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
  <link rel="stylesheet" href="/static/css/scifi_style.css/">
  <link rel="stylesheet" href="/static/css/textbox-notebook-effect.css/">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Dancing+Script&display=swap" rel="stylesheet">
  <script src="/static/js/tts.js/"></script>

</head>
<body>

<div class="wrapper">
  <h1><h1><i class="fas fa-book-dead"></i>   We wrote you a Scifi story</h1></h1>
</div>

    
	<textarea id="text-to-speech">
    {scifi_result}
    </textarea>

        <div><button type="button" onclick="textToAudio()"><i class="fas fa-volume-up"></i>   Narrate</button>
        <button onclick="saveTextAsFile()"><i class="fas fa-download"></i>   Download The Story</button>
        <!-- Button trigger modal -->
        <button type="button" data-toggle="modal" data-target="#exampleModalCenter"><i class="fas fa-share-alt"></i>    Share</button>
        <button type="button" data-toggle="modal" data-target="#exampleModalLong"><i class="fas fa-exclamation-circle"></i>    Grammatical Errors</button>
        <button type="button" data-toggle="modal" data-target=".bd-example-modal-lg"><i class="fas fa-project-diagram"></i>    Add To Wall</button>

<div class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <iframe frameborder="0" style="height:500px;width:99%;border:none;" src='https://forms.zohopublic.in/maliciousyunk/form/Clientreview/formperma/rSA2h2eUY9ktKDEIlqXnvPUPMlE5uGuWe_EZ0bTfjDM'></iframe>
    </div>
  </div>
</div>

<!-- Modal -->
<div class="modal fade" id="exampleModalCenter" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLongTitle">Modal title</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
      <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={share}"><br/></br>
       <input type="text" value="{share}" id="url" size="30" readonly>
        <div id="share-buttons">
        <!-- Email -->
    <a href="mailto:?Subject=Simple Share Buttons&amp;Body=AI%20Generated%20SScary%20Story%20 {share}">
        <img src="https://simplesharebuttons.com/images/somacro/email.png" alt="Email" />
    </a>

        <!-- Facebook -->
    <a href="http://www.facebook.com/sharer.php?u={share}" target="_blank">
        <img src="https://simplesharebuttons.com/images/somacro/facebook.png" alt="Facebook" />
    </a>

        <!-- LinkedIn -->
    <a href="http://www.linkedin.com/shareArticle?mini=true&amp;url={share}" target="_blank">
        <img src="https://simplesharebuttons.com/images/somacro/linkedin.png" alt="LinkedIn" />
    </a>

        <!-- Print -->
    <a href="javascript:;" onclick="window.print()">
        <img src="https://simplesharebuttons.com/images/somacro/print.png" alt="Print" />
    </a>

        <!-- Reddit -->
    <a href="http://reddit.com/submit?url={share};title=GRANNY" target="_blank">
        <img src="https://simplesharebuttons.com/images/somacro/reddit.png" alt="Reddit" />
    </a>

        <!-- StumbleUpon-->
    <a href="http://www.stumbleupon.com/submit?url={share};title=GRANNY" target="_blank">
        <img src="https://simplesharebuttons.com/images/somacro/stumbleupon.png" alt="StumbleUpon" />
    </a>
    
    <!-- Tumblr-->
    <a href="http://www.tumblr.com/share/link?url={share};title=GRANNY" target="_blank">
        <img src="https://simplesharebuttons.com/images/somacro/tumblr.png" alt="Tumblr" />
    </a>
     
    <!-- Twitter -->
    <a href="https://twitter.com/share?url={share};text=AI%20Generated%20Story&amp;hashtags=granny" target="_blank">
        <img src="https://simplesharebuttons.com/images/somacro/twitter.png" alt="Twitter" />
    </a>


        </div>
        
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" onclick="copy_that()">Copy</button>
      </div>
    </div>
  </div>
</div>
</div>

        
        </div>

<!-- Modal for grammar check-->
<div class="modal fade" id="exampleModalLong" tabindex="-1" role="dialog" aria-labelledby="exampleModalLongTitle" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
      <font color="black">
        <h5 class="modal-title" id="exampleModalLongTitle">Possible Grammatical Errors</h5>
    </font>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <font color="black">


        {grammatical_errors}


        </font>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>

<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
<script src="https://kit.fontawesome.com/5de545e21a.js" crossorigin="anonymous"></script>
<script src="/static/js/script.js/"></script>
<script src="/static/js/save_as.js/"></script>
<script src="/static/js/copy_function.js/"></script>
</body>
</html>

            '''.format(scifi_result=scifi_result,share=False,grammatical_errors=grammatical_errors)
    return '''
<!DOCTYPE html>
<html lang="en" >
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GENERATOR STORY</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/meyer-reset/2.0/reset.min.css">
    <link rel="stylesheet" href="/static/css/scifi_style.css/">
    <link rel="stylesheet" href="/static/css/text-glitch-style.css/">
    <link rel="stylesheet" href="/static/css/glitching-granny-image-style.css">
</head>
<body>
    {errors}


        <div id="glitch-granny-text-container">
        <div class="glitch" data-text="G">GENERATOR STORY</div>
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
            <defs>
            <filter id="glitch" x="0" y="0">
                <feColorMatrix in="SourceGraphic" mode="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r" />
                    
                <feOffset in="r" result="r" dx="-5">
                <animate attributeName="dx" attributeType="XML" values="0; -2; 0; -18; -2; -4; 0 ;-1; 0" dur="1s" repeatCount="indefinite"/>
                </feOffset>
                <feColorMatrix in="SourceGraphic" mode="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0" result="g"/>
                <feOffset in="g" result="g" dx="-5" dy="1">
                <animate attributeName="dx" attributeType="XML" values="0; 0; 0; -3; 0; 8; 0 ;-1; 0" dur="2s" repeatCount="indefinite"/>
                </feOffset>
                <feColorMatrix in="SourceGraphic" mode="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" result="b"/>
                <feOffset in="b" result="b" dx="5" dy="2">
                <animate attributeName="dx" attributeType="XML" values="0; 3; -1; 4; 0; 2; 0 ;18; 0" dur="4s" repeatCount="indefinite"/>
                </feOffset>
                <feBlend in="r" in2="g" mode="screen" result="blend" />
                <feBlend in="blend" in2="b" mode="screen" result="blend" />
            </filter>
            </defs>
        </svg>
        </div>

    <h1 id="suggest">SUGGEST A PROMPT TO START A STORY WITH</h1><br/>
    <form class="form" method="post" action="/scifi">
    <div id="form-container">
        <div class="form-group">
            <!--<textarea name="number1" placeholder="Starting of story" rows="4" cols="50"></textarea>-->
            <textarea name="start_of_story_post_request" placeholder="Starting of story" class="form-control" id="formGroupExampleInput"></textarea></br>
            <div class="slidecontainer">
                <p>Word Limit (<span id="demo"></span> Words)</p><br>
                <input type="range" min="50" max="400" value="225" class="slider" id="myRange" name="word_limit" value="225">  
            </div>
        </div>
        <button type="submit" class="btn btn-primary">Tell me a story</button>
    </div>
    </form>


    <div id="loader" style="display:none">
    <img src="https://1.bp.blogspot.com/-mZ8iF5zav0w/X8-PTwg3EyI/AAAAAAAABu0/GW1KVkmX9nQf9NQW_FTF8qbA6--iicw_gCLcBGAsYHQ/s320/flying_granny.gif" height="200" width="250"/>
    <p><i class="fas fa-pencil-alt"></i> Writing a Scifi Story... </p>
    </div>





  <img src="https://1.bp.blogspot.com/-2mPPg1BI9RM/X8dCSj0AbLI/AAAAAAAABuI/IwtAbLi62MIElNlZqTdVBKVcRYSu_gqqACLcBGAsYHQ/s320/oie_282223EToXDaF.gif"/>
		
</div> <!-- /.glitch-container -->

<!-- partial -->
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
<script src='https://cdnjs.cloudflare.com/ajax/libs/dat-gui/0.5/dat.gui.min.js'></script>
<script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js'></script>
<script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
<script src="https://kit.fontawesome.com/5de545e21a.js" crossorigin="anonymous"></script>
<script src="/static/js/script.js/"></script>
</body>
</html>

    '''.format(errors=errors)


if __name__ == '__main__':
    app.run()