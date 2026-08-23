import os
import sys

# =========================================================
# CLEAR TERMINAL
# =========================================================
def clear_screen():

    os.system("cls" if os.name == "nt" else "clear")

# =========================================================
# HEADER
# =========================================================
def show_header():

    print("\n" + "=" * 70)

    print("AI-BASED CYBERSECURITY DIGITAL TWIN")

    print("=" * 70)

    print("Real-Time Threat Detection & Automatic Node Isolation")

    print("=" * 70)

# =========================================================
# MENU
# =========================================================
def show_menu():

    print("\nSelect an option:\n")

    print("1. Run Model Evaluation")

    print("2. Run Live Threat Detection")

    print("3. Launch Digital Twin Dashboard")

    print("4. View Saved Logs")

    print("5. Exit")

# =========================================================
# VIEW LOG FILES
# =========================================================
def show_logs():

    log_dir = "logs"

    print("\n" + "=" * 60)

    print("AVAILABLE LOG FILES")

    print("=" * 60)

    if not os.path.exists(log_dir):

        print("No logs directory found.")

        return

    files = os.listdir(log_dir)

    if not files:

        print("No log files available.")

        return

    for file in files:

        print(f"- {file}")

# =========================================================
# MAIN
# =========================================================
def main():

    while True:

        clear_screen()

        show_header()

        show_menu()

        choice = input(
            "\nEnter your choice (1-5): "
        ).strip()

        # -------------------------------------------------
        # MODEL EVALUATION
        # -------------------------------------------------
        if choice == "1":

            print("\nRunning model evaluation...\n")

            os.system(
                "python anomaly_detection/test_real_data.py"
            )

        # -------------------------------------------------
        # LIVE DETECTION
        # -------------------------------------------------
        elif choice == "2":

            print(
                "\nStarting live digital twin detection...\n"
            )

            os.system(
                "python integration/live_detection.py"
            )

        # -------------------------------------------------
        # DASHBOARD
        # -------------------------------------------------
        elif choice == "3":

            print(
                "\nLaunching dashboard...\n"
            )

            os.system(
                "streamlit run dashboard/dashboard_app.py"
            )

        # -------------------------------------------------
        # VIEW LOGS
        # -------------------------------------------------
        elif choice == "4":

            show_logs()

        # -------------------------------------------------
        # EXIT
        # -------------------------------------------------
        elif choice == "5":

            print("\nExiting system...\n")

            sys.exit()

        # -------------------------------------------------
        # INVALID INPUT
        # -------------------------------------------------
        else:

            print("\nInvalid choice.")

        input("\nPress Enter to continue...")

# =========================================================
# ENTRY POINT
# =========================================================
if __name__ == "__main__":

    main()