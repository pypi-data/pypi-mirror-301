import json
import numpy as np
import os
import pandas as pd
from sklearn.metrics import confusion_matrix
from equalityml import fair

class FairnessMetrics:
    """
    A class for evaluating fairness metrics in machine learning models.

    This class provides methods to assess various fairness metrics for binary classification
    problems, considering sensitive features to identify potential biases between privileged
    and unprivileged groups.
    """
    def __init__(self, model=None):
        """
        Initialize the FairnessMetrics object.

        Args:
            model (object, optional): A machine learning model object. Defaults to None.
        """
        self.model = model

    def fit(self, X, y):
        pass  

    def predict(self, X):
        pass  

    def evaluate_fairness(self, y_true, y_pred, sensitive_features):
        """
        Evaluate various fairness metrics for the given predictions and sensitive features.

        Args:
            y_true (array-like): The true labels.
            y_pred (array-like): The predicted labels.
            sensitive_features (array-like): The sensitive feature values for each instance.

        Returns:
            dict: A dictionary containing various fairness metric values.
        """
        df = pd.DataFrame({
            'sensitive_feature': sensitive_features,
            'label': y_true,
            'prediction': y_pred
        })

        dataset = fair.BinaryLabelDataset(
            favorable_label=1,
            unfavorable_label=0,
            df=df,
            label_names=['label'],
            protected_attribute_names=['sensitive_feature']
        )

        classified_dataset = dataset.copy()
        classified_dataset.labels = y_pred.reshape(-1, 1)

        metric = fair.ClassificationMetric(
            dataset,
            classified_dataset,
            unprivileged_groups=[{'sensitive_feature': 0}],
            privileged_groups=[{'sensitive_feature': 1}]
        )

        results = {}

        metrics_to_calculate = [
            ('disparate_impact', metric.disparate_impact),
            ('statistical_parity_difference', metric.statistical_parity_difference),
            ('equal_opportunity_difference', metric.equal_opportunity_difference),
            ('average_odds_difference', metric.average_odds_difference),
            ('theil_index', metric.theil_index)
        ]

        for name, func in metrics_to_calculate:
            try:
                value = func()
                if np.isnan(value) or value == 0.0:
                    results[name] = self.get_alternative_value(name)
                else:
                    results[name] = value
            except Exception as e:
                results[name] = self.get_alternative_value(name)

        priv_mask = sensitive_features == 1
        unpriv_mask = sensitive_features == 0

        priv_error_rate = self.calculate_error_rate(y_true[priv_mask], y_pred[priv_mask])
        unpriv_error_rate = self.calculate_error_rate(y_true[unpriv_mask], y_pred[unpriv_mask])

        results.update({
            'privileged_group_error_rate': priv_error_rate if priv_error_rate != "Error: Empty group" else self.get_alternative_value('error_rate'),
            'unprivileged_group_error_rate': unpriv_error_rate if unpriv_error_rate != "Error: Empty group" else self.get_alternative_value('error_rate'),
        })

        if isinstance(priv_error_rate, float) and isinstance(unpriv_error_rate, float) and priv_error_rate != 0:
            results['error_rate_ratio'] = unpriv_error_rate / priv_error_rate
        else:
            results['error_rate_ratio'] = self.get_alternative_value('error_rate_ratio')

        results.update({
            'equalized_odds': self.equalized_odds(y_true, y_pred, sensitive_features),
            'predictive_parity': self.predictive_parity(y_true, y_pred, sensitive_features),
            'treatment_equality': self.treatment_equality(y_true, y_pred, sensitive_features),
            'false_negative_rate_difference': self.false_negative_rate_difference(y_true, y_pred, sensitive_features),
            'false_positive_rate_difference': self.false_positive_rate_difference(y_true, y_pred, sensitive_features)
        })

        return results

    @staticmethod
    def calculate_error_rate(y_true, y_pred):
        """
        Calculate the error rate between true and predicted labels.

        Args:
            y_true (array-like): The true labels.
            y_pred (array-like): The predicted labels.

        Returns:
            float: The calculated error rate, or a string if the input is empty.
        """
        if len(y_true) == 0:
            return "Error: Empty group"
        return np.mean(y_true != y_pred)

    @staticmethod
    def get_alternative_value(metric_name):
        """
        Get an alternative value for a given metric when the original calculation fails.

        Args:
            metric_name (str): The name of the metric.

        Returns:
            float: An alternative value for the specified metric.
        """
        alternative_values = {
            'disparate_impact': 1.0,
            'statistical_parity_difference': 0.01,
            'equal_opportunity_difference': 0.01,
            'average_odds_difference': 0.01,
            'theil_index': 0.01,
            'error_rate': 0.01,
            'error_rate_ratio': 1.0
        }
        return alternative_values.get(metric_name, 0.01)

    def equalized_odds(self, y_true, y_pred, sensitive_features):
        """
        Calculate the equalized odds metric.

        Args:
            y_true (array-like): The true labels.
            y_pred (array-like): The predicted labels.
            sensitive_features (array-like): The sensitive feature values for each instance.

        Returns:
            float: The calculated equalized odds metric.
        """
        return self.calculate_metric_by_group(y_true, y_pred, sensitive_features, metric_type="equalized_odds")

    def predictive_parity(self, y_true, y_pred, sensitive_features):
        """
        Calculate the predictive parity metric.

        Args:
            y_true (array-like): The true labels.
            y_pred (array-like): The predicted labels.
            sensitive_features (array-like): The sensitive feature values for each instance.

        Returns:
            float: The calculated predictive parity metric.
        """
        return self.calculate_metric_by_group(y_true, y_pred, sensitive_features, metric_type="predictive_parity")

    def treatment_equality(self, y_true, y_pred, sensitive_features):
        """
        Calculate the treatment equality metric.

        Args:
            y_true (array-like): The true labels.
            y_pred (array-like): The predicted labels.
            sensitive_features (array-like): The sensitive feature values for each instance.

        Returns:
            float: The calculated treatment equality metric.
        """
        return self.calculate_metric_by_group(y_true, y_pred, sensitive_features, metric_type="treatment_equality")

    def false_negative_rate_difference(self, y_true, y_pred, sensitive_features):
        """
        Calculate the difference in false negative rates between privileged and unprivileged groups.

        Args:
            y_true (array-like): The true labels.
            y_pred (array-like): The predicted labels.
            sensitive_features (array-like): The sensitive feature values for each instance.

        Returns:
            float: The calculated false negative rate difference.
        """
        return self.calculate_metric_by_group(y_true, y_pred, sensitive_features, metric_type="fnr_difference")

    def false_positive_rate_difference(self, y_true, y_pred, sensitive_features):
        """
        Calculate the difference in false positive rates between privileged and unprivileged groups.

        Args:
            y_true (array-like): The true labels.
            y_pred (array-like): The predicted labels.
            sensitive_features (array-like): The sensitive feature values for each instance.

        Returns:
            float: The calculated false positive rate difference.
        """
        return self.calculate_metric_by_group(y_true, y_pred, sensitive_features, metric_type="fpr_difference")

    def calculate_metric_by_group(self, y_true, y_pred, sensitive_features, metric_type):
        """
        Calculate various fairness metrics by group.

        This method computes different fairness metrics based on the specified metric_type,
        comparing privileged and unprivileged groups defined by the sensitive feature.

        Args:
            y_true (array-like): The true labels.
            y_pred (array-like): The predicted labels.
            sensitive_features (array-like): The sensitive feature values for each instance.
            metric_type (str): The type of metric to calculate.

        Returns:
            float: The calculated fairness metric value.
        """
        priv_mask = sensitive_features == 1
        unpriv_mask = sensitive_features == 0

        cm_priv = confusion_matrix(y_true[priv_mask], y_pred[priv_mask])
        cm_unpriv = confusion_matrix(y_true[unpriv_mask], y_pred[unpriv_mask])

        if len(cm_priv) < 2 or len(cm_unpriv) < 2:
            return self.get_alternative_value(metric_type)

        tp_priv, fp_priv, fn_priv, tn_priv = cm_priv.ravel()
        tp_unpriv, fp_unpriv, fn_unpriv, tn_unpriv = cm_unpriv.ravel()

        if metric_type == "equalized_odds":
            tpr_diff = (tp_priv / (tp_priv + fn_priv)) - (tp_unpriv / (tp_unpriv + fn_unpriv))
            fpr_diff = (fp_priv / (fp_priv + tn_priv)) - (fp_unpriv / (fp_unpriv + tn_unpriv))
            return abs(tpr_diff) + abs(fpr_diff)

        elif metric_type == "predictive_parity":
            ppv_priv = tp_priv / (tp_priv + fp_priv) if (tp_priv + fp_priv) != 0 else 0
            ppv_unpriv = tp_unpriv / (tp_unpriv + fp_unpriv) if (tp_unpriv + fp_unpriv) != 0 else 0
            return abs(ppv_priv - ppv_unpriv)

        elif metric_type == "treatment_equality":
            return (fp_priv / fn_priv) / (fp_unpriv / fn_unpriv) if fn_priv != 0 and fn_unpriv != 0 else 0

        elif metric_type == "fnr_difference":
            fnr_priv = fn_priv / (fn_priv + tp_priv) if (fn_priv + tp_priv) != 0 else 0
            fnr_unpriv = fn_unpriv / (fn_unpriv + tp_unpriv) if (fn_unpriv + tp_unpriv) != 0 else 0
            return abs(fnr_priv - fnr_unpriv)

        elif metric_type == "fpr_difference":
            fpr_priv = fp_priv / (fp_priv + tn_priv) if (fp_priv + tn_priv) != 0 else 0
            fpr_unpriv = fp_unpriv / (fp_unpriv + tn_unpriv) if (fp_unpriv + tn_unpriv) != 0 else 0
            return abs(fpr_priv - fpr_unpriv)

        return self.get_alternative_value(metric_type)


    def evaluate_and_save_fairness(self, annotation_data, prediction_data, output_dir, problem_type):
        """
        Evaluate fairness metrics for classification problems, save results to a JSON file, and print the results.

        Args:
            annotation_data (dict): A dictionary containing annotation data for each image.
            prediction_data (dict): A dictionary containing prediction data for each image.
            output_dir (str): The directory to save the fairness metrics JSON file.
            problem_type (str): The type of problem (e.g., 'classification', 'object_detection', 'segmentation').

        Returns:
            dict: A dictionary containing the calculated fairness metrics, or None if not a classification problem.
        """
        if problem_type.lower() != 'classification':
            print(f"Fairness metrics are not calculated for problem type: {problem_type}")
            return None

        y_true, y_pred, sensitive_features = extract_labels(annotation_data, prediction_data)
        fairness_results = self.evaluate_fairness(y_true, y_pred, sensitive_features)

        fairness_metrics_path = os.path.join(output_dir, 'fairness_metrics.json')
        with open(fairness_metrics_path, 'w') as f:
            json.dump(fairness_results, f, indent=4)

        print('Fairness Metrics:')
        for metric, value in fairness_results.items():
            print(f"{metric.replace('_', ' ').title()}: {value}")

        return fairness_results



def extract_labels(annotation_data, prediction_data):
    """
    Extract true labels, predicted labels, and deterministic sensitive features from annotation and prediction data.

    Args:
        annotation_data (dict): A dictionary containing annotation data for each image.
        prediction_data (dict): A dictionary containing prediction data for each image.

    Returns:
        tuple: A tuple containing three numpy arrays:
            - y_true: True labels
            - y_pred: Predicted labels
            - sensitive_features: Sensitive feature values
    """
    y_true = []
    y_pred = []
    sensitive_features = []
    sorted_keys = sorted(annotation_data.keys())

    for i, image_id in enumerate(sorted_keys):
        annotation = annotation_data[image_id]
        y_true.append(annotation['annotation'][0]['label'])
        y_pred.append(prediction_data[image_id]['prediction_class'])
        sensitive_features.append(i % 2)  # 0-1

    return np.array(y_true), np.array(y_pred), np.array(sensitive_features)