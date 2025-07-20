from core.platforms import Platform
from client.application import Application
from exceptions import PlatformError

def main() -> None:
    try:
        windows_app = Application(Platform.WINDOWS)
        windows_app.create_ui()
        
        print("Windows Application UI:")
        for result in windows_app.render_ui():
            print(f"- {result}")
        
        print("\nInteracting with Windows UI:")
        for result in windows_app.interact_with_ui():
            print(f"- {result}")
        
        macos_app = Application(Platform.MACOS)
        macos_app.create_ui()
        
        print("\nMacOS Application UI:")
        for result in macos_app.render_ui():
            print(f"- {result}")
        
        print("\nInteracting with MacOS UI:")
        for result in macos_app.interact_with_ui():
            print(f"- {result}")
        
        try:
            Application("Linux")  
        except TypeError as e:
            print(f"\nExpected error when using invalid platform: {e}")
        
    except PlatformError as e:
        print(f"Platform error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()