#!/usr/bin/env python3
"""
Dockerfile processor module to replace sed commands with Python functionality.
This module provides utilities to process Dockerfiles by replacing version strings
and environment variables.
"""

import re
import os
import tempfile
from pathlib import Path
from typing import Optional, Union


class DockerfileProcessor:
    """
    A class to process Dockerfiles by replacing version strings and environment variables.
    This replaces the functionality of sed commands used in shell scripts.
    """
    
    def __init__(self, dockerfile_path: Union[str, Path]):
        """
        Initialize the DockerfileProcessor with a path to a Dockerfile.
        
        Args:
            dockerfile_path: Path to the Dockerfile to process
        """
        self.dockerfile_path = Path(dockerfile_path)
        if not self.dockerfile_path.exists():
            raise FileNotFoundError(f"Dockerfile not found: {dockerfile_path}")
    
    def process_nginx_version(self, version: str, output_path: Optional[Union[str, Path]] = None) -> str:
        """
        Process the Dockerfile to replace NGINX version strings.
        
        This method performs the same operations as the sed command:
        sed -e "s/^ENV NGINX_VERSION.*$/ENV NGINX_VERSION=$version/" -e "s/\$NGINX_VERSION/$version/g"
        
        Args:
            version: The NGINX version to use for replacement
            output_path: Optional path to write the processed content. If None, returns content as string.
        
        Returns:
            The processed Dockerfile content as a string
        """
        with open(self.dockerfile_path, 'r') as f:
            content = f.read()
        
        # Replace ENV NGINX_VERSION line (equivalent to s/^ENV NGINX_VERSION.*$/ENV NGINX_VERSION=$version/)
        content = re.sub(r'^ENV NGINX_VERSION.*$', f'ENV NGINX_VERSION={version}', content, flags=re.MULTILINE)
        
        # Replace all occurrences of $NGINX_VERSION (equivalent to s/\$NGINX_VERSION/$version/g)
        content = content.replace('$NGINX_VERSION', version)
        
        if output_path:
            output_path = Path(output_path)
            with open(output_path, 'w') as f:
                f.write(content)
        
        return content
    
    def create_temp_dockerfile(self, version: str) -> str:
        """
        Create a temporary Dockerfile with processed version strings.
        
        Args:
            version: The NGINX version to use for replacement
        
        Returns:
            Path to the temporary Dockerfile
        """
        # Create a temporary file
        fd, temp_path = tempfile.mkstemp(suffix='.dockerfile', prefix='nginx_test_')
        os.close(fd)  # Close the file descriptor, we'll write to it separately
        
        # Process and write the content
        self.process_nginx_version(version, temp_path)
        
        return temp_path
    
    def validate_dockerfile_syntax(self, content: str) -> bool:
        """
        Basic validation of Dockerfile syntax.
        
        Args:
            content: Dockerfile content to validate
        
        Returns:
            True if basic syntax checks pass, False otherwise
        """
        lines = content.strip().split('\n')
        
        # Check for basic Dockerfile structure
        has_from = any(line.strip().upper().startswith('FROM') for line in lines)
        if not has_from:
            return False
        
        # Check for valid instruction format
        valid_instructions = {
            'FROM', 'RUN', 'CMD', 'LABEL', 'EXPOSE', 'ENV', 'ADD', 'COPY',
            'ENTRYPOINT', 'VOLUME', 'USER', 'WORKDIR', 'ARG', 'ONBUILD',
            'STOPSIGNAL', 'HEALTHCHECK', 'SHELL'
        }
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Extract the instruction (first word)
            instruction = line.split()[0].upper()
            if instruction not in valid_instructions:
                return False
        
        return True
    
    @staticmethod
    def replace_version_in_file(dockerfile_path: Union[str, Path], version: str, output_path: Union[str, Path]) -> None:
        """
        Static method to replace version in a Dockerfile and write to output file.
        This is the direct replacement for the sed command functionality.
        
        Args:
            dockerfile_path: Path to input Dockerfile
            version: Version string to replace
            output_path: Path to output the processed Dockerfile
        """
        processor = DockerfileProcessor(dockerfile_path)
        processor.process_nginx_version(version, output_path)


def main():
    """
    Command-line interface for the Dockerfile processor.
    Usage: python dockerfile_processor.py <dockerfile_path> <version> <output_path>
    """
    import sys
    
    if len(sys.argv) != 4:
        print("Usage: python dockerfile_processor.py <dockerfile_path> <version> <output_path>")
        sys.exit(1)
    
    dockerfile_path, version, output_path = sys.argv[1:4]
    
    try:
        DockerfileProcessor.replace_version_in_file(dockerfile_path, version, output_path)
        print(f"Successfully processed {dockerfile_path} -> {output_path} with version {version}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

