import customtkinter as ctk
from PIL import Image
import numpy as np
import tensorflow as tf
import os
import matplotlib.cm as cm
import scipy.ndimage

# Configure modern appearance
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Set up model path and classes
MODEL_PATH = 'fruit_classification_model.h5'
CLASS_NAMES = ["Fresh", "Rotten"]
model = None

def load_model():
    global model
    try:
        if os.path.exists(MODEL_PATH):
            model = tf.keras.models.load_model(MODEL_PATH, compile=False)
            return True
    except Exception as e:
        print(f"Error loading model: {e}")
    return False

def classify_image(file_path):
    if model is None:
        return "Model not loaded", 0.0
    
    img = tf.keras.preprocessing.image.load_img(file_path, target_size=(224, 224), color_mode="rgb")
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) 
    
    predictions = model.predict(img_array, verbose=0)
    winning_index = int(np.argmax(predictions[0]))
    confidence = float(np.max(predictions[0]) * 100)
    
    guess_label = CLASS_NAMES[winning_index] if winning_index < len(CLASS_NAMES) else str(winning_index)
    return guess_label, confidence

def get_gradcam_overlay(file_path):
    # 1. Find the last Conv2D layer dynamically
    last_conv_layer = None
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            last_conv_layer = layer
            break
            
    if not last_conv_layer:
        return None
        
    # 2. Build model to get conv output and predictions
    inputs = model.inputs
    x = inputs
    intermediate_conv_output = None
    for layer in model.layers:
        x = layer(x)
        if layer == last_conv_layer:
            intermediate_conv_output = x
    final_model_output = x

    grad_model = tf.keras.models.Model(inputs, [intermediate_conv_output, final_model_output])

    # 3. Predict & Calculate gradients
    img = tf.keras.preprocessing.image.load_img(file_path, target_size=(224, 224), color_mode="rgb")
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array_batch = np.expand_dims(img_array, axis=0)

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array_batch)
        pred_index = tf.argmax(predictions[0])
        loss_val = predictions[:, pred_index]

    grads = tape.gradient(loss_val, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    heatmap = heatmap.numpy()
    
    # 4. Resize and overlay
    heatmap_resized = scipy.ndimage.zoom(heatmap, (224 / heatmap.shape[0], 224 / heatmap.shape[1]), order=1)
    
    # Colorize
    jet = cm.get_cmap("jet")
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[np.uint8(heatmap_resized * 255)]
    
    # Mix heatmap & original image
    superimposed_img = (jet_heatmap * 255 * 0.5) + img_array
    superimposed_img = np.clip(superimposed_img, 0, 255).astype("uint8")
    
    return Image.fromarray(superimposed_img)

def show_explainability(file_path, prediction_label):
    if model is None:
        return
        
    popup = ctk.CTkToplevel(app)
    popup.title(f"AI Explainability: {prediction_label}")
    popup.geometry("600x400")
    popup.attributes("-topmost", True)
    popup.grab_set() # Lock focus to popup
    
    title = ctk.CTkLabel(popup, text="Grad-CAM: What the AI Looked At", font=ctk.CTkFont(size=20, weight="bold"))
    title.pack(pady=15)
    
    images_frame = ctk.CTkFrame(popup, fg_color="transparent")
    images_frame.pack(fill="both", expand=True, padx=20)
    
    # View 1: Original
    orig_img = Image.open(file_path).resize((224, 224))
    orig_ctk = ctk.CTkImage(light_image=orig_img, dark_image=orig_img, size=(224, 224))
    orig_lbl = ctk.CTkLabel(images_frame, image=orig_ctk, text="")
    orig_lbl.pack(side="left", expand=True)
    
    # View 2: Overlaid Heatmap
    heatmap_img = get_gradcam_overlay(file_path)
    if heatmap_img:
        heat_ctk = ctk.CTkImage(light_image=heatmap_img, dark_image=heatmap_img, size=(224, 224))
        heat_lbl = ctk.CTkLabel(images_frame, image=heat_ctk, text="")
        heat_lbl.pack(side="right", expand=True)
    else:
        err_lbl = ctk.CTkLabel(images_frame, text="Model doesn't have a Conv2D layer.\nHeatmap unsupported.", text_color="orange")
        err_lbl.pack(side="right", expand=True)

def upload_images():
    file_paths = ctk.filedialog.askopenfilenames(
        title="Select Fruit Images",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp"), ("All files", "*.*")]
    )
    if not file_paths:
        return
        
    # Clear the scrollable frame of any previous results
    for widget in results_scroll_frame.winfo_children():
        widget.destroy()

    info_label.configure(text=f"Classifying {len(file_paths)} image(s)...", text_color=("gray10", "gray90"))
    app.update()

    for file_path in file_paths:
        # Create a row container for each image
        row_frame = ctk.CTkFrame(results_scroll_frame, corner_radius=10, fg_color=("gray85", "gray15"))
        row_frame.pack(pady=10, padx=10, fill="x")

        # Load and scale the image
        try:
            my_image = ctk.CTkImage(light_image=Image.open(file_path),
                                    dark_image=Image.open(file_path),
                                    size=(120, 120))
            img_lbl = ctk.CTkLabel(row_frame, image=my_image, text="")
            img_lbl.pack(side="left", padx=15, pady=15)
        except Exception as e:
            img_lbl = ctk.CTkLabel(row_frame, text="[ Image Error ]", width=120, height=120)
            img_lbl.pack(side="left", padx=15, pady=15)

        # Run prediction
        label, confidence = classify_image(file_path)
        
        # Modern color coding
        color = "#22C55E" if label.lower() == "fresh" else "#EF4444" 
        filename = os.path.basename(file_path)
        
        # Details text
        details = (f"File: {filename}\n\n"
                   f"Prediction: {label}\n"
                   f"Confidence: {confidence:.2f}%")
        
        res_lbl = ctk.CTkLabel(row_frame, text=details, justify="left",
                               font=ctk.CTkFont(size=16, weight="bold"), text_color=color)
        res_lbl.pack(side="left", padx=20, pady=15)
        
        # New: Explainability Button ("Why?")
        explain_btn = ctk.CTkButton(row_frame, text="Why?", width=80,
                                    fg_color=("gray70", "gray30"), hover_color=("gray60", "gray40"), 
                                    text_color=("black", "white"), font=ctk.CTkFont(weight="bold"),
                                    command=lambda p=file_path, l=label: show_explainability(p, l))
        explain_btn.pack(side="right", padx=20, pady=15)

    info_label.configure(text=f"Finished analyzing {len(file_paths)} image(s).", text_color="#22C55E")

# --- GUI Setup ---
app = ctk.CTk()
app.title("Fresh vs Rotten AI")
app.geometry("600x700")

# Main Container Frame
frame = ctk.CTkFrame(app, corner_radius=15)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Title
title_label = ctk.CTkLabel(frame, text="🍏 AI Fruit Classifier 🍌", font=ctk.CTkFont(size=24, weight="bold"))
title_label.pack(pady=(20, 5))

subtitle = ctk.CTkLabel(frame, text="Select multiple images to classify them at once", font=ctk.CTkFont(size=14), text_color="gray")
subtitle.pack(pady=(0, 20))

# Upload Button
upload_btn = ctk.CTkButton(frame, text="Select Images", command=upload_images, 
                           font=ctk.CTkFont(size=15, weight="bold"),
                           corner_radius=8, height=40)
upload_btn.pack(pady=10)

# Info Text
info_label = ctk.CTkLabel(frame, text="Ready to classify.", font=ctk.CTkFont(size=14))
info_label.pack(pady=(5, 10))

# Scrollable Frame for Results
results_scroll_frame = ctk.CTkScrollableFrame(frame, corner_radius=10, fg_color=("gray90", "gray20"))
results_scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Model Loading Logic
print("Loading AI Model...")
if not load_model():
    info_label.configure(text=f"Error: Model not found at '{MODEL_PATH}'\nTrain/save the model first.", 
                         text_color="#EF4444")
    upload_btn.configure(state="disabled")

app.mainloop()
