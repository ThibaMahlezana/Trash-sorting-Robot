# Trash Sorting Arm Robot

## About the Project
This project involves a robotic arm powered by a Raspberry Pi, equipped with a camera that uses machine learning to identify and sort trash into three categories: paper, plastic, and metal. The application leverages TensorFlow Lite and OpenCV to enhance the robot's perception and sorting capabilities.

## Motivation
With the increasing amount of waste generated daily, efficient sorting of recyclables is crucial for sustainable waste management. This project aims to automate the sorting process, reducing human labor and improving recycling rates.

## Built With
- **Python**: The main programming language used for application development.
- **TensorFlow Lite**: For machine learning model deployment.
- **OpenCV**: For image processing tasks.
- **Raspberry Pi**: The hardware platform for running the application and controlling the robotic arm.

## Getting Started
To get started with this project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ThibaMahlezana/Trash-sorting-Robot.git
   cd Trash-sorting-Robot

2. **Install dependencies**:
   Ensure you have Python 3 installed, then install the required libraries:
   ```bash
   pip install -r requirements.txt

3. **Setup the Raspberry Pi**:
   - Connect the robotic arm and camera to the Raspberry Pi.
   - Configure the Raspberry Pi to allow access to the camera

4. **Run the application**:
   Start the application by executing:
   ```bash
   python main.py

## Usage
- Place various types of trash in front of the robot's camera.
- The robot will identify the item and move it to the designated bin based on its classification (paper, plastic, or metal).
- Monitor the performance and accuracy through the console output.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For inquiries or feedback, please reach out via:

- Email: thiba.ma@gmail.com

## Acknowledgements
- Special thanks to the TensorFlow and OpenCV communities for their resources and support.
- Inspiration from various robotics and AI projects.
