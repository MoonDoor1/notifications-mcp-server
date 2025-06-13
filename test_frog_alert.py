#!/usr/bin/env python3
"""Test script to play frog sound when showing an alert dialog"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

def play_frog_sound():
    """Play the frog sound asynchronously"""
    try:
        subprocess.run(['afplay', '/System/Library/Sounds/Frog.aiff'])
    except Exception as e:
        print(f"Error playing sound: {e}")

def show_alert_with_sound():
    """Show an alert dialog and play the frog sound"""
    # Play sound in a separate thread so it doesn't block the UI
    sound_thread = threading.Thread(target=play_frog_sound)
    sound_thread.start()
    
    # Show the alert dialog
    messagebox.showinfo("Test Alert", "This is a test alert with frog sound!")

def main():
    # Create a simple window with a button
    root = tk.Tk()
    root.title("Frog Sound Alert Test")
    root.geometry("300x150")
    
    # Add a label
    label = tk.Label(root, text="Click the button to test the frog sound alert")
    label.pack(pady=20)
    
    # Add a button that triggers the alert
    button = tk.Button(root, text="Show Alert with Frog Sound", command=show_alert_with_sound)
    button.pack(pady=10)
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()