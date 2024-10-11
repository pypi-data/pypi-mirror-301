# Python AI Prompt Manager

The Python AI Prompt Manager is a simple utility designed to help manage and render Jinja2 (.j2) templates for AI prompts or any other text-based templates. This tool recursively searches for prompt folders within a given directory structure, making it easy to organize and reuse templates. It supports template rendering with custom contexts, and it provides functionality to easily reload new templates as they are added to the project.
Features

    Singleton Pattern: Ensures only one instance of PromptManager is active at any time.
    Jinja2 Template Rendering: Automatically finds .j2 files in directories named prompts and renders them with custom contexts.
    Automatic Search and Reload: The manager automatically searches for prompt folders, and it can reload template paths as new ones are added.
    Easy Context Management: Supports passing Python dictionaries to be used as context variables in the templates.

## Features
- Automatically searches for j2 files to be used for prompts, which can also be manually set
- render_template method can take a .j2 extension or not
- Nested templates work
- Manager is a singleton which can be loaded from anywhere in your app

## Installation

`pip install py_prompt_ai`

## Usage
1. Install py_prompt_ai
2. Create a prompts/ subdirectory and place your jinja2 prompts in that directory
3. Call a PromptManager and start rendering prompts with `render_prompt("prompt_name", context_values)`

### Simple example to render a prompt
Filename: `example_template.j2`
```jinja2
You're a world class project manager working on {project}, and you're being asked about the: {topic}

Gather all the information about the project, and determine an acceptable 
response

```

Filename: `app.py`
```python
from py_prompt_ai.prompt_manager import PromptManager

pm = PromptManager(search_root="/path/to/search")

context = {
    "project": "example",
    "topic": "project status"
}

output = pm.render_prompt("example_template", context)
print(output)

# 
# 

# If you add a prompt template during runtime, you can reload the templates
pm.reload_templates()
```



### Example Directory Structure

The tool will search for directories named prompts:

```
/project-root
│
├── /agent1
│   └── /prompts
│       └── example_template.j2
│
└── /agent2
    └── /prompts
        └── another_template.j2
```

## Improvements and Future Features

- Text File Support: Currently, only Jinja2 templates (.j2) are supported. An easy improvement would be to also allow rendering plain text (.txt) templates by treating them as simple string replacements without Jinja2's logic.
- Prompt Validation: Add a mechanism to validate prompt templates and contexts to ensure variables are correctly passed.
- CLI Support: Add command-line support to easily render templates and manage prompt paths without writing Python code.

## License

This project is licensed under the MPL 2.0 License. See the LICENSE file for more details.