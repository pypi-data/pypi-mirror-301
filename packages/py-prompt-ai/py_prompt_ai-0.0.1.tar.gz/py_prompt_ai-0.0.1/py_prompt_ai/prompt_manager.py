import os

from jinja2 import Environment, FileSystemLoader, TemplateNotFound


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # Call the superclass __call__ to create the instance
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PromptManager(metaclass=SingletonMeta):
    def __init__(self, search_root=None):
        self.template_paths = {}  # Map of template names to directories
        self.search_root = search_root or os.getcwd()  # Root directory for searching
        self.load_template_paths()

    def find_prompt_folders(self):
        """
        Recursively find all folders named 'prompts' starting from the search_root.
        """
        prompt_dirs = []
        for root, dirs, _ in os.walk(self.search_root):
            if 'prompts' in dirs:
                prompt_dir = os.path.join(root, 'prompts')
                prompt_dirs.append(prompt_dir)
        return prompt_dirs

    def load_template_paths(self):
        """
        Clears current template paths and rebuilds by searching for 'prompts' directories.
        """
        self.template_paths.clear()

        prompt_dirs = self.find_prompt_folders()

        for prompt_dir in prompt_dirs:
            for file_name in os.listdir(prompt_dir):
                if file_name.endswith('.j2'):
                    template_name = file_name
                    self.template_paths[template_name] = prompt_dir

    def render_prompt(self, template_name: str, context: dict) -> str:
        """
        Render a template using the correct loader, ensuring template inheritance works.

        :param template_name: name of the template to render
        :param context: dict containing the key:values for the template
        :return: rendered string prompt
        """

        if template_name not in self.template_paths:
            if not template_name.endswith('.j2'):
                # Try adding the extension if it's missing
                template_name_with_ext = template_name + '.j2'
                if template_name_with_ext in self.template_paths:
                    template_name = template_name_with_ext
                else:
                    print(f"Template '{template_name}' not found in tracked paths.")
                    return None
            else:
                print(f"Template '{template_name}' not found in tracked paths.")
                return None

        try:
            # Get the directory containing the template
            template_dir = self.template_paths[template_name]

            # Set up a new FileSystemLoader for this specific template directory
            env = Environment(
                    loader=FileSystemLoader(template_dir),
                    autoescape=True
            )

            # Render the template
            template = env.get_template(template_name)
            return template.render(context)
        except TemplateNotFound:
            print(f"Template '{template_name}' not found in the provided directory .")
        except Exception as e:
            print(f"Error rendering template '{template_name}': {e}")
        return None

    def reload_templates(self):
        """
        Reloads the template paths by searching for new 'prompts' directories.
        """
        self.load_template_paths()
