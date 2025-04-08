import tkinter as tk
from tkinter import scrolledtext, messagebox
import ollama
import threading
import sys

MODEL_NAME = 'llama2'
chat_history = []

root = tk.Tk()
root.title(f"Pardus Ollama Chat - {MODEL_NAME}")
root.geometry("700x600")

def update_chat_display(message, role="Model"):
    chat_area.config(state=tk.NORMAL)
    if role == "Siz":
        chat_area.insert(tk.END, f"Siz: {message}\n\n", "user_message")
    elif role == "Model":
        chat_area.insert(tk.END, f"Model: {message}\n\n", "model_message")
    elif role == "Hata":
        chat_area.insert(tk.END, f"Hata: {message}\n\n", "error_message")
    else:
        chat_area.insert(tk.END, f"{message}\n\n", "system_message")
    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)

def update_chat_display_stream_start(text_part):
    chat_area.config(state=tk.NORMAL)
    try:
        last_line_start = chat_area.index("end-2l linestart")
        last_line_text = chat_area.get(last_line_start, "end-1c")
        if last_line_text.strip().startswith("Model yanıtı bekleniyor..."):
             chat_area.delete(last_line_start, "end-1c")
    except tk.TclError:
        pass

    chat_area.insert(tk.END, f"Model: {text_part}", "model_message")
    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)

def update_chat_display_stream_append(text_part):
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, text_part, "model_message")
    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)

def update_chat_display_stream_end():
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "\n\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)

def get_ollama_response_threaded(user_input):
    global chat_history

    root.after(0, lambda: input_field.config(state=tk.DISABLED))
    root.after(0, lambda: send_button.config(state=tk.DISABLED))
    root.after(0, lambda: update_chat_display("Model yanıtı bekleniyor...", role="Sistem"))

    try:
        chat_history.append({'role': 'user', 'content': user_input})

        stream = ollama.chat(
            model=MODEL_NAME,
            messages=chat_history,
            stream=True
        )

        full_response = ""
        first_chunk = True
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                response_part = chunk['message']['content']
                full_response += response_part
                if first_chunk:
                    root.after(0, lambda p=response_part: update_chat_display_stream_start(p))
                    first_chunk = False
                else:
                    root.after(0, lambda p=response_part: update_chat_display_stream_append(p))

        if full_response:
            chat_history.append({'role': 'assistant', 'content': full_response})
            root.after(0, update_chat_display_stream_end)
        else:
             root.after(0, lambda: update_chat_display("Modelden boş yanıt alındı.", role="Hata"))
             if chat_history and chat_history[-1]['role'] == 'user':
                  chat_history.pop()

    except Exception as e:
        error_message = f"Bağlantı hatası: {str(e)}"
        print(f"Hata: {e}", file=sys.stderr)
        if chat_history and chat_history[-1]['role'] == 'user':
            chat_history.pop()
        root.after(0, lambda: update_chat_display(error_message, role="Hata"))
    finally:
        root.after(0, lambda: input_field.config(state=tk.NORMAL))
        root.after(0, lambda: send_button.config(state=tk.NORMAL))
        root.after(10, lambda: input_field.focus_set())

def send_message(event=None):
    user_input = input_field.get("1.0", tk.END).strip()
    if user_input:
        update_chat_display(user_input, role="Siz")
        input_field.delete("1.0", tk.END)

        thread = threading.Thread(target=get_ollama_response_threaded, args=(user_input,))
        thread.daemon = True
        thread.start()
    else:
        messagebox.showwarning("Boş Mesaj", "Lütfen göndermek için bir mesaj yazın.")

def check_ollama_connection():
    update_chat_display("Ollama sunucusu kontrol ediliyor...", role="Sistem")
    try:
        response = ollama.list()
        if 'models' in response:
            available_models = [m['name'] for m in response['models']]
            if MODEL_NAME in available_models:
                update_chat_display(f"Bağlantı başarılı. {MODEL_NAME} modeli hazır.", role="Sistem")
                input_field.config(state=tk.NORMAL)
                send_button.config(state=tk.NORMAL)
                input_field.focus_set()
            else:
                update_chat_display(f"Model bulunamadı. Lütfen çalıştırın: 'ollama pull {MODEL_NAME}'", role="Hata")
        else:
            update_chat_display("Ollama'da kayıtlı model bulunamadı.", role="Hata")
    except Exception as e:
        update_chat_display(f"Ollama bağlantı hatası: {str(e)}", role="Hata")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, font=("Noto Sans", 11))
chat_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

chat_area.tag_configure("user_message", foreground="#00008B", font=("Noto Sans", 11, "bold"))
chat_area.tag_configure("model_message", foreground="#006400")
chat_area.tag_configure("error_message", foreground="#FF0000", font=("Noto Sans", 11, "italic"))
chat_area.tag_configure("system_message", foreground="#555555", font=("Noto Sans", 10, "italic"))

input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

input_field = tk.Text(input_frame, height=3, font=("Noto Sans", 11), wrap=tk.WORD)
input_field.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=5, padx=(0, 5))

send_button = tk.Button(input_frame, text="Gönder", command=send_message, font=("Noto Sans", 10, "bold"), width=10, height=2)
send_button.pack(side=tk.RIGHT)

root.after(500, check_ollama_connection)
root.mainloop()