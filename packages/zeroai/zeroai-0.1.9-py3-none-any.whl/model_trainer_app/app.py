# model_trainer_app/app.py

import os
import zipfile
import json
from PIL import Image
from datasets import Dataset, Features, Sequence, Value, ClassLabel, Image as Img, Array2D, Array3D
from transformers import Trainer, TrainingArguments, AutoProcessor, LiltForTokenClassification
from transformers.data.data_collator import default_data_collator
import evaluate
import numpy as np
import shutil
import threading
import subprocess
import time
import re  # For validating model names
import requests  # For sending HTTP requests
import base64
from flask_cors import CORS

from flask import Flask, request, jsonify, Response

class ModelTrainerApp:
    def __init__(self):
        # Initialize Flask app
        self.app = Flask(__name__)
        CORS(self.app,resources={r"/*": {"origins": "*"}},supports_credentials=True)  # Enable CORS for all routes

        self.setup_routes()

    def setup_routes(self):
        # Define your route for model training
        @self.app.route('/train-model', methods=['POST'])
        def train_model():
            # [Your existing training code]
            # Get input parameters
            data =request.get_json()
            model_name = data.get('model_name')
            zip_file = data.get('zip_file_data')
            test_size = float(data.get('test_size', 0.33))
            learning_rate = float(data.get('learning_rate', 4e-5))
            num_train_epochs = int(data.get('num_train_epochs', 50))

            # Validate input parameters
            if not model_name or not zip_file:
                return jsonify({'error': 'Model name and zip file are required.'}), 400

            # Validate model_name to contain only allowed characters
            if not re.match("^[A-Za-z0-9_-]+$", model_name):
                return jsonify({'error': 'Invalid model name. Use only letters, numbers, underscores, and hyphens.'}), 400

            # Prepare working directories
            data_dir = 'data'  # Changed to relative paths
            output_dir = 'output_model'
            if os.path.exists(data_dir):
                shutil.rmtree(data_dir)
            os.makedirs(data_dir, exist_ok=True)
            os.makedirs(output_dir, exist_ok=True)

            # Save and extract zip file
            zip_path = os.path.join(data_dir, 'data.zip')
            try:
                zip_data = base64.b64decode(zip_path)
            except Exception as e:
                return jsonify({'error': 'Failed to decode base64 data: ' + str(e)})
            
                # Save the decoded zip file
            with open(zip_path, 'wb') as f:
                f.write(zip_data)

            # Try to open the zip file to check its validity
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(data_dir)
            except zipfile.BadZipFile:
                return jsonify({'error': 'The file is not a valid zip file'})

            # Locate JSON and images directory
            json_file = None
            images_dir = None

            # Traverse extracted files to find JSON and image folder
            for root, dirs, files in os.walk(data_dir):
                for file in files:
                    if file.endswith('.json'):
                        json_file = os.path.join(root, file)
                for directory in dirs:
                    images_dir = os.path.join(root, directory)

            if not json_file or not images_dir:
                return jsonify({'error': 'JSON file or image directory not found in the zip.'}), 400

            # Read and parse JSON file
            with open(json_file, 'r') as file:
                data = json.load(file)

            words1, bboxes1, ner_tags1, image_path1 = [], [], [], []

            # Process JSON data
            for entry in data:
                file_name = os.path.basename(entry['file_name'])
                image_path1.append(file_name)

                words, bboxes, ner_tags = [], [], []
                for annotation in entry.get('annotations', []):
                    words.append(annotation.get('text', ''))
                    bboxes.append(annotation.get('box', [0, 0, 0, 0]))
                    ner_tags.append(annotation.get('label', 'O'))  # Default label 'O' for Outside
                words1.append(words)
                bboxes1.append(bboxes)
                ner_tags1.append(ner_tags)

            # Validate image paths
            image_path = [os.path.join(images_dir, f) for f in image_path1 if os.path.exists(os.path.join(images_dir, f))]

            if len(image_path) != len(image_path1):
                return jsonify({'error': 'Some images listed in JSON not found in the zip file.'}), 400

            # Prepare label mappings
            labels = sorted(list(set([tag for doc_tag in ner_tags1 for tag in doc_tag])))
            id2label = {v: k for v, k in enumerate(labels)}
            label2id = {k: v for v, k in enumerate(labels)}

            # Create dataset
            dataset_dict = {
                'id': [str(i) for i in range(len(words1))],
                'tokens': words1,
                'bboxes': [[list(map(int, bbox)) for bbox in doc] for doc in bboxes1],
                'ner_tags': [[label2id.get(tag, 0) for tag in ner_tag] for ner_tag in ner_tags1],
                'image': [Image.open(path).convert("RGB") for path in image_path]
            }

            features = Features({
                'id': Value(dtype='string'),
                'tokens': Sequence(Value(dtype='string')),
                'bboxes': Sequence(Sequence(Value(dtype='int64'))),
                'ner_tags': Sequence(ClassLabel(names=labels)),
                'image': Img(decode=True)
            })

            full_dataset = Dataset.from_dict(dataset_dict, features=features)
            dataset = full_dataset.train_test_split(test_size=test_size)

            processor = AutoProcessor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=False)

            def prepare_examples(examples):
                images = examples['image']
                words = examples['tokens']
                boxes = examples['bboxes']
                word_labels = examples['ner_tags']
                encoding = processor(images, words, boxes=boxes, word_labels=word_labels,
                                     truncation=True, padding="max_length")
                return encoding

            features = Features({
                'pixel_values': Array3D(dtype="float32", shape=(3, 224, 224)),
                'input_ids': Sequence(feature=Value(dtype='int64'), length=512),
                'attention_mask': Sequence(Value(dtype='int64'), length=512),
                'bbox': Array2D(dtype="int64", shape=(512, 4)),
                'labels': Sequence(ClassLabel(names=labels), length=512),
            })

            print('Preparing datasets...')

            train_dataset = dataset['train'].map(prepare_examples, batched=True, remove_columns=dataset['train'].column_names, features=features)
            eval_dataset = dataset['test'].map(prepare_examples, batched=True, remove_columns=dataset['test'].column_names, features=features)
            train_dataset.set_format("torch")
            eval_dataset.set_format("torch")

            # Initialize model and training arguments
            model_id = "SCUT-DLVCLab/lilt-roberta-en-base"
            model = LiltForTokenClassification.from_pretrained(
                model_id, num_labels=len(labels), label2id=label2id, id2label=id2label
            )
            metric = evaluate.load("seqeval")

            training_args = TrainingArguments(
                output_dir=output_dir,
                num_train_epochs=num_train_epochs,
                per_device_train_batch_size=4,
                per_device_eval_batch_size=4,
                learning_rate=learning_rate,
                save_total_limit=1,
                logging_strategy="epoch",
                evaluation_strategy="no",
                save_strategy="no",
                load_best_model_at_end=False
            )

            def compute_metrics(p):
                predictions, labels_ = p
                predictions = np.argmax(predictions, axis=2)

                # Remove ignored index (special tokens)
                true_predictions = [
                    [labels[p] for (p, l) in zip(prediction, label) if l != -100]
                    for prediction, label in zip(predictions, labels_)
                ]
                true_labels = [
                    [labels[l] for (p, l) in zip(prediction, label) if l != -100]
                    for prediction, label in zip(predictions, labels_)
                ]

                results = metric.compute(predictions=true_predictions, references=true_labels, zero_division='0')
                return {
                    "precision": results["overall_precision"],
                    "recall": results["overall_recall"],
                    "f1": results["overall_f1"],
                    "accuracy": results["overall_accuracy"],
                }

            # Train the model
            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=eval_dataset,
                compute_metrics=compute_metrics,
                data_collator=default_data_collator,
            )

            trainer.train()

            # Save the trained model
            model_path = os.path.join(output_dir, model_name)
            trainer.save_model(model_path)

            # Zip the model directory
            zip_model_path = model_path + '.zip'
            shutil.make_archive(model_path, 'zip', model_path)

            # Stream the zip file in chunks
            def generate():
                with open(zip_model_path, 'rb') as f:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        yield chunk

            # Return the streamed zip file as a response
            return Response(generate(), mimetype='application/zip',
                            headers={'Content-Disposition': f'attachment; filename={model_name}.zip'})


    def run_app(self):
        # Prompt for token
        # token = input("Enter your token: ")

        # Start Flask app in a separate thread
        flask_thread = threading.Thread(target=self.app.run, kwargs={'host': '0.0.0.0', 'port': 5000}, daemon=True)
        flask_thread.start()

        # Wait a moment for the server to start
        time.sleep(5)

        # Start Localtunnel process and capture the URL
        try:
            public_url = self.start_localtunnel()
            print(f"Public URL: {public_url}")
        except Exception as e:
            print(f"Failed to start Localtunnel: {e}")
            return

        # # Prepare authentication payload
        # auth_payload = {
        #     "token": token,
        #     "public_url": public_url
        # }

        # # Send authentication request to localhost:5001
        # auth_url = "http://127.0.0.1:15097/token_verifer_gpu"  # Adjust the endpoint as needed
        # try:
        #     response = requests.post(auth_url, json=auth_payload)
        # except requests.exceptions.RequestException as e:
        #     print(f"Failed to connect to authentication server: {e}")
        #     return

        # if response.status_code == 200:
        #     try:
        #         response_data = response.json()
        #         print(response_data)
        #         is_valid = response_data.get("valid", False)
        #         if is_valid:
        #             print("Token is valid. Application is running.")
        #             print("Keep the application running to maintain the server.")
        #         else:
        #             error_message = response_data.get("error", "Token is invalid.")
        #             print(f"Login unsuccessful: {error_message}")
        #             return
        #     except json.JSONDecodeError:
        #         print("Login failed: Invalid JSON response.")
        #         return
        # else:
        #     try:
        #         error_message = response.json().get("error", "Unknown error.")
        #         print(f"Login unsuccessful: {error_message}")
        #     except json.JSONDecodeError:
        #         print(f"Login unsuccessful: Status code {response.status_code}")
        #     return

        # Keep the process running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down...")

    def start_localtunnel(self):
        # Start Localtunnel and capture the URL
        command = ['lt', '--port', '5000', '--print-requests']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Read output line by line to get the URL
        public_url = None
        for line in iter(process.stdout.readline, ''):
            if 'your url is:' in line:
                public_url = line.split(' ')[-1].strip()
                break

        if not public_url:
            raise Exception("Failed to get public URL from Localtunnel.")

        return public_url

if __name__ == '__main__':
    app_instance = ModelTrainerApp()
    app_instance.run_app(host='0.0.0.0')
