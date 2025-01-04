import numpy as np
import plotly.graph_objects as go
import tkinter as tk
from tkinter import ttk, messagebox

# Function to generate the graph
def generate_graph(principal, annual_contribution, min_rate, max_rate, start_time, end_time):
    try:
        # Convert inputs to appropriate data types
        principal = float(principal)
        annual_contribution = float(annual_contribution)
        min_rate = float(min_rate) / 100
        max_rate = float(max_rate) / 100
        start_time = int(start_time)
        end_time = int(end_time)

        # Validate input ranges
        if min_rate < 0 or max_rate < 0:
            raise ValueError("Growth rates cannot be negative.")
        if start_time < 0 or end_time < 0 or start_time >= end_time:
            raise ValueError("Invalid time range: Start time must be less than end time.")

        # Create ranges for time and growth rate (as integers for display)
        t = np.arange(start_time, end_time + 1)  # Whole number years
        r = np.arange(int(min_rate * 100), int(max_rate * 100) + 1) / 100  # Whole number rates

        # Create meshgrid for 3D plot
        T, R = np.meshgrid(t, r)

        # Calculate ending balance using the compound interest formula
        A = principal * (1 + R)**T + annual_contribution * ((1 + R)**T - 1) / R

        # Create a Plotly figure
        fig = go.Figure()

        # Add a 3D surface
        fig.add_trace(go.Surface(
            z=A,
            x=T,
            y=R * 100,
            colorscale='Viridis',
            colorbar=dict(title='Ending Balance ($)')
        ))

        # Update layout
        fig.update_layout(
            title="Interactive 3D Account Balance Graph",
            scene=dict(
                xaxis_title='Time (years)',
                yaxis_title='Growth Rate (%)',
                zaxis_title='Ending Balance ($)',
                xaxis=dict(
                    tickmode="array",
                    tickvals=np.arange(start_time, end_time + 1, 5),  # Display every 5 years
                ),
                yaxis=dict(
                    tickmode="array",
                    tickvals=r * 100,
                ),
            )
        )

        # Show the plot
        fig.show()

    except ValueError as e:
        # Show error message for invalid input values
        messagebox.showerror("Input Error", f"Invalid input: {e}")
    except Exception as e:
        # Catch any unexpected errors and display a message
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# GUI Application
def create_gui():
    try:
        # Create the main window
        root = tk.Tk()
        root.title("Account Balance Model Inputs")

        # Labels and entry fields for inputs
        inputs = [
            ("Principal Starting Balance ($)", "1000"),
            ("Annual Contributions ($)", "500"),
            ("Minimum Growth Rate (%)", "0"),
            ("Maximum Growth Rate (%)", "15"),
            ("Start Time (years)", "0"),
            ("End Time (years)", "30"),
        ]

        entries = {}
        for label_text, default_value in inputs:
            frame = ttk.Frame(root)
            frame.pack(fill='x', padx=5, pady=5)

            label = ttk.Label(frame, text=label_text, width=30)
            label.pack(side='left', padx=5)

            entry = ttk.Entry(frame)
            entry.insert(0, default_value)
            entry.pack(side='right', expand=True, fill='x', padx=5)
            entries[label_text] = entry

        # Generate button
        def on_generate():
            try:
                values = {key: entry.get() for key, entry in entries.items()}
                generate_graph(
                    values["Principal Starting Balance ($)"],
                    values["Annual Contributions ($)"],
                    values["Minimum Growth Rate (%)"],
                    values["Maximum Growth Rate (%)"],
                    values["Start Time (years)"],
                    values["End Time (years)"],
                )
            except Exception as e:
                messagebox.showerror("Error", f"Error generating graph: {e}")

        button = ttk.Button(root, text="Generate Graph", command=on_generate)
        button.pack(pady=10)

        # Run the GUI event loop
        root.mainloop()

    except Exception as e:
        print(f"An unexpected error occurred while initializing the GUI: {e}")

# Run the GUI
if __name__ == "__main__":
    try:
        create_gui()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
