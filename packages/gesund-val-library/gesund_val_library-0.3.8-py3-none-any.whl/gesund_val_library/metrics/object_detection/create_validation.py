import time
import datetime
import pandas as pd
import json
import numpy as np

from .plots.plot_driver import ObjectDetectionPlotDriver

class ValidationCreation:
    def __init__(self, batch_job_id, filter_field="image_url", generate_metrics=True):
        self.batch_job_id = batch_job_id
        self.filter_field = filter_field
        self.generate_metrics = generate_metrics

    def create_validation_collection_data(self, successful_batch_data, annotation_data, format):
        
        validation_collection_data = list()
        # To Do: Optimize this
        for image_id in successful_batch_data:
            batch_item = successful_batch_data[image_id]
            annotation_item = annotation_data[image_id]
            image_information_dict = {}
            image_information_dict["batch_job_id"] = self.batch_job_id
            image_information_dict["image_id"] = batch_item["image_id"]
            if format == 'coco':
                image_information_dict["shape"] = annotation_item["shape"]
            else:
                image_information_dict["shape"] = batch_item["shape"]
            image_information_dict["ground_truth"] = [
                {
                    "class": i["label"],
                    "box": {
                        "x1": i["points"][0]["x"],
                        "x2": i["points"][1]["x"],
                        "y1": i["points"][0]["y"],
                        "y2": i["points"][1]["y"],
                    },
                }
                for i in annotation_item["annotation"]
            ]
            image_information_dict["objects"] = batch_item["objects"]
            image_information_dict["created_timestamp"] = time.time()
            validation_collection_data.append(image_information_dict)
        return validation_collection_data
    
    
    def _load_plotting_data(
        self, validation_collection_data, class_mappings
    ):
        """
        Creates data for PlotValidation class(which gives payloads). Similar function in another class will be implemented for ModelValidation.

        :RaiseException: raises error if setup is not initialized.
        :return:  ground_truth_dict, logits_dict, meta_data_dict,loss_dict,img_source_dict
        """
        plotting_data = dict()
        plotting_data["per_image"] = self._craft_per_image_plotting_data(
            validation_collection_data
        )
        plotting_data["per_dataset"] = self._craft_per_dataset_plotting_data(
            validation_collection_data, class_mappings
        )
        return plotting_data

    def _craft_per_dataset_plotting_data(
        self, validation_collection_data, class_mappings
    ):

        per_dataset = dict()

        if validation_collection_data:
            per_dataset["prediction_coco"] = self._load_pred_coco(
                validation_collection_data
            )
            per_dataset["ground_truth_coco"] = self._load_annot_coco(
                validation_collection_data, class_mappings
            )

        return per_dataset

    def _craft_per_image_plotting_data(
        self, validation_collection_data
    ):
        """
        Creates data for PlotValidation class(which gives payloads). Similar function in another class will be implemented for ModelValidation.

        :RaiseException: raises error if setup is not initialized.
        :return:  ground_truth_dict, logits_dict, meta_data_dict,loss_dict,img_source_dict
        """
        data = dict()
        validation_df = pd.DataFrame(validation_collection_data)
        # Ground truth dict
        ground_truth_dict = validation_df[["image_id", "ground_truth"]].values
        ground_truth_dict = dict(zip(ground_truth_dict[:, 0], ground_truth_dict[:, 1]))
        # Prediction dict
        prediction_dict = validation_df[["image_id", "objects"]].values
        prediction_dict = dict(zip(prediction_dict[:, 0], prediction_dict[:, 1]))

        try:
            loss_dict = (
                validation_df[["image_id", "loss"]]
                .set_index("image_id")
                .to_dict()["loss"]
            )
        except:
            pass

        data["ground_truth"] = ground_truth_dict
        data["objects"] = prediction_dict

        try:
            data["loss"] = loss_dict
        except:
            pass
        return data

    def load(self, validation_collection_data, class_mappings, study_list=None):

        plotting_data = self._load_plotting_data(
            validation_collection_data=validation_collection_data, class_mappings=class_mappings
        )

        # Create per image variables
        ground_truth_dict = plotting_data["per_image"]["ground_truth"]
        prediction_dict = plotting_data["per_image"]["objects"]

        pred_coco = plotting_data["per_dataset"]["prediction_coco"]
        gt_coco = plotting_data["per_dataset"]["ground_truth_coco"]
        coco_ = [pred_coco, gt_coco]
        meta_data_dict = None

        try:
            meta_data_dict = plotting_data["per_image"]["meta_data"]
        except:
            print(
                "Meta Data not found.")

        loss_dict = None

        try:
            loss_dict = plotting_data["per_image"]["loss"]
        except:
            print(
                "Loss not found.")

        self.plot_driver = ObjectDetectionPlotDriver(
            coco_=coco_,
            class_mappings=class_mappings,
            ground_truth_dict=ground_truth_dict,
            prediction_dict=prediction_dict,
            meta_data_dict=meta_data_dict,
            loss_dict=loss_dict,
            batch_job_id=self.batch_job_id,
        )
        
        overall_metrics = self.plot_driver._calling_all_plots()

        # Remove mAP11@10 from overall_metrics
        if 'mAP11@10' in overall_metrics['main_metric']:
            del overall_metrics['main_metric']['mAP11@10']

        for key in overall_metrics['plot_blind_spot_metrics']:
            if 'AP11@10' in overall_metrics['plot_blind_spot_metrics'][key]:
                del overall_metrics['plot_blind_spot_metrics'][key]['AP11@10']

        if 'mAP11@10' in overall_metrics['plot_highlighted_overall_metrics']['data']:
            del overall_metrics['plot_highlighted_overall_metrics']['data']['mAP11@10']

        for key in overall_metrics['plot_statistics_classbased_table']['data']['Validation']:
            if 'AP11@10' in overall_metrics['plot_statistics_classbased_table']['data']['Validation'][key]:
                del overall_metrics['plot_statistics_classbased_table']['data']['Validation'][key]['AP11@10']
                
        return overall_metrics



    def _load_pred_coco(self, validation_collection_data=None):

        pred_dict_list = []
        predictions_list = validation_collection_data
        for pred in predictions_list:

            objects = pred["objects"]
            image_id = pred["image_id"]

            for object_ in objects:

                bbox = list(object_["box"].values())
                class_label = object_["prediction_class"]
                confidence = object_["confidence"]

                add_dict = {
                    "image_id": image_id,
                    "category_id": class_label,
                    "bbox": [
                        bbox[0],
                        bbox[1],
                        (bbox[2] - bbox[0]),
                        (bbox[3] - bbox[1]),
                    ],
                    "score": confidence,
                }
                pred_dict_list.append(add_dict)
        
        return pred_dict_list

    def _load_annot_coco(self, validation_collection_data=None, class_mappings=None):

        coco_dict = {
            "info": {
                "year": "2022",
                "version": "1.0",
                "description": "Exported from Gesund AI",
                "contributor": "Gesund AI",
                "url": "https://gesund.ai",
                "date_created": datetime.datetime.strftime(
                    datetime.datetime.now(), format="%Y-%m-%dT%H:%M:%S%z"
                ),
            },
            "licenses": [
                {
                    "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
                    "id": 1,
                    "name": "NonLicensed Annotation",
                },
            ],
            "categories": [
                {"id": 0, "name": "cat", "supercategory": "animal"},
            ],
            "images": [
                {
                    "id": 0,
                    "license": 1,
                    "file_name": None,
                    "height": 480,
                    "width": 640,
                    "date_captured": None,
                },
            ],
            "annotations": [
                {
                    "id": 0,
                    "image_id": 0,
                    "category_id": 2,
                    "bbox": [260, 177, 231, 199],
                    "segmentation": None,
                    "area": 45969,
                    "iscrowd": 0,
                },
            ],
        }

        categories = []

        for id_, name in class_mappings.items():
            categories.append({"id": int(id_), "name": name, "supercategory": name})

        coco_images_list = []
        images_list = validation_collection_data
        for img in images_list:
            image_id = img["image_id"]
            file_name = f"{image_id}.jpg"
            image_dict = {
                "id": image_id,
                "license": 1,
                "file_name": file_name,
                "height": None,
                "width": None,
                "date_captured": None,
            }
            coco_images_list.append(image_dict)

        coco_annotations_list = []
        annotations_list = validation_collection_data
        obj_id = 0
        for ant in annotations_list:
            image_id = ant["image_id"]

            for p in ant["ground_truth"]:

                category = p["class"]

                ant_dict = {
                    "id": obj_id,
                    "image_id": image_id,
                    "category_id": category,
                    "bbox": [
                        p["box"]["x1"],
                        p["box"]["y1"],
                        (p["box"]["x2"] - p["box"]["x1"]),
                        (p["box"]["y2"] - p["box"]["y1"]),
                    ],
                    "segmentation": None,
                    "area": (p["box"]["x2"] - p["box"]["x1"])
                    * (p["box"]["y2"] - p["box"]["y1"]),
                    "iscrowd": 0,
                }
                obj_id += 1
                coco_annotations_list.append(ant_dict)

        coco_dict["categories"] = categories
        coco_dict["images"] = coco_images_list
        coco_dict["annotations"] = coco_annotations_list
        annot_dict = coco_dict

        return annot_dict
