# Interactive-LAB-Color-Extraction-from-Images-with-Python
Interactive Python tool to extract LAB color values from images with accurate region-based sampling for color analysis

##  Project Overview
This project is a Python-based application that allows users to extract **LAB color values** directly from an image by clicking on specific areas.  

The system uses **region-based sampling** and statistical methods to improve measurement accuracy and provide reliable color analysis.

---

##  Objectives
- Extract accurate **L*, a*, b*** color values from images  
- Improve measurement stability using **local region sampling**  
- Provide a simple and interactive tool for **color analysis**  

---

##  Features
-  Click on image to extract LAB values  
-  Region-based sampling (instead of single pixel)  
-  Improved accuracy using median color  
-  Real-time display of selected points  
-  Automatic saving of results to Excel  

---

##  How It Works
1. Load an image  
2. User clicks on a point  
3. A small region around the point is analyzed  
4. RGB values are extracted  
5. RGB is converted into LAB color space  
6. Results are saved for analysis  

---

##  Output
The system saves results into an Excel file:

| X | Y | L | a | b |
|--|--|--|--|--|

---

##  Methodology
- RGB → LAB conversion using `skimage.color`
- Median-based region sampling for robustness
- Localized processing to reduce noise impact
- Optional reflection filtering

---

##  Technologies Used
- Python  
- OpenCV  
- NumPy  
- Scikit-image  
- Pandas  

---

##  How to Run

1. Install required libraries:
2. run python script:
   python main.py
3. Click on the image to extract LAB values
4. Results will be saved automatically

# Project structure
   project/
│
├── main.py
└── README.md
├── requirements.txt 
├── sample.jpg
├── lab_color_analysis_example.png

## Screenshot

![LAB Color Analyzer] (screenshot.png)

# Author
Bilal Lukman Alkrayem

License
MIT License
