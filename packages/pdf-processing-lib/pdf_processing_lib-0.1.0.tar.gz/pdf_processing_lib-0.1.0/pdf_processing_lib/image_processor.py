import os
import cv2
import pandas as pd
from ultralytics import YOLO
from joblib import Parallel, delayed
import gc
import time

class ImageProcessor:
    def __init__(self, model_path):
        self.model_path = model_path

    def process_and_save_image(self, image_path, output_folder):
        # Load the model in this process
        model = YOLO(self.model_path)
        
        results = model(image_path, conf=0.12)
        image = cv2.imread(image_path)
        boxes = results[0].boxes.xyxy.cpu().numpy()
        class_ids = results[0].boxes.cls.cpu().numpy()
        confidences = results[0].boxes.conf.cpu().tolist()
        names = results[0].names

        data = []
        for box, class_id, confidence in zip(boxes, class_ids, confidences):
            x1, y1, x2, y2 = box
            class_id = int(class_id)
            class_name = names[class_id]
            data.append([x1, y1, x2, y2, confidence, class_id, class_name])

        df = pd.DataFrame(data, columns=['x1', 'y1', 'x2', 'y2', 'confidence', 'class_id', 'class_name'])

        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(output_folder, f'{base_name}.tsv')
        df.to_csv(output_path, sep='\t', index=False)

    def process_images_in_output_folder(self, output_folder):
        image_folder = os.path.join(output_folder, f"{os.path.basename(output_folder[:-7])}_images")
        if os.path.exists(image_folder):
            results_yolo_folder = os.path.join(output_folder, "results_yolo")
            os.makedirs(results_yolo_folder, exist_ok=True)

            image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f)) and f.lower().endswith('.jpg')]
            
            start_time = time.time()

            max_processes = 8
            batch_size = 250
            for i in range(0, len(image_files), batch_size):
                batch_files = image_files[i:i+batch_size]
                
                Parallel(n_jobs=max_processes, backend='loky')(delayed(self.process_and_save_image)(image_file, results_yolo_folder) for image_file in batch_files)
                
                gc.collect()

            end_time = time.time()

            return len(image_files), end_time - start_time
        return 0, 0

    def process_directory(self, input_directory):
        total_images_processed = 0
        total_time_spent = 0.0

        for entry in os.listdir(input_directory):
            path = os.path.join(input_directory, entry)
            if os.path.isdir(path) and path.endswith('_output'):
                images_processed, time_spent = self.process_images_in_output_folder(path)
                total_images_processed += images_processed
                total_time_spent += time_spent

        avg_time_per_image = total_time_spent / total_images_processed if total_images_processed > 0 else 0

        print(f"Total JPEG images processed: {total_images_processed}")
        print(f"Total processing time: {total_time_spent:.2f} seconds.")
        print(f"Average time per JPEG image: {avg_time_per_image:.2f} seconds.")

        return total_images_processed, total_time_spent, avg_time_per_image