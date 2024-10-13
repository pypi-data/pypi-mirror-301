import mkdocs
import mkdocs.plugins
import mkdocs.structure.files
import logging

class ExcludeUnused(mkdocs.plugins.BasePlugin):
    """
    An MkDocs plugin that removes unused .md files from the output.
    """

    valid_pages = []

    def on_config(self, config):
        """
        Collect all names of .md files that are present in the config.nav object.
        """
        self.valid_pages = []

        for item in config.nav:
            self.valid_pages.append(list(item.values())[0])
        return config
    
    def on_files(self, files, config):
        """
        Remove all .md files from the files object that are not included in config.nav.
        """
        log = logging.getLogger(f"mkdocs.plugins.{__name__}")
        output_files = []

        for file in files:
            if file.src_uri.endswith('.md'):
                if file.src_uri in self.valid_pages:
                    output_files.append(file)
                    continue
                
                # Support for literate-nav and navigation elements that end with /
                last_sep_index = file.src_uri.rfind('/')
                if last_sep_index != -1:
                    valid_path = file.src_uri[:last_sep_index + 1]
                    if any(vp.startswith(valid_path) for vp in self.valid_pages):
                        output_files.append(file)
                else:
                    log.debug(f"Excluding {file.src_uri} because it is not present in nav.")
            else:
                output_files.append(file)

        return mkdocs.structure.files.Files(output_files)