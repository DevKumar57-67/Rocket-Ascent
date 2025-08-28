'''
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello from Flask!'

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
'''

from flask import Flask, render_template, request
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Create static directory if it doesn't exist
if not os.path.exists('static'):
    os.makedirs('static')

# Route for homepage
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        # Get form inputs
        mass = float(request.form["mass"])
        thrust = float(request.form["thrust"])
        burn_time = float(request.form["burn_time"])
        dt = float(request.form["dt"])
        g = 9.81

        # Time array
        time = np.arange(0, burn_time + dt, dt)

        # Initialize arrays
        velocity = np.zeros_like(time)
        altitude = np.zeros_like(time)
        acceleration = np.zeros_like(time)

        # Simulation loop
        for i in range(1, len(time)):
            acceleration[i] = (thrust / mass) - g
            velocity[i] = velocity[i-1] + acceleration[i] * dt
            altitude[i] = altitude[i-1] + velocity[i] * dt

        # Save results
        result = {
            "final_altitude": round(float(altitude[-1]), 2),
            "final_velocity": round(float(velocity[-1]), 2),
            "final_acceleration": round(float(acceleration[-1]), 2)
        }

        # Plot results
        plt.figure(figsize=(10,6))

        plt.subplot(3,1,1)
        plt.plot(time, acceleration, label="Acceleration (m/s²)")
        plt.legend(); plt.grid(True)

        plt.subplot(3,1,2)
        plt.plot(time, velocity, label="Velocity (m/s)")
        plt.legend(); plt.grid(True)

        plt.subplot(3,1,3)
        plt.plot(time, altitude, label="Altitude (m)")
        plt.legend(); plt.grid(True)

        plt.xlabel("Time (s)")
        plt.tight_layout()

        # Save plot
        plot_path = os.path.join("static", "plot.png")
        plt.savefig(plot_path)
        plt.close()

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)



# The Software uses Physics, Mathematics and Computer Science to simulate the flight of a rocket in Space. 