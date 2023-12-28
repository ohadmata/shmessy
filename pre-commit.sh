#!/bin/bash

coverage run -m pytest
coverage-badge -f -o coverage.svg