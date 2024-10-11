import pandas as pd
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def data_analysis_example(train_brain, train_image, train_text):
    # Convert brain, image, and text data to pandas DataFrames for easier exploration
    train_brain_df = pd.DataFrame(train_brain.numpy())
    train_image_df = pd.DataFrame(train_image.numpy())
    train_text_df = pd.DataFrame(train_text.numpy())
    
    # Summary statistics for the brain data
    print("Brain data summary statistics:")
    print(train_brain_df.describe())
    
    # Summary statistics for the image data
    print("\nImage data summary statistics:")
    print(train_image_df.describe())
    
    # Summary statistics for the text data
    print("\nText data summary statistics:")
    print(train_text_df.describe())

def data_visualization_example(train_label):
    # Calculate the cumulative distribution
    train_label_np = train_label.numpy().ravel()
    label_counts = pd.Series(train_label_np).value_counts().sort_index()
    cumulative_counts = label_counts.cumsum() / label_counts.sum()
    
    # Visualizing the Cumulative Distribution Plot
    plt.figure(figsize=(10, 6))
    cumulative_counts.plot(drawstyle='steps-post', color='blue', linewidth=2)
    plt.title('Cumulative Distribution of Class Labels')
    plt.xlabel('Class Labels (Sorted)')
    plt.ylabel('Cumulative Proportion')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()

def evaluation_visualization_example(test_label_np, test_predictions):
    # Confusion matrix
    conf_matrix = confusion_matrix(test_label_np, test_predictions)
    
    # Plot confusion matrix
    plt.figure(figsize=(10, 7))
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues")
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.show()

def diverse_evaluation_metrics_example(test_label_np, test_predictions):
    precision = precision_score(test_label_np, test_predictions, average='weighted')
    recall = recall_score(test_label_np, test_predictions, average='weighted')
    f1 = f1_score(test_label_np, test_predictions, average='weighted')
    
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")