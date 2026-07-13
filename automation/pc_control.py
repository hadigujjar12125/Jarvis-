"""PC Control System for JARVIS Pro."""

import logging
import subprocess
import os
import sys
import psutil
import platform
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)


class PCControl:
    """Control PC applications, system, and hardware."""

    def __init__(self):
        """Initialize PC control system."""
        self.os_type = platform.system()
        logger.info(f"PC Control initialized for {self.os_type}")

    # ============ Application Control ============

    def open_application(self, app_name: str) -> Tuple[bool, str]:
        """Open an application.
        
        Args:
            app_name: Name or path of application to open
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if self.os_type == "Windows":
                os.startfile(app_name)
            elif self.os_type == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", app_name])
            elif self.os_type == "Linux":
                subprocess.Popen([app_name])
            
            logger.info(f"Opened application: {app_name}")
            return True, f"Opened {app_name}"
        except Exception as e:
            logger.error(f"Failed to open {app_name}: {e}")
            return False, f"Failed to open {app_name}: {str(e)}"

    def close_application(self, process_name: str) -> Tuple[bool, str]:
        """Close an application by process name.
        
        Args:
            process_name: Name of process to close
            
        Returns:
            Tuple of (success, message)
        """
        try:
            killed = False
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if process_name.lower() in proc.info['name'].lower():
                        proc.kill()
                        killed = True
                        logger.info(f"Closed process: {proc.info['name']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            if killed:
                return True, f"Closed {process_name}"
            return False, f"Process {process_name} not found"
        except Exception as e:
            logger.error(f"Failed to close {process_name}: {e}")
            return False, f"Error closing {process_name}: {str(e)}"

    def list_running_apps(self) -> str:
        """List all running applications.
        
        Returns:
            String with running app names
        """
        try:
            apps = []
            for proc in psutil.process_iter(['name']):
                try:
                    apps.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            return "Running applications: " + ", ".join(sorted(set(apps))[:20])
        except Exception as e:
            logger.error(f"Failed to list apps: {e}")
            return f"Error listing apps: {str(e)}"

    # ============ System Control ============

    def shutdown(self) -> Tuple[bool, str]:
        """Shutdown the computer."""
        try:
            logger.warning("Initiating system shutdown")
            if self.os_type == "Windows":
                subprocess.run(["shutdown", "/s", "/t", "60"])
            elif self.os_type in ["Darwin", "Linux"]:
                subprocess.run(["shutdown", "-h", "+1"])
            
            return True, "Shutdown initiated (60 seconds)"
        except Exception as e:
            logger.error(f"Failed to shutdown: {e}")
            return False, f"Failed to shutdown: {str(e)}"

    def restart(self) -> Tuple[bool, str]:
        """Restart the computer."""
        try:
            logger.warning("Initiating system restart")
            if self.os_type == "Windows":
                subprocess.run(["shutdown", "/r", "/t", "60"])
            elif self.os_type in ["Darwin", "Linux"]:
                subprocess.run(["shutdown", "-r", "+1"])
            
            return True, "Restart initiated (60 seconds)"
        except Exception as e:
            logger.error(f"Failed to restart: {e}")
            return False, f"Failed to restart: {str(e)}"

    def sleep(self) -> Tuple[bool, str]:
        """Put computer to sleep."""
        try:
            logger.info("Putting system to sleep")
            if self.os_type == "Windows":
                subprocess.run(["rundll32.exe", "powrprof.dll", "SetSuspendState", "0", "1", "0"])
            elif self.os_type == "Darwin":
                subprocess.run(["pmset", "sleepnow"])
            elif self.os_type == "Linux":
                subprocess.run(["systemctl", "suspend"])
            
            return True, "System entering sleep mode"
        except Exception as e:
            logger.error(f"Failed to sleep: {e}")
            return False, f"Failed to sleep: {str(e)}"

    def lock(self) -> Tuple[bool, str]:
        """Lock the computer."""
        try:
            logger.info("Locking system")
            if self.os_type == "Windows":
                subprocess.run(["rundll32.exe", "user32.dll", "LockWorkStation"])
            elif self.os_type == "Darwin":
                subprocess.run(["open", "-a", "/System/Library/CoreServices/ScreenLock.app"])
            elif self.os_type == "Linux":
                subprocess.run(["loginctl", "lock-session"])
            
            return True, "System locked"
        except Exception as e:
            logger.error(f"Failed to lock: {e}")
            return False, f"Failed to lock: {str(e)}"

    # ============ System Info ============

    def get_system_info(self) -> Dict[str, Any]:
        """Get system information.
        
        Returns:
            Dictionary with system stats
        """
        try:
            return {
                "os": platform.system(),
                "os_version": platform.release(),
                "processor": platform.processor(),
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "cpu_count": psutil.cpu_count()
            }
        except Exception as e:
            logger.error(f"Failed to get system info: {e}")
            return {"error": str(e)}

    def get_cpu_usage(self) -> str:
        """Get CPU usage percentage.
        
        Returns:
            CPU usage string
        """
        try:
            usage = psutil.cpu_percent(interval=1)
            return f"CPU usage: {usage}%"
        except Exception as e:
            logger.error(f"Failed to get CPU usage: {e}")
            return f"Error getting CPU usage: {str(e)}"

    def get_memory_usage(self) -> str:
        """Get memory usage.
        
        Returns:
            Memory usage string
        """
        try:
            memory = psutil.virtual_memory()
            return f"Memory: {memory.percent}% used ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)"
        except Exception as e:
            logger.error(f"Failed to get memory usage: {e}")
            return f"Error getting memory usage: {str(e)}"

    def get_disk_usage(self) -> str:
        """Get disk usage.
        
        Returns:
            Disk usage string
        """
        try:
            disk = psutil.disk_usage('/')
            return f"Disk: {disk.percent}% used ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)"
        except Exception as e:
            logger.error(f"Failed to get disk usage: {e}")
            return f"Error getting disk usage: {str(e)}"

    # ============ Volume Control ============

    def set_volume(self, level: int) -> Tuple[bool, str]:
        """Set system volume.
        
        Args:
            level: Volume level (0-100)
            
        Returns:
            Tuple of (success, message)
        """
        level = max(0, min(100, level))
        
        try:
            if self.os_type == "Windows":
                # Windows volume control
                import subprocess
                subprocess.run([
                    "powershell",
                    f"(Get-Volume -DriveLetter C).SoundLevel = {level}"
                ])
            elif self.os_type == "Darwin":
                # macOS volume control
                subprocess.run(["osascript", "-e", f"set volume output volume {level}"])
            elif self.os_type == "Linux":
                # Linux volume control
                subprocess.run(["amixer", "set", "Master", f"{level}%"])
            
            logger.info(f"Set volume to {level}%")
            return True, f"Volume set to {level}%"
        except Exception as e:
            logger.error(f"Failed to set volume: {e}")
            return False, f"Failed to set volume: {str(e)}"

    def mute(self) -> Tuple[bool, str]:
        """Mute system audio.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            if self.os_type == "Windows":
                subprocess.run(["powershell", "(Get-Volume -DriveLetter C).Mute = $true"])
            elif self.os_type == "Darwin":
                subprocess.run(["osascript", "-e", "set volume output muted true"])
            elif self.os_type == "Linux":
                subprocess.run(["amixer", "set", "Master", "mute"])
            
            logger.info("System muted")
            return True, "System muted"
        except Exception as e:
            logger.error(f"Failed to mute: {e}")
            return False, f"Failed to mute: {str(e)}"

    def unmute(self) -> Tuple[bool, str]:
        """Unmute system audio.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            if self.os_type == "Windows":
                subprocess.run(["powershell", "(Get-Volume -DriveLetter C).Mute = $false"])
            elif self.os_type == "Darwin":
                subprocess.run(["osascript", "-e", "set volume output muted false"])
            elif self.os_type == "Linux":
                subprocess.run(["amixer", "set", "Master", "unmute"])
            
            logger.info("System unmuted")
            return True, "System unmuted"
        except Exception as e:
            logger.error(f"Failed to unmute: {e}")
            return False, f"Failed to unmute: {str(e)}"

    # ============ Network Control ============

    def get_network_status(self) -> str:
        """Get network status.
        
        Returns:
            Network status string
        """
        try:
            stats = psutil.net_if_stats()
            info = []
            
            for interface, stats in stats.items():
                status = "UP" if stats.isup else "DOWN"
                info.append(f"{interface}: {status}")
            
            return "Network status: " + ", ".join(info[:5])
        except Exception as e:
            logger.error(f"Failed to get network status: {e}")
            return f"Error getting network status: {str(e)}"

    def is_internet_connected(self) -> bool:
        """Check if internet is connected.
        
        Returns:
            True if connected, False otherwise
        """
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    # ============ File Operations ============

    def open_file(self, file_path: str) -> Tuple[bool, str]:
        """Open a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if not os.path.exists(file_path):
                return False, f"File not found: {file_path}"
            
            if self.os_type == "Windows":
                os.startfile(file_path)
            elif self.os_type == "Darwin":
                subprocess.Popen(["open", file_path])
            elif self.os_type == "Linux":
                subprocess.Popen(["xdg-open", file_path])
            
            logger.info(f"Opened file: {file_path}")
            return True, f"Opened {file_path}"
        except Exception as e:
            logger.error(f"Failed to open file: {e}")
            return False, f"Failed to open file: {str(e)}"

    def open_folder(self, folder_path: str) -> Tuple[bool, str]:
        """Open a folder.
        
        Args:
            folder_path: Path to folder
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if not os.path.exists(folder_path):
                return False, f"Folder not found: {folder_path}"
            
            if self.os_type == "Windows":
                os.startfile(folder_path)
            elif self.os_type == "Darwin":
                subprocess.Popen(["open", folder_path])
            elif self.os_type == "Linux":
                subprocess.Popen(["xdg-open", folder_path])
            
            logger.info(f"Opened folder: {folder_path}")
            return True, f"Opened {folder_path}"
        except Exception as e:
            logger.error(f"Failed to open folder: {e}")
            return False, f"Failed to open folder: {str(e)}"

    def execute_command(self, command: str) -> Tuple[bool, str]:
        """Execute a shell command.
        
        Args:
            command: Command to execute
            
        Returns:
            Tuple of (success, output)
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            output = result.stdout or result.stderr or "Command executed"
            logger.info(f"Executed command: {command}")
            return True, output[:500]
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {command}")
            return False, "Command timed out"
        except Exception as e:
            logger.error(f"Failed to execute command: {e}")
            return False, f"Error: {str(e)}"
