"""
Security utilities for SuperClaude installation system
Path validation and input sanitization

This module provides comprehensive security validation for file paths and user inputs
during SuperClaude installation. It includes protection against:
- Directory traversal attacks
- Installation to system directories
- Path injection attacks
- Cross-platform security issues

Key Features:
- Platform-specific validation (Windows vs Unix)
- User-friendly error messages with actionable suggestions
- Comprehensive path normalization
- Backward compatibility with existing validation logic

Fixed Issues:
- GitHub Issue #129: Fixed overly broad regex patterns that prevented installation
  in legitimate paths containing "dev", "tmp", "bin", etc.
- Enhanced cross-platform compatibility
- Improved error message clarity

Architecture:
- Separated pattern categories for better maintainability
- Platform-aware validation logic
- Comprehensive test coverage
"""

import re
import os
from pathlib import Path
from typing import List, Optional, Tuple, Set
import urllib.parse
from setup.utils.localization import get_string


class SecurityValidator:
    """Security validation utilities"""
    
    # Directory traversal patterns (match anywhere in path - platform independent)
    # These patterns detect common directory traversal attack vectors
    TRAVERSAL_PATTERNS = [
        r'\.\./',           # Directory traversal using ../
        r'\.\.\.',          # Directory traversal using ...
        r'//+',             # Multiple consecutive slashes (path injection)
    ]
    
    # Unix system directories (match only at start of path)
    # These patterns identify Unix/Linux system directories that should not be writable
    # by regular users. Using ^ anchor to match only at path start prevents false positives
    # for user directories containing these names (e.g., /home/user/dev/ is allowed)
    UNIX_SYSTEM_PATTERNS = [
        r'^/etc/',          # System configuration files
        r'^/bin/',          # Essential command binaries
        r'^/sbin/',         # System binaries
        r'^/usr/bin/',      # User command binaries
        r'^/usr/sbin/',     # Non-essential system binaries
        r'^/var/',          # Variable data files
        r'^/tmp/',          # Temporary files (system-wide)
        r'^/dev/',          # Device files - FIXED: was r'/dev/' (GitHub Issue #129)
        r'^/proc/',         # Process information pseudo-filesystem
        r'^/sys/',          # System information pseudo-filesystem
    ]
    
    # Windows system directories (match only at start of path)
    # These patterns identify Windows system directories using flexible separator matching
    # to handle both forward slashes and backslashes consistently
    WINDOWS_SYSTEM_PATTERNS = [
        r'^c:[/\\]windows[/\\]',        # Windows system directory
        r'^c:[/\\]program files[/\\]',  # Program Files directory
        # Note: Removed c:\\users\\ to allow installation in user directories
        # Claude Code installs to user home directory by default
    ]
    
    # Combined dangerous patterns for backward compatibility
    # This maintains compatibility with existing code while providing the new categorized approach
    DANGEROUS_PATTERNS = TRAVERSAL_PATTERNS + UNIX_SYSTEM_PATTERNS + WINDOWS_SYSTEM_PATTERNS
    
    # Dangerous filename patterns
    DANGEROUS_FILENAMES = [
        r'\.exe$',          # Executables
        r'\.bat$',
        r'\.cmd$',
        r'\.scr$',
        r'\.dll$',
        r'\.so$',
        r'\.dylib$',
        r'passwd',          # System files
        r'shadow',
        r'hosts',
        r'\.ssh/',
        r'\.aws/',
        r'\.env',           # Environment files
        r'\.secret',
    ]
    
    # Allowed file extensions for installation
    ALLOWED_EXTENSIONS = {
        '.md', '.json', '.py', '.js', '.ts', '.jsx', '.tsx',
        '.txt', '.yml', '.yaml', '.toml', '.cfg', '.conf',
        '.sh', '.ps1', '.html', '.css', '.svg', '.png', '.jpg', '.gif'
    }
    
    # Maximum path lengths
    MAX_PATH_LENGTH = 4096
    MAX_FILENAME_LENGTH = 255
    
    @classmethod
    def validate_path(cls, path: Path, base_dir: Optional[Path] = None) -> Tuple[bool, str]:
        """
        Validate path for security issues with enhanced cross-platform support
        
        This method performs comprehensive security validation including:
        - Directory traversal attack detection
        - System directory protection (platform-specific)
        - Path length and filename validation
        - Cross-platform path normalization
        - User-friendly error messages
        
        Architecture:
        - Uses both original and resolved paths for validation
        - Applies platform-specific patterns for system directories
        - Checks traversal patterns against original path to catch attacks before normalization
        - Provides detailed error messages with actionable suggestions
        
        Args:
            path: Path to validate (can be relative or absolute)
            base_dir: Base directory that path should be within (optional)
            
        Returns:
            Tuple of (is_safe: bool, error_message: str)
            - is_safe: True if path passes all security checks
            - error_message: Detailed error message with suggestions if validation fails
        """
        try:
            # Check for null bytes
            if '\x00' in str(path):
                return False, get_string("security.validate_path.null_byte")

            # Convert to absolute path
            abs_path = path.resolve()
            
            # For system directory validation, use the original path structure
            # to avoid issues with symlinks and cross-platform path resolution
            original_path_str = cls._normalize_path_for_validation(path)
            resolved_path_str = cls._normalize_path_for_validation(abs_path)
            
            # Check path length
            if len(str(abs_path)) > cls.MAX_PATH_LENGTH:
                return False, get_string("security.validate_path.too_long", len(str(abs_path)), cls.MAX_PATH_LENGTH)
            
            # Check filename length
            if len(abs_path.name) > cls.MAX_FILENAME_LENGTH:
                return False, get_string("security.validate_path.filename_too_long", len(abs_path.name), cls.MAX_FILENAME_LENGTH)
            
            # Check for dangerous patterns using platform-specific validation
            # Always check traversal patterns (platform independent) - use original path string
            # to detect patterns before normalization removes them
            original_str = str(path).lower()
            for pattern in cls.TRAVERSAL_PATTERNS:
                if re.search(pattern, original_str, re.IGNORECASE):
                    return False, cls._get_user_friendly_error_message("traversal", pattern, abs_path)
            
            # Check platform-specific system directory patterns - use original path first, then resolved
            # Always check both Windows and Unix patterns to handle cross-platform scenarios
            
            # Check Windows system directory patterns
            for pattern in cls.WINDOWS_SYSTEM_PATTERNS:
                if (re.search(pattern, original_path_str, re.IGNORECASE) or 
                    re.search(pattern, resolved_path_str, re.IGNORECASE)):
                    return False, cls._get_user_friendly_error_message("windows_system", pattern, abs_path)
            
            # Check Unix system directory patterns
            for pattern in cls.UNIX_SYSTEM_PATTERNS:
                if (re.search(pattern, original_path_str, re.IGNORECASE) or 
                    re.search(pattern, resolved_path_str, re.IGNORECASE)):
                    return False, cls._get_user_friendly_error_message("unix_system", pattern, abs_path)
            
            # Check for dangerous filenames
            for pattern in cls.DANGEROUS_FILENAMES:
                if re.search(pattern, abs_path.name, re.IGNORECASE):
                    return False, get_string("security.validate_path.dangerous_filename", pattern)
            
            # Check if path is within base directory
            if base_dir:
                base_abs = base_dir.resolve()
                try:
                    abs_path.relative_to(base_abs)
                except ValueError:
                    return False, get_string("security.validate_path.outside_allowed_dir", abs_path, base_abs)
            
            # Check for null bytes
            if '\x00' in str(path):
                return False, get_string("security.validate_path.null_byte")
            
            # Check for Windows reserved names
            if os.name == 'nt':
                reserved_names = [
                    'CON', 'PRN', 'AUX', 'NUL',
                    'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                    'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
                ]
                
                name_without_ext = abs_path.stem.upper()
                if name_without_ext in reserved_names:
                    return False, get_string("security.validate_path.reserved_windows_name", name_without_ext)
            
            return True, get_string("security.validate_path.safe")
            
        except Exception as e:
            return False, get_string("security.validate_path.error", e)
    
    @classmethod
    def validate_file_extension(cls, path: Path) -> Tuple[bool, str]:
        """
        Validate file extension is allowed
        
        Args:
            path: Path to validate
            
        Returns:
            Tuple of (is_allowed: bool, message: str)
        """
        extension = path.suffix.lower()
        
        if not extension:
            return True, get_string("security.validate_extension.no_extension")
        
        if extension in cls.ALLOWED_EXTENSIONS:
            return True, get_string("security.validate_extension.allowed", extension)
        else:
            return False, get_string("security.validate_extension.not_allowed", extension)
    
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """
        Sanitize filename by removing dangerous characters
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove null bytes
        filename = filename.replace('\x00', '')
        
        # Remove or replace dangerous characters
        dangerous_chars = r'[<>:"/\\|?*\x00-\x1f]'
        filename = re.sub(dangerous_chars, '_', filename)
        
        # Remove leading/trailing dots and spaces
        filename = filename.strip('. ')
        
        # Ensure not empty
        if not filename:
            filename = 'unnamed'
        
        # Truncate if too long
        if len(filename) > cls.MAX_FILENAME_LENGTH:
            name, ext = os.path.splitext(filename)
            max_name_len = cls.MAX_FILENAME_LENGTH - len(ext)
            filename = name[:max_name_len] + ext
        
        # Check for Windows reserved names
        if os.name == 'nt':
            name_without_ext = os.path.splitext(filename)[0].upper()
            reserved_names = [
                'CON', 'PRN', 'AUX', 'NUL',
                'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
            ]
            
            if name_without_ext in reserved_names:
                filename = f"safe_{filename}"
        
        return filename
    
    @classmethod
    def sanitize_input(cls, user_input: str, max_length: int = 1000) -> str:
        """
        Sanitize user input
        
        Args:
            user_input: Raw user input
            max_length: Maximum allowed length
            
        Returns:
            Sanitized input
        """
        if not user_input:
            return ""
        
        # Remove null bytes and control characters
        sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', user_input)
        
        # Trim whitespace
        sanitized = sanitized.strip()
        
        # Truncate if too long
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized
    
    @classmethod
    def validate_url(cls, url: str) -> Tuple[bool, str]:
        """
        Validate URL for security issues
        
        Args:
            url: URL to validate
            
        Returns:
            Tuple of (is_safe: bool, message: str)
        """
        try:
            parsed = urllib.parse.urlparse(url)
            
            # Check scheme
            if parsed.scheme not in ['http', 'https']:
                return False, get_string("security.validate_url.invalid_scheme", parsed.scheme)
            
            # Check for localhost/private IPs (basic check)
            hostname = parsed.hostname
            if hostname:
                if hostname.lower() in ['localhost', '127.0.0.1', '::1']:
                    return False, get_string("security.validate_url.localhost_not_allowed")
                
                # Basic private IP check
                if hostname.startswith('192.168.') or hostname.startswith('10.') or hostname.startswith('172.'):
                    return False, get_string("security.validate_url.private_ip_not_allowed")
            
            # Check URL length
            if len(url) > 2048:
                return False, get_string("security.validate_url.too_long")
            
            return True, get_string("security.validate_url.safe")
            
        except Exception as e:
            return False, get_string("security.validate_url.error", e)
    
    @classmethod
    def check_permissions(cls, path: Path, required_permissions: Set[str]) -> Tuple[bool, List[str]]:
        """
        Check file/directory permissions
        
        Args:
            path: Path to check
            required_permissions: Set of required permissions ('read', 'write', 'execute')
            
        Returns:
            Tuple of (has_permissions: bool, missing_permissions: List[str])
        """
        missing = []
        
        try:
            if not path.exists():
                # For non-existent paths, check parent directory
                parent = path.parent
                if not parent.exists():
                    missing.append(get_string("security.check_permissions.path_not_exist"))
                    return False, missing
                path = parent
            
            if 'read' in required_permissions:
                if not os.access(path, os.R_OK):
                    missing.append('read')
            
            if 'write' in required_permissions:
                if not os.access(path, os.W_OK):
                    missing.append('write')
            
            if 'execute' in required_permissions:
                if not os.access(path, os.X_OK):
                    missing.append('execute')
            
            return len(missing) == 0, missing
            
        except Exception as e:
            missing.append(get_string("security.check_permissions.error", e))
            return False, missing
    
    @classmethod
    def validate_installation_target(cls, target_dir: Path) -> Tuple[bool, List[str]]:
        """
        Validate installation target directory with enhanced Windows compatibility
        
        Args:
            target_dir: Target installation directory
            
        Returns:
            Tuple of (is_safe: bool, error_messages: List[str])
        """
        errors = []
        
        # Enhanced path resolution with Windows normalization
        try:
            abs_target = target_dir.resolve()
        except Exception as e:
            errors.append(get_string("security.validate_target.resolve_error", e))
            return False, errors
            
        # Windows-specific path normalization
        if os.name == 'nt':
            # Normalize Windows paths for consistent comparison
            abs_target_str = str(abs_target).lower().replace('/', '\\')
        else:
            abs_target_str = str(abs_target).lower()
        
        # Special handling for Claude installation directory
        claude_patterns = ['.claude', '.claude' + os.sep, '.claude\\', '.claude/']
        is_claude_dir = any(abs_target_str.endswith(pattern) for pattern in claude_patterns)
        
        if is_claude_dir:
            try:
                home_path = Path.home()
            except (RuntimeError, OSError):
                # If we can't determine home directory, skip .claude special handling
                cls._log_security_decision("WARN", get_string("security.validate_target.log_home_dir_error", abs_target))
                # Fall through to regular validation
            else:
                try:
                    # Verify it's specifically the current user's home directory
                    abs_target.relative_to(home_path)
                    
                    # Enhanced Windows security checks for .claude directories
                    if os.name == 'nt':
                        # Check for junction points and symbolic links on Windows
                        if cls._is_windows_junction_or_symlink(abs_target):
                            errors.append(get_string("security.validate_target.no_junctions"))
                            return False, errors
                        
                        # Additional validation: verify it's in the current user's profile directory
                        # Use actual home directory comparison instead of username-based path construction
                        if ':' in abs_target_str and '\\users\\' in abs_target_str:
                            try:
                                # Check if target is within the user's actual home directory
                                home_path = Path.home()
                                abs_target.relative_to(home_path)
                                # Path is valid - within user's home directory
                            except ValueError:
                                # Path is outside user's home directory
                                current_user = os.environ.get('USERNAME', home_path.name)
                                errors.append(get_string("security.validate_target.must_be_in_user_dir", current_user))
                                return False, errors
                    
                    # Check permissions
                    has_perms, missing = cls.check_permissions(target_dir, {'read', 'write'})
                    if not has_perms:
                        if os.name == 'nt':
                            errors.append(get_string("security.validate_target.insufficient_perms_windows", missing))
                        else:
                            errors.append(get_string("security.validate_target.insufficient_perms", missing))
                    
                    # Log successful validation for audit trail
                    cls._log_security_decision("ALLOW", get_string("security.validate_target.log_claude_dir_validated", abs_target))
                    return len(errors) == 0, errors
                    
                except ValueError:
                    # Not under current user's home directory
                    if os.name == 'nt':
                        errors.append(get_string("security.validate_target.claude_must_be_in_user_dir_windows"))
                    else:
                        errors.append(get_string("security.validate_target.claude_must_be_in_home_dir"))
                    cls._log_security_decision("DENY", get_string("security.validate_target.log_claude_dir_outside_home", abs_target))
                    return False, errors
        
        # Validate path for non-.claude directories
        is_safe, msg = cls.validate_path(target_dir)
        if not is_safe:
            if os.name == 'nt':
                # Enhanced Windows error messages
                if "dangerous path pattern" in msg.lower():
                    errors.append(get_string("security.validate_target.invalid_windows_path", msg))
                elif "path too long" in msg.lower():
                    errors.append(get_string("security.validate_target.windows_path_too_long", msg))
                elif "reserved" in msg.lower():
                    errors.append(get_string("security.validate_target.windows_reserved_name", msg))
                else:
                    errors.append(get_string("security.validate_target.invalid_target_path", msg))
            else:
                errors.append(get_string("security.validate_target.invalid_target_path", msg))
        
        # Check permissions with platform-specific guidance
        has_perms, missing = cls.check_permissions(target_dir, {'read', 'write'})
        if not has_perms:
            if os.name == 'nt':
                errors.append(get_string("security.validate_target.insufficient_perms_windows_long", missing))
            else:
                errors.append(get_string("security.validate_target.insufficient_perms_unix", missing, target_dir))
        
        # Check if it's a system directory with enhanced messages
        system_dirs = [
            Path('/etc'), Path('/bin'), Path('/sbin'), Path('/usr/bin'), Path('/usr/sbin'),
            Path('/var'), Path('/tmp'), Path('/dev'), Path('/proc'), Path('/sys')
        ]
        
        if os.name == 'nt':
            system_dirs.extend([
                Path('C:\\Windows'), Path('C:\\Program Files'), Path('C:\\Program Files (x86)')
            ])
        
        for sys_dir in system_dirs:
            try:
                if abs_target.is_relative_to(sys_dir):
                    if os.name == 'nt':
                        errors.append(get_string("security.validate_target.cannot_install_to_windows_system_dir", sys_dir))
                    else:
                        errors.append(get_string("security.validate_target.cannot_install_to_system_dir", sys_dir))
                    cls._log_security_decision("DENY", get_string("security.validate_target.log_system_dir_attempt", sys_dir))
                    break
            except (ValueError, AttributeError):
                # is_relative_to not available in older Python versions
                try:
                    abs_target.relative_to(sys_dir)
                    errors.append(get_string("security.validate_target.cannot_install_to_system_dir", sys_dir))
                    break
                except ValueError:
                    continue
        
        return len(errors) == 0, errors
    
    @classmethod
    def validate_component_files(cls, file_list: List[Tuple[Path, Path]], base_source_dir: Path, base_target_dir: Path) -> Tuple[bool, List[str]]:
        """
        Validate list of files for component installation
        
        Args:
            file_list: List of (source, target) path tuples
            base_source_dir: Base source directory
            base_target_dir: Base target directory
            
        Returns:
            Tuple of (all_safe: bool, error_messages: List[str])
        """
        errors = []
        
        for source, target in file_list:
            # Validate source path
            is_safe, msg = cls.validate_path(source, base_source_dir)
            if not is_safe:
                errors.append(get_string("security.validate_components.invalid_source", source, msg))
            
            # Validate target path
            is_safe, msg = cls.validate_path(target, base_target_dir)
            if not is_safe:
                errors.append(get_string("security.validate_components.invalid_target", target, msg))
            
            # Validate file extension
            is_allowed, msg = cls.validate_file_extension(source)
            if not is_allowed:
                errors.append(get_string("security.validate_components.file_error", source, msg))
        
        return len(errors) == 0, errors
    
    @classmethod
    def _normalize_path_for_validation(cls, path: Path) -> str:
        """
        Normalize path for consistent validation across platforms
        
        Args:
            path: Path to normalize
            
        Returns:
            Normalized path string for validation
        """
        path_str = str(path)
        
        # Convert to lowercase for case-insensitive comparison
        path_str = path_str.lower()
        
        # Normalize path separators for consistent pattern matching
        if os.name == 'nt':  # Windows
            # Convert forward slashes to backslashes for Windows
            path_str = path_str.replace('/', '\\')
            # Ensure consistent drive letter format
            if len(path_str) >= 2 and path_str[1] == ':':
                path_str = path_str[0] + ':\\' + path_str[3:].lstrip('\\')
        else:  # Unix-like systems
            # Convert backslashes to forward slashes for Unix
            path_str = path_str.replace('\\', '/')
            # Ensure single leading slash
            if path_str.startswith('//'):
                path_str = '/' + path_str.lstrip('/')
        
        return path_str
    
    @classmethod
    def _get_user_friendly_error_message(cls, error_type: str, pattern: str, path: Path) -> str:
        """
        Generate user-friendly error messages with actionable suggestions
        
        Args:
            error_type: Type of error (traversal, windows_system, unix_system)
            pattern: The regex pattern that matched
            path: The path that caused the error
            
        Returns:
            User-friendly error message with suggestions
        """
        if error_type == "traversal":
            return get_string("security.error.traversal_detected", path)
        elif error_type == "windows_system":
            username = os.environ.get('USERNAME', 'YourName')
            if pattern == r'^c:[/\\]windows[/\\]':
                return get_string("security.error.install_to_windows_system_dir", path, username)
            elif pattern == r'^c:[/\\]program files[/\\]':
                return get_string("security.error.install_to_program_files", path, username)
            else:
                return get_string("security.error.install_to_windows_system_dir_generic", path)
        elif error_type == "unix_system":
            system_dirs = {
                r'^/dev/': get_string("security.dir_desc.dev"),
                r'^/etc/': get_string("security.dir_desc.etc"),
                r'^/bin/': get_string("security.dir_desc.bin"),
                r'^/sbin/': get_string("security.dir_desc.sbin"),
                r'^/usr/bin/': get_string("security.dir_desc.usr_bin"),
                r'^/usr/sbin/': get_string("security.dir_desc.usr_sbin"),
                r'^/var/': get_string("security.dir_desc.var"),
                r'^/tmp/': get_string("security.dir_desc.tmp"),
                r'^/proc/': get_string("security.dir_desc.proc"),
                r'^/sys/': get_string("security.dir_desc.sys")
            }
            
            dir_desc = system_dirs.get(pattern, get_string("security.dir_desc.default"))
            return get_string("security.error.install_to_unix_system_dir", dir_desc, path)
        else:
            return get_string("security.error.generic_validation_failed", path)
    
    @classmethod
    def _is_windows_junction_or_symlink(cls, path: Path) -> bool:
        """
        Check if path is a Windows junction point or symbolic link
        
        Args:
            path: Path to check
            
        Returns:
            True if path is a junction point or symlink, False otherwise
        """
        if os.name != 'nt':
            return False
            
        try:
            # Only check if path exists to avoid filesystem errors during testing
            if not path.exists():
                return False
                
            # Check if path is a symlink (covers most cases)
            if path.is_symlink():
                return True
                
            # Additional Windows-specific checks for junction points
            try:
                import stat
                st = path.stat()
                # Check for reparse point (junction points have this attribute)
                if hasattr(st, 'st_reparse_tag') and st.st_reparse_tag != 0:
                    return True
            except (OSError, AttributeError):
                pass
                    
            # Alternative method using os.path.islink
            try:
                if os.path.islink(str(path)):
                    return True
            except (OSError, AttributeError):
                pass
                
        except (OSError, AttributeError, NotImplementedError):
            # If we can't determine safely, default to False
            # This ensures the function doesn't break validation
            pass
            
        return False
    
    @classmethod
    def _log_security_decision(cls, action: str, message: str) -> None:
        """
        Log security validation decisions for audit trail
        
        Args:
            action: Security action taken (ALLOW, DENY, WARN)
            message: Description of the decision
        """
        try:
            import logging
            import datetime
            
            # Create security logger if it doesn't exist
            security_logger = logging.getLogger('superclaude.security')
            if not security_logger.handlers:
                # Set up basic logging if not already configured
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
                )
                handler.setFormatter(formatter)
                security_logger.addHandler(handler)
                security_logger.setLevel(logging.INFO)
            
            # Log the security decision
            if action == "DENY":
                log_message = get_string("security.log.decision_deny", message, os.getpid())
                security_logger.warning(log_message)
            elif action == "WARN":
                log_message = get_string("security.log.decision_warn", message, os.getpid())
                security_logger.warning(log_message)
            else: # ALLOW
                log_message = get_string("security.log.decision_allow", message, os.getpid())
                security_logger.info(log_message)
                
        except Exception:
            # Don't fail security validation if logging fails
            pass
    
    @classmethod
    def create_secure_temp_dir(cls, prefix: str = "superclaude_") -> Path:
        """
        Create secure temporary directory
        
        Args:
            prefix: Prefix for temp directory name
            
        Returns:
            Path to secure temporary directory
        """
        import tempfile
        
        # Create with secure permissions (0o700)
        temp_dir = Path(tempfile.mkdtemp(prefix=prefix))
        temp_dir.chmod(0o700)
        
        return temp_dir
    
    @classmethod
    def secure_delete(cls, path: Path) -> bool:
        """
        Securely delete file or directory
        
        Args:
            path: Path to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not path.exists():
                return True
            
            if path.is_file():
                # Overwrite file with random data before deletion
                try:
                    import secrets
                    file_size = path.stat().st_size
                    
                    with open(path, 'r+b') as f:
                        # Overwrite with random data
                        f.write(secrets.token_bytes(file_size))
                        f.flush()
                        os.fsync(f.fileno())
                except Exception:
                    pass  # If overwrite fails, still try to delete
                
                path.unlink()
            
            elif path.is_dir():
                # Recursively delete directory contents
                import shutil
                shutil.rmtree(path)
            
            return True
            
        except Exception:
            return False