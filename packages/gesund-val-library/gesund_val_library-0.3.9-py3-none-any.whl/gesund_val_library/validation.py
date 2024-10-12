import json
import bson
import os
from gesund_val_library.utils.io_utils import read_json, save_plot_metrics_as_json, format_metrics
from gesund_val_library.utils.yolo_converter import YOLOConverter
from gesund_val_library.utils.coco_converter import COCOConverter
from gesund_val_library.problem_type_factory import get_validation_creation

def run_metrics(args):
    """Run validation metrics based on the passed arguments."""
    try:
        successful_batch_data = read_json(args['predictions'])
        annotation_data = read_json(args['annotations_json_path'])
        class_mappings = read_json(args['class_mappings'])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading input files: {e}")
        return None

    batch_job_id = str(bson.ObjectId())
    output_dir = os.path.join("outputs", batch_job_id)

    if args['format'] == 'coco':
        converter_annot = COCOConverter(annotations=annotation_data, problem_type=args['problem_type'])
        converter_pred = COCOConverter(successful_batch_data=successful_batch_data, problem_type=args['problem_type'])
        annotation_data = converter_annot.convert_annot_if_needed()
        successful_batch_data = converter_pred.convert_pred_if_needed()

    elif args['format'] == 'yolo':
        yolo_converter = YOLOConverter(annotations=annotation_data, successful_batch_data=successful_batch_data)
        annotation_data = yolo_converter.convert_annot_if_needed()
        successful_batch_data = yolo_converter.convert_pred_if_needed()

    elif args['format'] == 'gesund_custom_format':
        pass

    ValidationCreationClass = get_validation_creation(args['problem_type'])
    validation = ValidationCreationClass(batch_job_id)

    try:
        validation_data = validation.create_validation_collection_data(successful_batch_data, annotation_data, args['format'])
        metrics = validation.load(validation_data, class_mappings)
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        return None

    #formatted_metrics = format_metrics(metrics)

    if args.get('write_results_to_json', False):
        save_plot_metrics_as_json(metrics, output_dir)
    validation.plot_metrics(metrics, output_dir)

    return metrics
