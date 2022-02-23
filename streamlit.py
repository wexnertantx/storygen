from cProfile import label
import streamlit as st
from transformers import pipeline,AutoTokenizer, AutoModelForCausalLM

# @st.cache(suppress_st_warning=True)
def generateText(inputtext,storylen,genre,page):
    if page==0:
            tokenizer = AutoTokenizer.from_pretrained("pranavpsv/genre-story-generator-v2")
            model = AutoModelForCausalLM.from_pretrained("pranavpsv/genre-story-generator-v2", pad_token_id=tokenizer.eos_token_id)
            textinp="<BOS> <"+genre+"> "+inputtext+ "Tell me what happens in the story and how the story ends."
            input=tokenizer(textinp, add_special_tokens=False, return_tensors="pt")["input_ids"]
            prompt_length = len(tokenizer.decode(input[0]))
            outputs = model.generate(input, max_length=story_length, do_sample=True, top_p=0.95, top_k=60)
            generated = story_start_with + tokenizer.decode(outputs[0],skip_special_tokens=True)[prompt_length+1:]
            #horror_result= story_gen("<BOS> <horror> "+horror_start_with+ "Tell me what happens in the story and how the story ends.",max_length=horror_length)[0]['generated_text'].replace("<BOS> <horror> ","")
            
            return(generated)
    # elif page==1:
    #         sess = gpt2_simple.start_tf_sess()
    #         gpt2_simple.load_gpt2(sess)
    #         scary_result = str(gpt2_simple.generate(sess, run_name='run1', length=storylen,temperature=0.7, top_k=96,prefix=inputtext,return_as_list=True)[0]).replace("\n","")
    #         gpt2_simple.reset_session(sess)
    #         return scary_result


pageno=st.sidebar.selectbox('Choose generator type',["Pipeline Based(Huggingface)","Model Based"])
if pageno=="Pipeline Based(Huggingface)":
    page=0
    st.title("GeneratorStory-Pipeline Based Text Generation")
    #story_gen = pipeline("text-generation", "pranavpsv/genre-story-generator-v2",max_length=400)
    with st.form('textgenform'):
        story_start_with=st.text_input(label="Input your story prompt")
        story_length=st.slider("Maximum word length",min_value=50,max_value=400)
        genre=st.selectbox('Choose your genre:',('Horror','Drama','Scifi'))
        genre=genre.lower()
        if genre=="scifi":
            genre="sci_fi"
        
        submit=st.form_submit_button("Submit")
        if submit:
            st.write("<DEBUGGING PURPOSES>Genre Chosen:",genre)
            textinp="<BOS> <"+genre+"> "+story_start_with+ "Tell me what happens in the story and how the story ends."
            st.write("<DEBUGGING PURPOSES>Text input: ",textinp)
            with st.spinner(text="In progress..."):
                
                st.write(generateText(story_start_with,story_length,genre,page))
                # input=tokenizer(textinp, add_special_tokens=False, return_tensors="pt")["input_ids"]
                # prompt_length = len(tokenizer.decode(input[0]))
                # outputs = model.generate(input, max_length=story_length, do_sample=True, top_p=0.95, top_k=60)
                # generated = story_start_with + tokenizer.decode(outputs[0],skip_special_tokens=True)[prompt_length+1:]
                # #horror_result= story_gen("<BOS> <horror> "+horror_start_with+ "Tell me what happens in the story and how the story ends.",max_length=horror_length)[0]['generated_text'].replace("<BOS> <horror> ","")
                # st.write(generated)
# if pageno=="Model Based":
#     page=1
#     import gpt_2_simple as gpt2_simple

#     st.title("GeneratorStory-Pipeline Based Text Generation")
#     #story_gen = pipeline("text-generation", "pranavpsv/genre-story-generator-v2",max_length=400)
#     with st.form('modelgenform'):
#         story_start_with=st.text_input(label="Input your story prompt")
#         story_length=st.slider("Maximum word length",min_value=50,max_value=400)
#         genre=st.selectbox('Choose your genre:',('Horror','Drama','Scifi'))
#         genre=genre.lower()
#         if genre=="scifi":
#             genre="sci_fi"
#         submit=st.form_submit_button("Submit")
#         if submit:
#             st.write("<DEBUGGING PURPOSES>Genre Chosen:",genre)
#             textinp="<BOS> <"+genre+"> "+story_start_with+ "Tell me what happens in the story and how the story ends."
#             st.write("<DEBUGGING PURPOSES>Text input: ",textinp)
#             with st.spinner(text="In progress..."):
                
#                 print(generateText(story_start_with,story_length,genre,page))