# Model Card for Registered Version v1.1.0

## Model Information
**Model Name:** digits-clf  
**Registered Version:** v1.1.0  
**Pipeline Lock File:** dvc.lock  

## Performance Metrics
- **Validation Accuracy:** 0.989 (measured on the validation split)

## Dataset Details
- **Dataset Name:** Optical Recognition of Handwritten Digits  
- **Creator(s):** E. Alpaydin and C. Kaynak  
- **Year:** 1998  
- **DOI:** 10.24432/C50P49  
- **URL:** [https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)  
- **License:** CC BY 4.0  
- **License URL:** [https://creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/)  
- **Number of Images:** 1797  
- **Image Size:** 8 by 8 pixels  
- **Classes:** 10  
- **Pixel Values Range:** 0 to 16  
- **Loaded with:** sklearn.datasets.load_digits

## Model Architecture
- **Hidden Units in Hidden Layer:** 64 (specified in params.yaml)

## Number of Rows in Splits
- **Train Split Rows:** 1078 (from release.yaml)
- **Validation Split Rows:** 359 (from release.yaml)
- **Test Split Rows:** 360 (from release.yaml)

## Model Purpose and Usage Restrictions
**Purpose:** The model is designed to classify 8x8 images of handwritten digits. It should be used for recognizing and categorizing handwritten digits in similar image formats.

**Usage Restrictions:**
- This model must not be used for any other type of classification tasks beyond the recognition of handwritten digits.
- The model should only be applied to images with a resolution of 8x8 pixels, as its performance may degrade on different image sizes or resolutions.
- It is intended for use in educational and research settings where accurate digit recognition is required. Misuse outside these parameters can lead to reduced accuracy.

## Acknowledgments
The dataset used in this project was sourced from the UCI Machine Learning Repository, with contributions from E. Alpaydin and C. Kaynak. The model architecture and training process were informed by best practices in machine learning and neural network design as documented in the scikit-learn library documentation.

---

