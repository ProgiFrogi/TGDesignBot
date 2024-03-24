import requests
import os
import aspose.slides as slides


# Takes path to file in local directory and list of templates (pptx files).
# Install them to a local directory.
def install_templates(path: str, templates: list):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    try:
        for template in templates:
            response = requests.get(template['file'])
            with open(path + template['name'], 'wb') as file:
                file.write(response.content)
    except Exception as e:
        for template in templates:
            if os.path.exists(path + template['name']):
                os.remove(path + template['file'])
        raise Exception("Can't install templates")


# Takes the path to presentation and returns a list of dictionary with keys:
#    slide_id: slide position in presentation. Using 0-indexation
#    tags: text of comment, that slide contains
def get_slides_information(path: str) -> list:
    slides_info = []
    if not os.path.exists(path):
        raise Exception("No such file or directory")
    with slides.Presentation(path) as presentation:
        for author in presentation.comment_authors:
            for comment in author.comments:
                slides_info.append({'slide_id': comment.slide.slide_number - 1,
                                   'tags': comment.text})
    return slides_info


# This function delete all comments from presentation placed in path.
def remove_all_comments(path: str):
    with slides.Presentation(path) as presentation:
        # Deletes all comments from the presentation
        for author in presentation.comment_authors:
            author.comments.clear()

        # Deletes all authors
        presentation.comment_authors.clear()

        presentation.save(path, slides.export.SaveFormat.PPTX)
