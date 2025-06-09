from translator import DialogTranslator
import gradio as gr

dialog = DialogTranslator()

with gr.Blocks() as demo:
    gr.Markdown("# 🎙️ Anime Dialog Translator")

    with gr.Column():
        audio_file = gr.Audio(type="filepath", label="Upload Dialog", max_length=300)
        button = gr.Button("Translate", variant="primary")

    with gr.Column():
        gr.Label(value="Result of translated text to 'English' and 'Filipino'", label="Character")
        output_text = gr.Markdown(value="## Translated text here")

    button.click(
        fn=dialog.translate,
        inputs=audio_file,
        outputs=output_text,
        trigger_mode="once"
    )


def launch():
    demo.launch()
