class YOLOConverter:
    def __init__(self, annotations=None, successful_batch_data=None, image_width=None, image_height=None):
        self.annotations = annotations
        self.successful_batch_data = successful_batch_data
        self.image_width = image_width
        self.image_height = image_height

    def is_annot_yolo_format(self):
        """
        Check if the given annotations follow YOLO format.
        """
        if isinstance(self.annotations, dict):
            for annot in self.annotations.values():
                if isinstance(annot, list) and len(annot) == 1 and isinstance(annot[0], str):
                    try:
                        int(annot[0])
                        return True
                    except ValueError:
                        return False
        return False

    def is_pred_yolo_format(self):
        """
        Check if the given predictions follow YOLO format.
        YOLO predictions typically contain class, confidence, and optionally loss.
        """
        if isinstance(self.successful_batch_data, list) and len(self.successful_batch_data) > 0:
            pred = self.successful_batch_data[0]
            return all(key in pred for key in ['image_id', 'class', 'confidence'])
        return False

    def convert_annotations(self):
        """
        Convert YOLO annotations to the custom format used in the codebase.
        """
        custom_annotations = {}
        for image_id, annotations in self.annotations.items():
            custom_annotations[image_id] = {
                "annotation": [{
                    'id': 0,
                    'label': int(annotations[0])
                }]
            }
        return custom_annotations

    def convert_annot_if_needed(self):
        """
        Convert to custom format if the annotations are in YOLO format.
        """
        if self.is_annot_yolo_format():
            print("Annotations are in YOLO format. Converting to custom format.")
            return self.convert_annotations()
        else:
            print("Annotations are already in custom format. No conversion needed.")
            return self.annotations

    def convert_predictions(self):
        """
        Convert predictions from YOLO format to the custom format.
        """
        custom_predictions = {}
        for pred in self.successful_batch_data:
            image_id = pred['image_id']
            class_id = pred['class']
            confidence = pred['confidence']
            loss = pred.get('loss', None)
            
             # Initialize logits with zeros for two categories
            logits = [0.0, 0.0]
            logits[class_id] = confidence  # Set confidence at the index of category_id
            logits[1 - class_id] = 1 - confidence  # Set the remaining confidence value
            
            custom_predictions[image_id] = {
                'image_id': image_id,
                'prediction_class': class_id,
                'confidence': confidence,
                'logits': logits,
                'loss': loss
            }
        return custom_predictions

    def convert_pred_if_needed(self):
        """
        Convert to custom format if the predictions are in YOLO format.
        """
        if self.is_pred_yolo_format():
            print("Predictions are in YOLO format. Converting to custom format.")
            return self.convert_predictions()
        else:
            print("Predictions are already in custom format. No conversion needed.")
            return self.successful_batch_data