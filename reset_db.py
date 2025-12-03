import os
import shutil
import time

def reset():
    # Delete smartspend.db
    if os.path.exists('smartspend.db'):
        try:
            os.remove('smartspend.db')
            print("Deleted smartspend.db")
        except Exception as e:
            print(f"Error deleting smartspend.db: {e}")
            return

    # Delete migrations folder
    if os.path.exists('migrations'):
        try:
            shutil.rmtree('migrations')
            print("Deleted migrations folder")
        except Exception as e:
            print(f"Error deleting migrations: {e}")
            return

    print("Reset complete. Now run flask commands.")

if __name__ == '__main__':
    reset()
