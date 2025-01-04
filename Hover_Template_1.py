import numpy as np
import plotly.graph_objects as go
import tkinter as tk
from tkinter import ttk, messagebox

def generate_graph(principal, annual_contribution, min_rate, max_rate,
                   start_time, end_time, inflation_rate):
    try:
        # Convert GUI inputs
        principal = float(principal)
        annual_contribution = float(annual_contribution)
        min_rate = float(min_rate) / 100
        max_rate = float(max_rate) / 100
        start_time = int(start_time)
        end_time = int(end_time)
        inflation_rate = round(float(inflation_rate), 2) / 100  # e.g. 3.3 => 0.033

        # Validation
        if min_rate < 0 or max_rate < 0:
            raise ValueError("Growth rates cannot be negative.")
        if start_time < 0 or end_time < 0 or start_time >= end_time:
            raise ValueError("Invalid time range: start time must be < end time, both >= 0.")
        if inflation_rate < 0:
            raise ValueError("Inflation rate cannot be negative.")

        # Make arrays for time and rates
        t = np.arange(start_time, end_time + 1)   # e.g. 0..30
        r_vals = np.arange(int(min_rate * 100), int(max_rate * 100) + 1) / 100  # e.g. 0..0.15
        # Create 2D grids
        T, R = np.meshgrid(t, r_vals)  # shape: (#rates, #years)


        # Compute nominal balance (A) in a single expression, handling R=0
        # Compound interest formula for R != 0
        #   A = principal*(1+R)^T + annual_contribution * [((1+R)^T - 1) / R]
        # For R = 0:
        #   A = principal + annual_contribution*T
        epsilon = 1e-10  # Small value to prevent division by zero
        A_nominal = np.where(
            R == 0,
            principal + annual_contribution * T,
            principal * (1 + R) ** T + annual_contribution * (((1 + R) ** T) - 1) / (R + epsilon)
        )

        # Compute the inflation-adjusted (real) balance
        real_A = A_nominal / ((1 + inflation_rate) ** T)

        # Ensure real_A has the same shape as T and R
        assert real_A.shape == T.shape, "Shape mismatch: real_A and T must have the same shape"

        # Build the 3D surface
        fig = go.Figure(data=[
            go.Surface(
                x=T,
                y=R * 100,  # Convert 0.00..0.15 -> 0..15
                z=A_nominal,
                customdata=real_A,
                colorscale='Viridis',
                colorbar=dict(title='Nominal Balance ($)'),
                hovertemplate=(
                    "Time: %{x} years<br>"
                    "Growth Rate: %{y:.2f}%<br>"
                    "Nominal Value: $%{z:,.0f}<br>"
                    "Real Value: $%{customdata:,.0f}<extra></extra>"
                )
            )
        ])

        # Configure axes
        fig.update_layout(
            title='Financial Growth Over Time',
            scene=dict(
                xaxis_title='Years',
                yaxis_title='Growth Rate (%)',
                zaxis_title='Nominal Balance ($)'
            )
        )

        fig.show()

    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")


def create_gui():
    try:
        root = tk.Tk()
        root.title("Account Balance Model Inputs")

        inputs = [
            ("Principal Starting Balance ($)", "1000"),
            ("Annual Contributions ($)", "500"),
            ("Minimum Growth Rate (%)", "0"),  # default 0
            ("Maximum Growth Rate (%)", "15"),
            ("Start Time (years)", "0"),       # default 0
            ("End Time (years)", "30"),
            ("Inflation Rate (%)", "3.3"),     # default 3.3
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

        def on_generate():
            try:
                values = {k: e.get() for k, e in entries.items()}
                generate_graph(
                    values["Principal Starting Balance ($)"],
                    values["Annual Contributions ($)"],
                    values["Minimum Growth Rate (%)"],
                    values["Maximum Growth Rate (%)"],
                    values["Start Time (years)"],
                    values["End Time (years)"],
                    values["Inflation Rate (%)"],
                )
            except Exception as err:
                messagebox.showerror("Error", f"Error generating graph: {err}")

        button = ttk.Button(root, text="Generate Graph", command=on_generate)
        button.pack(pady=10)

        root.mainloop()

    except Exception as e:
        print(f"An unexpected error occurred while initializing the GUI: {e}")


if __name__ == "__main__":
    try:
        create_gui()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
