# tests/test_prompt_manager.py

import os
import shutil
import pytest

from py_prompt_ai.prompt_manager import PromptManager


# Fixture to create a temporary 'prompts' directory and template file
@pytest.fixture(scope="module")
def temp_prompts_dir():
    """
    Creates a temporary 'prompts' directory with a test template file.
    This fixture lasts for the duration of the module and cleans up after tests.
    """
    # Setup: Create temporary directory and 'prompts' subdirectory
    original_cwd = os.getcwd()
    temp_dir = os.path.join(original_cwd, 'temp_test_dir')
    prompts_dir = os.path.join(temp_dir, 'prompts')
    os.makedirs(prompts_dir, exist_ok=True)

    # Create a sample template file
    template_content = "Hello, {{ name }}!"
    template_path = os.path.join(prompts_dir, 'test_prompt.j2')
    with open(template_path, 'w') as f:
        f.write(template_content)

    # Change working directory to the temporary directory
    os.chdir(temp_dir)

    yield temp_dir  # Tests will run here

    # Teardown: Return to original directory and remove temporary files
    os.chdir(original_cwd)
    shutil.rmtree(temp_dir)


def test_singleton_instance(temp_prompts_dir):
    pm1 = PromptManager()
    pm2 = PromptManager()
    assert pm1 is pm2, "PromptManager instances are not the same (Singleton pattern broken)"


def test_load_template_paths(temp_prompts_dir):
    pm = PromptManager()
    assert 'test_prompt.j2' in pm.template_paths, "Template 'test_prompt.j2' not found in template paths"


def test_render_prompt_success(temp_prompts_dir):
    pm = PromptManager()
    context = {'name': 'Alice'}
    result = pm.render_prompt('test_prompt.j2', context)
    assert result == "Hello, Alice!", f"Rendered output mismatch: {result}"


def test_render_prompt_missing_context(temp_prompts_dir):
    pm = PromptManager()
    context = {}  # Missing 'name' key
    result = pm.render_prompt('test_prompt.j2', context)
    assert "Hello, " in result, "Template did not render correctly with missing context"


def test_render_nonexistent_template(temp_prompts_dir):
    pm = PromptManager()
    context = {'name': 'Bob'}
    result = pm.render_prompt('nonexistent_template.j2', context)
    assert result is None, "Expected None when rendering a nonexistent template"


def test_reload_templates(temp_prompts_dir):
    pm = PromptManager()
    # Initially, the template should be present
    assert 'test_prompt.j2' in pm.template_paths

    # Remove the template file
    os.remove(os.path.join('prompts', 'test_prompt.j2'))
    pm.reload_templates()

    # After reloading, the template should not be present
    assert 'test_prompt.j2' not in pm.template_paths, "Template paths not updated after reload"


def test_find_prompt_folders(temp_prompts_dir):
    pm = PromptManager()
    prompt_dirs = pm.find_prompt_folders()
    assert os.path.join(temp_prompts_dir, 'prompts') in prompt_dirs, "Prompt directory not found"


def test_render_prompt_exception_handling(temp_prompts_dir, capsys):
    pm = PromptManager()
    context = {'name': 'Charlie'}

    # Induce an exception by corrupting the template
    with open(os.path.join('prompts', 'test_prompt.j2'), 'w') as f:
        f.write("Hello, {{ name }")  # Missing closing brace

    result = pm.render_prompt('test_prompt.j2', context)

    # Capture the printed output
    captured = capsys.readouterr()
    assert result is None, "Expected None due to template rendering error"
    assert "Template 'test_prompt.j2' not found" in captured.out, "Error message not printed as expected"
