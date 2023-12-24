import gradio as gr
from main import get_form_and_result

# Create title, description and article strings
title = "Question and answer based on Roberta model"
description = "سیستم پردازش زبانی"


demo = gr.Interface(fn=get_form_and_result,  # mapping function from input to output
                    inputs=[gr.Textbox(label='متن خود را وارد کنید:', show_label=True, text_align='right', lines=2)], # what are the inputs?
                    outputs=gr.Text(show_copy_button=True), # what are the outputs?
                    # Create examples list from "examples/" directory
                    title=title,
                    description=description
                    )

if __name__ == '__main__':
    # Launch the demo!
    demo.launch(share=True)
