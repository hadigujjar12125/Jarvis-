"""Command handler for JARVIS Pro."""

import logging
import re
from typing import Tuple
from automation.pc_control import PCControl

logger = logging.getLogger(__name__)


class CommandHandler:
    """Handle system commands and PC control."""

    def __init__(self):
        """Initialize command handler."""
        self.pc_control = PCControl()
        self.commands = {
            # System commands
            r'(shutdown|power off|turn off)': self.handle_shutdown,
            r'(restart|reboot)': self.handle_restart,
            r'(sleep|sleep mode)': self.handle_sleep,
            r'(lock|lock computer)': self.handle_lock,
            
            # Info commands
            r'(system info|system information|computer info)': self.handle_system_info,
            r'(cpu usage|cpu load)': self.handle_cpu_usage,
            r'(memory usage|ram usage)': self.handle_memory_usage,
            r'(disk usage|storage usage)': self.handle_disk_usage,
            r'(network status|internet status)': self.handle_network_status,
            
            # Application commands
            r'(open|launch|start)\s+(.+)': self.handle_open_app,
            r'(close|quit|kill)\s+(.+)': self.handle_close_app,
            r'(list apps|running apps|what apps)': self.handle_list_apps,
            
            # Volume commands
            r'(mute|silence)': self.handle_mute,
            r'(unmute|sound on)': self.handle_unmute,
            r'(volume|set volume)\s*(\d+)': self.handle_set_volume,
            
            # File operations
            r'(open file)\s+(.+)': self.handle_open_file,
            r'(open folder|open directory)\s+(.+)': self.handle_open_folder,
        }
        logger.info("Command handler initialized")

    def handle(self, user_input: str) -> Tuple[bool, str]:
        """Handle user input as command.
        
        Args:
            user_input: User input string
            
        Returns:
            Tuple of (handled, response)
        """
        user_input_lower = user_input.lower().strip()
        
        for pattern, handler in self.commands.items():
            match = re.search(pattern, user_input_lower, re.IGNORECASE)
            if match:
                try:
                    response = handler(user_input, match)
                    logger.info(f"Command handled: {pattern}")
                    return True, response
                except Exception as e:
                    logger.error(f"Error handling command: {e}", exc_info=True)
                    return True, f"Error executing command: {str(e)}"
        
        return False, ""

    # ============ System Commands ============

    def handle_shutdown(self, user_input: str, match) -> str:
        """Handle shutdown command."""
        success, message = self.pc_control.shutdown()
        return message

    def handle_restart(self, user_input: str, match) -> str:
        """Handle restart command."""
        success, message = self.pc_control.restart()
        return message

    def handle_sleep(self, user_input: str, match) -> str:
        """Handle sleep command."""
        success, message = self.pc_control.sleep()
        return message

    def handle_lock(self, user_input: str, match) -> str:
        """Handle lock command."""
        success, message = self.pc_control.lock()
        return message

    # ============ Info Commands ============

    def handle_system_info(self, user_input: str, match) -> str:
        """Handle system info command."""
        info = self.pc_control.get_system_info()
        
        if "error" in info:
            return f"Error: {info['error']}"
        
        return (f"System: {info.get('os', 'N/A')} {info.get('os_version', 'N/A')}\n"
                f"Processor: {info.get('processor', 'N/A')}\n"
                f"CPU Usage: {info.get('cpu_percent', 0)}%\n"
                f"Memory: {info.get('memory_percent', 0)}%\n"
                f"Disk: {info.get('disk_percent', 0)}%")

    def handle_cpu_usage(self, user_input: str, match) -> str:
        """Handle CPU usage command."""
        return self.pc_control.get_cpu_usage()

    def handle_memory_usage(self, user_input: str, match) -> str:
        """Handle memory usage command."""
        return self.pc_control.get_memory_usage()

    def handle_disk_usage(self, user_input: str, match) -> str:
        """Handle disk usage command."""
        return self.pc_control.get_disk_usage()

    def handle_network_status(self, user_input: str, match) -> str:
        """Handle network status command."""
        connected = self.pc_control.is_internet_connected()
        status = self.pc_control.get_network_status()
        return f"{status}\nInternet: {'Connected' if connected else 'Disconnected'}"

    # ============ Application Commands ============

    def handle_open_app(self, user_input: str, match) -> str:
        """Handle open application command."""
        app_name = match.group(2) if match.lastindex >= 2 else ""
        
        if not app_name:
            return "Please specify an application name."
        
        success, message = self.pc_control.open_application(app_name)
        return message

    def handle_close_app(self, user_input: str, match) -> str:
        """Handle close application command."""
        app_name = match.group(2) if match.lastindex >= 2 else ""
        
        if not app_name:
            return "Please specify an application name."
        
        success, message = self.pc_control.close_application(app_name)
        return message

    def handle_list_apps(self, user_input: str, match) -> str:
        """Handle list apps command."""
        return self.pc_control.list_running_apps()

    # ============ Volume Commands ============

    def handle_mute(self, user_input: str, match) -> str:
        """Handle mute command."""
        success, message = self.pc_control.mute()
        return message

    def handle_unmute(self, user_input: str, match) -> str:
        """Handle unmute command."""
        success, message = self.pc_control.unmute()
        return message

    def handle_set_volume(self, user_input: str, match) -> str:
        """Handle set volume command."""
        level = int(match.group(2)) if match.lastindex >= 2 else 50
        success, message = self.pc_control.set_volume(level)
        return message

    # ============ File Operations ============

    def handle_open_file(self, user_input: str, match) -> str:
        """Handle open file command."""
        file_path = match.group(2) if match.lastindex >= 2 else ""
        
        if not file_path:
            return "Please specify a file path."
        
        success, message = self.pc_control.open_file(file_path)
        return message

    def handle_open_folder(self, user_input: str, match) -> str:
        """Handle open folder command."""
        folder_path = match.group(2) if match.lastindex >= 2 else ""
        
        if not folder_path:
            return "Please specify a folder path."
        
        success, message = self.pc_control.open_folder(folder_path)
        return message
