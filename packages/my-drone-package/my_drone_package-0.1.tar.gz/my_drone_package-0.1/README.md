## **Drone Control - Simulation and Real Drone**

This project allows you to control a drone either in a **simulation** environment using the `DroneBlocksTelloSimulator` or control a real **Tello drone** using the `easyTello` library. You can switch between simulation and real drone modes based on your requirements.

### **Project Structure**

- **`simulated_tello.py`**: Contains the class for controlling the simulated drone using `DroneBlocksTelloSimulator`.
- **`real_tello.py`**: Contains the class for controlling the real Tello drone using the `easyTello` library.
- **`main.py`**: The main entry point for the project. This file prompts the user to choose between simulation or real drone control and allows the user to run different lessons to practice drone control commands.
- **`README.md`**: This documentation file.
  
---

### **Installation**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/drone-control.git
   cd drone-control
   ```

2. **Install Dependencies:**

   First, make sure you have Python installed. Then, install the required dependencies:

   - For the **simulator**:
     ```bash
     pip install DroneBlocksTelloSimulator
     ```

   - For the **real Tello drone**:
     ```bash
     pip install easytello
     ```

---

### **How to Use**

1. **Run the `main.py` File:**
   ```bash
   python main.py
   ```

2. **Choose Between Simulation or Real Drone:**

   When prompted, select your option:
   - Press **1** to use the **simulated drone**.
   - Press **2** to use the **real Tello drone**.

3. **Lessons**: The code contains several pre-defined lessons, each with different drone commands to control the drone.

   To run a lesson, simply uncomment the respective section in `main.py` and run the file.

---

### **Lessons**

The `main.py` file contains different lessons for learning and practicing drone commands. Each lesson is commented out, and you can uncomment the code to run the lesson.

Here is an overview of the lessons:

1. **Lesson 1: Basic Drone Commands**
   - Connect to the drone
   - Take off
   - Move up, forward, and rotate
   - Perform a flip
   - Land

2. **Lesson 2: Advanced Movement Commands**
   - Move left, right, backward
   - Rotate counterclockwise
   - Land

3. **Lesson 3: Speed and Flipping**
   - Set speed
   - Move forward with the new speed
   - Perform different flips
   - Land

4. **Lesson 4: Flying to Coordinates (Go and Curve)**
   - Fly to specific coordinates using the `go` command
   - Fly in a curve between two points
   - Land

5. **Lesson 5: Monitoring and Battery**
   - Check battery level (mocked in the simulator)
   - Land

6. **Lesson 6: Full Control with Rotation and Flipping**
   - Full control with moving up, down, forward, backward
   - Rotate clockwise and counterclockwise
   - Perform flips
   - Land

---

### **Running on Simulated Drone**

If you select **1** during the prompt, the program will run on the simulated drone. Make sure you have the **DroneBlocksTelloSimulator** installed.

**Example**: To run Lesson 1 on the simulator:
1. Open `main.py`.
2. Uncomment the code for Lesson 1.
3. Run the script.
4. Select **1** when prompted to use the simulator.
5. Enter your **simulator key** when prompted.

---

### **Running on Real Tello Drone**

If you select **2** during the prompt, the program will control the real Tello drone using the `easyTello` library.

**Example**: To run Lesson 1 on the real drone:
1. Open `main.py`.
2. Uncomment the code for Lesson 1.
3. Run the script.
4. Select **2** when prompted to use the real Tello drone.

---

### **Contributing**

Feel free to fork this repository, make changes, and submit pull requests if you'd like to contribute to this project.

---

### **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### **Contact**

If you have any questions or need further assistance, feel free to reach out:

- Email: b.gada@umbc.edu
- GitHub: bhavyabgada (https://github.com/bhavyabgada)

---

Let me know if you need any changes or additions to the `README.md` file!