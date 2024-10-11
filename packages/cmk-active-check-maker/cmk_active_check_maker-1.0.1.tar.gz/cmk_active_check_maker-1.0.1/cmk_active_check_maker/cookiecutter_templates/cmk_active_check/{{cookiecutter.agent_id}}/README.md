# Checkmk Active Check Plugin - {{cookiecutter.agent_id}}

## Overview

This Checkmk plugin provides an **Active Check** that monitors specific services or conditions in your infrastructure.  
The plugin is packaged as a `.mkp` file, which can be installed in Checkmk to extend its monitoring capabilities.  
The plugin allows for real-time checks on the specified services by running custom scripts or commands and integrates with Checkmk's monitoring system.

## Features

- Executes custom scripts for active checks.
- Fully integrates with Checkmk.
- Configurable thresholds and parameters.
- Generates alert and performance data.

## Requirements

- Checkmk version: `>= 2.1.1`
- Python version: `>= 3.12`
- Access to the system/service being monitored.

## Installation

### Step 1: Install the Plugin

1. Prepare python and poetry 
2. Install the requirements:

    ```bash
    poetry install && poetry shell 
    ```


## Development

### Step 1: Configure input parameters

1. Target file **run_check.py**
2. Update parameters:

    ```text
    HOST_IP = 'your-device'
    SNMP_COMMUNITY = 'snmp-community'
    SAMPLE_DATA = 'should be the dictionary contains data for active check'
    OTHER_KWARGS = 'should be the dictionary contains extra data, optionals'
    ```


### Step 2: Run the check for testing

1. Using python command
    ```bash
    poetry run python run_check.py
    ```

## Documents
1. Add/Update your documents to /docs