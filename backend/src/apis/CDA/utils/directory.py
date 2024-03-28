import os

from apis.utils.directory import dire
from apis.utils.recursive import recursion
from apis.CDA.utils.augment import templating
from core.config import settings


def check_exist(item):

    images_path = os.path.join(dire.image_path, item)

    if not os.path.exists(images_path):
        raise Exception(f"{item} folder not found in images folder.")

    item_fol_list = os.listdir(images_path)

    if len(item_fol_list) == 0:
        raise Exception(f"{item} folder do not have any folders inside.")

    if not any(x in item_fol_list for x in settings.BASE_TYPES):
        raise Exception(f"Cannot augment due to missing {settings.BASE_TYPES} folders.")

    if not any(x in item_fol_list for x in settings.G_TYPES):
        raise Exception(f"Missing {settings.G_TYPES} folders.")

    return images_path


def get_template(images_path, range):
    template_dict = {}

    for root, dirs, files in os.walk(images_path):
        if len(files):
            recursion(
                template_dict,
                root.split(images_path)[-1].split(os.sep)[1:],
                templating(root, files, range),
            )

    for key, value in template_dict.items():
        if any("count" in x.keys() for x in value.values() if isinstance(x, dict)):
            template_dict[key] = {
                "count": sum(x["count"] for x in value.values()),
                "template": sum((x["template"] for x in value.values()), []),
            }

    return template_dict
