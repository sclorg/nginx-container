import os


TAGS = {
    "rhel8": "-ubi8",
    "rhel9": "-ubi9",
    "rhel10": "-ubi10",
}


def return_app_name(request):
    return os.path.basename(request.param)
